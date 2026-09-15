#!/usr/bin/env python3
"""E000-B: feature-level shared-representation lower baseline.

Public PHM2010-derived feature table only. No proprietary data.

Representations
---------------
R0: raw statistical features
R1: train-only StandardScaler
R2: train-only StandardScaler + PCA(95% variance)

Evaluation
----------
Outer leave-one-cutter-out (LOCO):
  C1+C4 -> C6
  C1+C6 -> C4
  C4+C6 -> C1

No held-out-cutter statistics are used to fit transforms or probes.
The held-out cutter is used only for evaluation.

Outputs include:
- held-out wear probe (linear regression)
- sharedness geometry (cosine-distance state/domain ratio)
- trajectory consistency (early->late direction cosine)
- diagnostic cutter-domain separability (silhouette score)

Important: this is a lower baseline for H001. It does NOT test Process Token (H002).
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, silhouette_score
from sklearn.preprocessing import StandardScaler, normalize

META = {"cutter", "cut_index", "wear", "failure_label"}
CUTTERS = ["C1", "C4", "C6"]


def _safe_cos_dist(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, float).reshape(1, -1)
    b = np.asarray(b, float).reshape(1, -1)
    an = normalize(a)[0]
    bn = normalize(b)[0]
    return float(1.0 - np.clip(np.dot(an, bn), -1.0, 1.0))


def _wear_state_bins(df: pd.DataFrame) -> pd.Series:
    """Evaluation-only low/mid/high state bins, separately within each cutter.

    Uses wear labels ONLY for evaluation geometry. The bins are never model inputs.
    """
    out = pd.Series(index=df.index, dtype="object")
    for cutter, g in df.groupby("cutter"):
        q1, q2 = g["wear"].quantile([1 / 3, 2 / 3]).values
        vals = g["wear"].to_numpy()
        labels = np.where(vals <= q1, "low", np.where(vals <= q2, "mid", "high"))
        out.loc[g.index] = labels
    return out


def sharedness_metrics(z: np.ndarray, meta: pd.DataFrame) -> dict:
    """Geometry-only diagnostic using cosine distances.

    D_state: within-cutter low-vs-high centroid distance.
    D_domain: across-cutter centroid distance at matched low/mid/high states.
    S_shared = D_state / (D_domain + eps).

    Higher is better only if state separation is preserved; therefore D_state is
    always reported alongside the ratio.
    """
    work = meta[["cutter", "wear"]].copy()
    work["state_bin"] = _wear_state_bins(work)

    centroids = {}
    for (cutter, state), idx in work.groupby(["cutter", "state_bin"]).groups.items():
        centroids[(cutter, state)] = np.mean(z[list(idx)], axis=0)

    d_state = []
    for cutter in CUTTERS:
        if (cutter, "low") in centroids and (cutter, "high") in centroids:
            d_state.append(_safe_cos_dist(centroids[(cutter, "low")], centroids[(cutter, "high")]))

    d_domain = []
    for state in ["low", "mid", "high"]:
        for a, b in combinations(CUTTERS, 2):
            if (a, state) in centroids and (b, state) in centroids:
                d_domain.append(_safe_cos_dist(centroids[(a, state)], centroids[(b, state)]))

    ds = float(np.mean(d_state)) if d_state else np.nan
    dd = float(np.mean(d_domain)) if d_domain else np.nan
    ss = float(ds / (dd + 1e-12)) if np.isfinite(ds) and np.isfinite(dd) else np.nan

    return {
        "d_state_cosine": ds,
        "d_domain_cosine": dd,
        "sharedness_ratio": ss,
    }


def trajectory_consistency(z: np.ndarray, meta: pd.DataFrame) -> dict:
    """Compare early/low -> late/high state directions across cutters."""
    work = meta[["cutter", "wear"]].copy()
    work["state_bin"] = _wear_state_bins(work)

    directions = {}
    for cutter in CUTTERS:
        low_idx = work.index[(work.cutter == cutter) & (work.state_bin == "low")].tolist()
        high_idx = work.index[(work.cutter == cutter) & (work.state_bin == "high")].tolist()
        if low_idx and high_idx:
            lo = np.mean(z[low_idx], axis=0)
            hi = np.mean(z[high_idx], axis=0)
            v = hi - lo
            nv = np.linalg.norm(v)
            if nv > 1e-12:
                directions[cutter] = v / nv

    sims = {}
    vals = []
    for a, b in combinations(CUTTERS, 2):
        if a in directions and b in directions:
            val = float(np.clip(np.dot(directions[a], directions[b]), -1.0, 1.0))
            sims[f"{a}_{b}"] = val
            vals.append(val)

    return {
        "trajectory_cosine_mean": float(np.mean(vals)) if vals else np.nan,
        "trajectory_pairwise": sims,
    }


def domain_silhouette(z: np.ndarray, cutters: pd.Series) -> float:
    """Diagnostic domain leakage/separability. Higher => stronger cutter identity."""
    try:
        zn = normalize(z)
        return float(silhouette_score(zn, cutters.astype(str).to_numpy(), metric="cosine"))
    except Exception:
        return np.nan


def fit_transform_representation(name: str, x_train: np.ndarray, x_all: np.ndarray):
    if name == "raw":
        return x_train.copy(), x_all.copy(), {"n_components": x_train.shape[1]}

    scaler = StandardScaler().fit(x_train)
    xtr = scaler.transform(x_train)
    xall = scaler.transform(x_all)

    if name == "standardized":
        return xtr, xall, {"n_components": xtr.shape[1]}

    if name == "pca95":
        pca = PCA(n_components=0.95, svd_solver="full").fit(xtr)
        return pca.transform(xtr), pca.transform(xall), {
            "n_components": int(pca.n_components_),
            "explained_variance": float(np.sum(pca.explained_variance_ratio_)),
        }

    raise ValueError(name)


def evaluate_fold(df: pd.DataFrame, feature_cols: list[str], heldout: str, rep: str) -> dict:
    train_mask = df.cutter != heldout
    test_mask = df.cutter == heldout

    x = df[feature_cols].to_numpy(float)
    y = df.wear.to_numpy(float)
    x_train = x[train_mask]
    y_train = y[train_mask]

    z_train, z_all, rep_info = fit_transform_representation(rep, x_train, x)
    z_test = z_all[test_mask]
    y_test = y[test_mask]

    # Frozen/simple downstream probe. Transform is fit on training cutters only.
    probe = LinearRegression().fit(z_train, y_train)
    pred = probe.predict(z_test)

    wear_range = max(float(np.ptp(y_test)), 1e-12)
    mae = float(mean_absolute_error(y_test, pred))

    fold = {
        "heldout_cutter": heldout,
        "representation": rep,
        "n_train": int(train_mask.sum()),
        "n_test": int(test_mask.sum()),
        "wear_mae": mae,
        "wear_nmae_range": float(mae / wear_range),
        "wear_r2": float(r2_score(y_test, pred)),
        **rep_info,
    }

    # Geometry diagnostics are computed after applying this fold's train-only transform.
    geom = sharedness_metrics(z_all, df[["cutter", "wear"]])
    traj = trajectory_consistency(z_all, df[["cutter", "wear"]])
    fold.update(geom)
    fold.update({k: v for k, v in traj.items() if k != "trajectory_pairwise"})
    fold["domain_silhouette_cosine"] = domain_silhouette(z_all, df.cutter)
    fold["trajectory_pairwise"] = traj["trajectory_pairwise"]
    return fold


def aggregate(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    metrics = [
        "wear_mae",
        "wear_nmae_range",
        "wear_r2",
        "d_state_cosine",
        "d_domain_cosine",
        "sharedness_ratio",
        "trajectory_cosine_mean",
        "domain_silhouette_cosine",
        "n_components",
    ]
    out = []
    for rep, g in df.groupby("representation"):
        row = {"representation": rep}
        for m in metrics:
            vals = pd.to_numeric(g[m], errors="coerce")
            row[f"{m}_mean"] = float(vals.mean())
            row[f"{m}_std"] = float(vals.std(ddof=0))
        out.append(row)
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="PHM2010 derived feature CSV")
    ap.add_argument("--output", default="results/e000b")
    args = ap.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
    missing = {"cutter", "cut_index", "wear"} - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df[df.cutter.isin(CUTTERS)].copy().reset_index(drop=True)
    feature_cols = [c for c in df.columns if c not in META and pd.api.types.is_numeric_dtype(df[c])]
    if not feature_cols:
        raise ValueError("No numeric feature columns found")

    rows = []
    for heldout in CUTTERS:
        for rep in ["raw", "standardized", "pca95"]:
            rows.append(evaluate_fold(df, feature_cols, heldout, rep))

    detail = pd.DataFrame([{k: v for k, v in r.items() if k != "trajectory_pairwise"} for r in rows])
    summary = aggregate(rows)

    detail.to_csv(out / "e000b_loco_detail.csv", index=False)
    summary.to_csv(out / "e000b_summary.csv", index=False)

    payload = {
        "experiment": "E000-B",
        "dataset_rows": int(len(df)),
        "cutters": df.cutter.value_counts().sort_index().to_dict(),
        "n_features": int(len(feature_cols)),
        "features": feature_cols,
        "folds": rows,
    }
    (out / "e000b_results.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Concise markdown evidence report.
    lines = [
        "# E000-B Results — Feature-level shared-representation baseline",
        "",
        f"Rows: {len(df)}; numeric process features: {len(feature_cols)}.",
        "",
        "Outer split: leave-one-cutter-out. All transforms and wear probes are fit on training cutters only.",
        "",
        "## Aggregate results",
        "",
        summary.to_markdown(index=False),
        "",
        "## Interpretation guardrails",
        "",
        "- This experiment tests H001 lower baselines, not H002 Process Token.",
        "- Wear labels are used only for the simple probe and evaluation geometry.",
        "- Lower cutter-domain silhouette is desirable only if state/task information is preserved.",
        "- A larger sharedness ratio is useful only together with non-collapsed D_state.",
        "- PHM2010 wear-label limitations mean these metrics are directional evidence, not final proof.",
    ]
    (out / "README.md").write_text("\n".join(lines), encoding="utf-8")

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
