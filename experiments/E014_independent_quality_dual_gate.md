# E014 — Independent Quality Dual Gate

## Purpose
Test whether a process-aware representation adds information beyond a strong physics baseline on two independent outcome families.

## Cohort A — Independent visual quality anchors
Use externally observed visual weld-quality outcomes rather than waveform-derived labels. Keep issue subtypes separate (area-related, position-related, combined) instead of collapsing everything into a single NG class. Records with missing visual inspection must remain unknown and must not be treated as normal controls.

One product may map to multiple welding process instances, so evaluation should be performed at the event/product level using multiple-instance aggregation. Context-matched nearby process records may be used only as unlabeled local references.

## Cohort B — Height-event downstream outcomes
Use height-state events with observed downstream outcome flags. Signed height-state variables are part of the strong physics baseline; do not replace them with absolute magnitude only. The downstream outcome is a label only and must not enter the representation input.

## Representations
Compare under matched data/splits:

1. Physics
2. Fixed waveform representation
3. Process-aware representation
4. Physics + Fixed
5. Physics + Process

ADR or other waveform-derived anomaly scores may be reported as diagnostics but must not be used as input features in the core representation comparison.

## Primary decision test
The main question is whether:

`Physics + Process > Physics`

under grouped/device-aware validation and at the event level where appropriate.

## Decision rule
- If incremental value is stable across both independent visual-quality and downstream-outcome tasks, the shared-process-state hypothesis gains support.
- If incremental value appears only on one task, narrow the claim to task-relevant process representation.
- If Physics + Process is approximately equal to Physics on both tasks, stop the strong shared-state claim and retain process-aware / physics-aware representation as the practical result.

## Privacy
This public record intentionally excludes proprietary identifiers, raw industrial data, internal thresholds, database details, and company-specific examples.
