# HSGIN 3-Organ Patient-Level Dataset & Training Pipeline PRD

## 1. Objective

Build an automated, reproducible pipeline that converts NHANES August 2021–August 2023 XPT files into a clean patient-level heterogeneous graph dataset for:

> Liver–Kidney–Heart disease interaction modeling using HSGIN, as the experimentally validated subset of a broader 5-organ disease-linkage framework.

**Current experimental scope:** Liver + Kidney + Heart.

**Future research scope:** Brain + Gut.

Brain and Gut must not be represented as observed patient-level data in the current experiment.

---

## 2. Data Sources

Use `SEQN` as the patient-level join key.

### Demographics
- `DEMO_L`

### Laboratory
- `BIOPRO_L`
- `CBC_L`
- `ALB_CR_L`
- `HDL_L`
- `TRIGLY_L`
- `TCHOL_L`
- `HSCRP_L`
- `GLU_L`
- `INS_L`
- `GHB_L`
- `HEPA_L`
- `HEPB_S_L`
- `HEPBD_L`
- `HEPC_L`
- `HEPE_L`

### Examination
- `BMX_L`
- `BPXO_L`
- `LUX_L`

### Questionnaire
- `BPQ_L`
- `KIQ_U_L`
- `MCQ_L`
- `DIQ_L`
- `HEQ_L`
- `FNQ_L`
- `DPQ_L`
- `SLQ_L`
- `DBQ_L`

Only retain variables that are biologically defensible and actually available in the selected NHANES cycle.

---

## 3. Pipeline Architecture

```text
Raw NHANES XPT
      |
      v
Schema validation
      |
      v
SEQN-based joining
      |
      v
Patient-level master table
      |
      v
Feature extraction
      |
      v
Missingness audit
      |
      v
Cohort selection
      |
      v
Target construction
      |
      v
Train/test-safe preprocessing
      |
      v
3-organ HeteroData graphs
      |
      +----------------+
      |                |
      v                v
    HSGIN           Baselines
      |                |
      +-------+--------+
              v
       Cross-validation
              |
              v
       Metrics + ablations
              |
              v
       Reproducible results
```

---

## 4. Patient Identity

Every source must contain `SEQN`.

All joins must use `SEQN`.

Requirements:

- No row-number joins.
- No filename-based identity.
- No arbitrary IDs before merging.
- Verify one patient corresponds to one `SEQN` in the final patient table.
- Create `patient_uid = P_000001...` only after the final cohort is established.

---

## 5. Organ Feature Specification

### 5.1 Liver

Prioritize:

- ALT
- AST
- GGT
- Albumin
- Total bilirubin
- ALP
- Liver stiffness
- CAP

Use `LUX_L` where valid for liver stiffness/CAP.

### 5.2 Kidney

Prioritize:

- Serum creatinine
- BUN
- Uric acid
- Urine albumin
- Urine creatinine
- Albumin/creatinine ratio

Add relevant kidney-condition variables from `KIQ_U_L`.

Do not treat an abnormal biomarker as a diagnosis.

### 5.3 Heart / Cardiovascular

Prioritize:

- Systolic BP
- Diastolic BP
- Pulse
- HDL
- LDL
- Total cholesterol
- Triglycerides

Add relevant cardiovascular/BP questionnaire variables where appropriate.

---

## 6. Systemic Biomarkers

Create a separate biomarker group rather than forcing every variable into an organ.

Candidate features:

- WBC
- RBC
- Hemoglobin
- Platelets
- Glucose
- HbA1c
- Insulin
- hs-CRP

Distinguish organ-specific features from systemic biomarkers.

---

## 7. Target

### Primary target: True FIB-4

Do **not** use the previous proxy:

```text
(Age × AST) / (sqrt(ALT) × 15)
```

Use the standard formulation with actual platelet count:

```text
FIB-4 = (Age × AST) / (Platelets × sqrt(ALT))
```

Before training:

- inspect target distribution
- report mean, median, standard deviation
- detect NaN/Inf
- inspect extreme values
- verify units for age, AST, ALT and platelets
- document unit conversions

Do not apply clinical stage thresholds to a non-standard proxy.

---

## 8. Leakage Prevention

All preprocessing must be fitted inside each training fold.

This includes:

- StandardScaler
- imputation
- feature selection
- any target-derived transformation

Correct structure:

```text
Fold
 ├── Training patients
 │      |
 │   fit preprocessing
 │
 └── Validation patients
        |
    transform only
```

No validation/test information may influence preprocessing.

---

## 9. Missingness Audit

Before deleting patients, generate:

### Feature-level report

| Field | Required |
|---|---|
| feature | yes |
| organ | yes |
| source_file | yes |
| n_total | yes |
| n_available | yes |
| n_missing | yes |
| missing_percent | yes |

### Patient-level report

Track:

- `SEQN`
- liver completeness
- kidney completeness
- heart completeness
- target availability

### Cohort flow

```text
Initial participants
      ↓
Demographic availability
      ↓
Liver feature availability
      ↓
Kidney feature availability
      ↓
Heart feature availability
      ↓
Target availability
      ↓
FINAL COHORT
```

Do not assume the final cohort size before calculating feature-level missingness.

---

## 10. Missing Data Strategy

Do not blindly median-impute everything.

Rules:

- Low/moderate missingness: median imputation may be used inside training folds.
- High missingness: consider removing the feature.
- Subsample variables: report eligible N before inclusion.
- If essential organ features are unavailable, explicitly track organ completeness.

---

## 11. Graph Construction

Create one heterogeneous graph per patient.

### Node types

```text
patient
liver
kidney
heart
biomarker
```

Do not create Brain/Gut nodes with fake or zero-vector patient features.

### Conceptual graph

```text
                 Patient
              /     |     \
             /      |      \
         Liver    Kidney   Heart
           |        |        |
        markers   markers   markers
```

---

## 12. Edge Schema

Required relationships:

```text
patient → liver
patient → kidney
patient → heart

liver ↔ kidney
liver ↔ heart
kidney ↔ heart
```

Use reverse edges where required by the PyTorch Geometric HGT implementation.

Do not claim that every edge is a quantitatively validated biological interaction. At this stage, edges represent the modeled interaction topology.

---

## 13. HSGIN Architecture

Initial configuration:

```text
Node-specific input projections
          ↓
      HGTConv
          ↓
        ReLU
          ↓
      HGTConv
          ↓
      Organ-aware readout
          ↓
       MLP head
          ↓
       FIB-4 prediction
```

Recommended initial hyperparameters:

```text
hidden_dim = 64
layers = 2
heads = 4
dropout = 0.4
optimizer = AdamW
learning_rate = 1e-3
weight_decay = 1e-3
loss = HuberLoss
```

---

## 14. Readout — Mandatory

The prediction head must incorporate all validated organ representations.

Preferred structure:

```text
organ_pool = mean(
    liver_embedding,
    kidney_embedding,
    heart_embedding
)

representation = concat(
    patient_embedding,
    organ_pool,
    biomarker_pool
)
```

Then:

```text
Linear → ReLU → Dropout → Linear → FIB-4
```

Do not use a patient+liver-only readout.

---

## 15. Baselines

Compare HSGIN against:

1. XGBoost
2. GCN
3. GAT
4. GraphSAGE
5. Classical HGNN

Use the same patient-level folds where possible.

Avoid treating near-identical GraphConv variants as independent scientific baselines.

---

## 16. Cross-Validation

Primary evaluation:

```text
K-fold patient-level CV
shuffle = True
random_state = 42
```

Start with 5-fold CV.

If computationally feasible, use 10-fold CV for stronger statistical testing.

No patient may appear in both training and validation within a fold.

---

## 17. Reproducibility

Set global seeds:

```python
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
```

When CUDA is used, configure deterministic behavior appropriately.

Save:

```text
config.json
feature_manifest.json
cohort_manifest.csv
scalers/
model_checkpoints/
fold_predictions.csv
metrics.json
```

---

## 18. Evaluation

For regression report:

- MAE
- RMSE
- R²

Report:

```text
mean ± standard deviation
```

across folds.

Save all fold-level predictions.

---

## 19. Critical Ablation

Run:

```text
A: Liver only
B: Liver + Kidney
C: Liver + Heart
D: Liver + Kidney + Heart
```

Compare:

| Configuration | MAE | RMSE | R² |
|---|---:|---:|---:|
| Liver | | | |
| Liver + Kidney | | | |
| Liver + Heart | | | |
| Liver + Kidney + Heart | | | |

Primary scientific question:

> Does incorporating multiple organ representations improve patient-level prediction compared with liver-only modeling?

Only claim improvement if the experiment actually demonstrates it.

---

## 20. Y-Randomization

Shuffle the target while preserving the graph/features.

```text
Original Y
   ↓
Shuffle Y
   ↓
Retrain
   ↓
Evaluate
```

Expected result:

```text
Original target → meaningful performance
Randomized target → substantially degraded performance
```

Use the same evaluation protocol as the primary experiment where computationally feasible.

Y-randomization is a sanity check, not proof of biological validity.

---

## 21. Organ Contribution / Explainability

Extract model representation weighting or attention where technically valid.

Example:

```json
{
  "patient_uid": "P_000001",
  "prediction": 1.82,
  "organ_attention": {
    "liver": 0.XX,
    "kidney": 0.XX,
    "heart": 0.XX
  }
}
```

Do not describe attention weights as causal biological importance.

Use terminology such as:

> model attention / representation weighting

---

## 22. Research Scope

### Current validated scope

**Liver–Kidney–Heart patient-level modeling**

### Research framework

**Five-organ systemic disease-linkage framework**

### Future extension

```text
Current:
Liver + Kidney + Heart

Future:
Liver + Kidney + Heart + Gut + Brain
```

Brain and Gut must not be presented as having patient-level measurements in the current experiment.

---

## 23. Required Outputs

```text
/data/
    master_patient.csv
    final_cohort.csv
    feature_manifest.json
    missingness_report.csv
    cohort_flow.csv

/graphs/
    patient_graphs.pt

/models/
    hsgin_fold_01.pt
    ...

/results/
    fold_metrics.csv
    aggregate_metrics.csv
    predictions.csv
    ablation_results.csv
    y_randomization.csv

/reports/
    dataset_report.md
    experiment_report.md
```

---

## 24. Hard Validation Gates

Stop the pipeline if:

- duplicate `SEQN` exists in the final patient table
- target contains NaN/Inf
- target is accidentally BMI
- non-standard FIB-4 proxy is detected
- Brain/Gut placeholder nodes appear in the 3-organ experiment
- scaler was fitted before CV splitting
- train/validation patient overlap exists
- validation/test information enters feature preprocessing
- fewer than the configured minimum number of patients remain
- organ features exceed configured missingness thresholds

---

## 25. Scientific Claim Boundary

The pipeline must not claim:

> “HSGIN proves five-organ disease interaction.”

A defensible claim is:

> “We developed a heterogeneous graph framework targeting five-organ systemic disease linkage and performed initial patient-level validation using liver, kidney, and cardiovascular features from NHANES.”

If the ablation supports it, an additional claim may be:

> “Incorporating multi-organ representations improved predictive performance relative to liver-only modeling.”

---

## 26. Execution Order

```text
1. Load XPT files
        ↓
2. Verify SEQN uniqueness
        ↓
3. Join datasets
        ↓
4. Extract Liver/Kidney/Heart features
        ↓
5. Calculate missingness
        ↓
6. Lock final cohort
        ↓
7. Verify platelets + calculate TRUE FIB-4
        ↓
8. Build fold-safe preprocessing
        ↓
9. Build 3-organ HeteroData
        ↓
10. Fix HSGIN readout
        ↓
11. Train liver-only baseline
        ↓
12. Train 3-organ HSGIN
        ↓
13. Run organ ablations
        ↓
14. Run baseline models
        ↓
15. Run Y-randomization
        ↓
16. Generate final metrics
        ↓
17. Generate poster-ready tables/figures
```

**Training must not begin until Steps 1–7 pass.**

The most important pre-training artifacts are:

1. Final cohort
2. Feature manifest
3. Missingness report
4. True FIB-4 validation report
5. Cohort flow
