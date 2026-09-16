# E015 — CCD Label Provenance Gate

## Status
The first automatic label-source scan did not find explicit position-defect / weld-mark-area defect text in the initially queried database.

A second anchor-based provenance scan then matched all independently reviewed CCD anchors in multiple process-side tables. A generic CCD total-result field was present and marked all anchors as NG, confirming that a broad CCD outcome is propagated into process records.

However, the process-side records did **not** expose a reliable subtype field that distinguishes position-related defects from weld-mark-area defects.

## Interpretation
This resolves one part of provenance but not the full E015 requirement:

- broad CCD NG provenance: supported;
- detailed defect subtype provenance: unresolved;
- therefore the broad CCD flag may support a generic quality task, but it cannot yet support the subtype-specific position-defect gate.

This is still a provenance limitation, not a negative result for the representation hypothesis.

## Next step
Search other schemas / accessible sources for detailed CCD defect type, image/picture links, coded subtype fields, or inspection metadata using the already verified anchors. If no additional source is found, treat position/area subtype labels as external/manual truth and stop database-schema hunting.

Do not change the representation model while subtype provenance is unresolved.

## Scientific rule
Only independently verified CCD labels may enter the subtype-specific E015 quality test. A generic CCD NG flag must not be silently relabeled as POSITION_NG or AREA_NG. Missing labels, unavailable inspection, or unmatched records remain unknown and must not be treated as normal controls.

## Privacy
This public record intentionally excludes proprietary identifiers, table/field names, database details, internal thresholds, raw industrial data, and company-specific examples.
