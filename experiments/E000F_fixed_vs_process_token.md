# E000-F — Fixed Patch vs phase-aligned Process Token

## Purpose

Test H002c_2 on ordered raw PHM2010 force signals:

> Does alignment to a recovered physical process coordinate improve cross-cutter shared representation relative to an equal-budget fixed sampling patch?

E000-E established that the spindle coordinate (~173.33 Hz) is recoverable across all 21 audited cuts. E000-F now tests whether using that coordinate actually helps representation learning.

## Data

Public Kaggle PHM2010 mirror: `rabahba/phm-data-challenge-2010`.

For each cutter C1/C4/C6, use 15 approximately evenly spaced cuts over 1..315 (45 cuts total). Raw files are downloaded ephemerally by GitHub Actions and are never committed.

Only ordered force channels Fx/Fy/Fz are used in this first H002c_2 experiment so the manipulated variable stays close to the coordinate evidence from E000-E.

Wear is used only by the frozen downstream probe/evaluation; it is never used to train the self-supervised encoder.

## Three representations

All conditions produce the same token shape and token count.

### 1. Fixed Patch

Take the center of the same raw signal region and split it into 128 contiguous patches of 288 samples. The patch length is intentionally close to one spindle revolution, making this a strong baseline: it knows the approximate physical scale but not the phase boundaries.

### 2. Process Token

Recover spindle phase from Fx using the E000-E procedure. Segment true revolution-to-revolution cycles, select 128 center cycles, and resample every cycle to 288 phase-normalized samples. Each token therefore represents one physical revolution.

### 3. Random-Phase Process Token

Start from the phase-aligned Process Tokens, then apply one deterministic random circular phase offset per cut to every revolution in that cut. This preserves one-revolution segmentation, token count and signal content while destroying a common cross-cut phase origin.

This is a negative control for the hypothesis that common physical phase alignment, rather than cycle-length grouping alone, causes any gain.

## Fair encoder / SSL protocol

For every representation and outer fold:

- same local token encoder: `864 -> 128 -> 64 -> 12`;
- same train-only StandardScaler on flattened token coordinates;
- same VICReg-style objective and augmentation;
- same number of tokens per cut (128);
- same token dimensionality (3 x 288);
- same 5 random seeds;
- same leave-one-cutter-out split;
- same frozen cut representation: concatenate mean and standard deviation of token embeddings;
- same frozen Ridge wear probe.

The encoder sees no wear label, cut index, failure label or cutter ID during SSL.

Because cut representations pool tokens by mean/std, E000-F specifically tests **within-token physical alignment**. It does not test ordered composition across tokens; H002e remains open.

## Pre-registered decision rule

Before inspecting E000-F results, H002c_2 receives provisional support only if all of the following hold:

1. Process Token mean LOCO R2 exceeds Fixed Patch by at least 0.05;
2. Process Token worst-fold mean R2 is no worse than Fixed Patch worst-fold mean R2;
3. Process Token mean LOCO R2 exceeds Random-Phase by at least 0.05;
4. Process Token beats Fixed Patch in at least 2 of 3 fold means;
5. any apparent gain is not driven by a single random seed.

If gains are small/inconsistent, status is PARTIAL or NOT SUPPORTED rather than moving the thresholds after seeing results.

## Status

RUNNING via GitHub Actions. Results will be committed to `results/e000f/`.
