# D014 — Close CCD Subtype Schema Hunting

## Decision
Stop searching accessible database schemas for a universal CCD subtype field that separates position-related defects from weld-mark-area defects.

## Evidence
Anchor-based scans established that broad CCD-NG outcomes are propagated into process/quality records. A final cross-schema audit found multiple related records but no consistent subtype field that reproduces the independently reviewed position-vs-area labels across anchors.

A downstream position-related defect description was observed for one individual anchor. It is treated only as event-level corroboration and not as a reusable subtype source.

## Consequence
For E015, detailed CCD subtype labels are external/manual independent truth. Generic CCD NG remains a separate broad outcome and must not be relabeled as a subtype.

## Next
Accumulate a larger independently reviewed position-defect cohort plus area-defect controls. Evaluate the pre-registered incremental gate:

`Physics + Process > Physics ?`

Use grouped event/device-aware validation. If the exploratory position signal does not reproduce, close it rather than expand the model.

## Privacy
No proprietary identifiers, schema/table names, internal database details, raw industrial data, or company-specific examples are included.
