# E015 — CCD Position Defect Incremental Gate

## Purpose
Test whether process-aware representation adds information beyond a strong physics baseline specifically for independently reviewed visual position-related defects.

## Motivation
Prior independent-quality evaluation suggested a possible but small process-representation signal on position-related visual defects. The evidence is currently too small to support a strong claim and requires targeted replication.

A targeted literature scan found adjacent work on welding vision/geometric defect detection, stage-aware industrial time-series modeling, and physics-informed quality monitoring, but did not identify an exact prior study combining all four elements of this gate: physical-stage representation, strong explicit-physics control, independent geometric defect truth, and cross-context incremental evaluation. This is a boundary statement for the current search, not a claim that no such work exists.

## Truth provenance
Detailed position/area subtype labels are treated as external/manual visual truth. A broad database CCD-NG flag may confirm that an event is visually abnormal, but it must not be used to infer a detailed subtype.

Keep visual defect subtypes separate:

- position-related defect
- area-related defect
- combined area + position defect

Records with missing or unavailable visual inspection remain unknown and must not be treated as normal controls.

## Two complementary tasks

### T1 — Context-relative anomaly sensitivity
For each independently reviewed position-defect event, compare its process instances against context-matched unlabeled neighbors. Neighbors remain unlabeled references, not verified normal samples.

### T2 — Subtype discrimination
When enough labels are available, directly compare `POSITION_NG` against `AREA_NG` at the event/product level. This is the cleaner test because both sides have independent visual labels and neither class is treated as normal.

Combined area+position events are kept separate and are not silently merged into either pure subtype.

## Representation comparison
Use the same data, grouped splits, and event-level evaluation for:

1. Physics
2. Fixed waveform representation
3. Process-aware representation
4. Physics + Fixed
5. Physics + Process

ADR or other waveform-derived anomaly scores are diagnostic only and must not be used as core model inputs.

The strong Physics baseline must preserve signed state variables and other physically interpretable process quantities rather than using weakened or absolute-only versions.

## Primary hypothesis
For independently reviewed position-related defects:

`Physics + Process > Physics`

The effect must remain under grouped event-level evaluation and must not be explainable by one device, one context, or a few isolated samples.

For subtype discrimination, the strongest evidence would be that Process contributes information that separates position-related from area-related defects after explicit physics variables are already controlled.

## Evidence accumulation
- Fewer than 10 independently reviewed pure position events: descriptive only; no decision.
- Around 10–19: exploratory checkpoint only; inspect effect direction and context dependence.
- Around 20–30 or more: formal replication gate, using grouped resampling / paired event-level uncertainty estimates.

These counts are pragmatic evidence targets, not guaranteed statistical power thresholds.

## Decision rule
- Stable incremental value across grouped contexts and both T1/T2 where feasible: continue the targeted process-structure hypothesis.
- Increment only in one context/device or only under one fragile metric: classify as insufficient evidence.
- No reproducible incremental value after the formal gate: stop pursuing position-related Process advantage as a separate scientific branch.

## Privacy
This public protocol intentionally excludes proprietary identifiers, raw industrial data, internal thresholds, database details, and company-specific labels or examples.
