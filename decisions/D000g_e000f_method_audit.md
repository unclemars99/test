# D000g — E000-F v1 implementation audit found a phase-origin confound before results were inspected

## Discovery timing

This issue was identified while the first E000-F GitHub Actions run was still in progress and before any E000-F metrics were inspected.

## Problem

The v1 implementation recovered Hilbert phase and then defined cycle boundaries using:

`floor((phase - phase[0]) / 2π)`.

Subtracting `phase[0]` makes the phase origin depend on the arbitrary phase at the beginning of each cut's central window. This recovers stable **cycle lengths** but does not establish a common absolute phase origin across cuts.

Therefore the v1 condition named `process_token` is more accurately:

`cycle-segmented token with cut-relative phase origin`.

It cannot be used as a clean test of H002c_2 (cross-cut physical phase alignment), regardless of whether its downstream score is good or bad.

## Consequence

**E000-F v1 results are diagnostic only and are pre-declared INVALID as decisive H002c_2 evidence.**

We will not reinterpret the implementation after seeing its metrics.

## Correction

The corrected experiment must define boundaries from a consistent analytic-signal phase crossing, e.g. multiples of `2π` in the unwrapped Hilbert phase without subtracting the cut-specific initial phase. This makes the boundary correspond to the same Fx analytic-phase reference across cuts.

The corrected comparison will keep all other variables fixed:

- same raw cuts;
- same 128 tokens per cut;
- same 288 samples/token;
- same Fx/Fy/Fz channels;
- same CNN encoder;
- same VICReg objective;
- same seeds;
- same LOCO probe;
- same pre-registered decision rule.

This correction is methodological, not performance-driven.
