# D001 — Ultrasonic Shared-State Stage 1 Decision

## Decision date

2026-09-16

## Evidence considered

E001–E005.

## Current decisions

1. **Freeze the physical Process Token structure** as `P1 -> Gap -> P2` for the current ultrasonic-welding line. Do not continue tuning segmentation unless new evidence shows systematic boundary failure.
2. **Do not optimize for complete domain invariance.** Equipment identity is partly entangled with real process information; aggressive domain erasing damages useful state.
3. **Keep a low-capacity affine equipment/context adapter** as the current strongest baseline.
4. **Treat relative physical state as a promising coordinate**, but do not normalize every variable indiscriminately.
5. **A genuine `Z_shared` has not yet been demonstrated.** Waveform-internal transfer is strong; independent external-process probes remain materially weaker.
6. **Next decisive test is an unseen third same-material domain.** The purpose is external validation, not additional training volume.
7. **Cross-material transfer is deferred** until the unseen same-material domain test succeeds. Material and recipe are physical context, not nuisance noise.

## Current status

- Process Token: **SUPPORTED on current ultrasonic domain pair**
- Device affine context correction: **SUPPORTED**
- Aggressive domain erasing: **NOT SUPPORTED**
- Context-conditioned factorization: **PARTIALLY SUPPORTED**
- Universal/shared industrial process state: **OPEN**

## Stop rule

If a model only improves waveform-internal probes but fails external-process transfer or unseen-domain validation, it must not be promoted as evidence for `Z_shared`.