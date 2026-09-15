# E000-F Results — Fixed Patch vs Process Token

Common raw cuts used: 45; token shape per cut: 128 x 3 x 288.

## Aggregate comparison

| representation   |   wear_mae_mean |   wear_nmae_range_mean |   wear_r2_mean |   wear_r2_min_fold |   wear_r2_max_fold |   fold_r2_range |   mean_fold_seed_std |
|:-----------------|----------------:|-----------------------:|---------------:|-------------------:|-------------------:|----------------:|---------------------:|
| fixed_patch      |         25.3856 |               0.154912 |      0.400126  |          0.266327  |           0.581248 |        0.314921 |            0.0720993 |
| process_token    |         29.0765 |               0.172525 |      0.177161  |          0.0294452 |           0.306359 |        0.276914 |            0.157442  |
| random_phase     |         30.3576 |               0.183357 |      0.0842163 |         -0.218499  |           0.376884 |        0.595384 |            0.240729  |

## Fold comparison

| representation   | heldout_cutter   |   wear_mae |   wear_nmae_range |    wear_r2 |   wear_r2_seed_std |
|:-----------------|:-----------------|-----------:|------------------:|-----------:|-------------------:|
| fixed_patch      | C1               |    19.6704 |          0.1567   |  0.266327  |          0.136673  |
| fixed_patch      | C4               |    23.9242 |          0.133758 |  0.581248  |          0.0303548 |
| fixed_patch      | C6               |    32.5621 |          0.174278 |  0.352801  |          0.0492699 |
| process_token    | C1               |    16.1827 |          0.128916 |  0.306359  |          0.209959  |
| process_token    | C4               |    35.2024 |          0.196813 |  0.0294452 |          0.126922  |
| process_token    | C6               |    35.8444 |          0.191845 |  0.195677  |          0.135444  |
| random_phase     | C1               |    20.6461 |          0.164473 |  0.0942638 |          0.315968  |
| random_phase     | C4               |    36.2828 |          0.202854 | -0.218499  |          0.364718  |
| random_phase     | C6               |    34.1438 |          0.182743 |  0.376884  |          0.0415014 |

## Pre-registered H002c_2 gate

Status: **NOT_SUPPORTED**

- mean_gain_vs_fixed_ge_0p05: FAIL
- worst_fold_not_worse_than_fixed: FAIL
- mean_gain_vs_random_phase_ge_0p05: PASS
- beats_fixed_in_at_least_2_folds: FAIL
- beats_fixed_in_at_least_4_of_5_seed_means: FAIL

## Guardrails

- This is a small raw-data public POC, not final industrial validation.
- Wear labels are downstream evaluation only and retain PHM2010 label limitations.
- Token order is mean/std pooled, so this experiment tests within-token phase alignment, not ordered composition (H002e).
- Raw files are not committed.