# E007 — D3 unlabeled calibration sample-efficiency stress test

## Problem

Before collecting a true third domain, estimate how much unlabeled target-domain data is needed to initialize a lightweight device/context adapter without retraining the shared encoder.

## Setup

The existing two-domain ultrasonic dataset was used as a proxy new-domain test in both directions.

For each direction:

- source-domain early data: source context calibration;
- source-domain middle period: representation/probe training;
- target-domain early data: unlabeled context calibration only;
- target-domain final 20%: future-time test;
- frozen process representation;
- no target-domain label is used for calibration.

Calibration sizes tested: 20, 50, 100, 200, 500 target-domain samples.

## Results

| Target unlabeled calibration N | Wave-state Spearman | Wave-state window std | Worst wave-state window | External-state Spearman | External-state window std |
|---:|---:|---:|---:|---:|---:|
| 20 | 0.933 | 0.082 | 0.727 | 0.523 | 0.059 |
| 50 | 0.970 | 0.007 | 0.951 | 0.544 | 0.046 |
| 100 | 0.974 | 0.005 | 0.957 | 0.530 | 0.037 |
| 200 | 0.977 | 0.005 | 0.954 | 0.541 | 0.025 |
| 500 | 0.977 | 0.002 | 0.965 | 0.547 | 0.012 |

## Interpretation

1. About 50 unlabeled samples are already enough for a stable first-pass waveform/context calibration.
2. About 200–500 samples materially reduce calibration-window sensitivity and are better for a formal D3 preflight.
3. Increasing calibration data beyond this does not solve the main scientific bottleneck: external physical-state transfer remains only moderate and direction-dependent.

Therefore, the D3 experiment should be staged rather than collecting thousands of samples immediately.

## Decision

Use a two-stage D3 protocol:

1. **Preflight:** ~500 unlabeled samples for structure audit and context calibration.
2. **Formal external validation:** only if preflight passes, expand to ~2000–3000 samples for process-state transfer, future-time stability, and matched-state consistency.

The shared encoder must stay frozen; D3 may receive only lightweight unlabeled context calibration.

## Status

E007 supports the feasibility of low-cost third-domain onboarding, but does not itself support H004 because no true third domain has yet been observed.
