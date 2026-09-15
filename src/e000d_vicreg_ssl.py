"""E000-D: invariance-oriented generic SSL baseline (VICReg-lite).

This is still a feature-level H001 experiment. It does NOT test Process Token/H002.
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
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score, silhouette_score
from sklearn.preprocessing import StandardScaler

DATA_URL = "https://raw.githubusercontent.com/tayyabrehman96/XAI-PdMNet-Bench-Industry-5.0/main/data/phm2010/phm2010_feature_table.csv"
OUT = Path("results/e000d")
CUTTERS = ["C1", "C4", "C6"]
SEEDS = [7, 17, 29, 41, 53]


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class Encoder(nn.Module):
    def __init__(self, d_in: int, d_latent: int = 12):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, d_latent),
        )

    def forward(self, x):
        return self.net(x)


def augment(x: torch.Tensor, mask_p: float = 0.15, noise_std: float = 0.05) -> torch.Tensor:
    y = x.clone()
    mask = torch.rand_like(y) < mask_p
    y[mask] = 0.0
    y = y + torch.randn_like(y) * noise_std
    return y


def off_diagonal(x: torch.Tensor) -> torch.Tensor:
    n, m = x.shape
    assert n == m
    return x.flatten()[:-1].view(n - 1, n + 1)[:, 1:].flatten()


def vicreg_loss(z1: torch.Tensor, z2: torch.Tensor) -> torch.Tensor:
    inv = F.mse_loss(z1, z2)
    eps = 1e-4
    std1 = torch.sqrt(z1.var(dim=0) + eps)
    std2 = torch.sqrt(z2.var(dim=0) + eps)
    var = torch.mean(F.relu(1.0 - std1)) + torch.mean(F.relu(1.0 - std2))

    z1c = z1 - z1.mean(dim=0)
    z2c = z2 - z2.mean(dim=0)
    cov1 = (z1c.T @ z1c) / max(z1.shape[0] - 1, 1)
    cov2 = (z2c.T @ z2c) / max(z2.shape[0] - 1, 1)
    cov = off_diagonal(cov1).pow(2).mean() + off_diagonal(cov2).pow(2).mean()
    return 25.0 * inv + 25.0 * var + 1.0 * cov


def fit_encoder(x_train: np.ndarray, seed: int) -> Encoder:
    set_seed(seed)
    enc = Encoder(x_train.shape[1], 12)
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3, weight_decay=1e-5)
    xt = torch.tensor(x_train, dtype=torch.float32)
    n = len(xt)
    batch = 128
    for _ in range(350):
        perm = torch.randperm(n)
        for start in range(0, n, batch):
            idx = perm[start:start + batch]
            xb = xt[idx]
            z1 = enc(augment(xb))
            z2 = enc(augment(xb))
            loss = vicreg_loss(z1, z2)
            opt.zero_grad()
            loss.backward()
            opt.step()
    return enc.eval()


def encode(enc: Encoder, x: np.ndarray) -> np.ndarray:
    with torch.no_grad():
        return enc(torch.tensor(x, dtype=torch.float32)).cpu().numpy()


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return np.nan
    return float(1 - np.dot(a, b) / (na * nb))


def direction_cosine(ds: list[np.ndarray]) -> float:
    vals = []
    for i in range(len(ds)):
        for j in range(i + 1, len(ds)):
            a, b = ds[i], ds[j]
            if np.linalg.norm(a) > 1e-12 and np.linalg.norm(b) > 1e-12:
                vals.append(float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))))
    return float(np.mean(vals)) if vals else np.nan


def geometry(z_all: np.ndarray, df: pd.DataFrame) -> dict:
    state_d, dirs = [], []
    centroids = {}
    for c in CUTTERS:
        idx = np.where(df.cutter.to_numpy() == c)[0]
        w = df.iloc[idx].wear.to_numpy()
        q25, q75 = np.quantile(w, [0.25, 0.75])
        lo = z_all[idx[w <= q25]].mean(0)
        hi = z_all[idx[w >= q75]].mean(0)
        centroids[(c, "lo")] = lo
        centroids[(c, "hi")] = hi
        state_d.append(cosine_distance(lo, hi))
        dirs.append(hi - lo)
    domain_d = []
    for s in ["lo", "hi"]:
        cs = [centroids[(c, s)] for c in CUTTERS]
        for i in range(3):
            for j in range(i + 1, 3):
                domain_d.append(cosine_distance(cs[i], cs[j]))
    d_state = float(np.nanmean(state_d))
    d_domain = float(np.nanmean(domain_d))
    try:
        sil = float(silhouette_score(z_all, df.cutter.to_numpy(), metric="cosine"))
    except Exception:
        sil = np.nan
    return {
        "d_state_cosine": d_state,
        "d_domain_cosine": d_domain,
        "sharedness_ratio": d_state / (d_domain + 1e-12),
        "trajectory_cosine_mean": direction_cosine(dirs),
        "domain_silhouette_cosine": sil,
    }


def eval_rep(rep: str, heldout: str, seed: int, ztr, zte, zall, y, tr, te, df):
    probe = Ridge(alpha=10.0).fit(ztr, y[tr])
    pred = probe.predict(zte)
    return {
        "representation": rep,
        "heldout_cutter": heldout,
        "seed": seed,
        "wear_mae": float(mean_absolute_error(y[te], pred)),
        "wear_nmae_range": float(mean_absolute_error(y[te], pred) / (np.ptp(y[te]) + 1e-12)),
        "wear_r2": float(r2_score(y[te], pred)),
        **geometry(zall, df),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_URL)
    excluded = {"cutter", "cut_index", "wear", "failure_label"}
    feats = [c for c in df.columns if c not in excluded]
    x = df[feats].to_numpy(float)
    y = df.wear.to_numpy(float)
    cutters = df.cutter.to_numpy()
    rows = []

    for heldout in CUTTERS:
        tr = cutters != heldout
        te = cutters == heldout
        scaler = StandardScaler().fit(x[tr])
        xtr, xte, xall = scaler.transform(x[tr]), scaler.transform(x[te]), scaler.transform(x)

        pca = PCA(n_components=0.95, svd_solver="full").fit(xtr)
        rows.append(eval_rep("pca95", heldout, -1, pca.transform(xtr), pca.transform(xte), pca.transform(xall), y, tr, te, df))

        for seed in SEEDS:
            enc = fit_encoder(xtr, seed)
            rows.append(eval_rep("vicreg12", heldout, seed, encode(enc, xtr), encode(enc, xte), encode(enc, xall), y, tr, te, df))

    detail = pd.DataFrame(rows)
    detail.to_csv(OUT / "e000d_loco_seed_detail.csv", index=False)
    fold = (detail.groupby(["representation", "heldout_cutter"], as_index=False)
            .agg(wear_mae=("wear_mae", "mean"),
                 wear_nmae_range=("wear_nmae_range", "mean"),
                 wear_r2=("wear_r2", "mean"),
                 wear_r2_seed_std=("wear_r2", "std"),
                 sharedness_ratio=("sharedness_ratio", "mean"),
                 trajectory_cosine_mean=("trajectory_cosine_mean", "mean"),
                 domain_silhouette_cosine=("domain_silhouette_cosine", "mean")))
    fold.to_csv(OUT / "e000d_fold_summary.csv", index=False)

    summary = []
    for rep, g in fold.groupby("representation"):
        summary.append({
            "representation": rep,
            "wear_mae_mean": g.wear_mae.mean(),
            "wear_nmae_range_mean": g.wear_nmae_range.mean(),
            "wear_r2_mean": g.wear_r2.mean(),
            "wear_r2_min_fold": g.wear_r2.min(),
            "wear_r2_max_fold": g.wear_r2.max(),
            "fold_r2_range": g.wear_r2.max() - g.wear_r2.min(),
            "sharedness_ratio_mean": g.sharedness_ratio.mean(),
            "trajectory_cosine_mean": g.trajectory_cosine_mean.mean(),
            "domain_silhouette_cosine_mean": g.domain_silhouette_cosine.mean(),
        })
    summary = pd.DataFrame(summary).sort_values("representation")
    summary.to_csv(OUT / "e000d_summary.csv", index=False)
    (OUT / "e000d_results.json").write_text(json.dumps({
        "dataset_url": DATA_URL,
        "rows": len(df), "features": len(feats),
        "protocol": "3-fold LOCO; VICReg-lite 5 seeds; train-only scaler/SSL/probe",
        "summary": summary.to_dict("records"),
        "folds": fold.to_dict("records"),
    }, indent=2), encoding="utf-8")

    md = [
        "# E000-D Results — Invariance-oriented generic SSL",
        "",
        "VICReg-lite on engineered/statistical PHM2010-derived features; 5 seeds per LOCO fold.",
        "",
        "## Aggregate comparison",
        "", summary.to_markdown(index=False), "",
        "## Fold comparison", "", fold.to_markdown(index=False), "",
        "## Guardrails", "",
        "- This tests H001 only, not Process Token/H002.",
        "- Worst-fold performance and seed stability matter more than mean gain alone.",
        "- Feature augmentations are generic, not physically justified; success would establish a stronger generic SSL baseline, not a physical-token claim.",
    ]
    (OUT / "README.md").write_text("\n".join(md), encoding="utf-8")
    print(summary.to_string(index=False))
    print(fold.to_string(index=False))


if __name__ == "__main__":
    main()
