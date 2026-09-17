# D015 — Convergence Reset

## Why this reset exists
The research program has accumulated several negative and narrowing results. The project therefore needs a fixed definition of what "converged" means, so the goal does not drift as experiments become stricter.

## Claims and current status

### C1 — Process-aware structure is better than arbitrary time structure
Status: **Supported**.

Across internal cross-device and external-domain checks, physically organized process representations have shown reproducible advantages over arbitrary fixed-time partitioning.

### C2 — A reusable process representation transfers across devices
Status: **Partially supported**.

Cross-device transfer exists, but device/context effects remain entangled with the observed signal. Naive domain erasure damages useful process information.

### C3 — Process representation adds information beyond strong explicit physics features for independent quality outcomes
Status: **Not yet supported**.

Strong physics features explain much of the current quality-related signal. Existing independent-quality evidence is too limited to conclude that Process adds stable incremental value.

### C4 — A universal shared latent process state supports multiple tasks and is a justified path toward dynamics/world-model learning
Status: **Unproven**.

This stronger claim must not be treated as the default conclusion.

## Fixed primary question
The remaining scientific question is:

`Does process-aware representation retain task-relevant information that is not already captured by strong explicit physics variables, and does that incremental information transfer across contexts/devices?`

## Frozen evaluation rule
The primary comparison is:

- Physics
- Process
- Physics + Process

Fixed-window representation remains a secondary structural baseline.

The critical effect is:

`Delta = performance(Physics + Process) - performance(Physics)`

Evaluation must be grouped at the independent event/product level and must avoid leakage across devices/contexts.

## Convergence outcomes

1. **Strong convergence** — stable positive Delta on at least two independent task families and across contexts/devices. Then continue toward shared-state and dynamics modeling.
2. **Narrow scientific convergence** — positive Delta only on one task family. Then keep a task-relevant process representation claim and stop the universal shared-state claim.
3. **Engineering convergence** — no stable positive Delta, but process-aware organization remains useful relative to arbitrary temporal structure. Then converge on context-conditioned Physics + Process-aware monitoring and stop the strong shared-latent narrative.

## Stop rule
Do not introduce a new architecture, tokenization mechanism, proxy label, or domain-erasure objective merely to rescue C3/C4 after a failed quality test. New methods require a new hypothesis and a separate experiment.

## Methodological note
A negative result against a stronger baseline is not failure to converge. It narrows the final claim. The project is considered converged once one of the three outcomes above is established with independent evidence.

## Privacy
This decision record contains no proprietary identifiers, internal thresholds, raw industrial data, database details, or company-specific examples.
