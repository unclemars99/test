# H002 — Process Token vs Fixed Patch

## Proposition

Tokenization aligned to a physically meaningful process coordinate can produce a more transferable shared representation than tokenization aligned only to the sampling coordinate.

## Sub-hypotheses

- H002a: process-aware segmentation outperforms equal-length fixed patches.
- H002b: hierarchical `Local -> Stage -> Event` representation adds value beyond flat local tokens.
- H002c: physical-coordinate alignment itself improves cross-domain representation quality.
- H002d: the best process coordinate may depend on sensing modality.
- H002e: ordered composition of physical process units adds value beyond segmentation alone.

## Fair-comparison rule

All comparisons must use the same data split, comparable model capacity, the same backbone, the same self-supervised objective, and comparable token counts. The main manipulated variable should be tokenization / process alignment.

## Current status

OPEN. Synthetic process-coordinate audit code has passed sanity checks. Real-data support is still pending raw/high-frequency public data or an equivalent process-aligned public benchmark.
