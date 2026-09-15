# E000-H — Ordered Physical Composition

## Question

Does the **ordered relation among physical process units** add transferable state information beyond having the same segmented units without a common physical order?

This tests H002e. It does **not** revisit hard phase alignment or explicit phase-channel injection.

## Physical hierarchy

PHM2010 force signals provide a natural hierarchy:

`tooth sector -> spindle revolution -> cutting event`

Each common-phase spindle revolution is resampled to 288 samples and split into three consecutive 96-sample tooth sectors.

## Fair comparison

Two representations use exactly the same cuts, revolution boundaries, tooth sectors, raw Fx/Fy/Fz samples, model architecture, VICReg objective, token count, optimization, seeds and LOCO splits.

### Ordered composition

Within every revolution, the three tooth-sector embeddings are composed in their physical order:

`[T0, T1, T2] -> RevolutionEncoder`

### Shuffled composition

The same three tooth sectors are retained, but their positions are replaced by a deterministic non-identity random permutation for each revolution:

`[Tpi(0), Tpi(1), Tpi(2)] -> same RevolutionEncoder`

The permutation is fixed for both augmented SSL views of that revolution. Thus the control preserves segmentation and signal content but removes a globally consistent physical order.

## Model

`Raw tooth waveform -> shared ToothEncoder -> ordered/shuffled composition -> shared RevolutionEncoder -> revolution latent`

SSL is VICReg at revolution level. The encoder is then frozen. A cutting-event representation is `mean + std` over revolution latents, followed only by a Ridge wear probe.

## Evaluation

Strict three-fold leave-one-cutter-out:

- C1 + C4 -> C6
- C1 + C6 -> C4
- C4 + C6 -> C1

Five fixed seeds: 7, 17, 29, 41, 53.

Wear remains an auxiliary state probe; PHM2010 wear-label limitations still apply.

## Pre-registered H002e gate

Before inspecting results, ordered composition is **SUPPORTED** only if all five checks pass:

1. mean LOCO R2 gain over shuffled order >= 0.05;
2. worst-fold mean R2 is not worse than shuffled order;
3. ordered composition wins in at least 2 of 3 held-out cutters;
4. ordered composition wins in at least 4 of 5 seed-averaged comparisons;
5. mean fold seed standard deviation is no more than 0.05 worse than shuffled order.

`PARTIAL` if at least 3 of 5 checks pass; otherwise `NOT_SUPPORTED`.

## Interpretation boundary

A negative result does not prove that all industrial process order is useless. PHM2010 milling is highly periodic and its three flutes may be close to exchangeable. A positive result would be evidence that ordered physical composition carries cross-domain state information even in this relatively symmetric process.
