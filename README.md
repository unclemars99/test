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
- H002c_1: a physical process coordinate can be reliably recovered from real process signals.
- H002c_2: tokenizing on that coordinate improves shared-representation learning.
- H002d: the best process coordinate may depend on sensing modality.
- H002e: ordered physical process composition can add value beyond segmentation alone.

## Current execution plan

1. Public-data proof of concept.
2. Establish simple statistical/shared-representation baselines.
3. Compare Fixed Patch vs Process Token under the same backbone, loss, split, and parameter budget.
4. Validate using held-out-domain probes, domain leakage, fold consistency, and trajectory consistency.
5. Only after public-data validation, move to real industrial data.

## Current evidence status

### H001 — shared representation

- E000-B: raw/statistical features, train-only standardization and PCA do not transfer uniformly; held-out C6 collapses under PCA.
- E000-C: denoising autoencoder modestly improves the hardest domain but remains unstable.
- E000-D: VICReg-like invariance SSL raises mean LOCO R2 to about 0.585 and recovers the previously catastrophic C6 fold to a positive mean R2 about 0.416. All five C6 seeds are positive, but the pre-registered worst-fold seed-stability gate is missed narrowly (0.206 vs 0.20).

**H001 status: PARTIALLY SUPPORTED, with materially stronger evidence after E000-D.**

### H002 — physical Process Token

E000-E directly audited ordered raw 50 kHz PHM2010 force signals across 21 representative cuts (C1/C4/C6). Both the spindle coordinate (~173.33 Hz) and tooth-passing coordinate (~520 Hz) pass the pre-registered observability gate. The spindle coordinate is reliable on all 21 cuts; the tooth-passing coordinate is within 5% frequency error on 20/21 cuts and is much more spectrally prominent in most cuts.

This supports a hierarchical physical coordinate:

`spindle revolution -> three tooth-passing subcycles`.

**H002c_1 status: SUPPORTED on this representative PHM2010 force-signal audit.**

**H002c_2 / H002 overall: OPEN.** Coordinate recoverability does not prove that Process Token improves representation quality.

### Current experiment

E000-F is the fair raw-signal comparison of Fixed Patch vs Process Token with the same CNN encoder, VICReg objective, token count, seeds and LOCO split. During the first run, before inspecting metrics, a method audit found that subtracting each cut's initial Hilbert phase created a cut-relative phase origin. That v1 run was therefore pre-declared non-decisive for H002c_2. A corrected common-phase v2 was registered before looking at v1 results and is the decisive run.

## Research guardrails

- Synthetic sanity checks validate code behavior, not scientific hypotheses.
- No random train/test split as the main industrial-sequence evidence.
- No held-out-domain leakage into scaling, PCA, SSL or probes.
- Mean metrics cannot hide a catastrophic held-out fold.
- Sharedness ratios are secondary diagnostics when their denominator can approach zero.
- Do not move pre-registered thresholds after inspecting results.
- Do not claim H002 from coordinate recovery alone; Process Token must beat a fair Fixed Patch baseline.

> Note: This repository is public. Proprietary industrial data, internal system details, credentials, and company-sensitive information should not be committed here.
