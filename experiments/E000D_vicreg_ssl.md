# E000-D — Invariance-oriented generic SSL

## Purpose

Test whether an invariance-oriented self-supervised objective is more stable across cutters than reconstruction-oriented DAE, before introducing Process Token structure.

## Input

Same PHM2010-derived 48-D engineered/statistical feature table used in E000-B/C. This is still an H001 feature-level experiment and does **not** test H002.

## Method

VICReg-lite encoder:

- train-only StandardScaler;
- encoder 48 -> 64 -> 32 -> 12;
- two independently corrupted views per sample;
- 15% feature masking + Gaussian noise;
- invariance loss between paired views;
- variance regularization to prevent collapse;
- covariance regularization to reduce redundant latent dimensions;
- no wear, failure, cut index, or cutter identity used in SSL training.

## Evaluation

- 3-fold leave-one-cutter-out;
- held-out cutter never used for scaler/SSL/probe fitting;
- 5 seeds per fold;
- frozen Ridge wear probe;
- worst-fold R2 and fold spread are primary robustness criteria;
- sharedness, trajectory consistency, and cutter silhouette are secondary diagnostics.

## Pre-registered decision rule

To avoid post-hoc interpretation, the following gate is fixed before seeing E000-D results:

- **PASS as a strong generic SSL baseline**: all three held-out-cutter mean R2 values are > 0 and the worst-fold seed-to-seed R2 standard deviation is <= 0.20.
- **PARTIAL**: aggregate or worst-fold transfer improves over PCA/DAE, but at least one held-out fold remains R2 <= 0 or worst-fold seed std > 0.20.
- **FAIL**: no meaningful worst-fold improvement over the E000-C DAE/PCA baselines, or stronger collapse/instability is introduced.

Mean performance alone is not sufficient for PASS.

## Status

RUNNING via GitHub Actions. Results will be committed to `results/e000d/`.
