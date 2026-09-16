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
- zero-shot vs few-shot adapter gap;
- comparison against compact physics-feature baselines.

## Baselines

- Raw / Fixed representation;
- Process Token without device/context calibration;
- Process Token + lightweight context calibration;
- compact stage-level physics features;
- current context-conditioned factorization when applicable.

## Preflight protocol from E007

Two-domain proxy tests showed that target-domain onboarding can be staged:

- ~50 unlabeled target samples: enough for a first-pass stable waveform/context calibration;
- ~200–500 unlabeled target samples: substantially lower calibration-window sensitivity;
- formal D3 validation should only expand after the ~500-sample preflight passes.

D3 calibration may estimate a lightweight context adapter only. The shared encoder remains frozen.

## True D3 evidence from E008

A genuine third domain from the same material/process family has now been observed.

Preflight findings:

- the frozen `P1 -> Gap -> P2` decomposition succeeded throughout the D3 preflight sample;
- zero-shot Process representation transferred better than the matched Fixed representation across the tested stress grid;
- full target affine alignment was not consistently beneficial and often reduced independent process-state transfer;
- compact physics features remained a very strong baseline and outperformed the current learned latent on several easy process-feedback targets.

Interpretation:

The stage structure and process-aware representation survive a true third-domain shift, which is meaningful positive evidence for H004. However, the result does not yet establish a universal shared latent because strong physical features remain competitive or superior and quality-level transfer has not yet been tested.

## Falsification / stop rule

H004 is not supported if the formal larger-D3 study requires substantial D3-specific retraining, if Process Token loses its advantage over Fixed under stable evaluation, or if the learned representation adds no value beyond strong physics baselines on less waveform-direct tasks.

## Status

**PRELIMINARY SUPPORT / OPEN.**

True D3 preflight supports transfer of the physical stage representation and zero-shot Process Token beyond the original two-domain pair. Formal larger-D3 validation and stronger target tasks are still required before claiming `Z_shared`.
