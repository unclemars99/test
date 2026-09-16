# D008 — Lightweight matched sampling for ADR proxy validation

## Problem
Low-anomaly-score reference records are extremely abundant. Scanning or exporting the full low-score population adds cost without improving the first validation gate.

## Decision
Use sparse matched references rather than exhaustive low-score retrieval.

- Cap the high-confidence anomaly-proxy set for the first gate.
- Draw only one nearby low-score reference per anomaly.
- Match device / process position / polarity / recipe context where available.
- Restrict matching to a short local time window.
- Do not count or export the entire low-score population.
- Exclude the intermediate score region from the first binary diagnostic.

## Rationale
The first question is whether the frozen representation separates high-confidence waveform anomalies from closely matched low-score production records. A large easy negative pool would mainly increase class imbalance and database workload, while weakening contextual matching.

## Scientific boundary
The anomaly score is derived from waveform information, so this experiment tests waveform-anomaly sensitivity only. Independent quality truth still requires teardown / pull-test / confirmed-quality evidence.
