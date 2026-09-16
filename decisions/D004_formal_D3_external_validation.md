# D004 — Formal D3 external-validation decision

## Decision

The research line has now passed a stronger external-domain gate.

A process-aware representation based on the ordered physical stages `P1 -> Gap -> P2` transfers to a larger unseen third domain better than a matched Fixed waveform representation.

The result is not only a waveform-proxy effect: when compact physical features are already present, adding the Process latent improves formal D3 transfer, while adding a Fixed waveform latent does not.

## What is now supported

1. The physical stage coordinate survives a true third-domain shift.
2. Process Token transfer is not confined to the original D1/D2 pair.
3. Process-aware waveform structure contains some transferable information beyond compact hand-engineered physics features.
4. Unconditional target-domain affine matching is unsafe when domain shift also contains real process/recipe change.

## What is not yet supported

1. A universal domain-invariant `Z_shared`.
2. Cross-material shared state.
3. Quality-level generalization.
4. Claims that learned representation replaces compact physics features.

## Strategic change

Do not spend the next cycle further optimizing easy process-feedback proxies on the same three domains.

The next experiment must test information that is not almost directly recoverable from the power waveform itself.

Priority evidence:

1. teardown / pull-test / confirmed quality labels;
2. lifecycle or tool-state change;
3. new task transfer;
4. then cross-material transfer with material/context explicitly separated.

## Status

H004 is supported within the current same-material external-domain scope, while the broader `Z_shared` proposition remains open.
