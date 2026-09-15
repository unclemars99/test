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

## Current evidence

### E000-E — coordinate observability

21 representative raw 50 kHz PHM2010 cuts across C1/C4/C6 were audited. Both spindle (~173.33 Hz) and tooth-passing (~520 Hz) coordinates pass the pre-registered real-data observability gate. The spindle coordinate is reliable on all 21 cuts; the tooth-passing coordinate is within 5% frequency error on 20/21 cuts.

This supports a hierarchical physical coordinate for force observations:

`spindle revolution -> three tooth-passing subcycles`.

### E000-F v2 — hard alignment test

Mean LOCO R2:

- Fixed Patch: **0.400**
- hard phase-normalized Process Token: **0.177**
- Random-Phase cycle token: **0.084**

Hard alignment does not beat Fixed Patch. Physical phase is observable, but replacing raw sampling-time structure with phase-normalized cycles loses useful transfer information.

### E000-G — hybrid phase-channel test

The raw waveform and patch boundaries were held identical. Only explicit physical phase side-information changed.

Mean LOCO R2:

- Fixed Raw: **0.347**
- Hybrid Phase `[raw + sin(phi) + cos(phi)]`: **0.225**
- Hybrid Random Phase: **0.241**

Hybrid Phase beats Fixed Raw in **0/3** held-out cutters and **0/5** seed-level mean comparisons. The pre-registered H002f gate returns **NOT_SUPPORTED**.

## Current status

- **H002c_1: SUPPORTED** — physical coordinate is observable on representative PHM2010 force signals.
- **H002c_2: NOT SUPPORTED** — hard phase-normalized local tokenization fails.
- **H002f: NOT SUPPORTED** — naively appending phase channels to raw local patches also fails.
- **H002 overall: OPEN, but local phase-based tokenization is materially weakened.**

## Current interpretation

The evidence now argues against both of these local designs:

`raw waveform -> phase-normalized waveform`

and

`raw waveform -> raw waveform + instantaneous phase channels`.

If H002 is pursued further, the next scientifically distinct test should move the physical structure to a **higher level** rather than continue tuning local phase encoding. The most relevant remaining hypothesis is H002e: whether the ordered composition `tooth -> revolution -> event` adds transferable information beyond the same unordered/local raw token content.
