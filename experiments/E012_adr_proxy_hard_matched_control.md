# E012 — ADR proxy hard-matched control

## Goal

Test whether any anomaly-separation advantage remains after removing trivial physical and acquisition-scale differences between high-ADR and low-ADR samples.

## Sampling

For each high-ADR sample, search for a low-ADR reference under the same observable context whenever available:

- same machine/domain;
- same weld point / structural position;
- same polarity/material context;
- same amplitude/recipe context;
- close local time;
- closely matched weld duration;
- closely matched waveform sequence length;
- closely matched power level and height change when possible.

The matching variables are controls, not model targets.

## Evaluation

Compare frozen or fixed representations without using ADR as an input feature:

- Fixed waveform representation;
- Physics Features;
- Process Token representation;
- Physics + Fixed;
- Physics + Process.

Primary test: leave-context-out or pair-aware evaluation. Report not only classification AUC but also paired ranking consistency.

## Decision gate

- If Physics alone explains the proxy labels after hard matching, ADR remains an operational anomaly signal but contributes no evidence for a richer shared representation.
- If Process improves materially over strong Physics controls under hard matching, this supports residual waveform-structure information for H005a.
- Neither outcome is sufficient for H005b; independent quality truth is still required.

## Anti-leakage rule

`power_dtw_distance` / ADR is used only to define the proxy groups and is never passed to the representation or classifier as an input.
