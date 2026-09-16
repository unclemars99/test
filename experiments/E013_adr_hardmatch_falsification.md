# E013 — ADR hard-matched control

## Goal
Test whether a high-confidence waveform anomaly proxy still contains useful representation-level separation after obvious process/acquisition confounders are controlled.

## Method
Use a high-anomaly proxy group and a low-proxy reference group. For each high-proxy sample, search for a same-context low-proxy sample while constraining device/process context and requiring close agreement on simple observable quantities such as waveform length, process duration, power level, and height change.

The representation model is not part of the matching stage. Proxy values are used only to define evaluation groups and are never model inputs.

## Result
No valid hard-matched pairs were found under either the strict or the pre-defined relaxed matching gates.

The dominant failure modes were waveform length and process duration: every candidate reference remained materially separated from its paired high-proxy sample on both quantities. Other variables such as power and height change were sometimes close, but this did not remove the length/duration separation.

## Interpretation
The tested proxy group is strongly coupled to directly observable process/acquisition-scale differences. Therefore this proxy is not an appropriate source of evidence for latent quality-state information beyond strong physical features.

This does not invalidate the proxy as an engineering anomaly indicator. It only limits its use as scientific evidence for a shared latent quality state.

## Decision impact
Close the ADR-proxy line as a primary proof route for shared quality representation. Future H005 evidence should come from labels independent of the waveform-derived proxy, such as teardown, pull-test, verified defect, lifecycle, or other external process outcomes.
