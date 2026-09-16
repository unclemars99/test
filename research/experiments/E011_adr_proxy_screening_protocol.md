# E011 — ADR proxy screening protocol

## Question

Can the current representations separate a high-confidence waveform-abnormal subset from matched low-distance references without relying on device, polarity, weld-point, or recipe shortcuts?

## Evidence level

This is a **proxy-label experiment**, not an independent quality-truth experiment.

## Dataset construction

1. Select a high-confidence ADR-abnormal subset using a process-owner validated threshold.
2. Build a low-ADR reference subset.
3. Exclude the ambiguous middle band in the first experiment.
4. Match references to anomalies on available context:
   - device,
   - weld point,
   - electrode / material context,
   - amplitude / recipe context,
   - nearby time when available.
5. Keep both polarities available, but evaluate stratified results and pooled-with-context-controlled results separately.

## Representation comparison

Freeze preprocessing/model choices before evaluating the proxy labels.

Compare:

- Fixed temporal representation;
- explicit physics features;
- Process Token representation;
- physics + fixed representation;
- physics + Process representation.

## Metrics

Because the abnormal set may be imbalanced, report at least:

- AUROC;
- AUPRC;
- recall at a fixed low false-positive rate;
- per-context / per-device performance;
- positive- vs negative-electrode stratified performance.

## Leakage controls

Do not use the ADR value itself as an input feature.

Do not let true device ID, product ID, absolute timestamp, or explicit label-derived fields enter the representation probe.

Run a context-only probe as a negative control. If context alone predicts the proxy label strongly, the result must be treated as confounded.

## Decision rule

H005a becomes supported only if Process or Physics+Process improves over its corresponding Fixed baseline consistently across context-controlled splits, not only in one pooled split.

Even a strong positive result does not establish independent weld-quality information because the proxy label is waveform-derived.

Independent teardown / pull-test / confirmed-quality validation remains H005b.
