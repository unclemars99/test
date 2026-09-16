# H004 — Third-domain external validation

## Problem

The current ultrasonic-welding line has produced positive evidence that a process-aware representation based on ordered physical stages can improve transfer between two domains. However, evidence from only two domains cannot distinguish a genuinely reusable process representation from a representation that is merely well adapted to that pair.

## Hypothesis

A process representation that captures reusable shared process state should transfer to a third, previously unseen domain of the same material family without retraining the shared encoder.

Formally:

`D1 + D2 -> shared encoder -> frozen -> D3 probe / lightweight unlabeled context calibration`

The key question is not whether D3 can be fit after full retraining. The key question is whether the shared process coordinates learned from D1/D2 remain useful on D3.

## Scope

First external validation stays within one material family. Material changes are deferred to a later stage because different materials legitimately require different process parameters and should not be treated as nuisance domain shifts.

Preferred validation hierarchy:

1. same material + same process family + new device;
2. same material + nearby recipe + new device/domain;
3. only after this succeeds, cross-material validation.

## Observables

Primary:

- cross-domain process-state transfer on D3;
- future-time stability on D3;
- matched-state latent consistency between D3 and D1/D2;
- performance with frozen shared encoder and no full retraining.

Secondary:

- domain leakage;
- amount of context calibration needed for D3;
- zero-shot vs few-shot adapter gap.

## Baselines

- Raw / Fixed representation;
- Process Token without device/context calibration;
- Process Token + affine context calibration;
- current context-conditioned factorization.

## Preflight protocol from E007

Two-domain proxy tests show that target-domain onboarding can be staged:

- ~50 unlabeled target samples: enough for a first-pass stable waveform/context calibration;
- ~200–500 unlabeled target samples: substantially lower calibration-window sensitivity;
- formal D3 validation should only expand to ~2000–3000 samples after the ~500-sample preflight passes.

D3 calibration is allowed to estimate a lightweight context adapter only. The shared encoder remains frozen.

## Falsification / stop rule

H004 is not supported if the representation only works after substantial D3-specific retraining, or if D3 process-state transfer collapses while simpler baselines remain competitive.

A preflight may also reject a candidate D3 before formal testing if its physical-stage structure is not comparable to the current process family.

## Status

OPEN. E007 supports the feasibility of low-cost D3 onboarding, but no true third-domain evidence has yet been observed.
