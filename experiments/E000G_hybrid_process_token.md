# E000-G — Hybrid Process Token: raw waveform + explicit physical phase

## Purpose

Test H002f after E000-F v2 falsified the simple hard-alignment replacement.

E000-F produced two simultaneous observations:

- hard phase-normalized revolution tokens transferred worse than Fixed Patch;
- common physical phase still improved over random phase within the cycle-token family.

E000-G therefore isolates the next hypothesis:

> Physical coordinate information is useful when added to the raw waveform, rather than used to normalize/replace the raw sampling-coordinate signal.

## Data and split

Exactly the same public PHM2010 setup as E000-F:

- C1/C4/C6;
- 15 approximately evenly spaced raw cuts per cutter (45 total);
- Fx/Fy/Fz ordered 50 kHz force signals;
- 128 patches/cut;
- 288 samples/patch;
- strict leave-one-cutter-out;
- 5 seeds;
- wear used only by the frozen downstream probe.

## Representations

All three conditions use the **same raw patches and same boundaries**. No waveform resampling is performed.

1. **Fixed Raw**: `[Fx, Fy, Fz, 0, 0]`.
2. **Hybrid Phase**: `[Fx, Fy, Fz, sin(phi), cos(phi)]`, where `phi` is the recovered common Fx spindle phase.
3. **Hybrid Random Phase**: same raw Fx/Fy/Fz, but the phase channels receive one deterministic random phase offset per cut.

The two extra zero channels in Fixed Raw ensure the encoder input dimensionality and parameter count are exactly matched.

## Fair model

- identical position-sensitive 5-channel CNN token encoder;
- identical token-level VICReg objective;
- identical augmentation, epochs and optimizer;
- raw-force channels standardized using training cutters only;
- phase channels remain bounded sin/cos coordinates;
- cut embedding = mean + std of frozen token embeddings;
- identical train-only Ridge probe.

## Pre-registered H002f gate

Hybrid Phase receives provisional support only if all hold:

1. mean LOCO R2 exceeds Fixed Raw by >= 0.05;
2. worst-fold mean R2 is no worse than Fixed Raw;
3. mean LOCO R2 exceeds Hybrid Random Phase by >= 0.05;
4. Hybrid Phase beats Fixed Raw in at least 2/3 fold means;
5. Hybrid Phase beats Fixed Raw in at least 4/5 seed-averaged comparisons.

Thresholds are fixed before inspecting E000-G results.

## Status

RUNNING via GitHub Actions. Results will be committed to `results/e000g/`.
