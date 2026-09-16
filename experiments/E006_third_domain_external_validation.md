# E006 — Third-domain external validation protocol

## Purpose

Test whether the current ultrasonic-welding Process Token / context-calibrated representation generalizes beyond the two domains used during method development.

## Data requirement

A third domain from the same material family is preferred.

Minimum package:

- 2,000–5,000 normal production waveforms;
- time ordering preserved;
- raw process waveform;
- available process feedback variables such as energy, duration, pressure, power and displacement/height;
- domain identity retained locally but anonymized in shared artifacts.

Confirmed destructive-test or field-confirmed abnormal samples are useful but not required for this experiment.

## Split

- Learn shared representation on D1 + D2 only.
- Freeze the shared encoder.
- Hold D3 completely out during shared-representation training.
- On D3 evaluate:
  - zero-shot representation;
  - calibration-only affine adapter using an unlabeled early window;
  - small few-shot context adapter, if necessary.

No full D3 retraining is allowed for the primary claim.

## Evaluation

### A. Process-state transfer

Use wave-internal and external process-state probes separately. External feedback variables remain the stronger evidence.

### B. Future-time stability

Use early D3 data for optional unsupervised calibration and reserve later D3 data for testing.

### C. Matched-state consistency

Find D3 samples with similar external process states to D1/D2 and test whether latent distances are lower than random cross-domain distances.

### D. Context burden

Measure how much D3-specific adaptation is required:

`zero-shot -> affine calibration -> small adapter -> full retraining`

A reusable shared representation should succeed before the last step.

## Pre-registered interpretation

Strong support:

- frozen shared encoder remains useful on D3;
- simple unsupervised context calibration is sufficient;
- future-time performance remains stable;
- matched-state latent consistency improves over raw/fixed baselines.

Partial support:

- useful D3 transfer is obtained only with a small context adapter.

Not supported:

- D3 requires substantial encoder retraining or collapses relative to simple baselines.

## Data privacy

Do not commit proprietary raw waveforms, device identifiers, credentials, internal host information, or production codes to this public repository. Commit only generic protocol, anonymized aggregate metrics and decisions.

## Status

WAITING FOR D3 CANDIDATE / DATA.
