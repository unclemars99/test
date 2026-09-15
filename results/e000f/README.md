# E000-F Results — Fixed Patch vs Process Token

Common raw cuts used: 45; token shape per cut: 128 x 3 x 288.

## Aggregate comparison

| representation   |   wear_mae_mean |   wear_nmae_range_mean |   wear_r2_mean |   wear_r2_min_fold |   wear_r2_max_fold |   fold_r2_range |   mean_fold_seed_std |
|:-----------------|----------------:|-----------------------:|---------------:|-------------------:|-------------------:|----------------:|---------------------:|
| fixed_patch      |         25.2427 |               0.153927 |     0.407744   |           0.275218 |           0.59739  |        0.322172 |            0.0786476 |
| process_token    |         31.58   |               0.186296 |     0.00286304 |          -0.339191 |           0.305017 |        0.644208 |            0.165544  |
| random_phase     |         30.586  |               0.182311 |     0.064477   |          -0.390521 |           0.394071 |        0.784592 |            0.144465  |

## Fold comparison

| representation   | heldout_cutter   |   wear_mae |   wear_nmae_range |    wear_r2 |   wear_r2_seed_std |
|:-----------------|:-----------------|-----------:|------------------:|-----------:|-------------------:|
| fixed_patch      | C1               |    19.4341 |          0.154818 |  0.275218  |          0.162803  |
| fixed_patch      | C4               |    23.7492 |          0.13278  |  0.59739   |          0.023424  |
| fixed_patch      | C6               |    32.5448 |          0.174185 |  0.350625  |          0.049716  |
| process_token    | C1               |    16.3679 |          0.130392 |  0.305017  |          0.219752  |
| process_token    | C4               |    37.8407 |          0.211564 | -0.339191  |          0.17861   |
| process_token    | C6               |    40.5315 |          0.216932 |  0.0427631 |          0.0982693 |
| random_phase     | C1               |    17.5704 |          0.139971 |  0.189881  |          0.0899244 |
| random_phase     | C4               |    41.4562 |          0.231778 | -0.390521  |          0.278456  |
| random_phase     | C6               |    32.7313 |          0.175183 |  0.394071  |          0.0650145 |

## Pre-registered H002c_2 gate

Status: **NOT_SUPPORTED**

- mean_gain_vs_fixed_ge_0p05: FAIL
- worst_fold_not_worse_than_fixed: FAIL
- mean_gain_vs_random_phase_ge_0p05: FAIL
- beats_fixed_in_at_least_2_folds: FAIL
- beats_fixed_in_at_least_4_of_5_seed_means: FAIL

## Guardrails

- This is a small raw-data public POC, not final industrial validation.
- Wear labels are downstream evaluation only and retain PHM2010 label limitations.
- Token order is mean/std pooled, so this experiment tests within-token phase alignment, not ordered composition (H002e).
- Raw files are not committed.