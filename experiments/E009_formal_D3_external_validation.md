# E009 — Formal third-domain external validation

## Purpose

Test whether the process-aware representation learned from two source domains transfers to a larger, genuinely unseen third domain from the same material/process family, without retraining on target-domain labels.

The third domain also contains a small recipe/context shift, making this harder than a pure device-only transfer.

## Protocol

Source domains: D1 + D2 only.

Target domain: D3, 2500 held-out samples.

No D3 target labels were used for representation or hyperparameter selection. Representation/model settings were selected using D1↔D2 source-domain transfer only.

All identifiers and raw industrial data remain private. Only anonymized aggregate evidence is recorded here.

## Stage observability

The frozen `P1 -> Gap -> P2` process decomposition succeeded on all source and D3 samples used in this run.

This supports transfer of the physical process coordinate itself beyond the original two-domain pair.

## Main external-transfer results

Mean Spearman across five process-feedback probes:

| representation | D3 mean Spearman |
|---|---:|
| Fixed waveform PCA + Ridge | 0.313 |
| Process Token PCA + Ridge | **0.550** |
| Compact physics features + nonlinear probe | 0.622 |
| Physics + Fixed waveform latent | 0.605 |
| Physics + Process latent | **0.655** |

Target-level Process vs Fixed:

- feedback-energy proxy: 0.747 vs 0.033
- duration: 0.380 vs 0.378
- pressure/context channel: -0.048 vs -0.052
- power proxy: 0.987 vs 0.436
- height-change: 0.683 vs 0.769

Process Token is therefore not universally better on every probe, but its overall external-transfer advantage over Fixed is large and stable.

Paired bootstrap on D3 gave Process minus Fixed mean-Spearman improvement about +0.238, with 95% interval approximately [0.223, 0.253].

## Incremental information beyond physics features

The stronger question is whether process-waveform structure adds anything after compact physical features are already present.

Results:

- Physics only: 0.622
- Physics + Process latent: **0.655**
- Physics + Fixed latent: 0.605

Thus the Process latent adds about +0.032 mean Spearman over the physics-only baseline, while the Fixed latent does not.

The gain is especially visible on height-change:

- Physics only: 0.647
- Physics + Process latent: **0.737**
- Physics + Fixed latent: 0.530

Paired bootstrap for Physics+Process minus Physics gives about +0.032 mean improvement, 95% interval roughly [0.023, 0.042].

This is the first current-line evidence that the process-aware waveform representation contains some transferable information beyond a compact hand-engineered physics baseline.

## Context calibration stress test

Applying full target-domain affine alignment using 50/100/200/500 unlabeled D3 samples reduced overall Process transfer compared with zero-shot.

Interpretation:

A new domain can contain real process/recipe change as well as measurement/device shift. Forcing the entire target distribution back to the source distribution can erase meaningful physical differences.

Therefore target adaptation should be context-conditioned, not unconditional domain matching.

## Important limitation

One source pressure/context channel contains a mixed or inconsistent regime and is not reliable primary evidence. The strongest current conclusions come from the other process-feedback probes and the physics-residual comparison.

Quality outcomes, teardown/pull-test labels, lifecycle targets and cross-material transfer remain untested in this formal D3 study.

## Decision

- physical `P1 -> Gap -> P2` coordinate: supported on D3;
- Process Token > Fixed: supported on formal D3 external transfer;
- Process latent adds some information beyond compact physics features: preliminary supported;
- unconditional target affine alignment: not supported;
- universal `Z_shared`: still open.

## Next

Stop optimizing D1/D2/D3 process-feedback proxies.

The next decisive evidence should use a target that is not almost directly encoded by the power waveform, preferably quality / teardown / pull-test, lifecycle change, or a genuinely new task. Cross-material validation should come after that or in parallel with strict material/context separation.
