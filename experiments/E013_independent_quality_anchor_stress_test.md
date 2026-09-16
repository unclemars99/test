# E013 — Independent Quality Anchor Stress Test

## Problem
Test whether independently confirmed quality events contain representation-level evidence beyond simple physics features.

## Evidence design
- Independent site-confirmed quality anchors were used rather than waveform-derived proxy labels.
- Each quality case can map to multiple process records, so evaluation is treated as a **multiple-instance / bag-of-contexts** problem: a case is considered process-abnormal when at least one matched process context is an outlier relative to its local unlabeled context distribution.
- Local neighbors are context-matched and **unlabeled**; they are not treated as verified normal samples.
- ADR is used only as an external diagnostic and never as an input feature.

## Representations compared
1. Physics features: aggregate process quantities and simple waveform/acquisition observables.
2. Fixed waveform representation: generic resampled waveform shape.
3. Process representation: stage-aware representation using the first physical process packets and their relative structure.

For each anchor record, anomaly evidence is measured as its percentile relative to local same-context neighbors. The case-level score is the maximum percentile across its process contexts.

## Sanitized results
Across the small set of independent quality cases:
- Every confirmed quality event contained at least one process context that was strongly unusual relative to its local context distribution.
- Physics features already identified strong evidence in all cases.
- Fixed waveform shape also identified strong evidence in all cases.
- Process representation identified quality-related structure, but it did **not** consistently exceed either strong physics features or the fixed waveform baseline.
- In the two confirmed virtual-weld cases, the strongest local ADR evidence was high relative to the local context but remained below the previously used high-confidence absolute ADR threshold. This shows that an absolute high threshold can be sufficient for severe anomalies while being incomplete as a detector of real quality failures.
- One independent quality case exhibited a context in which absolute ADR values were on a dramatically different numeric scale from other contexts. Because local neighbors shared the same scale, the absolute value alone cannot be interpreted as transferable evidence without validating ADR scale/provenance by context.

## Important diagnostic
A generic fixed representation can become highly sensitive to late isolated waveform spikes that appear physically inconsistent with the main welding process. The stage-aware Process representation is less sensitive to such late isolated components because it focuses on the principal physical packets. This may be a robustness advantage, but it is not yet evidence of superior quality-state information.

## Decision
**H005: PARTIALLY SUPPORTED / CORE CLAIM NOT SUPPORTED YET**

Supported:
- Independent quality events are reflected in the measured process.
- Process-aware representation carries quality-related structure.

Not supported yet:
- Process representation adds stable quality information beyond a strong physics baseline.
- The current evidence is sufficient to claim a reusable shared latent quality state.

## Next
1. Expand independent quality truth, especially teardown / pull-strength / confirmed defect labels.
2. Preserve the multiple-instance formulation when one quality case maps to multiple process records.
3. Require the decisive criterion: `Physics + Process > Physics` under frozen representations and held-out quality truth.
4. Audit ADR provenance/scale before using any absolute ADR threshold across contexts.
5. If no stable incremental gain appears after stronger independent-quality validation, stop the strong `Z_shared` claim and retain Process Token as a process-aware representation method.
