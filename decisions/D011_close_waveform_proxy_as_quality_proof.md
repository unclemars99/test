# D011 — Close waveform-derived proxy as primary quality-proof route

## Decision
Do not use a waveform-derived anomaly proxy as the primary evidence that the learned process representation contains independent quality-state information.

## Reason
The hard-matched control failed: even after same-context matching, the high-proxy group could not be paired with low-proxy references that were simultaneously close in simple observable process quantities. The proxy separation is therefore already strongly explained by physical/acquisition-scale differences.

## What remains supported
- Process-aware representation remains useful for staged, non-stationary process organization.
- Cross-device / third-domain transfer evidence remains relevant.
- The anomaly proxy remains useful for engineering screening and operational monitoring.

## What remains open
Whether the representation captures quality state beyond strong physical features is still unresolved.

## Next evidence gate
Require labels that are independent of the waveform-derived proxy, preferably teardown, pull-test, verified defect, lifecycle transition, or another external outcome. Compare strong physics features against physics plus learned process representation under frozen-encoder and cross-context evaluation.
