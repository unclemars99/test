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

## Preflight evidence

A genuine third domain from the same material/process family was first evaluated in a low-cost preflight.

The frozen `P1 -> Gap -> P2` decomposition survived the domain shift and zero-shot Process representation transferred better than matched Fixed representation. Full target affine alignment was not consistently beneficial, suggesting the shift contains real process/context change rather than only sensor/device offset.

## Formal D3 evidence — E009

The larger formal third-domain study used 2500 held-out D3 samples. Model/representation choices were selected only from source-domain D1↔D2 transfer.

Mean Spearman across five process-feedback probes:

- Fixed waveform representation: 0.313
- Process Token representation: **0.550**
- compact physics features: 0.622
- physics + Fixed latent: 0.605
- physics + Process latent: **0.655**

Process minus Fixed improvement is about +0.238 mean Spearman, with paired-bootstrap 95% interval approximately [0.223, 0.253].

Adding Process latent to compact physics features improves mean transfer by about +0.032, with paired-bootstrap 95% interval approximately [0.023, 0.042]. Adding Fixed latent does not provide the same gain.

Interpretation:

1. The physical stage coordinate survives a true external-domain shift.
2. Process Token advantage is not confined to the original D1/D2 pair.
3. Process-aware waveform structure carries some transferable information beyond a compact physics baseline.
4. This still does not establish a universal `Z_shared`, because quality-level, lifecycle and cross-material tasks remain untested.

One source pressure/context channel contains a mixed or inconsistent regime and is not treated as primary evidence.

## Falsification / stop rule

The same-material external-transfer claim would be weakened if future independent tasks require substantial target-specific retraining, if Process Token loses its advantage over Fixed under comparable evaluation, or if its residual value beyond physics features disappears on quality/lifecycle targets.

## Status

**SUPPORTED within the current same-material third-domain scope.**

This status supports external transfer of the physical process representation. It does **not** yet prove the broader universal shared-state proposition `Z_shared`.

## Next

Stop optimizing easy process-feedback proxies on the same three domains. The next decisive test should target information not almost directly encoded by the power waveform: quality / teardown / pull-test, lifecycle/tool-state change, or another genuinely new task. Cross-material validation follows with material/context explicitly separated.
