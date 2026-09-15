# E000-G Results — Hybrid Process Token

| representation      |   wear_mae_mean |   wear_nmae_range_mean |   wear_r2_mean |   wear_r2_min_fold |   wear_r2_max_fold |   fold_r2_range |   mean_fold_seed_std |
|:--------------------|----------------:|-----------------------:|---------------:|-------------------:|-------------------:|----------------:|---------------------:|
| fixed_raw           |         25.9828 |               0.158963 |       0.347364 |          0.172492  |           0.510415 |        0.337923 |            0.0891269 |
| hybrid_phase        |         28.1488 |               0.171064 |       0.225163 |          0.0869448 |           0.425977 |        0.339032 |            0.0942863 |
| hybrid_random_phase |         27.4817 |               0.167634 |       0.240985 |          0.017158  |           0.422802 |        0.405644 |            0.122744  |

## Fold results

| representation      | heldout_cutter   |   wear_mae |   wear_nmae_range |   wear_r2 |   wear_r2_seed_std |
|:--------------------|:-----------------|-----------:|------------------:|----------:|-------------------:|
| fixed_raw           | C1               |    20.5178 |          0.163451 | 0.172492  |          0.125491  |
| fixed_raw           | C4               |    25.385  |          0.141925 | 0.510415  |          0.107761  |
| fixed_raw           | C6               |    32.0457 |          0.171514 | 0.359184  |          0.0341289 |
| hybrid_phase        | C1               |    20.9383 |          0.1668   | 0.0869448 |          0.0815424 |
| hybrid_phase        | C4               |    27.1688 |          0.151898 | 0.425977  |          0.139641  |
| hybrid_phase        | C6               |    36.3392 |          0.194494 | 0.162567  |          0.061675  |
| hybrid_random_phase | C1               |    21.0668 |          0.167825 | 0.017158  |          0.138421  |
| hybrid_random_phase | C4               |    27.5168 |          0.153844 | 0.422802  |          0.189287  |
| hybrid_random_phase | C6               |    33.8617 |          0.181233 | 0.282994  |          0.0405261 |

## Pre-registered H002f gate

Status: **NOT_SUPPORTED**

- mean_gain_vs_fixed_ge_0p05: FAIL
- worst_fold_not_worse_than_fixed: FAIL
- mean_gain_vs_random_phase_ge_0p05: FAIL
- beats_fixed_in_at_least_2_folds: FAIL
- beats_fixed_in_at_least_4_of_5_seed_means: FAIL

The raw force waveform and patch boundaries are identical across all conditions; only explicit phase side-information changes.