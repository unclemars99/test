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
4. Validate using held-out-domain probes, domain leakage, and trajectory consistency.
5. Only after public-data validation, move to real industrial data.

## Status

The code-level process-coordinate audit has passed synthetic sanity checks. Real-data hypotheses are still open and will only be marked supported after reproducible experiments on public datasets.

> Note: This repository is public. Proprietary industrial data, internal system details, credentials, and company-sensitive information should not be committed here.
