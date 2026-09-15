# E000-C — Generic self-supervised baseline

## Purpose

Test whether a generic non-physical self-supervised encoder can improve cross-cutter shared representation before introducing Process Token structure.

## Input

PHM2010-derived 48-dimensional engineered/statistical feature table. This experiment does **not** use raw 50 kHz waveforms and therefore does **not** test H002.

## Representation

Denoising autoencoder (DAE):

- train-only StandardScaler;
- MLP encoder/decoder hidden sizes `(32, 12, 32)`;
- 12-D bottleneck;
- 15% feature masking plus small Gaussian corruption;
- reconstruction target is the clean standardized feature vector;
- no wear labels, failure labels, cut index, or cutter identity are used to train the encoder.

## Evaluation

Three outer leave-one-cutter-out folds:

- C4 + C6 -> C1;
- C1 + C6 -> C4;
- C1 + C4 -> C6.

The held-out cutter is never used to fit scaler, PCA, DAE, or wear probe.

DAE is repeated over 5 random seeds. PCA95 is rerun as the deterministic lower baseline.

Metrics:

- held-out wear MAE / normalized MAE / R2 using a frozen Ridge probe;
- worst-fold R2;
- fold R2 spread;
- state-vs-domain sharedness geometry;
- trajectory direction consistency;
- cutter-domain silhouette.

## Decision logic

Evidence for H001 strengthens only if generic SSL improves held-out-domain state readability **and** reduces worst-domain collapse without merely encoding cutter identity.

A higher mean score with one catastrophic held-out domain is not considered a robust shared representation.

## Status

**COMPLETED.**

Main aggregate result:

- DAE12 mean R2: 0.231 vs PCA95: 0.194;
- DAE12 worst-fold R2: -0.604 vs PCA95: -0.835;
- DAE12 fold R2 range: 1.375 vs PCA95: 1.614.

However, held-out C6 remains negative on average and DAE C6 R2 varies strongly across seeds (-1.553 to +0.222). Therefore the decision is **PARTIALLY SUPPORTED**, not a full validation of H001.

See `results/e000c/` and `decisions/D000d_e000c.md`.
