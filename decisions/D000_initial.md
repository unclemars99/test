# D000 — Initial research decisions

## D000-code

Synthetic sanity checks for the process-coordinate audit implementation passed. This validates code behavior only; it does not validate the scientific hypothesis on real data.

## D000b

PHM2010-derived public data show meaningful cross-cutter domain shift. Therefore the shared-representation problem is real enough to justify H001 experiments.

Status: PASS for problem existence, not for solution effectiveness.

## Guardrails

- Do not infer scientific support from synthetic tests alone.
- Do not use random train/test splits as the main evidence for industrial sequence data.
- Do not let held-out domain statistics leak into scaling, PCA or pretraining.
- Do not treat attractive t-SNE/UMAP plots as proof of a shared representation.
- Do not claim Process Token value before a fair fixed-patch comparison on suitable data.
