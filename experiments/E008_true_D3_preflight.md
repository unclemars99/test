# E008 — True third-domain preflight

## Purpose

Test whether the ultrasonic process representation learned from two source domains survives contact with a genuinely unseen third domain before spending effort on a full external-validation dataset.

No proprietary device identifiers, database details, raw waveforms, or process setpoints are recorded here.

## Setup

- D1 + D2 are the two previously studied source domains.
- D3 is a new device/domain from the same material/process family with a nearby recipe.
- Shared representation learning uses D1 + D2 only.
- D3 is not used for shared-encoder retraining.
- D3 preflight contains 500 time-distributed unlabeled process records; process feedback variables are used only for evaluation.

## E1 — Physical-stage audit

The frozen stage rule `P1 -> Gap -> P2` was applied without D3-specific tuning.

Result:

- D3 stage detection succeeded on all 500 preflight records.
- Stage durations and major P1/P2 statistics remained inside or near the source-domain envelope.

This is positive evidence that the Process Token decomposition itself transfers to the new domain.

## E2 — Zero-shot representation transfer

A frozen PCA/probe protocol was trained on D1 + D2 and evaluated on D3 with no target-domain retraining.

Across a stress grid of representation dimensions and probe regularization values:

- Fixed representation mean primary external-state Spearman: ~0.62.
- Process representation mean primary external-state Spearman: ~0.68.
- Process exceeded Fixed on every tested configuration; the average gain was about +0.06.
- Process also preserved waveform-stage observables more consistently than Fixed.

Primary external-state evaluation uses the feedback variables with meaningful target-domain variation; near-constant control/context variables are reported separately rather than allowed to dominate the mean.

## E3 — Target affine calibration

A lightweight target-domain affine adapter was estimated from small unlabeled D3 prefixes.

Result:

- calibration improved some waveform alignment diagnostics;
- but full affine alignment did not improve the primary independent process-state transfer and usually reduced it relative to zero-shot Process Token.

Interpretation:

The D3 shift is not pure nuisance/device shift. A nearby recipe/context change contains real physical information, so blindly normalizing the target to the source can erase meaningful state differences.

## E4 — Physics-feature baseline

A deliberately simple physical baseline using stage-level peak, area, and duration features was also tested.

Result:

- simple physical features remained very strong on the D3 process-feedback tasks;
- a nonlinear probe on these features outperformed the current learned low-dimensional Process representation on several easy feedback targets.

This is an important negative control: current D3 evidence supports Process Token transfer, but does **not** yet prove that the learned latent representation is superior to compact physics features or that a universal `Z_shared` has been found.

## Decision

### Supported at preflight level

- `P1 -> Gap -> P2` transfers to a true third domain.
- Process-aware representation transfers better than a matched Fixed baseline in the zero-shot stress test.
- full target affine alignment is not automatically beneficial when device and recipe shifts are mixed.

### Still open

- superiority over strong physics-feature baselines;
- transfer to independent quality outcomes;
- robust `Z_shared` beyond waveform-derived/easy process-feedback tasks;
- cross-material transfer.

## Next

Proceed to a larger D3 external-validation sample while keeping:

1. Shared Encoder frozen;
2. zero-shot Process Token as a primary baseline;
3. Fixed representation as a fair baseline;
4. compact physics features as a mandatory strong baseline;
5. target adaptation limited and explicitly recipe-aware rather than full distribution erasing.

Do not move to cross-material validation until this formal D3 study is complete.
