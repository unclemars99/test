# E000-B Results — Feature-level shared-representation baseline

Rows: 945; numeric process features: 48.

Outer split: leave-one-cutter-out. All transforms and wear probes are fit on training cutters only.

## Aggregate results

| representation   |   wear_mae_mean |   wear_mae_std |   wear_nmae_range_mean |   wear_nmae_range_std |   wear_r2_mean |   wear_r2_std |   d_state_cosine_mean |   d_state_cosine_std |   d_domain_cosine_mean |   d_domain_cosine_std |   sharedness_ratio_mean |   sharedness_ratio_std |   trajectory_cosine_mean_mean |   trajectory_cosine_mean_std |   domain_silhouette_cosine_mean |   domain_silhouette_cosine_std |   n_components_mean |   n_components_std |
|:-----------------|----------------:|---------------:|-----------------------:|----------------------:|---------------:|--------------:|----------------------:|---------------------:|-----------------------:|----------------------:|------------------------:|-----------------------:|------------------------------:|-----------------------------:|--------------------------------:|-------------------------------:|--------------------:|-------------------:|
| pca95            |         22.9298 |       14.3524  |               0.134646 |             0.0692171 |      0.179106  |      0.748455 |              1.65939  |           0.00353026 |             0.562089   |           0.0121967   |                 2.95368 |               0.06895  |                      0.860224 |                    0.0271334 |                       0.118569  |                     0.00645999 |             10.3333 |           0.471405 |
| raw              |         23.1012 |        6.17892 |               0.143615 |             0.0362579 |      0.101903  |      0.438894 |              0.147096 |           0          |             0.00357084 |           4.33681e-19 |                41.1936  |               0        |                      0.991704 |                    0         |                      -0.0444559 |                     0          |             48      |           0        |
| standardized     |         23.1867 |        6.18154 |               0.144276 |             0.0368178 |      0.0826813 |      0.455597 |              1.61464  |           0.021741   |             0.59375    |           0.0167233   |                 2.72234 |               0.106765 |                      0.830298 |                    0.0135259 |                       0.141795  |                     0.0060554  |             48      |           0        |

## Interpretation guardrails

- This experiment tests H001 lower baselines, not H002 Process Token.
- Wear labels are used only for the simple probe and evaluation geometry.
- Lower cutter-domain silhouette is desirable only if state/task information is preserved.
- A larger sharedness ratio is useful only together with non-collapsed D_state.
- PHM2010 wear-label limitations mean these metrics are directional evidence, not final proof.