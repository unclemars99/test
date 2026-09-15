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
- H002f: a **hybrid Process Token** that retains the raw local waveform and adds explicit physical-coordinate information outperforms either raw Fixed Patch alone or hard phase-normalized tokens alone.

## Fair-comparison rule

All comparisons must use the same data split, comparable model capacity, the same backbone, the same self-supervised objective, and comparable token counts. The main manipulated variable should be process structure / coordinate information.

## Current evidence

### E000-E — coordinate observability

21 representative raw 50 kHz PHM2010 cuts across C1/C4/C6 were audited. Both spindle (~173.33 Hz) and tooth-passing (~520 Hz) coordinates pass the pre-registered real-data observability gate. The spindle coordinate is reliable on all 21 cuts; the tooth-passing coordinate is within 5% frequency error on 20/21 cuts and is much more spectrally prominent in most cuts.

This supports a hierarchical physical coordinate for force observations:

`spindle revolution -> three tooth-passing subcycles`.

### E000-F v2 — hard alignment test

45 raw cuts were evaluated with strict leave-one-cutter-out, identical position-sensitive CNN token encoders, identical token-level VICReg objectives, identical token counts and five seeds.

Mean LOCO R2:

- Fixed Patch: **0.400**;
- hard phase-normalized Process Token: **0.177**;
- Random-Phase cycle token: **0.084**.

Hard Process Token therefore does **not** beat Fixed Patch. However, common-phase alignment improves over random phase by about +0.093 mean R2, suggesting that physical phase contains useful information even though hard normalization loses other useful state information.

## Current status

- **H002c_1: SUPPORTED on representative PHM2010 force signals.**
- **H002c_2: NOT SUPPORTED on E000-F v2.**
- **H002f: OPEN and now the next primary test.**
- **H002 overall: OPEN.**

The current evidence argues against defining Process Token as a replacement `raw waveform -> phase-normalized waveform only`. The next test should retain the raw sampling-coordinate waveform and add physical phase explicitly, e.g. `raw Fx/Fy/Fz + sin(phi) + cos(phi)`, under a parameter-matched encoder.
