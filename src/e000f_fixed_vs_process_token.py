"""E000-F: fair raw-signal comparison of Fixed Patch vs Process Token.

H002c_2 experiment on PHM2010 force signals. Raw Kaggle files are downloaded
only during the GitHub Actions run and are never committed.
"""
from __future__ import annotations

import json
import os
import random
from pathlib import Path

import kagglehub
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy import signal
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

HANDLE = "rabahba/phm-data-challenge-2010"
LABEL_URL = "https://raw.githubusercontent.com/tayyabrehman96/XAI-PdMNet-Bench-Industry-5.0/main/data/phm2010/phm2010_feature_table.csv"
FS = 50_000.0
SPINDLE_HZ = 10_400.0 / 60.0
CUTTERS = ["C1", "C4", "C6"]
CUTS = [1, 23, 46, 68, 91, 113, 136, 158, 180, 203, 225, 248, 270, 293, 315]
K_TOKENS = 128
Q = 288
SEEDS = [7, 17, 29, 41, 53]
REPS = ["fixed_patch", "process_token", "random_phase"]
OUT = Path("results/e000f")
CACHE = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "phm2010_e000f"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def remote_path(cutter: str, cut: int) -> str:
    c = cutter.lower()
    cid = c[1:]
    return f"{c}/{c}/c_{cid}_{cut:03d}.csv"


def download_cut(cutter: str, cut: int) -> Path:
    rel = remote_path(cutter, cut)
    returned = kagglehub.dataset_download(HANDLE, path=rel, output_dir=str(CACHE))
    p = Path(returned)
    if p.is_file():
        return p
    hits = list(p.rglob(Path(rel).name)) if p.is_dir() else []
    if not hits and CACHE.exists():
        hits = list(CACHE.rglob(Path(rel).name))
    if not hits:
        raise FileNotFoundError(f"downloaded {rel} but could not locate local file: {returned}")
    return hits[0]


def central_force(df: pd.DataFrame) -> np.ndarray:
    x = df.iloc[:, :3].to_numpy(np.float32).T  # (3,T)
    n = x.shape[1]
    s, e = n // 4, (3 * n) // 4
    return x[:, s:e]


def robust_phase_signal(x: np.ndarray) -> np.ndarray:
    y = signal.detrend(np.asarray(x, dtype=float), type="linear")
    med = np.median(y)
    mad = np.median(np.abs(y - med)) * 1.4826
    scale = mad if np.isfinite(mad) and mad > 1e-12 else np.std(y) + 1e-12
    return (y - med) / scale


def spindle_peak(x: np.ndarray) -> tuple[float, float]:
    nperseg = min(16384, max(2048, len(x) // 4))
    f, pxx = signal.welch(
        x, fs=FS, window="hann", nperseg=nperseg, noverlap=nperseg // 2,
        detrend="linear", scaling="density"
    )
    band = (f >= SPINDLE_HZ * 0.82) & (f <= SPINDLE_HZ * 1.18)
    fb, pb = f[band], pxx[band]
    j = int(np.argmax(pb))
    peak = float(fb[j])
    err = abs(peak - SPINDLE_HZ) / SPINDLE_HZ * 100.0
    return peak, err


def phase_boundaries(force: np.ndarray) -> tuple[np.ndarray, float, float]:
    # E000-E found Fx to be the stable spindle-coordinate channel across audited cuts.
    xp = robust_phase_signal(force[0])
    peak, err = spindle_peak(xp)
    low, high = peak * 0.82, peak * 1.18
    sos = signal.butter(4, [low, high], btype="bandpass", fs=FS, output="sos")
    xf = signal.sosfiltfilt(sos, xp)
    ph = np.unwrap(np.angle(signal.hilbert(xf)))
    turns = np.floor((ph - ph[0]) / (2 * np.pi)).astype(np.int64)
    b = np.flatnonzero(np.diff(turns) > 0) + 1
    return b, peak, err


def resample_cycle(seg: np.ndarray, q: int = Q) -> np.ndarray:
    old = np.linspace(0.0, 1.0, seg.shape[1], dtype=np.float64)
    new = np.linspace(0.0, 1.0, q, dtype=np.float64)
    return np.stack([np.interp(new, old, seg[c]).astype(np.float32) for c in range(seg.shape[0])])


def build_tokens(force: np.ndarray, cutter: str, cut: int) -> tuple[dict[str, np.ndarray], dict]:
    b, peak, freq_err = phase_boundaries(force)
    expected_period = FS / SPINDLE_HZ
    cycles = []
    periods = []
    for i in range(len(b) - 1):
        s, e = int(b[i]), int(b[i + 1])
        period = e - s
        if 0.80 * expected_period <= period <= 1.20 * expected_period:
            cycles.append(resample_cycle(force[:, s:e], Q))
            periods.append(period)
    if len(cycles) < K_TOKENS:
        raise ValueError(f"only {len(cycles)} valid spindle cycles; need {K_TOKENS}")
    mid = len(cycles) // 2
    s0 = mid - K_TOKENS // 2
    proc = np.stack(cycles[s0:s0 + K_TOKENS]).astype(np.float32)  # (K,3,Q)

    # Strong fixed-patch control: same approximate physical scale, no phase alignment.
    need = K_TOKENS * Q
    if force.shape[1] < need:
        raise ValueError(f"center force segment too short: {force.shape[1]} < {need}")
    fs0 = (force.shape[1] - need) // 2
    fixed = force[:, fs0:fs0 + need].reshape(3, K_TOKENS, Q).transpose(1, 0, 2).copy().astype(np.float32)

    # Preserve revolution segmentation but randomize cross-cut phase origin.
    rng = np.random.default_rng(int(cutter[1:]) * 10000 + cut)
    shift = int(rng.integers(1, Q))
    rand = np.roll(proc, shift=shift, axis=2).copy()

    periods_arr = np.asarray(periods, dtype=float)
    audit = {
        "cutter": cutter,
        "cut": cut,
        "peak_hz": peak,
        "freq_error_pct": freq_err,
        "valid_cycles": len(cycles),
        "median_period_samples": float(np.median(periods_arr)),
        "period_cv": float(np.std(periods_arr) / (np.mean(periods_arr) + 1e-12)),
        "random_phase_shift_samples": shift,
    }
    return {"fixed_patch": fixed, "process_token": proc, "random_phase": rand}, audit


class TokenEncoder(nn.Module):
    """Position-sensitive local waveform encoder; identical for all tokenizations."""
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(3, 16, kernel_size=9, stride=4, padding=4), nn.ReLU(),
            nn.Conv1d(16, 32, kernel_size=7, stride=4, padding=3), nn.ReLU(),
        )
        self.head = nn.Linear(32 * 18, 12)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.conv(x)
        return self.head(h.flatten(1))


def augment(x: torch.Tensor, mask_p: float = 0.10, noise_std: float = 0.04) -> torch.Tensor:
    y = x.clone()
    mask = torch.rand_like(y) < mask_p
    y[mask] = 0.0
    return y + torch.randn_like(y) * noise_std


def off_diagonal(x: torch.Tensor) -> torch.Tensor:
    n, m = x.shape
    assert n == m
    return x.flatten()[:-1].view(n - 1, n + 1)[:, 1:].flatten()


def vicreg_loss(z1: torch.Tensor, z2: torch.Tensor) -> torch.Tensor:
    inv = F.mse_loss(z1, z2)
    eps = 1e-4
    std1 = torch.sqrt(z1.var(dim=0) + eps)
    std2 = torch.sqrt(z2.var(dim=0) + eps)
    var = F.relu(1.0 - std1).mean() + F.relu(1.0 - std2).mean()
    z1c, z2c = z1 - z1.mean(0), z2 - z2.mean(0)
    cov1 = (z1c.T @ z1c) / max(z1.shape[0] - 1, 1)
    cov2 = (z2c.T @ z2c) / max(z2.shape[0] - 1, 1)
    cov = off_diagonal(cov1).pow(2).mean() + off_diagonal(cov2).pow(2).mean()
    return 25.0 * inv + 25.0 * var + cov


def channel_standardizer(train_tokens: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # train_tokens: (Ncut,K,3,Q)
    mu = train_tokens.mean(axis=(0, 1, 3), keepdims=True)
    sd = train_tokens.std(axis=(0, 1, 3), keepdims=True)
    sd = np.maximum(sd, 1e-6)
    return mu.astype(np.float32), sd.astype(np.float32)


def apply_standardizer(x: np.ndarray, mu: np.ndarray, sd: np.ndarray) -> np.ndarray:
    return ((x - mu) / sd).astype(np.float32)


def fit_encoder(train_tokens: np.ndarray, seed: int) -> TokenEncoder:
    set_seed(seed)
    enc = TokenEncoder()
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3, weight_decay=1e-5)
    flat = torch.tensor(train_tokens.reshape(-1, 3, Q), dtype=torch.float32)
    n = len(flat)
    batch = 256
    for _ in range(40):
        perm = torch.randperm(n)
        for start in range(0, n, batch):
            xb = flat[perm[start:start + batch]]
            z1, z2 = enc(augment(xb)), enc(augment(xb))
            loss = vicreg_loss(z1, z2)
            opt.zero_grad()
            loss.backward()
            opt.step()
    return enc.eval()


def encode_cuts(enc: TokenEncoder, x: np.ndarray) -> np.ndarray:
    # x: (Ncut,K,3,Q); cut representation = mean + std over local-token embeddings.
    out = []
    with torch.no_grad():
        for cut_tokens in x:
            zs = []
            for start in range(0, K_TOKENS, 64):
                xb = torch.tensor(cut_tokens[start:start + 64], dtype=torch.float32)
                zs.append(enc(xb).cpu().numpy())
            z = np.concatenate(zs, axis=0)
            out.append(np.concatenate([z.mean(0), z.std(0)], axis=0))
    return np.asarray(out, dtype=np.float32)


def eval_one(ztr: np.ndarray, zte: np.ndarray, ytr: np.ndarray, yte: np.ndarray) -> dict:
    # Train-only normalization makes the fixed Ridge alpha comparable across representations.
    sc = StandardScaler().fit(ztr)
    a, b = sc.transform(ztr), sc.transform(zte)
    probe = Ridge(alpha=10.0).fit(a, ytr)
    pred = probe.predict(b)
    return {
        "wear_mae": float(mean_absolute_error(yte, pred)),
        "wear_nmae_range": float(mean_absolute_error(yte, pred) / (np.ptp(yte) + 1e-12)),
        "wear_r2": float(r2_score(yte, pred)),
    }


def decision(summary: pd.DataFrame, fold: pd.DataFrame, detail: pd.DataFrame) -> dict:
    means = summary.set_index("representation")["wear_r2_mean"].to_dict()
    mins = summary.set_index("representation")["wear_r2_min_fold"].to_dict()
    proc, fixed, rand = means["process_token"], means["fixed_patch"], means["random_phase"]
    fold_p = fold[fold.representation == "process_token"].set_index("heldout_cutter").wear_r2
    fold_f = fold[fold.representation == "fixed_patch"].set_index("heldout_cutter").wear_r2
    folds_won = int((fold_p > fold_f).sum())

    pivot = detail.pivot_table(index=["heldout_cutter", "seed"], columns="representation", values="wear_r2")
    seed_mean = pivot.groupby("seed").mean(numeric_only=True)
    seeds_won = int((seed_mean["process_token"] > seed_mean["fixed_patch"]).sum())

    checks = {
        "mean_gain_vs_fixed_ge_0p05": bool(proc - fixed >= 0.05),
        "worst_fold_not_worse_than_fixed": bool(mins["process_token"] >= mins["fixed_patch"]),
        "mean_gain_vs_random_phase_ge_0p05": bool(proc - rand >= 0.05),
        "beats_fixed_in_at_least_2_folds": bool(folds_won >= 2),
        "beats_fixed_in_at_least_4_of_5_seed_means": bool(seeds_won >= 4),
    }
    n = sum(checks.values())
    status = "SUPPORTED" if n == len(checks) else ("PARTIAL" if n >= 3 else "NOT_SUPPORTED")
    return {
        "h002c_2_status": status,
        "checks": checks,
        "process_minus_fixed_mean_r2": float(proc - fixed),
        "process_minus_random_mean_r2": float(proc - rand),
        "folds_process_beats_fixed": folds_won,
        "seed_means_process_beats_fixed": seeds_won,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    labels = pd.read_csv(LABEL_URL)[["cutter", "cut_index", "wear"]]
    label_map = {(str(r.cutter), int(r.cut_index)): float(r.wear) for r in labels.itertuples()}

    tokens: dict[str, list[np.ndarray]] = {r: [] for r in REPS}
    meta = []
    audits = []
    failures = []

    for cutter in CUTTERS:
        for cut in CUTS:
            try:
                p = download_cut(cutter, cut)
                df = pd.read_csv(p, header=None)
                if df.shape[1] != 7:
                    raise ValueError(f"expected 7 columns, got {df.shape[1]}")
                force = central_force(df)
                reps, audit = build_tokens(force, cutter, cut)
                if audit["freq_error_pct"] >= 5.0:
                    raise ValueError(f"spindle coordinate error {audit['freq_error_pct']:.3f}% >= 5%")
                key = (cutter, cut)
                if key not in label_map:
                    raise KeyError(f"missing wear label for {key}")
                for rep in REPS:
                    tokens[rep].append(reps[rep])
                meta.append({"cutter": cutter, "cut": cut, "wear": label_map[key]})
                audits.append(audit)
            except Exception as exc:
                failures.append({"cutter": cutter, "cut": cut, "error": f"{type(exc).__name__}: {exc}"})

    meta_df = pd.DataFrame(meta)
    pd.DataFrame(audits).to_csv(OUT / "tokenization_audit.csv", index=False)
    pd.DataFrame(failures).to_csv(OUT / "preparation_failures.csv", index=False)
    if len(meta_df) < 36 or any((meta_df.cutter == c).sum() < 12 for c in CUTTERS):
        raise RuntimeError(f"insufficient common raw cuts for fair E000-F: {meta_df.groupby('cutter').size().to_dict()}")

    arrays = {rep: np.stack(tokens[rep]).astype(np.float32) for rep in REPS}
    cutters = meta_df.cutter.to_numpy()
    y = meta_df.wear.to_numpy(float)
    rows = []

    for heldout in CUTTERS:
        tr = cutters != heldout
        te = cutters == heldout
        for rep in REPS:
            mu, sd = channel_standardizer(arrays[rep][tr])
            xtr = apply_standardizer(arrays[rep][tr], mu, sd)
            xte = apply_standardizer(arrays[rep][te], mu, sd)
            for seed in SEEDS:
                enc = fit_encoder(xtr, seed)
                ztr, zte = encode_cuts(enc, xtr), encode_cuts(enc, xte)
                metrics = eval_one(ztr, zte, y[tr], y[te])
                rows.append({
                    "representation": rep,
                    "heldout_cutter": heldout,
                    "seed": seed,
                    "n_train_cuts": int(tr.sum()),
                    "n_test_cuts": int(te.sum()),
                    **metrics,
                })

    detail = pd.DataFrame(rows)
    detail.to_csv(OUT / "e000f_seed_detail.csv", index=False)
    fold = (detail.groupby(["representation", "heldout_cutter"], as_index=False)
            .agg(wear_mae=("wear_mae", "mean"),
                 wear_nmae_range=("wear_nmae_range", "mean"),
                 wear_r2=("wear_r2", "mean"),
                 wear_r2_seed_std=("wear_r2", "std")))
    fold.to_csv(OUT / "e000f_fold_summary.csv", index=False)

    summary_rows = []
    for rep, g in fold.groupby("representation"):
        summary_rows.append({
            "representation": rep,
            "wear_mae_mean": float(g.wear_mae.mean()),
            "wear_nmae_range_mean": float(g.wear_nmae_range.mean()),
            "wear_r2_mean": float(g.wear_r2.mean()),
            "wear_r2_min_fold": float(g.wear_r2.min()),
            "wear_r2_max_fold": float(g.wear_r2.max()),
            "fold_r2_range": float(g.wear_r2.max() - g.wear_r2.min()),
            "mean_fold_seed_std": float(g.wear_r2_seed_std.mean()),
        })
    summary = pd.DataFrame(summary_rows).sort_values("representation")
    summary.to_csv(OUT / "e000f_summary.csv", index=False)
    dec = decision(summary, fold, detail)

    report = {
        "dataset": HANDLE,
        "cuts_requested_per_cutter": len(CUTS),
        "cuts_used": int(len(meta_df)),
        "tokens_per_cut": K_TOKENS,
        "samples_per_token": Q,
        "channels": ["Fx", "Fy", "Fz"],
        "ssl": "token-level VICReg, identical CNN encoder, 5 seeds, strict LOCO",
        "summary": summary.to_dict("records"),
        "folds": fold.to_dict("records"),
        "decision": dec,
    }
    (OUT / "e000f_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# E000-F Results — Fixed Patch vs Process Token",
        "",
        f"Common raw cuts used: {len(meta_df)}; token shape per cut: {K_TOKENS} x 3 x {Q}.",
        "",
        "## Aggregate comparison",
        "", summary.to_markdown(index=False), "",
        "## Fold comparison", "", fold.to_markdown(index=False), "",
        "## Pre-registered H002c_2 gate", "",
        f"Status: **{dec['h002c_2_status']}**", "",
    ]
    for k, v in dec["checks"].items():
        md.append(f"- {k}: {'PASS' if v else 'FAIL'}")
    md += [
        "",
        "## Guardrails",
        "",
        "- This is a small raw-data public POC, not final industrial validation.",
        "- Wear labels are downstream evaluation only and retain PHM2010 label limitations.",
        "- Token order is mean/std pooled, so this experiment tests within-token phase alignment, not ordered composition (H002e).",
        "- Raw files are not committed.",
    ]
    (OUT / "README.md").write_text("\n".join(md), encoding="utf-8")
    print(summary.to_string(index=False))
    print(fold.to_string(index=False))
    print(json.dumps(dec, indent=2))


if __name__ == "__main__":
    main()
