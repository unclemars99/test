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

## Decision rule

The method is a stronger generic baseline only if it reduces held-out-domain collapse and stochastic instability relative to both PCA95 and E000-C DAE, rather than merely improving the mean score.

## Status

RUNNING via GitHub Actions. Results will be committed to `results/e000d/`.
