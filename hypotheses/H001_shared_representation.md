# H001 — Cross-domain shared representation

## Proposition

Self-supervised or unsupervised representation learning can produce a process representation that transfers across tools/domains while retaining useful process-state information.

## Formal target

Let `X` be observed process data and `Z = E(X)` the learned representation. A useful shared representation should:

1. preserve state/task information;
2. reduce domination by domain identity;
3. transfer to a held-out tool/domain;
4. remain usable by simple frozen probes.

A conceptual sharedness ratio is:

`S_shared = D_state / (D_domain + eps)`

where `D_state` measures separation between process states and `D_domain` measures variation caused by domain identity under comparable state conditions.

## Evidence required

- leave-one-domain-out transfer;
- frozen linear / simple probes;
- domain leakage probe;
- trajectory consistency;
- no test-domain leakage during scaling/PCA/pretraining;
- worst-domain and fold-consistency checks, not mean performance alone.

## Current status

**PARTIALLY SUPPORTED, with substantially stronger evidence after E000-D.**

E000-C showed that reconstruction-oriented generic SSL modestly improved the average and worst-domain result over PCA but remained unstable and failed on C6 on average.

E000-D then tested a VICReg-like invariance objective. Its frozen-probe mean R2 reached 0.585, every held-out-cutter fold had positive mean R2, and all five C6 seeds were positive. The previous catastrophic C6 domain shift was therefore substantially reduced.

The pre-registered PASS gate is still not met because C6 seed-to-seed R2 std is 0.206, narrowly above the fixed 0.20 threshold. We do not move this threshold after seeing the result.

H001 is therefore not yet promoted to fully SUPPORTED as a general industrial claim. Stronger evidence is still required on raw process signals, additional domains, and ideally physical-process representations.

See `decisions/D000d_e000c.md`, `decisions/D000e_e000d.md`, `results/e000c/`, and `results/e000d/`.
