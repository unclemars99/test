"""E000-H: test whether ordered physical composition adds value.

The same three tooth-sector waveforms are used in both conditions. Only their
within-revolution order differs. This isolates H002e from the already rejected
hard-alignment and explicit-phase-channel hypotheses.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy import signal
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

import e000f_fixed_vs_process_token as base

OUT = Path("results/e000h")
REPS = ["ordered_composition", "shuffled_composition"]
TOOTH_Q = 96
REV_Q = 3 * TOOTH_Q
NONIDENTITY_PERMS = np.asarray([
    [0, 2, 1],
    [1, 0, 2],
    [1, 2, 0],
    [2, 0, 1],
    [2, 1, 0],
], dtype=np.int64)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def common_phase_boundaries(force: np.ndarray):
    """Common analytic-phase 2pi crossings, matching corrected E000-F v2."""
    xp = base.robust_phase_signal(force[0])
    peak, err = base.spindle_peak(xp)
    sos = signal.butter(
        4, [peak * 0.82, peak * 1.18], btype="bandpass", fs=base.FS, output="sos"
    )
    xf = signal.sosfiltfilt(sos, xp)
    ph = np.unwrap(np.angle(signal.hilbert(xf)))
    turns = np.floor(ph / (2 * np.pi)).astype(np.int64)
    boundaries = np.flatnonzero(np.diff(turns) > 0) + 1
    return boundaries, peak, err


def build_revolutions(force: np.ndarray, cutter: str, cut: int):
    boundaries, peak, freq_err = common_phase_boundaries(force)
    expected = base.FS / base.SPINDLE_HZ
    revs, periods = [], []
    for i in range(len(boundaries) - 1):
        s, e = int(boundaries[i]), int(boundaries[i + 1])
        period = e - s
        if 0.80 * expected <= period <= 1.20 * expected:
            rev = base.resample_cycle(force[:, s:e], REV_Q)  # (3 channels, 288)
            teeth = rev.reshape(3, 3, TOOTH_Q).transpose(1, 0, 2)  # (3 teeth,3 ch,96)
            revs.append(teeth.astype(np.float32))
            periods.append(period)

    if len(revs) < base.K_TOKENS:
        raise ValueError(f"only {len(revs)} valid revolutions; need {base.K_TOKENS}")
    mid = len(revs) // 2
    s0 = mid - base.K_TOKENS // 2
    ordered = np.stack(revs[s0:s0 + base.K_TOKENS]).astype(np.float32)

    # Deterministic but non-identity permutation for every revolution. The same
    # permutation is seen by both SSL views; content and segmentation are intact,
    # but there is no globally consistent physical tooth order.
    shuffled = ordered.copy()
    perm_ids = []
    rng = np.random.default_rng(int(cutter[1:]) * 100_000 + cut)
    for r in range(base.K_TOKENS):
        pid = int(rng.integers(0, len(NONIDENTITY_PERMS)))
        perm = NONIDENTITY_PERMS[pid]
        shuffled[r] = ordered[r, perm]
        perm_ids.append(pid)

    periods = np.asarray(periods, dtype=float)
    audit = {
        "cutter": cutter,
        "cut": cut,
        "peak_hz": float(peak),
        "freq_error_pct": float(freq_err),
        "valid_revolutions": int(len(revs)),
        "median_period_samples": float(np.median(periods)),
        "period_cv": float(np.std(periods) / (np.mean(periods) + 1e-12)),
        "nonidentity_fraction": 1.0,
        "n_unique_permutation_types": int(len(np.unique(perm_ids))),
    }
    return {
        "ordered_composition": ordered,
        "shuffled_composition": shuffled,
    }, audit


class HierarchicalEncoder(nn.Module):
    """Tooth -> revolution encoder. Architecture is identical for both conditions."""

    def __init__(self):
        super().__init__()
        self.tooth = nn.Sequential(
            nn.Conv1d(3, 16, kernel_size=7, stride=4, padding=3),
            nn.ReLU(),
            nn.Conv1d(16, 32, kernel_size=5, stride=4, padding=2),
            nn.ReLU(),
        )
        self.tooth_head = nn.Linear(32 * 6, 12)
        self.rev_head = nn.Sequential(
            nn.Linear(36, 32),
            nn.ReLU(),
            nn.Linear(32, 12),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, 3 tooth sectors, 3 force channels, 96 samples)
        b = x.shape[0]
        t = x.reshape(b * 3, 3, TOOTH_Q)
        h = self.tooth(t).flatten(1)
        zt = self.tooth_head(h).reshape(b, 3, 12)
        return self.rev_head(zt.flatten(1))


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


def fit_standardizer(train_x: np.ndarray):
    # (Ncut, Nrev, 3 teeth, 3 channels, 96)
    mu = train_x.mean(axis=(0, 1, 2, 4), keepdims=True)
    sd = train_x.std(axis=(0, 1, 2, 4), keepdims=True)
    return mu.astype(np.float32), np.maximum(sd, 1e-6).astype(np.float32)


def standardize(x: np.ndarray, mu: np.ndarray, sd: np.ndarray) -> np.ndarray:
    return ((x - mu) / sd).astype(np.float32)


def fit_encoder(train_x: np.ndarray, seed: int) -> HierarchicalEncoder:
    set_seed(seed)
    enc = HierarchicalEncoder()
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3, weight_decay=1e-5)
    revs = torch.tensor(train_x.reshape(-1, 3, 3, TOOTH_Q), dtype=torch.float32)
    n, batch = len(revs), 256
    for _ in range(40):
        perm = torch.randperm(n)
        for start in range(0, n, batch):
            xb = revs[perm[start:start + batch]]
            z1 = enc(augment(xb))
            z2 = enc(augment(xb))
            loss = vicreg_loss(z1, z2)
            opt.zero_grad()
            loss.backward()
            opt.step()
    return enc.eval()


def encode_cuts(enc: HierarchicalEncoder, x: np.ndarray) -> np.ndarray:
    ncut, nrev = x.shape[:2]
    flat = x.reshape(-1, 3, 3, TOOTH_Q)
    zs = []
    with torch.no_grad():
        for start in range(0, len(flat), 512):
            xb = torch.tensor(flat[start:start + 512], dtype=torch.float32)
            zs.append(enc(xb).cpu().numpy())
    z = np.concatenate(zs, axis=0).reshape(ncut, nrev, 12)
    return np.concatenate([z.mean(axis=1), z.std(axis=1)], axis=1).astype(np.float32)


def eval_probe(ztr, zte, ytr, yte):
    sc = StandardScaler().fit(ztr)
    model = Ridge(alpha=10.0).fit(sc.transform(ztr), ytr)
    pred = model.predict(sc.transform(zte))
    return {
        "wear_mae": float(mean_absolute_error(yte, pred)),
        "wear_nmae_range": float(mean_absolute_error(yte, pred) / (np.ptp(yte) + 1e-12)),
        "wear_r2": float(r2_score(yte, pred)),
    }


def decision(summary: pd.DataFrame, fold: pd.DataFrame, detail: pd.DataFrame) -> dict:
    sm = summary.set_index("representation")
    ordered = float(sm.loc["ordered_composition", "wear_r2_mean"])
    shuffled = float(sm.loc["shuffled_composition", "wear_r2_mean"])
    omin = float(sm.loc["ordered_composition", "wear_r2_min_fold"])
    smin = float(sm.loc["shuffled_composition", "wear_r2_min_fold"])
    ostd = float(sm.loc["ordered_composition", "mean_fold_seed_std"])
    sstd = float(sm.loc["shuffled_composition", "mean_fold_seed_std"])

    fp = fold.pivot(index="heldout_cutter", columns="representation", values="wear_r2")
    folds_won = int((fp.ordered_composition > fp.shuffled_composition).sum())
    dp = detail.pivot_table(index=["heldout_cutter", "seed"], columns="representation", values="wear_r2")
    seed_means = dp.groupby("seed").mean(numeric_only=True)
    seeds_won = int((seed_means.ordered_composition > seed_means.shuffled_composition).sum())

    checks = {
        "mean_gain_over_shuffled_ge_0p05": bool(ordered - shuffled >= 0.05),
        "worst_fold_not_worse_than_shuffled": bool(omin >= smin),
        "wins_at_least_2_of_3_folds": bool(folds_won >= 2),
        "wins_at_least_4_of_5_seed_means": bool(seeds_won >= 4),
        "seed_std_not_more_than_0p05_worse": bool(ostd <= sstd + 0.05),
    }
    n = sum(checks.values())
    status = "SUPPORTED" if n == 5 else ("PARTIAL" if n >= 3 else "NOT_SUPPORTED")
    return {
        "h002e_status": status,
        "checks": checks,
        "ordered_minus_shuffled_mean_r2": ordered - shuffled,
        "folds_ordered_wins": folds_won,
        "seed_means_ordered_wins": seeds_won,
        "ordered_mean_fold_seed_std": ostd,
        "shuffled_mean_fold_seed_std": sstd,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    base.CACHE.mkdir(parents=True, exist_ok=True)
    labels = pd.read_csv(base.LABEL_URL)[["cutter", "cut_index", "wear"]]
    label_map = {(str(r.cutter), int(r.cut_index)): float(r.wear) for r in labels.itertuples()}

    data = {r: [] for r in REPS}
    meta, audits, failures = [], [], []
    for cutter in base.CUTTERS:
        for cut in base.CUTS:
            try:
                p = base.download_cut(cutter, cut)
                df = pd.read_csv(p, header=None)
                if df.shape[1] != 7:
                    raise ValueError(f"expected 7 columns, got {df.shape[1]}")
                force = base.central_force(df)
                reps, audit = build_revolutions(force, cutter, cut)
                if audit["freq_error_pct"] >= 5.0:
                    raise ValueError(f"spindle coordinate error {audit['freq_error_pct']:.3f}% >= 5%")
                key = (cutter, cut)
                wear = label_map[key]
                for rep in REPS:
                    data[rep].append(reps[rep])
                meta.append({"cutter": cutter, "cut": cut, "wear": wear})
                audits.append(audit)
            except Exception as exc:
                failures.append({"cutter": cutter, "cut": cut, "error": f"{type(exc).__name__}: {exc}"})

    meta = pd.DataFrame(meta)
    pd.DataFrame(audits).to_csv(OUT / "composition_audit.csv", index=False)
    pd.DataFrame(failures).to_csv(OUT / "preparation_failures.csv", index=False)
    if len(meta) < 36 or any((meta.cutter == c).sum() < 12 for c in base.CUTTERS):
        raise RuntimeError(f"insufficient common cuts: {meta.groupby('cutter').size().to_dict()}")

    arr = {rep: np.stack(data[rep]).astype(np.float32) for rep in REPS}
    cutters = meta.cutter.to_numpy()
    y = meta.wear.to_numpy(float)
    rows = []

    for heldout in base.CUTTERS:
        tr, te = cutters != heldout, cutters == heldout
        for rep in REPS:
            mu, sd = fit_standardizer(arr[rep][tr])
            xtr = standardize(arr[rep][tr], mu, sd)
            xte = standardize(arr[rep][te], mu, sd)
            for seed in base.SEEDS:
                enc = fit_encoder(xtr, seed)
                ztr = encode_cuts(enc, xtr)
                zte = encode_cuts(enc, xte)
                metrics = eval_probe(ztr, zte, y[tr], y[te])
                rows.append({
                    "representation": rep,
                    "heldout_cutter": heldout,
                    "seed": seed,
                    "n_train_cuts": int(tr.sum()),
                    "n_test_cuts": int(te.sum()),
                    **metrics,
                })

    detail = pd.DataFrame(rows)
    detail.to_csv(OUT / "e000h_seed_detail.csv", index=False)
    fold = (detail.groupby(["representation", "heldout_cutter"], as_index=False)
            .agg(wear_mae=("wear_mae", "mean"),
                 wear_nmae_range=("wear_nmae_range", "mean"),
                 wear_r2=("wear_r2", "mean"),
                 wear_r2_seed_std=("wear_r2", "std")))
    fold.to_csv(OUT / "e000h_fold_summary.csv", index=False)

    summaries = []
    for rep, g in fold.groupby("representation"):
        summaries.append({
            "representation": rep,
            "wear_mae_mean": float(g.wear_mae.mean()),
            "wear_nmae_range_mean": float(g.wear_nmae_range.mean()),
            "wear_r2_mean": float(g.wear_r2.mean()),
            "wear_r2_min_fold": float(g.wear_r2.min()),
            "wear_r2_max_fold": float(g.wear_r2.max()),
            "fold_r2_range": float(g.wear_r2.max() - g.wear_r2.min()),
            "mean_fold_seed_std": float(g.wear_r2_seed_std.mean()),
        })
    summary = pd.DataFrame(summaries).sort_values("representation")
    summary.to_csv(OUT / "e000h_summary.csv", index=False)
    dec = decision(summary, fold, detail)

    report = {
        "dataset": base.HANDLE,
        "cuts_used": int(len(meta)),
        "revolutions_per_cut": base.K_TOKENS,
        "tooth_sectors_per_revolution": 3,
        "samples_per_tooth_sector": TOOTH_Q,
        "ssl": "revolution-level VICReg with identical hierarchical encoder; 5 seeds; strict LOCO",
        "summary": summary.to_dict("records"),
        "folds": fold.to_dict("records"),
        "decision": dec,
    }
    (OUT / "e000h_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# E000-H Results — Ordered Physical Composition",
        "",
        summary.to_markdown(index=False),
        "",
        "## Fold results",
        "",
        fold.to_markdown(index=False),
        "",
        "## Pre-registered H002e gate",
        "",
        f"Status: **{dec['h002e_status']}**",
        "",
    ]
    md += [f"- {k}: {'PASS' if v else 'FAIL'}" for k, v in dec["checks"].items()]
    md += [
        "",
        "Both conditions contain the same raw tooth-sector samples and use the same hierarchy/model. Only globally meaningful within-revolution order is preserved or destroyed.",
    ]
    (OUT / "README.md").write_text("\n".join(md), encoding="utf-8")

    print(summary.to_string(index=False))
    print(fold.to_string(index=False))
    print(json.dumps(dec, indent=2))


if __name__ == "__main__":
    main()
