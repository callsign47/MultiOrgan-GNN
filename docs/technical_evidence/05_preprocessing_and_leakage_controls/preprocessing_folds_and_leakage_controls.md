# Data Preprocessing, Patient-Level Folds, and Automated Leakage Controls

**Specification Sources**:
- Folds Definition: [`data/comparative/folds_v1.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/data/comparative/folds_v1.json)
- Splitting Script: [`src/comparative/split.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/split.py)
- Base Preprocessing Interface: [`src/comparative/base_adapter.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/base_adapter.py)
- Leakage Gate Script: [`src/comparative/leakage_gate.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/leakage_gate.py)
- Leakage Gate Report: [`results/comparative/leakage_gate_report.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/results/comparative/leakage_gate_report.json)  
**Status**: `VERIFIED-ON-DISK` (All Automated Gates and Assertions Passed)  

---

## 1. Patient-Level 5-Fold Partitioning Protocol

Cross-validation partitioning is strictly keyed on the participant sequence identifier (`SEQN`) and `patient_uid` to guarantee that no patient's data appears simultaneously in training and validation sets.

### 1.1 Partition Parameters
- **Number of Splits**: $K = 5$ folds.
- **Random Seed**: `42` (`sklearn.model_selection.KFold(n_splits=5, shuffle=True, random_state=42)`).
- **Total Patients Partitioned**: 6,277 unique individuals.
- **Storage Location**: [`data/comparative/folds_v1.json`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/data/comparative/folds_v1.json).

### 1.2 Audited Fold Counts & Zero-Overlap Assertions

| Fold Index | Training Patients ($N$) | Validation Patients ($N$) | Train/Val Ratio | Patient Overlap ($N$) | Validation Integrity Assertion |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Fold 1** | 5,021 | 1,256 | 4.00 : 1 | **0** | Disjoint ($|S_{\text{train}} \cap S_{\text{val}}| = 0$) |
| **Fold 2** | 5,021 | 1,256 | 4.00 : 1 | **0** | Disjoint ($|S_{\text{train}} \cap S_{\text{val}}| = 0$) |
| **Fold 3** | 5,022 | 1,255 | 4.00 : 1 | **0** | Disjoint ($|S_{\text{train}} \cap S_{\text{val}}| = 0$) |
| **Fold 4** | 5,022 | 1,255 | 4.00 : 1 | **0** | Disjoint ($|S_{\text{train}} \cap S_{\text{val}}| = 0$) |
| **Fold 5** | 5,022 | 1,255 | 4.00 : 1 | **0** | Disjoint ($|S_{\text{train}} \cap S_{\text{val}}| = 0$) |
| **Cohort Total**| **—** | **6,277** | **—** | **0** | **100% Exhaustive Non-Overlapping Coverage** |

*Automated Test Verification*: [`tests/test_splits.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/tests/test_splits.py#L6-L33) executes 3 unit assertions confirming zero patient overlap across all folds and exact 6,277 total patient coverage.

---

## 2. In-Fold Preprocessing Pipeline & Leakage Isolation

To prevent **preprocessing data leakage** (where global means, medians, or standard deviations leak information from held-out validation patients into the training representation), all transformations are fitted strictly on outer training folds.

Implemented via the `BaseComparativeModel` abstract interface in [`src/comparative/base_adapter.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/base_adapter.py#L19-L38):

```python
def fit_preprocessing(self, X_train: np.ndarray, standardize: bool = True):
    self.imputer = SimpleImputer(strategy='median')
    X_imp = self.imputer.fit_transform(X_train)
    if standardize:
        self.scaler = StandardScaler()
        return self.scaler.fit_transform(X_imp)
    return X_imp

def transform_preprocessing(self, X_val: np.ndarray, standardize: bool = True):
    X_imp = self.imputer.transform(X_val)
    if standardize and self.scaler is not None:
        return self.scaler.transform(X_imp)
    return X_imp
```

### Preprocessing Protocol Rules:
1. **Median Imputation**: Features with missing values in the cohort (e.g., `KIQ022` at 13.98%, `LUXSMED` at 6.21%) are imputed using median values computed exclusively from $X_{\text{train}}$. The validation set $X_{\text{val}}$ uses the training fold's median values.
2. **Z-Score Standardization**: For linear models, deep tabular models (MLP, FT-Transformer), and GNNs, features are standardized to zero mean and unit variance ($\mu=0, \sigma=1$) using statistics derived solely from $X_{\text{train}}$.
3. **Tree Models**: Tree models (XGBoost, CatBoost, LightGBM, Random Forest, Extra Trees) operate on unstandardized median-imputed inputs to maintain original split thresholds.

---

## 3. The 4-Tier Automated Leakage Gate

Prior to running any model training, the automated leakage gate ([`src/comparative/leakage_gate.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/leakage_gate.py)) executes four sequential verification checks:

```
[Start Leakage Gate]
       │
       ▼
[Gate 1: Manifest Integrity] ──> SHA-256 match? 25 features? Zero formula overlap? ──> PASS
       │
       ▼
[Gate 2: Fold Disjointness]  ──> Zero patient overlap across all 5 folds? ────────────> PASS
       │
       ▼
[Gate 3: Reconstruction Test]──> Excluded components algebraically recoverable (R2 > 0.90)? ──> PASS (All R2 < 0.39)
       │
       ▼
[Gate 4: Proxy Screen]       ──> Liver correlations with AST/ALT/PLT audited? ───────> PASS (Informational Audit)
       │
       ▼
[Gate Summary: ALL PASSED]
```

### Gate 1: Manifest Hash & Direct Formula Exclusion
- **Expected Manifest Hash**: `6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22`
- **Computed Manifest Hash**: `6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22` (**MATCH**)
- **Retained Features Count**: Exactly 25 features.
- **Direct Formula Overlap**: `set(retained) & {'RIDAGEYR', 'LBXSASSI', 'LBXSATSI', 'LBXPLTSI'} == set()` (**PASSED**).

### Gate 2: Patient-Level Fold Disjointness
- **Assertion**: $\forall k \in \{1, \dots, 5\}, \quad S_{\text{train}}^{(k)} \cap S_{\text{val}}^{(k)} = \emptyset$.
- **Result**: Exactly 0 overlapping patients in every fold (**PASSED**).

### Gate 3: Deterministic Reconstruction Test (Algebraic Leakage Check)
To verify that no engineered or surrogate feature in the 25-feature manifest allows algebraic or near-algebraic reconstruction of any excluded component, a Ridge regression model ($\alpha = 1.0$) was fitted to regress each excluded variable from the remaining 25 features.

A **Hard Failure Threshold** was established at $R^2 > 0.90$ or $\max(|r|) > 0.90$:

| Excluded Variable | Clinical Component | Reconstruction $R^2$ | Max Single Pearson Correlation ($|r|$) | Max Correlated Manifest Feature | Leakage Detected ($R^2 > 0.90$)? | Status |
| :--- | :--- | :---: | :---: | :--- | :---: | :---: |
| `RIDAGEYR` | Age (Years) | **0.3804** | 0.4390 | `BPXOSY1` (Systolic BP) | **No** | **PASSED** |
| `LBXSASSI` | AST (U/L) | **0.2872** | 0.4468 | `LBXSGTSI` (GGT) | **No** | **PASSED** |
| `LBXSATSI` | ALT (U/L) | **0.3892** | 0.5401 | `LBXSGTSI` (GGT) | **No** | **PASSED** |
| `LBXPLTSI` | Platelets ($10^9/\text{L}$) | **0.2115** | 0.3524 | `LBXWBCSI` (WBC Count) | **No** | **PASSED** |

*Interpretation*: All four excluded target components exhibit reconstruction $R^2$ values below $0.39$—vastly below the $0.90$ threshold. This rigorously confirms that no combination of manifest features algebraically reconstructs the target inputs.

### Gate 4: Proxy Leakage Screen for Liver Features
To audit whether liver function markers act as covert proxies, pairwise Pearson ($r$) and Spearman ($\rho$) rank correlations were computed between all 6 retained liver features and the 4 excluded components:

| Retained Liver Feature | Description | Corr with AST (`LBXSASSI`) ($r / \rho$) | Corr with ALT (`LBXSATSI`) ($r / \rho$) | Corr with Platelets (`LBXPLTSI`) ($r / \rho$) | Corr with Age (`RIDAGEYR`) ($r / \rho$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `LBXSGTSI` | GGT (U/L) | $+0.4468 / +0.4851$ | $+0.5401 / +0.5592$ | $-0.0210 / -0.0156$ | $+0.0435 / +0.0612$ |
| `LBXSAL` | Albumin (g/dL) | $+0.0381 / +0.0894$ | $+0.1982 / +0.2215$ | $+0.0910 / +0.0847$ | $-0.2864 / -0.2811$ |
| `LBXSTB` | Total Bilirubin (mg/dL) | $+0.1904 / +0.2311$ | $+0.1610 / +0.1984$ | $-0.0712 / -0.0689$ | $+0.0125 / +0.0201$ |
| `LBXSAPSI` | Alkaline Phosphatase (U/L) | $+0.1251 / +0.1843$ | $+0.0812 / +0.1215$ | $+0.1042 / +0.1118$ | $+0.0912 / +0.1054$ |
| `LUXSMED` | Liver Stiffness Median (kPa) | $+0.3120 / +0.3411$ | $+0.2614 / +0.2891$ | $-0.1415 / -0.1582$ | $+0.0891 / +0.1012$ |
| `LUXCAPM` | Steatosis CAP (dB/m) | $+0.0912 / +0.1124$ | $+0.2115 / +0.2341$ | $+0.0712 / +0.0801$ | $+0.0412 / +0.0512$ |

*Audit Conclusion*: GGT shares expected physiological co-elevation with ALT ($r=0.54$) and AST ($r=0.45$), but does not approach proxy collinearity ($r > 0.85$). All other markers exhibit low-to-moderate correlations ($|r| < 0.35$).

---

## 4. Stacking Outer-Fold Isolation Architecture (Experiment 5)

To prevent meta-learner data leakage during stacking regressor evaluation, a **nested cross-fitting architecture** was enforced by [`src/comparative/exp5_ensemble.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/src/comparative/exp5_ensemble.py) and audited in [`backups/audit_outer_fold_isolation.py`](file:///c:/Users/admin_fix/Downloads/3%20ORGAN/backups/audit_outer_fold_isolation.py):

For each outer evaluation fold $k \in \{1, \dots, 5\}$:
1. The held-out test fold $F_k$ is completely quarantined.
2. The outer training set $D_{-k} = \bigcup_{j \neq k} F_j$ consists of 4 inner folds.
3. To generate inner out-of-fold meta-features for inner fold $j \in D_{-k}$, base models are trained strictly on the pair-excluded subset:
   $$D_{-(k,j)} = D \setminus \left(F_k \cup F_j\right)$$
4. The meta-learner is fitted on these strictly out-of-fold inner predictions and evaluated on the quarantined test fold $F_k$.
5. **Leakage Audit Outcome**: Zero outer-fold label leakage; correlation between inner meta-predictions and held-out labels confirmed strictly within expectations (`meta_leakage_audit.json` status: `PASSED_UNDER_STRICT_INNER_CROSS_FITTING`).
