# E014 — Independent Quality Dual Gate

## Purpose
Test whether a process-aware representation adds information beyond a strong physics baseline on two independent outcome families.

## Cohort A — Independent visual quality anchors
Use externally observed visual weld-quality outcomes rather than waveform-derived labels. Keep issue subtypes separate (area-related, position-related, combined) instead of collapsing everything into a single NG class. Records with missing visual inspection must remain unknown and must not be treated as normal controls.

One product may map to multiple welding process instances, so evaluation is performed at the event/product level using multiple-instance aggregation. Context-matched nearby process records are used only as unlabeled local references.

### Result
The strong physics baseline already provides high local anomaly evidence for many independently observed visual-quality events. Process-aware waveform structure also detects multiple events, but it does not show a consistent overall advantage over the physics baseline.

A small position-related subset shows a possible Process-specific signal: in some events, process-aware waveform structure is more locally anomalous than the physics baseline. This is a follow-up hypothesis only; the subset is too small for a scientific claim.

## Cohort B — Height-event downstream outcomes
Use height-state events with observed downstream outcome flags. Signed height-state variables are part of the strong physics baseline; do not replace them with absolute magnitude only. The downstream outcome is a label only and must not enter the representation input.

### Result
Signed physical-state variables are substantially more informative than waveform representations for the downstream outcome. Under grouped validation, a parsimonious signed physical-state baseline outperforms both Fixed and Process waveform representations.

Adding Process representation does not produce a stable incremental gain over the strong physics baseline.

## Representations
Compared under matched data/splits:

1. Physics
2. Fixed waveform representation
3. Process-aware representation
4. Physics + Fixed
5. Physics + Process

ADR or other waveform-derived anomaly scores are diagnostics only and are not used as input features in the core representation comparison.

## Primary decision test
The main question is whether:

`Physics + Process > Physics`

under grouped/device-aware validation and at the event level where appropriate.

## Decision
**Partially Supported / Negative for the strong shared-state claim on E014.**

E014 supports the engineering value of process-aware representation, but does not provide evidence that the current Process representation contains broad quality-state information beyond strong explicit physics features.

## Follow-up
1. Do not tune larger representation models on this dataset.
2. Preserve the position-related visual-quality hypothesis for a larger independent sample.
3. Prioritize independent teardown, pull-strength, or otherwise verified weld-quality labels.
4. Keep the stop-loss rule: if another orthogonal independent task also shows no stable Process-over-Physics increment, narrow the project claim to process-aware / context-conditioned industrial representation rather than a general shared latent state.

## Privacy
This public record intentionally excludes proprietary identifiers, raw industrial data, internal thresholds, database details, exact private sample counts, and company-specific examples.
