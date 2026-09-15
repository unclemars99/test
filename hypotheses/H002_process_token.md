# H002 — Process Token vs Fixed Patch

## Proposition

Process-aware representation should preserve useful raw state information while exposing physically meaningful process coordinates and structure. The value of Process Token must be demonstrated against a fair sampling-coordinate baseline, not assumed from physical interpretability alone.

## Sub-hypotheses

- H002a: process-aware segmentation can outperform equal-length fixed patches under suitable representation design.
- H002b: hierarchical `Local -> Stage -> Event` representation adds value beyond flat local tokens.
- H002c: physical-coordinate information can improve cross-domain representation quality.
- H002c_1: a physically meaningful process coordinate can be reliably recovered from real process signals.
- H002c_2: **hard phase-normalized tokenization** on that recovered coordinate outperforms an equal-budget fixed-patch baseline.
- H002d: the best process coordinate may depend on sensing modality.
- H002e: ordered composition of physical process units adds value beyond segmentation alone.
- H002f: a **hybrid Process Token** that retains the raw local waveform and appends explicit physical phase channels outperforms raw Fixed Patch alone.

## Fair-comparison rule

All comparisons must use the same data split, comparable model capacity, the same backbone, the same self-supervised objective, and comparable token counts. The main manipulated variable should be process structure / coordinate information.

## Evidence summary

### E000-E — coordinate observability

21 representative raw 50 kHz PHM2010 cuts across C1/C4/C6 were audited. Both spindle (~173.33 Hz) and tooth-passing (~520 Hz) coordinates pass the pre-registered real-data observability gate.

**H002c_1: SUPPORTED.**

### E000-F v2 — hard alignment

Mean LOCO R2:

- Fixed Patch: **0.400**
- hard phase-normalized Process Token: **0.177**
- Random-Phase cycle token: **0.084**

**H002c_2: NOT SUPPORTED.**

### E000-G — raw + explicit phase

Mean LOCO R2:

- Fixed Raw: **0.347**
- Hybrid Phase: **0.225**
- Hybrid Random Phase: **0.241**

**H002f: NOT SUPPORTED.**

### E000-H — ordered physical composition

The same three tooth-sector signals and the same hierarchical encoder were used; only globally consistent within-revolution physical order was preserved or destroyed.

Mean LOCO R2:

- Ordered composition: **0.083**
- Shuffled composition: **0.105**

Worst-fold R2:

- Ordered: **-0.130**
- Shuffled: **-0.063**

All five pre-registered H002e checks fail.

**H002e: NOT SUPPORTED on PHM2010.**

## Current status

- **H002c_1: SUPPORTED** — the physical coordinate is observable.
- **H002c_2: NOT SUPPORTED** — hard phase-normalized local tokenization fails.
- **H002f: NOT SUPPORTED** — explicit local phase side-information fails.
- **H002e: NOT SUPPORTED on PHM2010** — ordered tooth-to-revolution composition does not beat shuffled composition.
- **H002-PHM2010: NOT SUPPORTED under the tested formulations.**
- **Broader H002 across genuinely stage-asymmetric industrial processes: OPEN.**

## Research decision

PHM2010 is now frozen as a falsification benchmark. We will not keep tuning new PHM-specific Process Token variants to rescue the hypothesis.

The important combined finding is:

> **A physical process coordinate can be real, stable and recoverable without being the right representation variable for a given downstream/shared-state problem.**

The next legitimate test of the broader Process Token idea should move to a process whose stages are physically asymmetric and non-exchangeable, such as ultrasonic welding, where `start -> main weld -> tail -> second packet -> residual` has genuine directional process semantics.
