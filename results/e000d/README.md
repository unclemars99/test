# E000-D Results — Invariance-oriented generic SSL

VICReg-lite on engineered/statistical PHM2010-derived features; 5 seeds per LOCO fold.

## Aggregate comparison

| representation   |   wear_mae_mean |   wear_nmae_range_mean |   wear_r2_mean |   wear_r2_min_fold |   wear_r2_max_fold |   fold_r2_range |   sharedness_ratio_mean |   trajectory_cosine_mean |   domain_silhouette_cosine_mean |
|:-----------------|----------------:|-----------------------:|---------------:|-------------------:|-------------------:|----------------:|------------------------:|-------------------------:|--------------------------------:|
| pca95            |         22.7321 |               0.133512 |       0.194251 |          -0.834968 |           0.778705 |        1.61367  |                 8.14319 |                 0.87077  |                        0.118569 |
| vicreg12         |         16.9072 |               0.102864 |       0.584849 |           0.415938 |           0.732452 |        0.316514 |                68.4492  |                 0.628222 |                        0.066907 |

## Fold comparison

| representation   | heldout_cutter   |   wear_mae |   wear_nmae_range |   wear_r2 |   wear_r2_seed_std |   sharedness_ratio |   trajectory_cosine_mean |   domain_silhouette_cosine |
|:-----------------|:-----------------|-----------:|------------------:|----------:|-------------------:|-------------------:|-------------------------:|---------------------------:|
| pca95            | C1               |    12.3996 |         0.0987789 |  0.639016 |        nan         |            6.20864 |                 0.843279 |                 0.126497   |
| pca95            | C4               |    13.0837 |         0.0731495 |  0.778705 |        nan         |            6.49016 |                 0.858617 |                 0.110673   |
| pca95            | C6               |    42.7131 |         0.228608  | -0.834968 |        nan         |           11.7308  |                 0.910415 |                 0.118538   |
| vicreg12         | C1               |    12.9064 |         0.102816  |  0.606158 |          0.0733125 |            2.63042 |                 0.549941 |                 0.107797   |
| vicreg12         | C4               |    14.173  |         0.0792398 |  0.732452 |          0.031361  |            2.59169 |                 0.538594 |                 0.10194    |
| vicreg12         | C6               |    23.6422 |         0.126537  |  0.415938 |          0.20616   |          200.125   |                 0.796131 |                -0.00901623 |

## Guardrails

- This tests H001 only, not Process Token/H002.
- Worst-fold performance and seed stability matter more than mean gain alone.
- Feature augmentations are generic, not physically justified; success would establish a stronger generic SSL baseline, not a physical-token claim.