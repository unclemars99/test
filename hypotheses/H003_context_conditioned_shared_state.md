# H003 — Context-conditioned Shared Process State

## Problem

Process-aware segmentation is now supported on real ultrasonic-welding data, but the learned representation still contains strong equipment/domain identity.

The question is no longer simply whether Process Token is useful. The question is:

> Can a reusable process state be separated from equipment, recipe, and material context without destroying real physical information?

## Hypothesis

Observed process signals are better modeled as

`X = G(Z_process, C_device, C_recipe, C_material)`

rather than assuming that equipment information is removable noise.

The target is a shared process coordinate `Z_process` that preserves transferable process relations, while context variables explain observation-specific transformations.

## Sub-hypotheses

- H003a: simple equipment mean/scale effects can be removed without harming process information.
- H003b: aggressive domain erasing will hurt real process information when equipment effects and process state are entangled.
- H003c: relative physical state, defined against local equipment/recipe reference, is closer to a shared coordinate than absolute physical values.
- H003d: a small context-conditioned adapter/factorization can improve cross-domain process alignment while preserving future-time stability.

## Evaluation

Primary evidence must include:

- cross-domain process-state transfer;
- future-time stability;
- matched-state latent distance across domains;
- domain leakage as a diagnostic, not as the sole optimization target;
- external process feedback probes in addition to waveform-internal probes.

## Current status

**PARTIALLY SUPPORTED.**

Evidence through E005 supports simple affine context correction and weakly supports context-conditioned factorization. A fully domain-invariant `Z_shared` has not yet been established.

## Next falsification step

External validation on a third unseen domain under the same material class. Only after that should the study proceed to cross-material transfer.