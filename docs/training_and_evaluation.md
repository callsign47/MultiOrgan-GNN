# ORGANIX: Training and Evaluation Protocol

## 1. Cross-Validation Protocol

- **5-Fold Cross-Validation**: Stratified patient-level partition ($N = 6,277$).
- **Disjoint Patient Assignment**: Every participant ($SEQN$) exists in exactly one validation fold.
- **Leakage-Free Preprocessing**: Imputation parameters and standardizers are fitted **strictly on the 4 training folds** and applied out-of-fold.

---

## 2. Evaluation Metrics

Model performance is evaluated across both individual cross-validation folds and pooled out-of-fold (OOF) predictions ($N=6,277$):

1. **Coefficient of Determination ($R^2$)**:
   $$R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}$$
2. **Root Mean Squared Error (RMSE)**:
   $$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2}$$
3. **Mean Absolute Error (MAE)**:
   $$\text{MAE} = \frac{1}{N} \sum_{i=1}^N |y_i - \hat{y}_i|$$
4. **Spearman's Rank Correlation ($\rho$)**: Non-parametric monotonic correlation across risk percentiles.

---

## 3. Statistical Testing & Multiple Testing Corrections

To assess whether performance gains are statistically significant:
- **Paired Patient-Level Bootstrapping**: $B = 2,000$ paired resamples comparing out-of-fold error distributions.
- **Hypothesis Testing**: Empirical two-sided $p$-values computed from bootstrap delta distributions.
- **Family-Wise Error Rate Control**: Step-down Holm-Bonferroni correction.
- **False Discovery Rate (FDR)**: Benjamini-Hochberg adjustment.
