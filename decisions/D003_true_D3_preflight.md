# D003 — True D3 preflight decision

## Decision

Proceed to formal third-domain validation.

## Evidence

- The physical stage decomposition transfers to a genuinely unseen third domain without D3-specific segmentation tuning.
- Zero-shot Process representation is consistently stronger than the matched Fixed representation across the tested hyperparameter grid.
- Blind target affine alignment can reduce independent process-state transfer, indicating that some domain shift is real process/context information rather than nuisance.
- Compact physics features remain a strong baseline and currently outperform the learned latent on several easy process-feedback tasks.

## Consequence

The research question is no longer simply whether Process Token survives a new device. It does at preflight level.

The next question is stricter:

> Does the learned shared representation provide reusable information beyond a compact set of physically engineered stage features on a larger unseen domain and on less waveform-direct targets?

## Rules for the next experiment

- Freeze the source Shared Encoder.
- Do not tune P1/Gap/P2 boundaries on D3.
- Use D3 labels only for final evaluation/probes, not target calibration.
- Keep Fixed, zero-shot Process, and physics-feature baselines side by side.
- Treat recipe/material context as physical context, not noise to be erased.
- No cross-material claim until the same-material third-domain study is complete.

## Status

GO to formal D3 validation; `Z_shared` remains unproven.
