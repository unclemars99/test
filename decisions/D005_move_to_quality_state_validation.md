# D005 — Move from easy process-feedback targets to quality-state validation

## Decision

Stop treating power/energy/timing feedback prediction as decisive evidence for `Z_shared`.

## Why

The formal third-domain audit shows two things simultaneously:

1. Process Token transfers substantially better than Fixed representation.
2. A comprehensive physical-feature baseline explains most of the easy feedback targets, leaving only a small incremental Process gain.

Therefore continued optimization on those targets has diminishing scientific value and risks optimizing for a proxy that is already well described by explicit physics features.

## Next stage

The decisive next test is H005: independently verified quality state beyond strong physics features.

Protocol:

- normal-only reference construction;
- frozen Process representation;
- no tuning on the small verified anomaly set;
- Physics vs Fixed vs Process vs Physics+Process comparisons;
- explicit false-positive controls using verified normal variants;
- defect-type-specific conclusions rather than one pooled OK/NG score.

If the quality-state increment is absent, the correct conclusion is that Process Token is a useful process coordinate but not yet evidence of a broader shared latent. If it is present and stable, the evidence for `Z_shared` becomes materially stronger.