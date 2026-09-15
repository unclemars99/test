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

**PARTIALLY SUPPORTED on the current PHM2010-derived feature-level benchmark.**

E000-C shows that a generic denoising autoencoder modestly improves average and worst-fold transfer over PCA, but C6 still fails on average and the result is highly seed-sensitive. Therefore H001 remains open as a general industrial claim and requires stronger, more stable evidence on raw process signals and additional domains.

See `decisions/D000d_e000c.md` and `results/e000c/`.
