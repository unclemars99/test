# D001 — Transition from two-domain method development to external-domain validation

## Evidence so far

The current two-domain ultrasonic-welding study supports the following points:

- physical-stage Process Tokenization is useful in this staged process;
- simple device/context calibration removes part of the domain shift without destroying process information;
- aggressive domain erasing is not supported because it also removes useful process state;
- context-conditioned factorization is promising but not yet sufficient evidence for a true reusable shared state.

## Decision

Stop using the current two domains as the main source of new claims.

The next decisive experiment is external validation on a third unseen domain from the same material family.

The shared encoder must be trained only on D1/D2 and then frozen for the primary D3 test. D3-specific full retraining is not acceptable evidence for shared representation.

## Why

Further tuning on the same two domains risks converting the research problem into pair-specific optimization. A third domain is necessary to test whether the learned process coordinates are reusable rather than memorized for the original pair.

## Next

Run E006 once a suitable third-domain candidate is available.

After same-material external validation, move to cross-material testing using relative process state rather than absolute parameter equality.
