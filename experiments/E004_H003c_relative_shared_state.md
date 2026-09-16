# E004 / H003c — Relative Physical State

## P

Is shared process state better represented by absolute physical values or by state relative to each equipment/recipe reference distribution?

## Rationale

Absolute peak power, energy and related values legitimately depend on equipment, recipe and material. A shared state may therefore be closer to a normalized deviation coordinate than to absolute magnitudes.

## Experiment

A context-conditioned factorization model was trained with either:

- absolute physical anchors, or
- relative physical anchors normalized against local reference distributions.

Three random seeds were used for the relative-state version.

## Evidence

Absolute-anchor version:

- cross-domain process Spearman: ~0.867
- linear equipment accuracy: ~98.6%

Relative-anchor version, three seeds:

- cross-domain process Spearman: 0.881 / 0.887 / 0.891
- future-time Spearman: ~0.906–0.908
- linear equipment accuracy: ~63–74%, mean ~68%
- nonlinear equipment leakage remained substantial.

## Decision

**H003c: PARTIALLY SUPPORTED.**

Relative physical state is more promising than absolute physical magnitude as a shared coordinate, but it does not eliminate higher-order domain information.

The result also implies that future cross-material work should compare relative process structure rather than forcing absolute parameters to align.

## N

Build a shared process coordinate that combines Process Token structure, low-capacity context correction, and relative physical state without over-normalizing real process differences.