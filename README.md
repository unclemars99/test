# Industrial Process Representation Research

This repository is a versioned research ledger for experiments on industrial shared representations and Process Tokens.

## Core question

Can unlabeled industrial process data learn a shared representation that is transferable across domains, reusable across tasks, and robust to equipment, recipe, and material context?

## Current research line

`Process Token -> Context-conditioned canonicalization -> Shared process state -> Dynamics / multi-task`

The target is not a specific anomaly detector. The target is a reusable latent process state `Z_shared`.

## Research protocol

Each major research step follows:

- P: Problem / Proposition
- H: Hypothesis
- O: Observable
- B: Baseline
- E: Experiment / Evidence
- D: Decision
- N: Next

## Current hypotheses

- H001: self-supervised learning can learn cross-domain shared process representations.
- H002: physical/process-aware tokenization can improve representation quality when the process has meaningful internal structure.
- H003: observed industrial signals are better modeled as `X = G(Z_process, C_device, C_recipe, C_material)` than by treating all domain information as removable noise.

## Evidence status

### Public-data stage — PHM2010

- Generic invariance-oriented SSL improved cross-domain transfer relative to simple statistical/PCA and reconstruction baselines.
- Physical process coordinates were observable.
- Hard phase alignment, raw+phase side information, and ordered physical composition did **not** consistently beat Fixed Patch.

Decision: Process Token should not be treated as universally useful for all time-series domains.

### Real staged-process stage — ultrasonic welding

E001–E005 test a clearly staged process with frozen structure:

`P1 -> Gap -> P2`

Current findings:

- Process-stage structure outperforms ordinary time-coordinate baselines on the current strict two-domain experiment.
- Shuffling stage order degrades the representation, supporting the value of physical organization.
- Simple equipment affine correction removes large first-order domain effects without harming process transfer.
- Aggressive domain erasing damages real process information.
- Relative physical state is more promising than absolute physical magnitude as a shared coordinate.
- Small context-conditioned factorization improves matched-state cross-domain alignment, but nonlinear equipment leakage remains substantial.
- Independent external-process probes remain weaker than waveform-internal probes.

## Current decision

- Process Token: **SUPPORTED on the current ultrasonic domain pair**
- Device affine context correction: **SUPPORTED**
- Aggressive domain erasing: **NOT SUPPORTED**
- Context-conditioned factorization: **PARTIALLY SUPPORTED**
- Genuine universal/shared `Z_shared`: **OPEN**

The next decisive experiment is external validation on a third unseen domain of the same material class:

`D1 + D2 -> unseen D3`

Only after that succeeds should the work proceed to cross-material transfer.

## Research guardrails

- Do not treat attractive UMAP/t-SNE plots as evidence.
- Do not use random train/test split as the main industrial-sequence result.
- Keep calibration/reference windows separated from future-time evaluation.
- Mean metrics must not hide a catastrophic held-out domain.
- Domain accuracy is a diagnostic, not an objective that must be minimized at all costs.
- Waveform-internal probes alone are insufficient evidence for a physical shared state.
- Do not change a failed hypothesis after inspecting results without recording the change.

> This repository is public. Proprietary raw data, internal equipment identifiers, credentials, database details, and company-sensitive operational information must not be committed.