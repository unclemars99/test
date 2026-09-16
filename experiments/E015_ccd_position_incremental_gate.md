# E015 — CCD Position Defect Incremental Gate

## Purpose
Test whether process-aware representation adds information beyond a strong physics baseline specifically for independent visual position-related defects.

## Motivation
Prior independent-quality evaluation suggested a possible but small process-representation signal on position-related visual defects. The evidence is currently too small to support a strong claim and requires targeted replication.

## Cohorts
Keep visual defect subtypes separate:

- position-related defect
- area-related defect
- combined area + position defect

Records with missing or unavailable visual inspection remain unknown and must not be treated as normal controls.

## Representation comparison
Use the same data, grouped splits, and event-level evaluation for:

1. Physics
2. Fixed waveform representation
3. Process-aware representation
4. Physics + Fixed
5. Physics + Process

ADR or other waveform-derived anomaly scores are diagnostic only and must not be used as core model inputs.

## Primary hypothesis
For position-related independent visual defects:

`Physics + Process > Physics`

The effect must remain under grouped event-level evaluation and must not be explainable by one device, one context, or a few isolated samples.

## Decision rule
- Stable incremental value across grouped contexts: continue targeted process-structure hypothesis.
- Increment only in one context/device: classify as insufficient evidence.
- No incremental value: stop pursuing position-related Process advantage as a separate scientific branch.

## Privacy
This public protocol intentionally excludes proprietary identifiers, raw industrial data, internal thresholds, database details, and company-specific labels or examples.
