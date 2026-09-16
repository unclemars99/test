# E005 / H003d — Shared Process Coordinate Validation

## P

Can context-conditioned factorization improve cross-equipment process alignment while preserving future-time stability and real physical information?

## Protocol

Each domain was split by time:

- first 20%: unlabeled reference/calibration only;
- middle 60%: representation learning and probes;
- final 20%: future-time evaluation.

Evaluation distinguishes:

- waveform-internal process state;
- external process feedback;
- equipment leakage;
- matched-state latent distance across domains.

## Evidence

Representative results:

| Method | Cross waveform state | Cross external state | Future waveform | Future external | Logistic domain | RF domain | HGB domain | Matched-state distance ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Raw Process | 0.907 | 0.457 | 0.935 | 0.459 | 99.6% | 99.3% | 99.9% | 0.984 |
| Affine Adapter | 0.930 | 0.470 | 0.935 | 0.459 | 56.4% | 91.2% | 98.6% | 0.922 |
| Factorization, adv=0 | 0.937 | 0.450 | 0.926 | 0.428 | 70.5% | 92.8% | 97.1% | 0.875 |
| Factorization, adv=0.03 | 0.937 | 0.452 | 0.927 | 0.432 | 65.2% | 88.6% | 96.0% | 0.877 |
| Factorization, adv=0.10 | 0.925 | 0.446 | 0.924 | 0.421 | 60.2% | 88.4% | 94.7% | 0.881 |
| Fully Relative Coordinate | 0.855 | 0.359 | 0.932 | 0.395 | 86.8% | 90.7% | 95.3% | 0.931 |

Lower matched-state distance ratio is better.

## Decision

**H003d: PARTIALLY SUPPORTED.**

A low-capacity context adapter/factorization improves alignment of similar process states across equipment. However, independent external-process probes do not improve in the same way, and nonlinear equipment leakage remains high.

Therefore a genuine equipment-independent `Z_shared` is **not yet demonstrated**.

## Current frozen structure

`Process Token -> Affine Context Adapter -> Shared Encoder -> Z_process`

with a small context embedding used only to explain observation-specific transformations.

## N

The next decisive experiment is external validation on a third unseen domain of the same material class:

`D1 + D2 -> unseen D3`

Only after this succeeds should the study proceed to cross-material transfer.