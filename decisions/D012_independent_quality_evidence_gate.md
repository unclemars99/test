# D012 — Independent Quality Evidence Gate

## Decision
The research line will no longer use waveform-derived anomaly proxies as primary evidence for a shared latent quality state.

Independent quality truth is now the governing gate.

## Current interpretation
The latest independent-quality stress test shows that confirmed quality failures are visible in the process, but strong physics features already explain much of the detectable abnormality. Process-aware representation is informative, yet no stable incremental advantage over the strong physics baseline has been demonstrated.

Therefore:

- `Process Token is useful` remains supported.
- `Process Token implies a reusable Z_shared quality state` remains unproven.
- Absolute ADR thresholds may remain engineering rules for high-confidence anomalies, but they are not accepted as scientific proof of latent quality state.
- ADR must be interpreted with context/provenance checks because numeric scale can differ strongly across process contexts.

## Stop-loss gate
Continue the strong shared-state hypothesis only if independent held-out quality truth shows a stable gain:

`Physics + Process > Physics`

under frozen representations, matched context, and without using waveform-derived labels as input or target leakage.

If this gain does not emerge after a reasonable expansion of independent quality truth, close the strong `Z_shared` claim and converge on **Process-aware / Physics-aware Representation** as the supported outcome.
