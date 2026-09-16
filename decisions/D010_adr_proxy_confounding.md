# D010 — ADR proxy batch is not independent quality evidence

## Decision

The ADR-proxy pilot batch is useful for operational waveform-anomaly validation, but it must not be used as independent evidence that the learned representation contains latent physical quality state.

## Reason

The proxy label is itself derived from the power waveform. In the pilot matched sample, the two proxy groups were already strongly separable by simple waveform/time-scale observables such as stored sequence length and weld duration. Therefore, a high classification score can be obtained without demonstrating representation value beyond known physics or beyond the proxy construction.

## Consequence

H005 is refined into two levels:

1. **H005a — waveform anomaly proxy sensitivity.** ADR-derived groups may be used to test whether a representation preserves known anomaly structure, but not as final quality evidence.
2. **H005b — independent quality-state validation.** Final support requires teardown, pull-test, verified defect, lifecycle, or another target that is not computed from the same waveform used as model input.

For H005a, the next experiment must use hard-matched controls so that duration, sequence length, power level, material/polarity context, machine/weld-point context, and local time are matched as closely as possible. If the classes cease to separate after this control, the previous result is interpreted as physical-scalar separation rather than latent-state evidence.

## Status

- ADR proxy: useful operational signal.
- Process Token quality-state claim from ADR: **not supported by this batch**.
- Independent quality-state hypothesis: **open**.
