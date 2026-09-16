# E015 — CCD Label Provenance Gate

## Status
The initial automatic label-source scan did not find explicit position-defect / weld-mark-area defect text in the first queried process database.

A second anchor-based provenance scan matched all independently reviewed CCD anchors in process-side records and confirmed that a generic CCD total-result is propagated into process data. This established broad CCD-NG provenance, but not detailed subtype provenance.

A final cross-schema scan then searched all accessible non-system schemas using independently reviewed anchors. Multiple quality / inspection / process records were found, including broad visual-inspection results and downstream defect records. However, no reliable, general subtype field was found that consistently separates independently reviewed position-related defects from weld-mark-area defects.

One downstream record contained a position-related tab-defect description for a single position anchor. That record is useful corroborating evidence for that individual event, but it is not a general CCD subtype source and must not be generalized to the other anchors.

## Interpretation
The provenance question is now sufficiently resolved:

- broad CCD NG provenance: supported;
- detailed position-vs-area subtype provenance from accessible databases: not supported;
- independently reviewed position/area subtype labels therefore remain external/manual truth.

This is a data-provenance boundary, not a negative result for the process-representation hypothesis.

## Decision
Stop database-schema hunting for CCD subtype labels.

Future subtype-specific E015 experiments must use independently reviewed visual labels as external ground truth. Generic CCD NG may support a broad quality task, but it must not be silently relabeled as POSITION_NG or AREA_NG.

## Next step
Accumulate additional independently reviewed position-related defects and matched area-related controls, then test the pre-registered incremental question under event/device-aware validation:

`Physics + Process > Physics ?`

If subtype-specific incremental value does not reproduce with a larger independently reviewed cohort, close the position-defect signal as exploratory.

## Scientific rule
Missing inspection, generic CCD NG, downstream defect categories, or unmatched records remain distinct provenance classes. They must not be merged merely to increase sample size.

## Privacy
This public record intentionally excludes proprietary identifiers, table/field names, database details, internal thresholds, raw industrial data, and company-specific examples.
