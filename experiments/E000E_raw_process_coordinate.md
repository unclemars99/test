# E000-E — Raw PHM2010 process-coordinate audit

## Purpose

Open H002c on real high-frequency public data before training any Process Token model.

The question is deliberately narrow:

> Can a stable physical periodic coordinate be recovered from raw PHM2010 milling signals across cutters and wear stages?

This experiment does **not** yet compare Process Token against Fixed Patch. It only tests the prerequisite H002c_1: process-coordinate observability.

## Public data source

Kaggle mirror: `rabahba/phm-data-challenge-2010` (CC0 public-domain mirror of the PHM2010 challenge).

Only a small set of raw files is downloaded ephemerally by GitHub Actions. Raw CSVs are **not committed** to this repository.

Dataset facts used as physical priors:

- sampling rate: 50 kHz/channel;
- spindle speed: 10,400 RPM -> about 173.33 Hz;
- three-flute cutter -> tooth-passing frequency about 520 Hz;
- channels: Fx, Fy, Fz, Vx, Vy, Vz, AE-RMS.

## Sampled cuts

For C1, C4 and C6, audit representative lifecycle locations:

`1, 50, 100, 150, 200, 250, 315`.

The cut index is used only to choose coverage. It is not used to infer phase.

## Audit protocol

For each raw cut and force channel:

1. read the ordered 50 kHz signal;
2. use the central region to reduce entry/exit transients;
3. estimate PSD with Welch;
4. search around the physically expected spindle and tooth-passing bands;
5. select the force channel with the strongest physically plausible periodic peak;
6. band-pass around that peak;
7. recover analytic phase with the Hilbert transform;
8. measure frequency error, phase monotonicity, cycle-length coefficient of variation and spectral prominence.

## Pre-registered engineering gate

A candidate coordinate is provisionally `PASS` when, over downloaded cuts:

- at least 80% of cuts are successfully audited;
- median physical-frequency error < 5%;
- at least 80% of audited cuts have frequency error < 5%;
- median cycle-length CV < 5%;
- median positive phase-increment ratio >= 95%.

`WARN` means a physical coordinate is visible but one or more stability gates are missed. `FAIL` means the expected coordinate is not reliably recoverable.

These are engineering gates, not theoretical constants.

## Important guardrail

The previously used `originfeature/data_x*.npy` arrays are not suitable for H002 because their 5,000 points per channel were created by random sampling without replacement from each cut, destroying temporal order. Downstream 500-point CSVs made from those arrays therefore cannot be used as phase-aligned Process Token evidence.

## Status

RUNNING via GitHub Actions. Results are written to `results/e000e/` and committed back without raw data.
