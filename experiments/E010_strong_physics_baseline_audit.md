# E010 — Strong-physics baseline audit on formal third-domain validation

## Question

Does the process-aware representation add transferable information beyond a reasonably comprehensive set of stage-level physical features, or was the apparent gain in E009 mainly caused by an underpowered physics baseline?

## Protocol

- Keep the physical decomposition frozen: `P1 -> Gap -> P2`.
- Fit all preprocessing and models on the two source domains only.
- Evaluate once on the untouched third domain.
- Use external process-feedback targets, not waveform reconstruction.
- Compare Fixed, Process, comprehensive physics features, Physics+Fixed, and Physics+Process.
- Model/representation settings are selected from source-domain transfer only; the target domain is not used for tuning.

## Results

Mean third-domain Spearman across the external feedback tasks:

- Fixed representation: **0.478**
- Process representation: **0.582**
- Comprehensive physics features: **0.739**
- Physics + Fixed: **0.738**
- Physics + Process: **0.744**

Paired bootstrap findings:

- Process - Fixed: median gain about **+0.104**, 95% interval roughly **[+0.090, +0.116]**.
- Physics + Process - Physics: median gain about **+0.005**, 95% interval roughly **[+0.002, +0.009]**.
- Physics + Fixed - Physics: no reliable aggregate gain.

The small Physics+Process increment is concentrated mainly in one timing-related feedback variable. It is not a broad improvement across all feedback variables.

Chronological-window analysis shows the same ordering overall: Process remains stronger than Fixed, while the comprehensive physics baseline remains the strongest simple representation.

## Interpretation

E009's core conclusion survives: physical-stage Process Token transfers materially better than ordinary Fixed representation to a genuine unseen domain.

However, the stronger audit weakens the broader claim that the current learned/process representation contains large amounts of information beyond well-designed physical features. Once the physics baseline is made comprehensive, most of the easy process-feedback signal is already captured.

Therefore:

- **Process Token > Fixed: supported.**
- **Large beyond-physics incremental information on easy feedback tasks: not supported.**
- **Small incremental information beyond physics: observed, but narrow.**

This is an important correction rather than a failure: process-aware tokenization is useful, but easy power/energy/timing feedback tasks are no longer a sufficient test for `Z_shared`.

## Next

Move the decisive test to targets that are not direct re-expressions of waveform amplitude or stage area:

1. teardown / pull-test / confirmed quality state;
2. lifecycle / tool-change state;
3. drift and task transfer;
4. later, cross-material transfer.

The next hypothesis should ask whether Process representation adds quality-state information after conditioning on strong physics features.