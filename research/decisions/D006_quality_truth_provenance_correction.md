# D006 — Quality truth provenance correction

## Observation

The first H005 collector returned zero matches for all pre-registered quality-truth keys in the current XZ2 production table.

## Diagnosis

The small dismantling-confirmed quality set used in the earlier V4 work came from a different historical ultrasonic-welding source/domain than the current XZ2 D1/D2/D3 dataset. Therefore, directly querying the current XZ2 table with those historical keys is a provenance error rather than evidence that the labels are invalid.

## Decision

H005 is split into two tracks:

1. **H005a — historical quality-state diagnostic**
   - use the original historical labeled waveform source;
   - treat results as a mechanism diagnostic only;
   - do not mix it into the XZ2 external-validation score.

2. **H005b — XZ2 quality-state validation**
   - require XZ2-local teardown / pull-test / verified quality truth;
   - keep the already frozen Process Token / Physics / Fixed representations;
   - compare Physics vs Physics+Process without training on the tiny anomaly set.

## Method correction

Before extracting labels from a production database, the collector must first verify source provenance (database/table/domain/time) instead of assuming that a historical label list belongs to the current table.

Status: **PROVENANCE ERROR IDENTIFIED; H005 remains OPEN**.
