# FIB-4 Target Formulation, Clinical Units, and Empirical Distribution

**Specification Source**: [`data/fib4_target_validation.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/data/fib4_target_validation.json)  
**Implementation Script**: [`src/target.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/target.py)  
**Target Variable Name**: `fib4_target`  
**Prediction Paradigm**: Continuous Regression on Raw Clinical Index Scale  
**Transformation Status**: **NONE (Raw Untransformed Target)**  
**Verification Status**: `VERIFIED-ON-DISK` (All 3 Hard Validation Gates Passed)  

---

## 1. Clinical Definition and Mathematical Formulation

The **Fibrosis-4 (FIB-4) Index** is a widely adopted non-invasive biomarker panel used in clinical hepatology to estimate liver scarring (fibrosis) in patients with metabolic dysfunction-associated steatotic liver disease (MASLD), nonalcoholic fatty liver disease (NAFLD), and viral hepatitis.

The index is mathematically computed as:

$$\text{FIB-4} = \frac{\text{Age} \times \text{AST}}{\text{Platelet Count} \times \sqrt{\text{ALT}}}$$

### Component Mapping and Clinical Units

| Mathematical Component | NHANES Variable Code | Source Table | Clinical Measurement | Survey Measurement Unit | Conventional Clinical Unit | Scale Factor Applied |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| $\text{Age}$ | `RIDAGEYR` | `DEMO_L.xpt` | Chronological Age | Years | Years | None ($1.0$) |
| $\text{AST}$ | `LBXSASSI` | `BIOPRO_L.xpt` | Aspartate Aminotransferase | U/L | U/L | None ($1.0$) |
| $\text{ALT}$ | `LBXSATSI` | `BIOPRO_L.xpt` | Alanine Aminotransferase | U/L | U/L | None ($1.0$) |
| $\text{Platelets}$ | `LBXPLTSI` | `CBC_L.xpt` | Blood Platelet Count | $10^9/\text{L}$ ($10^3/\mu\text{L}$) | $10^9/\text{L}$ | None ($1.0$) |

*Unit Verification Finding*: CDC NHANES measures platelet counts in $10^9/\text{L}$ (equivalent to $10^3/\mu\text{L}$ or $1,000\text{ platelets}/\mu\text{L}$), and transaminases in $\text{U/L}$. Therefore, the raw NHANES numeric values directly correspond to the standard clinical FIB-4 formula without requiring any scalar unit conversion factors.

---

## 2. Hard Validation Gates in Implementation

As implemented in [`src/target.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/target.py#L21-L44):

1. **Non-Positive Input Exclusion**:
   Participants with $\text{Age} \le 0$, $\text{AST} \le 0$, $\text{ALT} \le 0$, or $\text{Platelets} \le 0$ are filtered out during cohort flow ([`src/cohort.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/cohort.py#L26-L34)). This eliminates division-by-zero errors and negative square roots.
2. **Hard Gate 1 (NaN / Inf Check)**:
   The computed target vector is strictly audited:
   ```python
   nan_count = df_valid['fib4_target'].isna().sum()
   inf_count = np.isinf(df_valid['fib4_target']).sum()
   if nan_count > 0 or inf_count > 0:
       raise ValueError(f"HARD GATE FAIL: Target contains {nan_count} NaNs and {inf_count} Infs!")
   ```
   **Audit Result**: 0 NaNs, 0 Infs across all 6,277 patients.
3. **Hard Gate 2 (SEQN & Patient UID Uniqueness)**:
   Asserts that `df['SEQN'].nunique() == len(df)` and `df['patient_uid'].nunique() == len(df)`. Zero duplicate rows exist.
4. **Hard Gate 3 (Placeholder Quarantine Check)**:
   Scans all dataframe columns for unexpected synthetic or placeholder strings (e.g., `'BRAIN'`, `'GUT'`). None were detected.

---

## 3. Transformation and Scaling Audit

| Potential Transformation | Status in Baseline & Comparative Framework | Verification Source |
| :--- | :---: | :--- |
| **Natural Log ($\ln$) Transformation** | **NOT APPLIED** | [`src/target.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/target.py#L26), [`src/pipeline.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/pipeline.py) |
| **Winsorization / Clipping** | **NOT APPLIED** | Raw values preserved up to maximum $\text{FIB-4} = 13.9971$ |
| **Z-Score Target Standardization** | **NOT APPLIED** | Target remains in original clinical units for all models |
| **Target Quantile Binning / Discretization** | **NOT APPLIED** | Continuous regression strictly enforced across all experiments |

*Significance for Metrics*: Because no nonlinear monotonic transformation was applied to $y$, all reported $R^2$, MAE, and RMSE metrics across all models reflect performance directly on the raw clinical FIB-4 scale.

---

## 4. Empirical Target Distribution Statistics

The empirical distribution of continuous FIB-4 in the locked $N=6,277$ cohort:

| Distribution Metric | Exact Empirical Value | Interpretation |
| :--- | :---: | :--- |
| **Cohort Sample Size ($N$)** | **6,277** | Verified total patient count |
| **Arithmetic Mean ($\mu$)** | **1.058987** ($\approx 1.0590$) | Population mean |
| **Standard Deviation ($\sigma$)** | **0.774845** ($\approx 0.7748$) | Population spread |
| **Variance ($\sigma^2$)** | **0.600385** ($\approx 0.6004$) | Implied target variance ($SS_{\text{tot}} / N$) |
| **Median** | **0.902784** ($\approx 0.9028$) | 50th percentile (substantially below mean) |
| **Minimum** | **0.063433** | Lowest individual FIB-4 score |
| **Maximum** | **13.997084** | Highest individual FIB-4 score (severe fibrosis/cirrhosis) |
| **25th Percentile ($P_{25}$)** | **0.509125** | Lower quartile |
| **75th Percentile ($P_{75}$)** | **1.402287** | Upper quartile |
| **Interquartile Range (IQR)** | **0.893163** | $P_{75} - P_{25}$ |
| **Fisher-Pearson Skewness** | **+2.923571** | Markedly right-skewed positive tail |

*Reference*: [`data/fib4_target_validation.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/data/fib4_target_validation.json#L1-L20)

---

## 5. Clinical Risk Cutoffs and Cohort Composition

Standard clinical practice stratifies FIB-4 into 3 diagnostic risk tiers for advanced liver fibrosis ($\ge F3$ on Ishak/METAVIR staging):

```
       Low Risk (<1.30)           Indeterminate (1.30 - 2.67)       High Risk (>2.67)
[==============================|================================|========================]
         N = 4,447 (70.8%)              N = 1,622 (25.8%)             N = 208 (3.3%)
     Rule-out advanced fibrosis      Requires second-line testing   Rule-in advanced fibrosis
```

1. **Low Risk (< 1.30)**:
   - Clinical Action: Advanced fibrosis reliably ruled out (high negative predictive value); managed in primary care.
   - Cohort Frequency: $N = 4,447$ patients (**$70.8\%$** of cohort).
2. **Indeterminate Risk (1.30 – 2.67)**:
   - Clinical Action: Indeterminate zone; guidelines recommend second-line elastography (FibroScan) or serum biomarkers (ELF).
   - Cohort Frequency: $N = 1,622$ patients (**$25.8\%$** of cohort).
3. **High Risk (> 2.67)**:
   - Clinical Action: High probability of advanced fibrosis/cirrhosis; warrants hepatology referral and liver biopsy consideration.
   - Cohort Frequency: $N = 208$ patients (**$3.3\%$** of cohort).

---

## 6. The Range-Restriction Phenomenon in Continuous Evaluation

Because continuous FIB-4 is right-skewed and clinical risk tiers restrict the outcome range, evaluating $R^2$ within narrow subgroup slices (e.g. Low Risk $< 1.30$) drastically reduces the total sum of squares denominator ($SS_{\text{tot}} = \sum (y_i - \bar{y}_{\text{slice}})^2 \approx 0.05$). Consequently, residual mean squared errors that are small in absolute terms ($\text{RMSE} \approx 0.28$) still exceed the truncated slice variance, producing negative slice $R^2$ values despite high clinical classification concordance:

$$\text{Slice } R^2 = 1 - \frac{\text{MSE}}{\text{Var}(y_{\text{slice}})} < 0 \quad \text{when } \text{Var}(y_{\text{slice}}) \ll \text{Var}(y_{\text{global}})$$

This mathematical range-restriction phenomenon is fully analyzed and documented in Experiment 9 ([`results/comparative/exp9_subgroups/exp9_subgroups_summary.md`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/exp9_subgroups/exp9_subgroups_summary.md)).
