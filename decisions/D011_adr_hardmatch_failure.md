# D011 — ADR hard-match failure closes proxy-quality branch

## Result
A hard-matched ADR control was attempted under the following matching constraints: same context, nearby time, similar waveform length, duration, power, and height change. Among 46 high-ADR candidates, no strict or relaxed matched pair was found.

Observed nearest-match gaps remained large on average: waveform-length difference about 36.8 points, duration difference about 0.073, and substantial residual differences in other process variables. This indicates that the ADR proxy groups are structurally separated by directly observable process/acquisition variables.

## Decision
- Stop using ADR-defined groups as evidence for latent quality-state information.
- Keep ADR as an engineering anomaly proxy / screening signal only.
- Do not spend additional effort optimizing ADR proxy classification.
- Return the main research line to independent quality truth: teardown, pull-test, verified virtual-weld or other labels not computed from the waveform itself.

## Implication for H005
H005 cannot be supported by ADR proxy data. The next valid test is whether Process representation adds information beyond strong physics features on independent quality labels.

## Privacy
No proprietary identifiers, raw industrial data, device IDs, database configuration, or internal sample codes are included in this record.
