# Industrial Process Representation Research

This repository is used as a versioned research ledger for experiments on industrial shared representations and Process Tokens.

## Core question

Can unlabeled industrial process data learn a shared representation that is transferable across domains, reusable across tasks, and robust to equipment/tool differences?

## Current research line

Process Token -> self-supervised learning -> shared representation (`Z_shared`)

## Research protocol

We use a fixed research ledger structure:

- P: Problem / Proposition
- H: Hypothesis
- O: Observable
- B: Baseline
- E: Experiment / Evidence
- D: Decision
- N: Next

## Current hypotheses

- H001: Self-supervised learning can learn cross-domain shared process representations.
- H002: Process-aware tokenization can outperform fixed sampling patches for shared representation learning.
- H002c: Alignment to a physical process coordinate can improve cross-domain representation quality.
- H002d: The best process coordinate may depend on sensing modality.
- H002e: Ordered physical process composition can add value beyond segmentation alone.

## Current execution plan

1. Public-data proof of concept.
2. Establish simple statistical/shared-representation baselines.
3. Compare Fixed Patch vs Process Token under the same backbone, loss, split, and parameter budget.
4. Validate using held-out-domain probes, domain leakage, fold consistency, and trajectory consistency.
5. Only after public-data validation, move to real industrial data.

## Current evidence status

### Completed

- Synthetic process-coordinate audit sanity checks passed. This validates code behavior only, not the scientific hypothesis.
- PHM2010 public/derived data confirm a meaningful cross-cutter domain-shift problem.
- E000-B feature-level lower baseline completed on 945 cuts using strict leave-one-cutter-out evaluation.

### E000-B conclusion

Raw/statistical features, train-only standardization and PCA do **not** provide uniformly transferable representations across C1/C4/C6. PCA improves some folds and representation-geometry diagnostics but fails strongly on the held-out C6 fold. Therefore H001 remains OPEN; simple statistical transforms do not solve the shared-representation problem.

Detailed evidence is stored under `results/e000b/` and the decision record under `decisions/D000c_e000b.md`.

### Next

- preserve E000-B as the lower baseline;
- require later methods to improve fold consistency, not just mean metrics;
- continue H002c / Process Token validation when suitable high-frequency or cycle-aligned public data are available;
- keep Process Token evaluation separate from feature-level H001 evidence.

> Note: This repository is public. Proprietary industrial data, internal system details, credentials, and company-sensitive information should not be committed here.
