"""E000-E: PHM2010 raw-data physical process-coordinate audit.

Downloads a small, representative subset of raw PHM2010 cuts from the public
Kaggle mirror using kagglehub. Raw files stay in the runner temp directory and
are never committed. Only small audit summaries are written to results/e000e/.

This tests H002c_1 (physical-coordinate observability), not H002 itself.
"""
from __future__ import annotations

import json
import os
import traceback
from pathlib import Path

import kagglehub
import numpy as np
import pandas as pd
from scipy import signal

HANDLE = "rabahba/phm-data-challenge-2010"
FS = 50_000.0
SPINDLE_HZ = 10_400.0 / 60.0
TOOTH_HZ = SPINDLE_HZ * 3.0
CUTTERS = ["c1", "c4", "c6"]
CUTS = [1, 50, 100, 150, 200, 250, 315]
FORCE_CHANNELS = ["Fx", "Fy", "Fz"]
ALL_CHANNELS = ["Fx", "Fy", "Fz", "Vx", "Vy", "Vz", "AE_RMS"]
OUT = Path("results/e000e")
CACHE = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "phm2010_kaggle"


def remote_candidates(cutter: str, cut: int) -> list[str]:
    cid = cutter[1:]
    name = f"c_{cid}_{cut:03d}.csv"
    return [
        f"{cutter}/{cutter}/{name}",
        f"{cutter}/{name}",
        f"{cutter}/{cutter}/c{cid}_{cut:03d}.csv",
        f"{cutter}/c{cid}_{cut:03d}.csv",
    ]


def locate_downloaded(returned: str | os.PathLike, basename: str) -> Path | None:
    p = Path(returned)
    if p.is_file():
        return p
    if p.is_dir():
        hits = list(p.rglob(basename))
        if hits:
            return hits[0]
    hits = list(CACHE.rglob(basename)) if CACHE.exists() else []
    return hits[0] if hits else None


def download_cut(cutter: str, cut: int) -> tuple[Path | None, str | None, list[str]]:
    errors = []
    for rel in remote_candidates(cutter, cut):
        try:
            returned = kagglehub.dataset_download(
                HANDLE,
                path=rel,
                output_dir=str(CACHE),
            )
            found = locate_downloaded(returned, Path(rel).name)
            if found is not None and found.exists():
                return found, rel, errors
            errors.append(f"{rel}: download returned {returned!r}, file not located")
        except Exception as exc:  # keep the access failure as evidence
            errors.append(f"{rel}: {type(exc).__name__}: {exc}")
    return None, None, errors


def robust_center(x: np.ndarray) -> np.ndarray:
    n = len(x)
    if n < 4096:
        return x
    # Central 50% reduces entry/exit transients while retaining many rotations.
    s, e = n // 4, (3 * n) // 4
    y = np.asarray(x[s:e], dtype=float)
    y = signal.detrend(y, type="linear")
    scale = np.median(np.abs(y - np.median(y))) * 1.4826
    if not np.isfinite(scale) or scale < 1e-12:
        scale = np.std(y) + 1e-12
    return (y - np.median(y)) / scale


def spectral_peak(x: np.ndarray, expected_hz: float) -> dict:
    nperseg = min(16384, max(2048, len(x) // 4))
    f, pxx = signal.welch(
        x,
        fs=FS,
        window="hann",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        detrend="linear",
        scaling="density",
    )
    lo, hi = expected_hz * 0.82, expected_hz * 1.18
    band = (f >= lo) & (f <= hi)
    if not np.any(band):
        raise ValueError("empty physical-frequency search band")
    fb, pb = f[band], pxx[band]
    j = int(np.argmax(pb))
    peak_f, peak_p = float(fb[j]), float(pb[j])

    ref = (f >= expected_hz * 0.55) & (f <= expected_hz * 1.45)
    exclusion = np.abs(f - peak_f) <= max(12.0, expected_hz * 0.04)
    ref_vals = pxx[ref & ~exclusion]
    floor = float(np.median(ref_vals)) if len(ref_vals) else float(np.median(pb))
    prominence = peak_p / (floor + 1e-18)
    return {
        "peak_hz": peak_f,
        "freq_error_pct": abs(peak_f - expected_hz) / expected_hz * 100.0,
        "spectral_prominence": float(prominence),
    }


def phase_metrics(x: np.ndarray, peak_hz: float) -> dict:
    low = max(5.0, peak_hz * 0.82)
    high = min(FS * 0.49, peak_hz * 1.18)
    sos = signal.butter(4, [low, high], btype="bandpass", fs=FS, output="sos")
    xf = signal.sosfiltfilt(sos, x)
    ph = np.unwrap(np.angle(signal.hilbert(xf)))
    dph = np.diff(ph)
    positive_ratio = float(np.mean(dph > 0))

    turns = np.floor((ph - ph[0]) / (2 * np.pi)).astype(np.int64)
    idx = np.flatnonzero(np.diff(turns) > 0) + 1
    if len(idx) >= 4:
        periods = np.diff(idx).astype(float)
        # Remove extreme boundary/phase-slip intervals before CV calculation.
        q1, q3 = np.quantile(periods, [0.1, 0.9])
        keep = periods[(periods >= q1) & (periods <= q3)]
        if len(keep) < 3:
            keep = periods
        period_mean = float(np.mean(keep))
        period_cv = float(np.std(keep) / (period_mean + 1e-12))
        phase_freq = float(FS / period_mean)
        n_cycles = int(len(periods))
    else:
        period_mean = np.nan
        period_cv = np.nan
        phase_freq = np.nan
        n_cycles = 0
    return {
        "phase_positive_ratio": positive_ratio,
        "cycle_period_samples": period_mean,
        "cycle_length_cv": period_cv,
        "phase_frequency_hz": phase_freq,
        "n_cycles": n_cycles,
    }


def audit_coordinate(df: pd.DataFrame, coord: str, expected: float) -> dict:
    best = None
    for ch in FORCE_CHANNELS:
        x = robust_center(df[ch].to_numpy(float))
        s = spectral_peak(x, expected)
        item = {"channel": ch, "signal": x, **s}
        if best is None or item["spectral_prominence"] > best["spectral_prominence"]:
            best = item
    assert best is not None
    pm = phase_metrics(best.pop("signal"), best["peak_hz"])
    return {"coordinate": coord, "expected_hz": expected, **best, **pm}


def gate(g: pd.DataFrame, attempted: int) -> dict:
    success_fraction = len(g) / max(attempted, 1)
    err_med = float(g.freq_error_pct.median()) if len(g) else np.nan
    err_pass = float((g.freq_error_pct < 5.0).mean()) if len(g) else 0.0
    cv_med = float(g.cycle_length_cv.median()) if len(g) else np.nan
    pos_med = float(g.phase_positive_ratio.median()) if len(g) else np.nan

    hard = [
        success_fraction >= 0.80,
        np.isfinite(err_med) and err_med < 5.0,
        err_pass >= 0.80,
        np.isfinite(cv_med) and cv_med < 0.05,
        np.isfinite(pos_med) and pos_med >= 0.95,
    ]
    if all(hard):
        status = "PASS"
    elif success_fraction >= 0.50 and np.isfinite(err_med) and err_med < 10.0:
        status = "WARN"
    else:
        status = "FAIL"
    return {
        "status": status,
        "success_fraction": success_fraction,
        "median_frequency_error_pct": err_med,
        "fraction_error_below_5pct": err_pass,
        "median_cycle_length_cv": cv_med,
        "median_phase_positive_ratio": pos_med,
        "median_spectral_prominence": float(g.spectral_prominence.median()) if len(g) else np.nan,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    attempts = []
    rows = []

    for cutter in CUTTERS:
        for cut in CUTS:
            path, remote, errors = download_cut(cutter, cut)
            att = {
                "cutter": cutter.upper(),
                "cut": cut,
                "remote_path": remote,
                "download_ok": path is not None,
                "errors": errors,
            }
            if path is None:
                attempts.append(att)
                continue
            try:
                df = pd.read_csv(path, header=None)
                if df.shape[1] != 7:
                    raise ValueError(f"expected 7 columns, got {df.shape[1]}")
                df.columns = ALL_CHANNELS
                att.update({"rows": int(len(df)), "local_bytes": int(path.stat().st_size)})
                for coord, expected in [("spindle", SPINDLE_HZ), ("tooth", TOOTH_HZ)]:
                    r = audit_coordinate(df, coord, expected)
                    rows.append({
                        "cutter": cutter.upper(),
                        "cut": cut,
                        "rows": int(len(df)),
                        **r,
                    })
            except Exception as exc:
                att["analysis_error"] = f"{type(exc).__name__}: {exc}"
                att["traceback"] = traceback.format_exc(limit=4)
            attempts.append(att)

    attempts_df = pd.DataFrame(attempts)
    attempts_df.to_csv(OUT / "download_audit.csv", index=False)
    raw = pd.DataFrame(rows)
    raw.to_csv(OUT / "phase_audit_detail.csv", index=False)

    attempted = len(CUTTERS) * len(CUTS)
    summaries = []
    if len(raw):
        for coord, g in raw.groupby("coordinate"):
            summaries.append({"coordinate": coord, **gate(g, attempted)})
    summary = pd.DataFrame(summaries)
    summary.to_csv(OUT / "phase_audit_summary.csv", index=False)

    if len(summary):
        rank = {"PASS": 2, "WARN": 1, "FAIL": 0}
        tmp = summary.copy()
        tmp["rank"] = tmp.status.map(rank).fillna(-1)
        tmp = tmp.sort_values(["rank", "fraction_error_below_5pct", "median_spectral_prominence"], ascending=False)
        preferred = str(tmp.iloc[0].coordinate)
        overall = str(tmp.iloc[0].status)
    else:
        preferred, overall = None, "ACCESS_BLOCKED"

    report = {
        "dataset": HANDLE,
        "sampling_hz": FS,
        "spindle_hz_prior": SPINDLE_HZ,
        "tooth_hz_prior": TOOTH_HZ,
        "attempted_cuts": attempted,
        "downloaded_cuts": int(attempts_df.download_ok.sum()) if len(attempts_df) else 0,
        "audited_coordinate_rows": int(len(raw)),
        "preferred_coordinate": preferred,
        "overall_status": overall,
        "summary": summary.replace({np.nan: None}).to_dict("records") if len(summary) else [],
    }
    (OUT / "e000e_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# E000-E Results — Raw PHM2010 process-coordinate audit",
        "",
        f"Dataset: `{HANDLE}`; raw files are downloaded only on the runner and are not committed.",
        "",
        f"Attempted cuts: {attempted}; downloaded: {report['downloaded_cuts']}; coordinate rows audited: {len(raw)}.",
        "",
    ]
    if len(summary):
        md += ["## Coordinate summary", "", summary.to_markdown(index=False), ""]
        md += [
            f"Preferred provisional coordinate: **{preferred}**; gate result: **{overall}**.",
            "",
            "This result addresses only H002c_1 (observability). It is not evidence that Process Token outperforms Fixed Patch.",
        ]
    else:
        md += [
            "## Result",
            "",
            "No raw cuts could be audited. This is a data-access result, not a scientific failure of H002c_1.",
            "See `download_audit.csv` for access errors.",
        ]
    (OUT / "README.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
