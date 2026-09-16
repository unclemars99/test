# H005 — Quality-state information beyond strong physics features

## Problem

Formal third-domain validation shows that Process Token transfers better than Fixed representation, but a comprehensive set of stage-level physical features explains most of the easy process-feedback targets.

The remaining scientific question is therefore stronger:

> Does the process-aware representation contain reusable information about quality state that is not already explained by strong physical features?

## Hypothesis

After conditioning on strong stage-level physical features, a frozen process-aware representation should still improve ranking or separation of independently verified quality states.

Conceptually:

`quality evidence = physics baseline + incremental process representation`

The claim is not that every defect must be visible in the power waveform. Different failure modes may have different observability limits.

## Evaluation principles

- Do not train a black-box classifier on a tiny anomaly set.
- Build the normal reference from normal data only.
- Freeze representation construction before inspecting quality labels.
- Use verified quality labels only for evaluation.
- Compare Physics, Fixed, Process, Physics+Fixed, Physics+Process.
- Include teardown-normal variants as false-positive controls.
- Treat defect types separately when their physical observability differs.
- Do not tune thresholds on the verified anomaly samples.

## Primary evidence

For the best-observed quality mode, ask whether `Physics + Process` improves anomaly rank/separation over `Physics` alone while preserving normal-variant specificity.

## Negative / boundary evidence

If a defect class overlaps normal waveform space, that should be recorded as an observability boundary rather than forced into a positive result.

## Falsification

H005 is not supported if Process adds no stable quality-state information beyond the strong physics baseline, or if any apparent gain depends on tuning directly to the small verified anomaly set.

## Status

OPEN.