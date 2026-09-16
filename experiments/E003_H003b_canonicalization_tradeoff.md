# E003 / H003b — Canonicalization Tradeoff

## P

How much equipment/context normalization can be applied before useful process information is damaged?

## Methods

Compared:

- Raw Process representation
- Device affine canonicalization
- Device quantile canonicalization
- Affine + CORAL
- Quantile + CORAL

## Evidence

Representative results:

| Method | Cross-domain process Spearman | Future-time | Domain logistic | Domain RF | Domain HGB |
|---|---:|---:|---:|---:|---:|
| Raw | 0.831 | 0.906 | 99.5% | 98.5% | 99.2% |
| Affine | 0.839 | 0.907 | 50.0% | 87.3% | 95.3% |
| Quantile | 0.833 | 0.893 | 51.0% | 82.5% | 91.1% |
| Affine + CORAL | 0.770 | 0.905 | 50.0% | 84.2% | 88.5% |
| Quantile + CORAL | 0.747 | 0.891 | 50.0% | 77.5% | 81.2% |

## Decision

**Device affine canonicalization: SUPPORTED as a strong low-capacity baseline.**

**Aggressive domain alignment: NOT SUPPORTED as the main objective.**

Removing more domain information does not monotonically improve shared process representation; stronger alignment begins to erase real physical variation.

## N

Replace “domain invariance” with a generative/context-conditioned view:

`X = Decoder(Z_process, C_device)`.

Evaluate whether relative physical state is a better shared coordinate than absolute process values.