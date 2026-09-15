"""E000-C: generic self-supervised baseline on PHM2010-derived feature table.

Purpose
-------
Test H001 with a deliberately generic, non-physical self-supervised encoder before
attempting Process Token models. The encoder is a denoising autoencoder (DAE)
trained only on the two training cutters in each LOCO fold.

Important: this experiment does NOT test H002 Process Token because the input is
an engineered feature table rather than raw high-frequency waveforms.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score, silhouette_score
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

DATA_URL = "https://raw.githubusercontent.com/tayyabrehman96/XAI-PdMNet-Bench-Industry-5.0/main/data/phm2010/phm2010_feature_table.csv"
OUT = Path("results/e000c")
SEEDS = [7, 17, 29, 41, 53]
CUTTERS = ["C1", "C4", "C6"]


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(x, 0.0)


def encode_bottleneck(model: MLPRegressor, x: np.ndarray) -> np.ndarray:
    """Forward-pass to the 12-D bottleneck of hidden=(32,12,32)."""
    h1 = relu(x @ model.coefs_[0] + model.intercepts_[0])
    z = relu(h1 @ model.coefs_[1] + model.intercepts_[1])
    return z


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return np.nan
    return float(1.0 - np.dot(a, b) / (na * nb))


def pairwise_direction_cosine(directions: list[np.ndarray]) -> float:
    vals = []
    for i in range(len(directions)):
        for j in range(i + 1, len(directions)):
            a, b = directions[i], directions[j]
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            if na > 1e-12 and nb > 1e-12:
                vals.append(float(np.dot(a, b) / (na * nb)))
    return float(np.mean(vals)) if vals else np.nan


def geometry_metrics(z_all: np.ndarray, df: pd.DataFrame) -> dict:
    """Evaluation-only geometry using wear/cutter labels; labels never train encoder."""
    # Within each cutter, define low/high wear states by its own 25/75% quantiles.
    state_distances = []
    directions = []
    state_centroids: dict[tuple[str, str], np.ndarray] = {}
    for cutter in CUTTERS:
        idx = np.where(df["cutter"].to_numpy() == cutter)[0]
        w = df.iloc[idx]["wear"].to_numpy()
        q25, q75 = np.quantile(w, [0.25, 0.75])
        low_idx = idx[w <= q25]
        high_idx = idx[w >= q75]
        low = z_all[low_idx].mean(axis=0)
        high = z_all[high_idx].mean(axis=0)
        state_centroids[(cutter, "low")] = low
        state_centroids[(cutter, "high")] = high
        state_distances.append(cosine_distance(low, high))
        directions.append(high - low)

    # Cross-domain distance under approximately matched state (low/high wear state).
    domain_distances = []
    for state in ["low", "high"]:
        cs = [state_centroids[(c, state)] for c in CUTTERS]
        for i in range(3):
            for j in range(i + 1, 3):
                domain_distances.append(cosine_distance(cs[i], cs[j]))

    d_state = float(np.nanmean(state_distances))
    d_domain = float(np.nanmean(domain_distances))
    sharedness = d_state / (d_domain + 1e-12)
    traj = pairwise_direction_cosine(directions)

    # Cutter silhouette is evaluation-only. Lower domain separation is desirable
    # only when state/task information is retained.
    try:
        sil = float(silhouette_score(z_all, df["cutter"].to_numpy(), metric="cosine"))
    except Exception:
        sil = np.nan

    return {
        "d_state_cosine": d_state,
        "d_domain_cosine": d_domain,
        "sharedness_ratio": float(sharedness),
        "trajectory_cosine_mean": traj,
        "domain_silhouette_cosine": sil,
    }


def fit_dae(x_train: np.ndarray, seed: int) -> MLPRegressor:
    rng = np.random.default_rng(seed)
    corrupted = x_train.copy()
    mask = rng.random(corrupted.shape) < 0.15
    corrupted[mask] = 0.0
    corrupted += rng.normal(0.0, 0.05, size=corrupted.shape)

    model = MLPRegressor(
        hidden_layer_sizes=(32, 12, 32),
        activation="relu",
        solver="adam",
        alpha=1e-4,
        batch_size=64,
        learning_rate_init=1e-3,
        max_iter=800,
        early_stopping=True,
        validation_fraction=0.15,
        n_iter_no_change=40,
        random_state=seed,
    )
    model.fit(corrupted, x_train)
    return model


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_URL)
    excluded = {"cutter", "cut_index", "wear", "failure_label"}
    features = [c for c in df.columns if c not in excluded]
    x = df[features].to_numpy(dtype=float)
    y = df["wear"].to_numpy(dtype=float)
    cutters = df["cutter"].to_numpy()

    detail = []
    for heldout in CUTTERS:
        tr = cutters != heldout
        te = cutters == heldout
        scaler = StandardScaler().fit(x[tr])
        xtr = scaler.transform(x[tr])
        xte = scaler.transform(x[te])
        xall = scaler.transform(x)

        # Deterministic PCA95 lower baseline, train cutters only.
        pca = PCA(n_components=0.95, svd_solver="full").fit(xtr)
        reps = {
            "pca95": (pca.transform(xtr), pca.transform(xte), pca.transform(xall), int(pca.n_components_)),
        }
        for rep, (ztr, zte, zall, dim) in reps.items():
            probe = Ridge(alpha=10.0).fit(ztr, y[tr])
            pred = probe.predict(zte)
            geom = geometry_metrics(zall, df)
            detail.append({
                "heldout_cutter": heldout,
                "seed": -1,
                "representation": rep,
                "n_train": int(tr.sum()),
                "n_test": int(te.sum()),
                "wear_mae": float(mean_absolute_error(y[te], pred)),
                "wear_nmae_range": float(mean_absolute_error(y[te], pred) / (np.ptp(y[te]) + 1e-12)),
                "wear_r2": float(r2_score(y[te], pred)),
                "n_components": dim,
                **geom,
            })

        # Generic SSL: denoising autoencoder. No wear/cutter labels used in training.
        for seed in SEEDS:
            dae = fit_dae(xtr, seed)
            ztr = encode_bottleneck(dae, xtr)
            zte = encode_bottleneck(dae, xte)
            zall = encode_bottleneck(dae, xall)
            probe = Ridge(alpha=10.0).fit(ztr, y[tr])
            pred = probe.predict(zte)
            geom = geometry_metrics(zall, df)
            detail.append({
                "heldout_cutter": heldout,
                "seed": seed,
                "representation": "dae12",
                "n_train": int(tr.sum()),
                "n_test": int(te.sum()),
                "wear_mae": float(mean_absolute_error(y[te], pred)),
                "wear_nmae_range": float(mean_absolute_error(y[te], pred) / (np.ptp(y[te]) + 1e-12)),
                "wear_r2": float(r2_score(y[te], pred)),
                "n_components": 12,
                **geom,
            })

    detail_df = pd.DataFrame(detail)
    detail_df.to_csv(OUT / "e000c_loco_seed_detail.csv", index=False)

    # Fold-level DAE means over seeds; PCA has one deterministic row per fold.
    fold_df = (detail_df.groupby(["representation", "heldout_cutter"], as_index=False)
               .agg(wear_mae=("wear_mae", "mean"),
                    wear_nmae_range=("wear_nmae_range", "mean"),
                    wear_r2=("wear_r2", "mean"),
                    wear_r2_seed_std=("wear_r2", "std"),
                    d_state_cosine=("d_state_cosine", "mean"),
                    d_domain_cosine=("d_domain_cosine", "mean"),
                    sharedness_ratio=("sharedness_ratio", "mean"),
                    trajectory_cosine_mean=("trajectory_cosine_mean", "mean"),
                    domain_silhouette_cosine=("domain_silhouette_cosine", "mean")))
    fold_df.to_csv(OUT / "e000c_fold_summary.csv", index=False)

    summary_rows = []
    for rep, g in fold_df.groupby("representation"):
        summary_rows.append({
            "representation": rep,
            "wear_mae_mean": g["wear_mae"].mean(),
            "wear_nmae_range_mean": g["wear_nmae_range"].mean(),
            "wear_r2_mean": g["wear_r2"].mean(),
            "wear_r2_min_fold": g["wear_r2"].min(),
            "wear_r2_max_fold": g["wear_r2"].max(),
            "fold_r2_range": g["wear_r2"].max() - g["wear_r2"].min(),
            "sharedness_ratio_mean": g["sharedness_ratio"].mean(),
            "trajectory_cosine_mean": g["trajectory_cosine_mean"].mean(),
            "domain_silhouette_cosine_mean": g["domain_silhouette_cosine"].mean(),
        })
    summary = pd.DataFrame(summary_rows).sort_values("representation")
    summary.to_csv(OUT / "e000c_summary.csv", index=False)

    payload = {
        "dataset_url": DATA_URL,
        "rows": int(len(df)),
        "features": len(features),
        "protocol": "3-fold leave-one-cutter-out; train-only scaler/encoder/probe; DAE 5 seeds",
        "summary": summary.to_dict(orient="records"),
        "folds": fold_df.to_dict(orient="records"),
    }
    (OUT / "e000c_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = [
        "# E000-C Results — Generic self-supervised baseline",
        "",
        f"Rows: {len(df)}; numeric process features: {len(features)}.",
        "",
        "Protocol: 3-fold leave-one-cutter-out. Standardizer, PCA/DAE and wear probe are fit on training cutters only. DAE uses 5 seeds and reconstructs corrupted standardized features without wear/cutter labels.",
        "",
        "## Aggregate comparison",
        "",
        summary.to_markdown(index=False),
        "",
        "## Fold comparison",
        "",
        fold_df.to_markdown(index=False),
        "",
        "## Interpretation guardrails",
        "",
        "- This is H001 evidence only; feature-level DAE does not test Process Token/H002.",
        "- PHM2010 wear-label limitations make wear probes directional evidence, not final truth.",
        "- Mean performance is insufficient: worst-fold performance and fold spread are primary robustness checks.",
        "- Lower cutter-domain separation is useful only if wear/state information remains readable.",
        "- If generic SSL fails to improve worst-domain transfer, this is evidence against assuming 'deep = shared'.",
    ]
    (OUT / "README.md").write_text("\n".join(md), encoding="utf-8")

    print(summary.to_string(index=False))
    print("\nFold summary:\n", fold_df.to_string(index=False))


if __name__ == "__main__":
    main()
