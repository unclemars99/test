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
- no test-domain leakage during scaling/PCA/pretraining.

## Current status

OPEN. Public PHM2010-derived data confirm a meaningful cutter-domain shift, but H001 itself is not yet supported until reproducible representation experiments are completed.
