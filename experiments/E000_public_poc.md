# E000 — Public-data proof of concept

## Purpose

Test the research framework on public data before using proprietary industrial data.

## Current dataset focus

PHM2010 CNC tool-wear family.

## E000-A — Process-coordinate audit

Goal: determine whether a stable physical process coordinate can be recovered from high-frequency process signals before training any representation model.

Decision rule:
- PASS: process coordinate is stable and reproducible across representative cuts/tools;
- WARN: partial observability or modality dependence;
- FAIL: current process-coordinate definition is not reliable enough for Process Token experiments.

## E000-B — Shared-representation lower baseline

Representations:
1. raw engineered/statistical features;
2. train-only standardization;
3. train-only standardization + PCA.

Protocol:
- outer leave-one-cutter-out evaluation;
- no held-out cutter statistics used for scaling/PCA;
- frozen/simple probes only;
- evaluate state/task information, domain leakage and sharedness.

Primary purpose: establish a simple baseline that any later deep Process Token model must beat.

## Status

Domain shift is confirmed in public PHM2010-derived data. Full E000-B metrics are pending execution on the complete accessible feature table. Process Token comparison remains pending suitable raw/process-aligned data.
