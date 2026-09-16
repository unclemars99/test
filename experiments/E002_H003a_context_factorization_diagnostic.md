# E002 / H003a — Context Factorization Diagnostic

## P

Can equipment information simply be removed from a Process Token representation to reveal a shared process state?

## Experiment

Starting from the E001 Process Token representation, three tests were performed:

1. Equipment-wise affine normalization using only early-time unlabeled reference data.
2. Stronger domain removal with iterative linear projection.
3. Matched-state control: pair cross-domain samples with similar external process feedback, then ask whether equipment identity is still predictable from waveform shape.

## Evidence

Affine normalization:

- cross-domain process Spearman: ~0.879
- future-time Spearman: ~0.842
- linear domain accuracy: ~50%

Strong domain removal:

- when linear domain accuracy was reduced to ~67%, cross-domain process Spearman fell to ~0.474.

Matched-state control:

- even after matching process state, equipment identity remained predictable at roughly 97–99% with nonlinear classifiers.

## Decision

**Simple domain erasing: NOT SUPPORTED.**

A part of equipment variation is a removable calibration/scale effect, but higher-order equipment effects are entangled with real process information.

The observation model should therefore be treated as:

`X = G(Z_process, C_device)`

rather than `Z_process = erase_device(X)`.

## N

Test context-conditioned canonicalization: absorb simple equipment transfer characteristics while preserving process-state geometry.