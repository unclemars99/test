# D002 — Third-domain preflight strategy

## Decision

Do not collect a large third-domain dataset by default.

Use a staged external-validation workflow:

1. identify a candidate third domain within the same material family;
2. collect about 500 unlabeled samples first;
3. audit physical-stage compatibility and estimate a lightweight context adapter;
4. keep the shared encoder frozen;
5. only if the preflight is structurally compatible, expand to about 2000–3000 samples for formal external validation.

## Evidence

E007 showed that 50 target-domain samples are enough for a stable first-pass waveform calibration, while 200–500 samples substantially reduce calibration-window sensitivity. More target calibration data does not materially resolve the remaining weakness in independent external-state transfer.

## Rationale

The next scientific question is whether the representation generalizes to a genuinely unseen domain, not whether a target-specific model can be retrained successfully. A small preflight prevents wasting data collection effort on an incompatible domain and reduces the risk of silently adapting the shared representation to the test domain.

## Constraints

- same material family first;
- no D3 labels for context calibration;
- no full D3 retraining before the external-validation decision;
- material changes remain a later validation stage;
- raw proprietary data and internal identifiers remain outside the public research ledger.
