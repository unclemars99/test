# H002 — Process Token vs Fixed Patch

## Proposition

Tokenization aligned to a physically meaningful process coordinate can produce a more transferable shared representation than tokenization aligned only to the sampling coordinate.

## Sub-hypotheses

- H002a: process-aware segmentation outperforms equal-length fixed patches.
- H002b: hierarchical `Local -> Stage -> Event` representation adds value beyond flat local tokens.
- H002c: physical-coordinate alignment itself improves cross-domain representation quality.
- H002c_1: a physically meaningful process coordinate can be reliably recovered from real process signals.
- H002c_2: tokenizing on that recovered coordinate improves shared-representation learning relative to an equal-budget fixed-patch baseline.
- H002d: the best process coordinate may depend on sensing modality.
- H002e: ordered composition of physical process units adds value beyond segmentation alone.

## Fair-comparison rule

All comparisons must use the same data split, comparable model capacity, the same backbone, the same self-supervised objective, and comparable token counts. The main manipulated variable should be tokenization / process alignment.

## Current evidence

E000-E used 21 representative raw 50 kHz PHM2010 cuts across C1/C4/C6. Both spindle (~173.33 Hz) and tooth-passing (~520 Hz) coordinates passed the pre-registered real-data observability gate. The spindle coordinate was reliable on all 21 cuts; the tooth-passing coordinate met the <5% frequency-error condition on 20/21 cuts and was much more spectrally prominent in most cuts.

This supports a hierarchical physical coordinate for force observations:

`spindle revolution -> three tooth-passing subcycles`.

## Current status

- **H002c_1: SUPPORTED on representative PHM2010 force signals.**
- **H002c_2: OPEN.**
- **H002 overall: OPEN.**

The next experiment must compare Fixed Patch and phase-aligned Process Token using the same raw cuts, encoder, VICReg-style objective, token count and LOCO protocol. Recoverability alone is not evidence that Process Token improves representation quality.
