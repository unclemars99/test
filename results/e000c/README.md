# E000-C Results — Generic self-supervised baseline

Rows: 945; numeric process features: 48.

Protocol: 3-fold leave-one-cutter-out. Standardizer, PCA/DAE and wear probe are fit on training cutters only. DAE uses 5 seeds and reconstructs corrupted standardized features without wear/cutter labels.

## Aggregate comparison

| representation   |   wear_mae_mean |   wear_nmae_range_mean |   wear_r2_mean |   wear_r2_min_fold |   wear_r2_max_fold |   fold_r2_range |   sharedness_ratio_mean |   trajectory_cosine_mean |   domain_silhouette_cosine_mean |
|:-----------------|----------------:|-----------------------:|---------------:|-------------------:|-------------------:|----------------:|------------------------:|-------------------------:|--------------------------------:|
| dae12            |         22.0773 |               0.131802 |       0.230608 |          -0.604137 |           0.771014 |         1.37515 |                 8.3049  |                 0.830486 |                        0.103956 |
| pca95            |         22.7321 |               0.133512 |       0.194251 |          -0.834968 |           0.778705 |         1.61367 |                 8.14319 |                 0.87077  |                        0.118569 |

## Fold comparison

| representation   | heldout_cutter   |   wear_mae |   wear_nmae_range |   wear_r2 |   wear_r2_seed_std |   d_state_cosine |   d_domain_cosine |   sharedness_ratio |   trajectory_cosine_mean |   domain_silhouette_cosine |
|:-----------------|:-----------------|-----------:|------------------:|----------:|-------------------:|-----------------:|------------------:|-------------------:|-------------------------:|---------------------------:|
| dae12            | C1               |    14.4413 |         0.115043  |  0.524949 |          0.199963  |         0.686093 |         0.136058  |            5.13352 |                 0.836272 |                  0.117583  |
| dae12            | C4               |    13.2807 |         0.0742514 |  0.771014 |          0.0244554 |         0.68506  |         0.135063  |            5.25662 |                 0.827381 |                  0.117904  |
| dae12            | C6               |    38.5099 |         0.206111  | -0.604137 |          0.650168  |         0.688847 |         0.0492444 |           14.5246  |                 0.827806 |                  0.0763814 |
| pca95            | C1               |    12.3996 |         0.0987789 |  0.639016 |        nan         |         1.69698  |         0.273326  |            6.20864 |                 0.843279 |                  0.126497  |
| pca95            | C4               |    13.0837 |         0.0731495 |  0.778705 |        nan         |         1.70934  |         0.263374  |            6.49016 |                 0.858617 |                  0.110673  |
| pca95            | C6               |    42.7131 |         0.228608  | -0.834968 |        nan         |         1.71195  |         0.145937  |           11.7308  |                 0.910415 |                  0.118538  |

## Interpretation guardrails

- This is H001 evidence only; feature-level DAE does not test Process Token/H002.
- PHM2010 wear-label limitations make wear probes directional evidence, not final truth.
- Mean performance is insufficient: worst-fold performance and fold spread are primary robustness checks.
- Lower cutter-domain separation is useful only if wear/state information remains readable.
- If generic SSL fails to improve worst-domain transfer, this is evidence against assuming 'deep = shared'.