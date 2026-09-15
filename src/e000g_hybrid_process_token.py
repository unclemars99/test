"""E000-G: Hybrid Process Token = raw force patch + explicit spindle phase.

Raw waveform boundaries are identical across all conditions. The only manipulated
variable is whether physically recovered phase is exposed as sin/cos channels.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from scipy import signal
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

import e000f_fixed_vs_process_token as base

REPS = ["fixed_raw", "hybrid_phase", "hybrid_random_phase"]
OUT = Path("results/e000g")


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def phase_series(force: np.ndarray) -> tuple[np.ndarray, float, float]:
    xp = base.robust_phase_signal(force[0])
    peak, err = base.spindle_peak(xp)
    sos = signal.butter(4, [peak * 0.82, peak * 1.18], btype="bandpass", fs=base.FS, output="sos")
    xf = signal.sosfiltfilt(sos, xp)
    ph = np.unwrap(np.angle(signal.hilbert(xf)))
    return ph, peak, err


def build_tokens(force: np.ndarray, cutter: str, cut: int):
    ph, peak, err = phase_series(force)
    need = base.K_TOKENS * base.Q
    if force.shape[1] < need:
        raise ValueError(f"force segment too short: {force.shape[1]} < {need}")
    s0 = (force.shape[1] - need) // 2
    raw = force[:, s0:s0 + need].reshape(3, base.K_TOKENS, base.Q).transpose(1, 0, 2).astype(np.float32)
    p = ph[s0:s0 + need].reshape(base.K_TOKENS, base.Q)

    sinp, cosp = np.sin(p).astype(np.float32), np.cos(p).astype(np.float32)
    zeros = np.zeros_like(sinp, dtype=np.float32)
    fixed = np.concatenate([raw, zeros[:, None, :], zeros[:, None, :]], axis=1)
    hybrid = np.concatenate([raw, sinp[:, None, :], cosp[:, None, :]], axis=1)

    rng = np.random.default_rng(int(cutter[1:]) * 10000 + cut)
    delta = float(rng.uniform(0.0, 2 * np.pi))
    sr, cr = np.sin(p + delta).astype(np.float32), np.cos(p + delta).astype(np.float32)
    random_phase = np.concatenate([raw, sr[:, None, :], cr[:, None, :]], axis=1)

    return {
        "fixed_raw": fixed,
        "hybrid_phase": hybrid,
        "hybrid_random_phase": random_phase,
    }, {
        "cutter": cutter,
        "cut": cut,
        "peak_hz": peak,
        "freq_error_pct": err,
        "random_phase_offset_rad": delta,
    }


class TokenEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(5, 16, kernel_size=9, stride=4, padding=4), nn.ReLU(),
            nn.Conv1d(16, 32, kernel_size=7, stride=4, padding=3), nn.ReLU(),
        )
        self.head = nn.Linear(32 * 18, 12)

    def forward(self, x):
        return self.head(self.conv(x).flatten(1))


def standardize_raw_channels(train_x: np.ndarray, x: np.ndarray) -> np.ndarray:
    # Only raw force channels are standardized. Phase channels remain bounded sin/cos or zero.
    mu = train_x[:, :, :3, :].mean(axis=(0, 1, 3), keepdims=True)
    sd = train_x[:, :, :3, :].std(axis=(0, 1, 3), keepdims=True)
    sd = np.maximum(sd, 1e-6)
    out = x.copy().astype(np.float32)
    out[:, :, :3, :] = (out[:, :, :3, :] - mu) / sd
    return out


def fit_encoder(train_tokens: np.ndarray, seed: int):
    set_seed(seed)
    enc = TokenEncoder()
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3, weight_decay=1e-5)
    flat = torch.tensor(train_tokens.reshape(-1, 5, base.Q), dtype=torch.float32)
    n, batch = len(flat), 256
    for _ in range(40):
        perm = torch.randperm(n)
        for start in range(0, n, batch):
            xb = flat[perm[start:start + batch]]
            z1 = enc(base.augment(xb))
            z2 = enc(base.augment(xb))
            loss = base.vicreg_loss(z1, z2)
            opt.zero_grad(); loss.backward(); opt.step()
    return enc.eval()


def encode_cuts(enc, x: np.ndarray) -> np.ndarray:
    out = []
    with torch.no_grad():
        for tokens in x:
            zs = []
            for s in range(0, base.K_TOKENS, 64):
                xb = torch.tensor(tokens[s:s + 64], dtype=torch.float32)
                zs.append(enc(xb).cpu().numpy())
            z = np.concatenate(zs, axis=0)
            out.append(np.concatenate([z.mean(0), z.std(0)]))
    return np.asarray(out, np.float32)


def eval_probe(ztr, zte, ytr, yte):
    sc = StandardScaler().fit(ztr)
    model = Ridge(alpha=10.0).fit(sc.transform(ztr), ytr)
    pred = model.predict(sc.transform(zte))
    return {
        "wear_mae": float(mean_absolute_error(yte, pred)),
        "wear_nmae_range": float(mean_absolute_error(yte, pred) / (np.ptp(yte) + 1e-12)),
        "wear_r2": float(r2_score(yte, pred)),
    }


def gate(summary, fold, detail):
    sm = summary.set_index("representation")
    h, f, r = sm.loc["hybrid_phase", "wear_r2_mean"], sm.loc["fixed_raw", "wear_r2_mean"], sm.loc["hybrid_random_phase", "wear_r2_mean"]
    hmin, fmin = sm.loc["hybrid_phase", "wear_r2_min_fold"], sm.loc["fixed_raw", "wear_r2_min_fold"]
    fp = fold.pivot(index="heldout_cutter", columns="representation", values="wear_r2")
    folds_won = int((fp.hybrid_phase > fp.fixed_raw).sum())
    dp = detail.pivot_table(index=["heldout_cutter", "seed"], columns="representation", values="wear_r2")
    seed_means = dp.groupby("seed").mean(numeric_only=True)
    seeds_won = int((seed_means.hybrid_phase > seed_means.fixed_raw).sum())
    checks = {
        "mean_gain_vs_fixed_ge_0p05": bool(h - f >= 0.05),
        "worst_fold_not_worse_than_fixed": bool(hmin >= fmin),
        "mean_gain_vs_random_phase_ge_0p05": bool(h - r >= 0.05),
        "beats_fixed_in_at_least_2_folds": bool(folds_won >= 2),
        "beats_fixed_in_at_least_4_of_5_seed_means": bool(seeds_won >= 4),
    }
    n = sum(checks.values())
    status = "SUPPORTED" if n == 5 else ("PARTIAL" if n >= 3 else "NOT_SUPPORTED")
    return {
        "h002f_status": status,
        "checks": checks,
        "hybrid_minus_fixed_mean_r2": float(h - f),
        "hybrid_minus_random_mean_r2": float(h - r),
        "folds_hybrid_beats_fixed": folds_won,
        "seed_means_hybrid_beats_fixed": seeds_won,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base.CACHE.mkdir(parents=True, exist_ok=True)
    labels = pd.read_csv(base.LABEL_URL)[["cutter", "cut_index", "wear"]]
    label_map = {(str(r.cutter), int(r.cut_index)): float(r.wear) for r in labels.itertuples()}

    tokens = {r: [] for r in REPS}
    meta, audits, failures = [], [], []
    for cutter in base.CUTTERS:
        for cut in base.CUTS:
            try:
                p = base.download_cut(cutter, cut)
                df = pd.read_csv(p, header=None)
                force = base.central_force(df)
                reps, audit = build_tokens(force, cutter, cut)
                if audit["freq_error_pct"] >= 5.0:
                    raise ValueError(f"spindle coordinate error {audit['freq_error_pct']:.3f}% >= 5%")
                wear = label_map[(cutter, cut)]
                for rep in REPS:
                    tokens[rep].append(reps[rep])
                meta.append({"cutter": cutter, "cut": cut, "wear": wear})
                audits.append(audit)
            except Exception as exc:
                failures.append({"cutter": cutter, "cut": cut, "error": f"{type(exc).__name__}: {exc}"})

    meta = pd.DataFrame(meta)
    pd.DataFrame(audits).to_csv(OUT / "phase_audit.csv", index=False)
    pd.DataFrame(failures).to_csv(OUT / "preparation_failures.csv", index=False)
    if len(meta) < 36 or any((meta.cutter == c).sum() < 12 for c in base.CUTTERS):
        raise RuntimeError(f"insufficient common cuts: {meta.groupby('cutter').size().to_dict()}")

    arr = {rep: np.stack(tokens[rep]).astype(np.float32) for rep in REPS}
    cutters = meta.cutter.to_numpy(); y = meta.wear.to_numpy(float)
    rows = []
    for heldout in base.CUTTERS:
        tr, te = cutters != heldout, cutters == heldout
        for rep in REPS:
            xtr = standardize_raw_channels(arr[rep][tr], arr[rep][tr])
            xte = standardize_raw_channels(arr[rep][tr], arr[rep][te])
            for seed in base.SEEDS:
                enc = fit_encoder(xtr, seed)
                ztr, zte = encode_cuts(enc, xtr), encode_cuts(enc, xte)
                m = eval_probe(ztr, zte, y[tr], y[te])
                rows.append({"representation": rep, "heldout_cutter": heldout, "seed": seed,
                             "n_train_cuts": int(tr.sum()), "n_test_cuts": int(te.sum()), **m})

    detail = pd.DataFrame(rows)
    detail.to_csv(OUT / "e000g_seed_detail.csv", index=False)
    fold = (detail.groupby(["representation", "heldout_cutter"], as_index=False)
            .agg(wear_mae=("wear_mae", "mean"), wear_nmae_range=("wear_nmae_range", "mean"),
                 wear_r2=("wear_r2", "mean"), wear_r2_seed_std=("wear_r2", "std")))
    fold.to_csv(OUT / "e000g_fold_summary.csv", index=False)
    sr = []
    for rep, g in fold.groupby("representation"):
        sr.append({"representation": rep, "wear_mae_mean": float(g.wear_mae.mean()),
                   "wear_nmae_range_mean": float(g.wear_nmae_range.mean()),
                   "wear_r2_mean": float(g.wear_r2.mean()), "wear_r2_min_fold": float(g.wear_r2.min()),
                   "wear_r2_max_fold": float(g.wear_r2.max()), "fold_r2_range": float(g.wear_r2.max()-g.wear_r2.min()),
                   "mean_fold_seed_std": float(g.wear_r2_seed_std.mean())})
    summary = pd.DataFrame(sr).sort_values("representation")
    summary.to_csv(OUT / "e000g_summary.csv", index=False)
    dec = gate(summary, fold, detail)
    report = {"dataset": base.HANDLE, "cuts_used": int(len(meta)), "tokens_per_cut": base.K_TOKENS,
              "samples_per_token": base.Q, "representations": REPS, "summary": summary.to_dict("records"),
              "folds": fold.to_dict("records"), "decision": dec}
    (OUT / "e000g_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = ["# E000-G Results — Hybrid Process Token", "", summary.to_markdown(index=False), "",
          "## Fold results", "", fold.to_markdown(index=False), "", "## Pre-registered H002f gate", "",
          f"Status: **{dec['h002f_status']}**", ""]
    md += [f"- {k}: {'PASS' if v else 'FAIL'}" for k, v in dec["checks"].items()]
    md += ["", "The raw force waveform and patch boundaries are identical across all conditions; only explicit phase side-information changes."]
    (OUT / "README.md").write_text("\n".join(md), encoding="utf-8")
    print(summary.to_string(index=False)); print(fold.to_string(index=False)); print(json.dumps(dec, indent=2))


if __name__ == "__main__":
    main()
