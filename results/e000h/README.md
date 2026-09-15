# E000-H Results — Ordered Physical Composition

| representation       |   wear_mae_mean |   wear_nmae_range_mean |   wear_r2_mean |   wear_r2_min_fold |   wear_r2_max_fold |   fold_r2_range |   mean_fold_seed_std |
|:---------------------|----------------:|-----------------------:|---------------:|-------------------:|-------------------:|----------------:|---------------------:|
| ordered_composition  |         29.242  |               0.175879 |      0.0830031 |         -0.13043   |           0.284107 |        0.414537 |             0.556883 |
| shuffled_composition |         29.3839 |               0.176971 |      0.104575  |         -0.0629065 |           0.292245 |        0.355152 |             0.433363 |

## Fold results

| representation       | heldout_cutter   |   wear_mae |   wear_nmae_range |    wear_r2 |   wear_r2_seed_std |
|:---------------------|:-----------------|-----------:|------------------:|-----------:|-------------------:|
| ordered_composition  | C1               |    19.0533 |          0.151784 | -0.13043   |           1.16985  |
| ordered_composition  | C4               |    34.7898 |          0.194507 |  0.0953319 |           0.262027 |
| ordered_composition  | C6               |    33.8829 |          0.181347 |  0.284107  |           0.238771 |
| shuffled_composition | C1               |    19.4859 |          0.15523  | -0.0629065 |           0.727218 |
| shuffled_composition | C4               |    34.2346 |          0.191402 |  0.0843848 |           0.29908  |
| shuffled_composition | C6               |    34.4312 |          0.184281 |  0.292245  |           0.27379  |

## Pre-registered H002e gate

Status: **NOT_SUPPORTED**

- mean_gain_over_shuffled_ge_0p05: FAIL
- worst_fold_not_worse_than_shuffled: FAIL
- wins_at_least_2_of_3_folds: FAIL
- wins_at_least_4_of_5_seed_means: FAIL
- seed_std_not_more_than_0p05_worse: FAIL

Both conditions contain the same raw tooth-sector samples and use the same hierarchy/model. Only globally meaningful within-revolution order is preserved or destroyed.