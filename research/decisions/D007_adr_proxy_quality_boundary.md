# D007 — ADR proxy is not independent quality truth

## Context

The ultrasonic-welding pipeline contains a waveform-derived distance signal that can be used to identify a high-confidence abnormal subset at a site-validated threshold. This is useful for scaling anomaly studies beyond a handful of teardown samples.

## Decision

Use the waveform-derived ADR signal as a **proxy label** for H005a, but do not call it teardown-confirmed virtual weld or independent physical quality truth.

### Label semantics

- `HIGH_ADR_ANOMALY`: high-confidence waveform anomaly proxy defined by the process-owner validated threshold.
- `LOW_ADR_REFERENCE`: matched low-distance reference subset; it is not automatically a verified-normal quality label.
- Intermediate-distance samples are excluded from the first proxy experiment to avoid ambiguous supervision.

## Experimental control

Proxy anomalies and references must be matched by available process context (device, weld point, polarity/material context, amplitude/recipe context, and nearby time where possible).

Both positive- and negative-electrode data may be used, but they must not be pooled in a way that lets polarity or recipe become a shortcut label.

## Scientific boundary

Because ADR is computed from the waveform itself, success on this task can support:

1. sensitivity of Process Token / learned representation to waveform-process abnormality;
2. comparison against Fixed Patch and explicit physics features;
3. cross-device/context robustness of anomaly separation.

It **cannot by itself prove** that the representation contains independent weld-quality information or establish a true shared physical latent state.

Independent teardown, pull-test, or other quality truth remains necessary for H005b.

## Consequence

H005 is split into two evidence levels:

- **H005a — waveform anomaly proxy:** scalable, high-confidence proxy experiment using ADR-derived labels;
- **H005b — independent quality truth:** teardown / pull-test / confirmed quality labels.

A strong H005a result is useful, but only H005b can materially strengthen the claim that the learned state contains quality information beyond the waveform-derived proxy itself.
