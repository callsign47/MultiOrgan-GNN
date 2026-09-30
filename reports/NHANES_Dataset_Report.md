# Complete NHANES Dataset Acquisition, Integration & Construction Report
## HSGIN 3-Organ Disease Modeling Pipeline

**Project**: Heterogeneous Systemic Graph Interaction Network (HSGIN)  
**Cohort**: NHANES August 2021–August 2023 | **N = 6,277 Patients**  
**Target Variable**: Continuous FIB-4 Score (Liver Fibrosis Index)  
**Report Basis**: Project source files — `dataset_report.md`, `FINAL_MASTER_HANDOVER.md`, `leakage_audit_report.md`, `feature_manifest.json`, `cohort_flow.csv`, `missingness_report.csv`, `fib4_target_validation.json`, `ingestion_summary.csv`

> [!NOTE]
> This report is written so that **a complete beginner who has never used NHANES before** can reproduce the dataset end-to-end. All variable names, file names, row counts, formulas, and statistics are drawn **directly from project source files**. Anything not confirmed from project files is explicitly labelled **"Not documented / requires verification."**

---

## Section 1 — What Is NHANES?

### 1.1 Overview

**NHANES** stands for the **National Health and Nutrition Examination Survey**. It is a large-scale public health survey conducted in the United States that collects health, nutrition, and laboratory data from thousands of Americans every year.

Think of it as a giant health checkup program where trained medical professionals:
- Interview participants about their health history, diet, and lifestyle.
- Conduct physical examinations (blood pressure, body measurements, liver scans).
- Collect blood and urine samples for laboratory analysis.

All the collected data is **made freely available to the public** on the internet.

### 1.2 Who Maintains NHANES?

NHANES is maintained by the **Centers for Disease Control and Prevention (CDC)**, specifically by the **National Center for Health Statistics (NCHS)**. It is a US government program.

**Official Website**: `https://www.cdc.gov/nchs/nhanes/`

### 1.3 What Is the "August 2021–August 2023" Cycle?

NHANES historically ran in **2-year cycles** (e.g., 2017–2018, 2019–2020). The **August 2021–August 2023** cycle is a **new format** cycle introduced after a COVID-19 pandemic pause. This specific cycle is notable because it:

- Included **FibroScan liver elastography** (ultrasound-based liver stiffness measurement via the `LUX_L` file) — a clinically important addition not present in all earlier cycles.
- Covered a representative sample of the US population collected between August 2021 and August 2023.
- Was the cycle chosen for this HSGIN project precisely because it contained the liver imaging data (`LUXSMED`, `LUXCAPM`) needed alongside the biochemistry and cardiovascular variables.

**Why this matters**: Not every NHANES cycle has every type of measurement. This project **specifically requires** this cycle because it is one of the few to include FibroScan data.

### 1.4 How Is NHANES Data Organized?

NHANES organizes data into **components** (broad categories), and within each component there are **individual data files**:

| Component Name | What It Contains | Examples in This Project |
|:---|:---|:---|
| **Demographics (DEMO G)** | Age, gender, race, income, education | `DEMO_L` |
| **Laboratory** | Blood tests, urine tests, biochemistry results | `BIOPRO_L`, `CBC_L`, `HDL_L`, `TCHOL_L`, etc. |
| **Examination** | Physical exams done by a clinician | `BPXO_L` (blood pressure), `LUX_L` (liver scan) |
| **Questionnaire** | Self-reported health history answers | `BPQ_L`, `KIQ_U_L`, `MCQ_L` |

Each component has multiple individual data files. Every file is released as a separate download.

### 1.5 File Format: What Is an `.XPT` File?

NHANES data files are distributed in **SAS Transport Format**, with the file extension `.XPT`. This is a standard data interchange format.

**How to open `.XPT` files**:
- In Python: use the `pyreadstat` or `pandas.read_sas()` function.
- In R: use the `haven` package (`read_xpt()`).
- In SAS: natively supported.

For a Python beginner, the simplest approach is:
```python
import pandas as pd
df = pd.read_sas("BIOPRO_L.xpt", format="xport", encoding="utf-8")
```

### 1.6 What Is SEQN? Why Is It Critical?

**`SEQN`** stands for **Respondent Sequence Number**. It is the **unique numeric identifier assigned to each NHANES participant**. Every single NHANES data file — regardless of component or topic — contains the `SEQN` column.

**Why SEQN is critical**:
- A single participant's data is **split across many files** (their blood test is in `BIOPRO_L`, their blood pressure is in `BPXO_L`, their questionnaire answers are in `MCQ_L`, etc.).
- To combine all information about one person into a single row, you **join all files using SEQN**.
- It is a one-to-one mapping: each SEQN appears **exactly once per file**.

> [!IMPORTANT]
> Every data file in this project was verified to have **unique SEQN** (confirmed via `ingestion_summary.csv`: all 27 files show `is_seqn_unique = True`). This means a simple left-merge on SEQN is safe with no duplicate patient rows.

---

## Section 2 — Exact Data Acquisition: Step-by-Step Beginner Tutorial

This section walks through finding and downloading the correct NHANES files from scratch.

### Step 1 — Find the NHANES Website

1. Open a web browser.
2. Go to: **`https://www.cdc.gov/nchs/nhanes/`**
3. This is the official NHANES homepage maintained by the CDC/NCHS.

### Step 2 — Navigate to the Data Page

On the NHANES homepage:
1. Look for the menu item or link labeled **"Data, Documentation, Codebooks, SAS Code"** or simply **"Data Files"**.
2. The direct URL is: **`https://wwwn.cdc.gov/nchs/nhanes/default.aspx`**
3. This page lists all available NHANES data cycles.

### Step 3 — Locate the August 2021–August 2023 Cycle

On the Data Files page:
1. Look for the section labeled **"NHANES August 2021-August 2023"** (sometimes shown as "2021-2023").
2. The suffix used for this cycle's files is **`_L`** (e.g., `DEMO_L`, `BIOPRO_L`). This suffix distinguishes this cycle from older ones (which used `_J`, `_I`, `_H`, etc.).

> [!NOTE]
> The `_L` suffix is the cycle identifier. All files used in this project end in `_L`.

### Step 4 — Navigate to Each Component Tab

Within the August 2021–August 2023 section, NHANES organizes files under tabs:
- **Demographics**
- **Dietary**
- **Examination**
- **Laboratory**
- **Questionnaire**

You must download files from multiple tabs.

### Step 5 — Download the Required XPT Files

For each required file below, click its name on the NHANES website to download the `.XPT` file.

**From Demographics Tab:**
| File to Download | Why Needed |
|:---|:---|
| `DEMO_L.XPT` | Age, Gender — two variables required for FIB-4 target construction and cohort filtering |

**From Laboratory Tab:**
| File to Download | Why Needed |
|:---|:---|
| `BIOPRO_L.XPT` | Comprehensive biochemistry — AST, ALT (FIB-4 inputs), GGT, Albumin, Bilirubin, ALP, Creatinine, BUN, Uric Acid |
| `CBC_L.XPT` | Complete blood count — Platelets (FIB-4 input), WBC, RBC, Hemoglobin |
| `ALB_CR_L.XPT` | Urine albumin and creatinine — kidney filtration markers |
| `HDL_L.XPT` | HDL cholesterol — cardiovascular health marker |
| `TCHOL_L.XPT` | Total cholesterol — cardiovascular health marker |
| `HSCRP_L.XPT` | High-sensitivity C-Reactive Protein — systemic inflammation marker |

**From Examination Tab:**
| File to Download | Why Needed |
|:---|:---|
| `BPXO_L.XPT` | Oscillometric blood pressure — systolic BP, diastolic BP, pulse rate |
| `LUX_L.XPT` | Liver ultrasound elastography — FibroScan stiffness (kPa) and CAP attenuation |

**From Questionnaire Tab:**
| File to Download | Why Needed |
|:---|:---|
| `BPQ_L.XPT` | Blood pressure questionnaire — self-reported hypertension history |
| `KIQ_U_L.XPT` | Kidney conditions questionnaire — self-reported kidney disease history |
| `MCQ_L.XPT` | Medical conditions questionnaire — self-reported coronary heart disease and heart attack history |

### Step 6 — Organize Your Downloaded Files

After downloading, organize files into a folder structure matching the NHANES component hierarchy. This project used:

```
NHANES AUG'21 - AUG'23/
├── DEMO G/
│   └── DEMO_L.xpt
├── LABORATORY/
│   ├── ALB_CR_L.xpt
│   ├── BIOPRO_L.xpt
│   ├── CBC_L.xpt
│   ├── HDL_L.xpt
│   ├── HSCRP_L.xpt
│   └── TCHOL_L.xpt
├── EXAMINATION/
│   ├── BPXO_L.xpt
│   └── LUX_L.xpt
└── QUESTIONNAIRE/
    ├── BPQ_L.xpt
    ├── KIQ_U_L.xpt
    └── MCQ_L.xpt
```

> [!NOTE]
> The project's raw download folder also contains additional files (`BMX_L`, `TRIGLY_L`, `GHB_L`, `GLU_L`, `INS_L`, `HEPA_L`, `HEPBD_L`, `HEPC_L`, `HEPE_L`, `DIQ_L`, `DPQ_L`, `FNQ_L`, `HEQ_L`, `SLQ_L`, `DBQ_L`) that were ingested during the exploratory missingness audit but whose variables were **not retained** in the final 25-feature model manifest. These files are listed in `ingestion_summary.csv`. **You only need to download the 12 files listed in Steps 5 above** to reproduce the final model. The others were audited for completeness but their variables did not meet the selection criteria (not documented which specific criteria eliminated them vs. simply not being needed for the target organ systems).

---

## Section 3 — Complete Source File Inventory

The following table covers every NHANES XPT file that appears in `ingestion_summary.csv`. Files are marked for whether their variables entered the **final 25-feature model**, the **FIB-4 target**, or were **audited only**.

| File Key | Component | Description | Rows | Columns | SEQN Unique? | Variables Used in Final Model / Target | Role |
|:---|:---|:---|---:|---:|:---:|:---|:---|
| `DEMO_L` | DEMO G | Demographics | 11,933 | 27 | ✅ | `RIAGENDR` (model), `RIDAGEYR` (target construction — excluded from model) | Demographics |
| `BIOPRO_L` | LABORATORY | Biochemistry Profile | 7,199 | 42 | ✅ | `LBXSGTSI`, `LBXSAL`, `LBXSTB`, `LBXSAPSI` (liver model); `LBXSCR`, `LBXSBU`, `LBXSUA` (kidney model); `LBXSASSI`, `LBXSATSI` (target only — excluded from model) | Liver + Kidney + Target |
| `CBC_L` | LABORATORY | Complete Blood Count | 8,727 | 23 | ✅ | `LBXWBCSI`, `LBXRBCSI`, `LBXHGB`, `LBXHSCRP` (biomarker model); `LBXPLTSI` (target only — excluded from model) | Biomarker + Target |
| `ALB_CR_L` | LABORATORY | Albumin & Creatinine — Urine | 8,493 | 8 | ✅ | `URXUMA`, `URXUCR` (kidney model) | Kidney |
| `HDL_L` | LABORATORY | HDL Cholesterol | 8,068 | 4 | ✅ | `LBDHDD` (heart model) | Heart |
| `TCHOL_L` | LABORATORY | Total Cholesterol | 8,068 | 4 | ✅ | `LBXTC` (heart model) | Heart |
| `HSCRP_L` | LABORATORY | High-Sensitivity C-Reactive Protein | 8,727 | 4 | ✅ | `LBXHSCRP` (biomarker model) | Biomarker |
| `BPXO_L` | EXAMINATION | Blood Pressure — Oscillometric | 7,801 | 12 | ✅ | `BPXOSY1`, `BPXODI1`, `BPXOPLS1` (heart model) | Heart |
| `LUX_L` | EXAMINATION | Liver Ultrasound Elastography (FibroScan) | 7,199 | 13 | ✅ | `LUXSMED`, `LUXCAPM` (liver model) | Liver |
| `BPQ_L` | QUESTIONNAIRE | Blood Pressure Questionnaire | 8,501 | 6 | ✅ | `BPQ020` (heart model) | Heart |
| `KIQ_U_L` | QUESTIONNAIRE | Kidney Conditions Questionnaire | 7,809 | 9 | ✅ | `KIQ022` (kidney model) | Kidney |
| `MCQ_L` | QUESTIONNAIRE | Medical Conditions Questionnaire | 11,744 | 35 | ✅ | `MCQ160C`, `MCQ160E` (heart model) | Heart |
| `TRIGLY_L` | LABORATORY | Triglycerides | 3,996 | 10 | ✅ | None retained | Audited only |
| `GHB_L` | LABORATORY | Glycohemoglobin (HbA1c) | 7,199 | 3 | ✅ | None retained | Audited only |
| `GLU_L` | LABORATORY | Fasting Glucose | 3,996 | 4 | ✅ | None retained | Audited only |
| `INS_L` | LABORATORY | Insulin | 3,996 | 5 | ✅ | None retained | Audited only |
| `HEPA_L` | LABORATORY | Hepatitis A | 8,611 | 3 | ✅ | None retained | Audited only |
| `HEPBD_L` | LABORATORY | Hepatitis B Surface/Core Antibody | 8,068 | 5 | ✅ | None retained | Audited only |
| `HEPC_L` | LABORATORY | Hepatitis C | 8,068 | 5 | ✅ | None retained | Audited only |
| `HEPE_L` | LABORATORY | Hepatitis E | 8,068 | 4 | ✅ | None retained | Audited only |
| `BMX_L` | EXAMINATION | Body Measures | 8,860 | 22 | ✅ | None retained | Audited only |
| `DIQ_L` | QUESTIONNAIRE | Diabetes Questionnaire | 11,744 | 9 | ✅ | None retained | Audited only |
| `HEQ_L` | QUESTIONNAIRE | Hepatitis Questionnaire | 10,696 | 2 | ✅ | None retained | Audited only |
| `FNQ_L` | QUESTIONNAIRE | Functioning Questionnaire | 10,942 | 32 | ✅ | None retained | Audited only |
| `DPQ_L` | QUESTIONNAIRE | Depression Screening Questionnaire | 6,337 | 11 | ✅ | None retained | Audited only |
| `SLQ_L` | QUESTIONNAIRE | Sleep Disorders Questionnaire | 8,501 | 7 | ✅ | None retained | Audited only |
| `DBQ_L` | QUESTIONNAIRE | Diet Behavior Questionnaire | 11,933 | 27 | ✅ | None retained | Audited only |

**Source**: `data/ingestion_summary.csv` and `reports/dataset_report.md`.

---

## Section 4 — File-by-File Variable Explanation

The table below covers every variable from the 12 model-relevant files. Variables from audit-only files are not listed individually as none were retained.

| Variable Code | Plain English Meaning | Unit | Source File | Category | Final Role |
|:---|:---|:---|:---|:---|:---|
| `SEQN` | Unique participant ID number | — | All files | Identifier | Join key only; not a model feature |
| `RIDAGEYR` | Age of the participant in years | Years | `DEMO_L` | Demographics | **Target construction only** — EXCLUDED from model inputs |
| `RIAGENDR` | Biological sex (1 = Male, 2 = Female) | Categorical | `DEMO_L` | Demographics | ✅ Model input — Patient node feature |
| `LBXSATSI` | Alanine Aminotransferase (ALT) — a liver enzyme elevated when liver cells are damaged | U/L | `BIOPRO_L` | Liver enzyme | **Target construction only** — EXCLUDED from model inputs |
| `LBXSASSI` | Aspartate Aminotransferase (AST) — another liver enzyme; marker of liver cell injury | U/L | `BIOPRO_L` | Liver enzyme | **Target construction only** — EXCLUDED from model inputs |
| `LBXSGTSI` | Gamma-Glutamyl Transferase (GGT) — liver enzyme sensitive to alcohol and bile duct problems | U/L | `BIOPRO_L` | Liver | ✅ Model input — Liver node feature |
| `LBXSAL` | Albumin — protein made by the liver; low levels suggest poor liver synthesis function | g/dL | `BIOPRO_L` | Liver | ✅ Model input — Liver node feature |
| `LBXSTB` | Total Bilirubin — waste product processed by the liver; elevated in liver/bile disease | mg/dL | `BIOPRO_L` | Liver | ✅ Model input — Liver node feature |
| `LBXSAPSI` | Alkaline Phosphatase (ALP) — enzyme elevated in liver, bile duct, or bone disease | U/L | `BIOPRO_L` | Liver | ✅ Model input — Liver node feature |
| `LBXSCR` | Serum Creatinine — waste product filtered by kidneys; high levels suggest poor kidney function | mg/dL | `BIOPRO_L` | Kidney | ✅ Model input — Kidney node feature |
| `LBXSBU` | Blood Urea Nitrogen (BUN) — another kidney filtration waste marker | mg/dL | `BIOPRO_L` | Kidney | ✅ Model input — Kidney node feature |
| `LBXSUA` | Uric Acid — metabolic waste product; elevated in gout and kidney disease | mg/dL | `BIOPRO_L` | Kidney | ✅ Model input — Kidney node feature |
| `LBXPLTSI` | Platelet Count — blood cells involved in clotting; low count is a liver fibrosis marker | 10⁹/L | `CBC_L` | Blood count | **Target construction only** — EXCLUDED from model inputs |
| `LBXWBCSI` | White Blood Cell Count — immune cells; elevated in infection and inflammation | 10⁹/L | `CBC_L` | Biomarker | ✅ Model input — Biomarker node feature |
| `LBXRBCSI` | Red Blood Cell Count — oxygen-carrying cells; low count suggests anemia | 10¹²/L | `CBC_L` | Biomarker | ✅ Model input — Biomarker node feature |
| `LBXHGB` | Hemoglobin — protein in red blood cells that carries oxygen | g/dL | `CBC_L` | Biomarker | ✅ Model input — Biomarker node feature |
| `URXUMA` | Urine Albumin (Microalbumin) — protein leaking into urine; marker of kidney damage | µg/mL | `ALB_CR_L` | Kidney | ✅ Model input — Kidney node feature |
| `URXUCR` | Urine Creatinine — used alongside urine albumin to assess kidney filtration efficiency | mg/dL | `ALB_CR_L` | Kidney | ✅ Model input — Kidney node feature |
| `LBDHDD` | Direct HDL Cholesterol — "good" cholesterol; low HDL is a cardiovascular risk factor | mg/dL | `HDL_L` | Heart | ✅ Model input — Heart node feature |
| `LBXTC` | Total Cholesterol — combined measurement of all cholesterol types in blood | mg/dL | `TCHOL_L` | Heart | ✅ Model input — Heart node feature |
| `LBXHSCRP` | High-Sensitivity C-Reactive Protein (hs-CRP) — protein marker of systemic inflammation | mg/L | `HSCRP_L` | Biomarker | ✅ Model input — Biomarker node feature |
| `BPXOSY1` | Systolic Blood Pressure Reading 1 — the "top number" in a blood pressure reading (peak pressure) | mmHg | `BPXO_L` | Heart | ✅ Model input — Heart node feature |
| `BPXODI1` | Diastolic Blood Pressure Reading 1 — the "bottom number" (resting pressure between heartbeats) | mmHg | `BPXO_L` | Heart | ✅ Model input — Heart node feature |
| `BPXOPLS1` | Pulse Rate Reading 1 — heart rate in beats per minute | bpm | `BPXO_L` | Heart | ✅ Model input — Heart node feature |
| `LUXSMED` | Liver Stiffness Median — FibroScan elastography result; stiffer liver = more fibrosis | kPa | `LUX_L` | Liver | ✅ Model input — Liver node feature |
| `LUXCAPM` | Controlled Attenuation Parameter (CAP) — FibroScan measurement of liver fat (steatosis) | dB/m | `LUX_L` | Liver | ✅ Model input — Liver node feature |
| `BPQ020` | "Ever told by a doctor you have high blood pressure?" — self-reported history | Binary 1/2 | `BPQ_L` | Heart | ✅ Model input — Heart node feature |
| `KIQ022` | "Ever told by a doctor you have kidney failure or disease?" — self-reported history | Binary 1/2 | `KIQ_U_L` | Kidney | ✅ Model input — Kidney node feature |
| `MCQ160C` | "Ever told by a doctor you have coronary heart disease?" — self-reported history | Binary 1/2 | `MCQ_L` | Heart | ✅ Model input — Heart node feature |
| `MCQ160E` | "Ever told by a doctor you had a heart attack?" — self-reported history | Binary 1/2 | `MCQ_L` | Heart | ✅ Model input — Heart node feature |

---

## Section 5 — FIB-4 Target Construction

### 5.1 What Is FIB-4?

FIB-4 is the **Fibrosis-4 Index** — a clinically validated, non-invasive blood test score used in hepatology (liver medicine) to estimate the degree of liver scarring (fibrosis). It requires no biopsy. Doctors use it to screen for liver fibrosis in patients with chronic liver disease.

### 5.2 The Exact Formula

$$\text{FIB-4} = \frac{\text{Age (years)} \times \text{AST (U/L)}}{\text{Platelets } (10^9/\text{L}) \times \sqrt{\text{ALT (U/L)}}}$$

### 5.3 Mapping to NHANES Variable Codes

| FIB-4 Component | NHANES Variable | Unit | Source File |
|:---|:---|:---|:---|
| **Age** | `RIDAGEYR` | Years | `DEMO_L` |
| **AST** (Aspartate Aminotransferase) | `LBXSASSI` | U/L | `BIOPRO_L` |
| **ALT** (Alanine Aminotransferase) | `LBXSATSI` | U/L | `BIOPRO_L` |
| **Platelets** | `LBXPLTSI` | 10⁹/L (same as 10³/µL) | `CBC_L` |

**Source confirmed in**: `data/fib4_target_validation.json` → `unit_verification` block.

### 5.4 How the Target Was Computed

1. All four source variables were extracted from their respective NHANES files after SEQN-based merging into the master patient table.
2. Patients with any missing or zero value in Age, AST, ALT, or Platelets were **excluded from the cohort** during the sequential filtering steps (see Section 6).
3. FIB-4 was computed exactly as the formula above for all 6,277 remaining patients.
4. No transformation (e.g., log-transform) was applied; the raw continuous FIB-4 score was used as the regression target.

### 5.5 Target Validation Results

After computation, an automated validation pass was run. All validation gates passed (source: `data/fib4_target_validation.json`):

| Statistic | Value |
|:---|---:|
| **N Patients** | 6,277 |
| **Mean** | 1.0590 |
| **Standard Deviation** | 0.7748 |
| **Median** | 0.9028 |
| **25th Percentile** | 0.5091 |
| **75th Percentile** | 1.4023 |
| **IQR** | 0.8932 |
| **Minimum** | 0.0634 |
| **Maximum** | 13.9971 |
| **Skewness** | 2.9236 |
| **Validation Gates Passed** | ✅ True |

The distribution is **positively skewed** (skewness = 2.92), meaning most patients have FIB-4 scores below 1.3 (low fibrosis risk), with a long right tail of high-risk patients.

### 5.6 Target Construction Variables vs. Model Input Variables

> [!IMPORTANT]
> This is the most critical distinction in the entire project. Understanding this distinction is essential before using the dataset.

**The FIB-4 score is a deterministic mathematical formula.** If you feed Age, AST, ALT, or Platelets into a machine learning model that is trying to predict FIB-4, the model can simply **mathematically reconstruct the formula** and achieve near-perfect accuracy. This is called **mathematical identity leakage** — the model "cheats" by using the formula's own inputs.

This leakage was confirmed experimentally (see Section 10). When all 4 formula inputs were included as model features (Experiment 1), XGBoost achieved $R^2 = 0.9302$ — not because it learned anything meaningful about multi-organ biology, but because it reconstructed the formula.

**Therefore, all 4 FIB-4 formula inputs were permanently excluded from the model input feature matrix:**

| Variable | Role |
|:---|:---|
| `RIDAGEYR` (Age) | ❌ Used only to compute FIB-4 target; EXCLUDED from all model inputs |
| `LBXSASSI` (AST) | ❌ Used only to compute FIB-4 target; EXCLUDED from all model inputs |
| `LBXSATSI` (ALT) | ❌ Used only to compute FIB-4 target; EXCLUDED from all model inputs |
| `LBXPLTSI` (Platelets) | ❌ Used only to compute FIB-4 target; EXCLUDED from all model inputs |

The remaining 25 features form the locked **Experiment 3 model input manifest** (see Section 9).

---

## Section 6 — Cohort Construction & Attrition

### 6.1 Why Cohort Filtering Was Necessary

Not all 11,933 NHANES participants have complete data for every variable. FIB-4 requires four specific lab values. The project required that **every patient in the final cohort has a computable FIB-4 score** and at least baseline kidney and cardiovascular laboratory data, ensuring the model can always receive node features for all organ types.

### 6.2 Complete Sequential Attrition Table

**Source**: `data/cohort_flow.csv`

| Step | Filter Applied | N Remaining | N Excluded | % of Previous Lost |
|:---:|:---|---:|---:|---:|
| **1** | Initial NHANES August 2021–August 2023 participants | 11,933 | 0 | 0.0% |
| **2** | Demographic availability (Age & Gender complete) | 11,933 | 0 | 0.0% |
| **3** | Liver enzymes availability (ALT & AST both complete & > 0) | 6,308 | 5,625 | 47.1% |
| **4** | Platelet count availability (LBXPLTSI complete & > 0) | 6,282 | 26 | 0.4% |
| **5** | Kidney baseline availability (Serum Creatinine & BUN complete) | 6,277 | 5 | 0.08% |
| **6** | Cardiovascular baseline availability (HDL & Total Cholesterol complete) | **6,277** | 0 | 0.0% |

**Final locked cohort: N = 6,277 patients.**

### 6.3 Why Each Step Excludes Patients

- **Step 2 (No exclusions)**: All NHANES participants have demographic records. Age and gender were universally complete.
- **Step 3 (Largest exclusion — 5,625 patients)**: The biochemistry lab panel (BIOPRO_L) was only administered to ~53% of participants. Participants who were fasting-ineligible, refused, or were not sampled for biochemistry are missing. This is by NHANES design (sub-sample strategy). The positivity condition (> 0) ensures no zero-valued enzyme entries corrupt the FIB-4 denominator (√ALT must be non-zero).
- **Step 4 (26 excluded)**: A small number of participants had biochemistry data but were missing platelet counts from the CBC panel, or had zero platelet values.
- **Step 5 (5 excluded)**: A very small number passed all prior filters but had missing creatinine or BUN values despite having biochemistry data. This may reflect failed sample collection or out-of-range values that were suppressed by NHANES.
- **Step 6 (0 excluded)**: Every patient passing Step 5 already had HDL and Total Cholesterol data because these were required as cardiovascular prerequisites.

---

## Section 7 — Data Integration and Joining

### 7.1 The Core Concept: Joining on SEQN

Each NHANES data file stores different measurements for the same people. To create a single row per patient containing all their information, you perform a series of **left-join merges on the SEQN column**.

**Conceptual flow:**
```
DEMO_L  →  (left join SEQN)  →  + BIOPRO_L
         →  (left join SEQN)  →  + CBC_L
         →  (left join SEQN)  →  + ALB_CR_L
         →  (left join SEQN)  →  + HDL_L
         →  (left join SEQN)  →  + TCHOL_L
         →  (left join SEQN)  →  + HSCRP_L
         →  (left join SEQN)  →  + BPXO_L
         →  (left join SEQN)  →  + LUX_L
         →  (left join SEQN)  →  + BPQ_L
         →  (left join SEQN)  →  + KIQ_U_L
         →  (left join SEQN)  →  + MCQ_L
         ═══════════════════════════════════
         → master_patient.csv  (N = 11,933 rows, one per NHANES participant)
```

### 7.2 Why Left-Join?

Starting from `DEMO_L` (which has all 11,933 participants) and left-joining subsequent files preserves all participants, even those missing data in specific lab files. This produces NaN values for missing data, which are handled later during cohort filtering and fold-safe imputation.

### 7.3 One-to-One Relationship Guarantee

As confirmed by `data/ingestion_summary.csv`, every file used has `is_seqn_unique = True`. This means each SEQN appears at most once per file, guaranteeing the left join will produce exactly one row per NHANES participant in the merged table. No fan-out, no duplicates.

### 7.4 Outputs of Integration

- **`data/master_patient.csv`**: The full merged table of all 11,933 participants × all extracted variables. Size: ~11.5 MB on disk.
- Cohort filtering is then applied to this master table to extract the final 6,277 patients.
- **`data/final_cohort.csv`**: The filtered table of 6,277 patients × 29 variables (25 model features + 4 excluded target-construction variables). Size: ~8.2 MB on disk.

### 7.5 Patient UID Assignment

After SEQN-based merging, patients were assigned a formatted string ID:
- `patient_uid = "P_000001"` through `"P_006277"` (zero-padded, sequential).
- Verified: Zero SEQN duplicates in the final cohort.

---

## Section 8 — Missingness, Cleaning & Validation

### 8.1 Understanding Three Levels of Availability

A common point of confusion with NHANES data is that a variable's missingness changes between levels. Three levels are tracked in `data/missingness_report.csv`:

| Level | N Denominator | What It Measures |
|:---|:---|:---|
| **Raw file availability** | 11,933 (all NHANES participants) | What fraction of all participants had this measurement |
| **Intermediate/Pre-cohort** | ~6,282–6,308 (FIB-4-eligible participants) | Not separately reported; implicitly captured in attrition steps |
| **Final cohort availability** | 6,277 (final locked cohort) | What fraction of the final study population is missing this variable |

### 8.2 Missingness Audit Results

From `data/missingness_report.csv`, the full missingness profile for all 29 variables tracked:

| Variable | Organ | Raw Missing % | Cohort Missing % | Status |
|:---|:---|---:|---:|:---|
| `RIDAGEYR` | Demographics | 0.00% | 0.00% | RETAINED (target only) |
| `RIAGENDR` | Demographics | 0.00% | 0.00% | RETAINED (model) |
| `LBXSATSI` (ALT) | Liver | 47.03% | 0.00% | RETAINED (target only) |
| `LBXSASSI` (AST) | Liver | 47.14% | 0.00% | RETAINED (target only) |
| `LBXSGTSI` (GGT) | Liver | 46.98% | 0.00% | RETAINED (model) |
| `LBXSAL` (Albumin) | Liver | 46.65% | 0.00% | RETAINED (model) |
| `LBXSTB` (Bilirubin) | Liver | 47.00% | 0.05% | RETAINED (model) |
| `LBXSAPSI` (ALP) | Liver | 46.98% | 0.00% | RETAINED (model) |
| `LUXSMED` (FibroScan Stiffness) | Liver | 43.85% | **6.21%** | RETAINED (model) |
| `LUXCAPM` (CAP Attenuation) | Liver | 43.86% | **6.21%** | RETAINED (model) |
| `LBXSCR` (Creatinine) | Kidney | 46.99% | 0.03% | RETAINED (model) |
| `LBXSBU` (BUN) | Kidney | 46.99% | 0.05% | RETAINED (model) |
| `LBXSUA` (Uric Acid) | Kidney | 46.96% | 0.00% | RETAINED (model) |
| `URXUMA` (Urine Albumin) | Kidney | 31.68% | 1.97% | RETAINED (model) |
| `URXUCR` (Urine Creatinine) | Kidney | 31.67% | 1.96% | RETAINED (model) |
| `KIQ022` (Kidney Disease History) | Kidney | 34.58% | **13.98%** | RETAINED (model) |
| `BPXOSY1` (Systolic BP) | Heart | 37.01% | 3.07% | RETAINED (model) |
| `BPXODI1` (Diastolic BP) | Heart | 37.01% | 3.07% | RETAINED (model) |
| `BPXOPLS1` (Pulse Rate) | Heart | 37.01% | 3.07% | RETAINED (model) |
| `LBDHDD` (HDL Cholesterol) | Heart | 42.26% | 0.00% | RETAINED (model) |
| `LBXTC` (Total Cholesterol) | Heart | 42.26% | 0.00% | RETAINED (model) |
| `BPQ020` (Hypertension History) | Heart | 28.79% | 7.07% | RETAINED (model) |
| `MCQ160C` (Coronary Heart Disease) | Heart | 34.58% | **13.99%** | RETAINED (model) |
| `MCQ160E` (Heart Attack) | Heart | 34.58% | **13.99%** | RETAINED (model) |
| `LBXWBCSI` (WBC Count) | Biomarker | 36.37% | 0.00% | RETAINED (model) |
| `LBXRBCSI` (RBC Count) | Biomarker | 36.37% | 0.00% | RETAINED (model) |
| `LBXHGB` (Hemoglobin) | Biomarker | 36.37% | 0.00% | RETAINED (model) |
| `LBXPLTSI` (Platelet Count) | Biomarker | 36.37% | 0.00% | RETAINED (target only) |
| `LBXHSCRP` (hs-CRP) | Biomarker | 38.98% | 0.00% | RETAINED (model) |

**Highest missingness variables in final cohort**: `KIQ022` (13.98%), `MCQ160C` (13.99%), `MCQ160E` (13.99%), `LUXSMED` (6.21%), `LUXCAPM` (6.21%).

### 8.3 Missingness Handling Strategy

The retention threshold was **< 30% missingness in the final cohort**. All 29 candidate variables passed this threshold (the highest, `KIQ022` / `MCQ160C` / `MCQ160E` at ~14%, are well within the limit).

**Residual missingness was handled by fold-safe median imputation:**
- The median of each feature is computed **only on the training fold data**.
- The training fold's median is then applied to fill missing values in **both the training and validation folds**.
- This is critical for preventing **data leakage from the validation fold into imputation**. The validation fold's true distribution never informs the imputation values.

### 8.4 Validation Checks Performed

| Check | Status |
|:---|:---|
| Zero SEQN duplicates in all 27 source files | ✅ Passed |
| Zero NaN/Inf in the computed FIB-4 target | ✅ Passed |
| FIB-4 formula re-verified against source variables | ✅ Passed |
| All patients have a unique `patient_uid` | ✅ Passed |
| Final cohort N exactly 6,277 | ✅ Passed |
| Brain/Gut nodes confirmed excluded (no valid NHANES variables available) | ✅ Passed |

---

## Section 9 — Final 25-Feature Model Manifest (Experiment 3 Locked)

This is the **exact and complete set of 25 features** used as model inputs. None of the four FIB-4 formula components are included.

### Patient / Demographics (1 Feature)

| NHANES Code | Meaning | Unit | Source File | Node Type | Type |
|:---|:---|:---|:---|:---|:---|
| `RIAGENDR` | Gender (1 = Male, 2 = Female) | Binary Categorical | `DEMO_L` | `patient` | Categorical |

### Liver (6 Features)

| NHANES Code | Meaning | Unit | Source File | Node Type | Cohort Missing % | Type |
|:---|:---|:---|:---|:---|---:|:---|
| `LBXSGTSI` | Gamma-Glutamyl Transferase (GGT) | U/L | `BIOPRO_L` | `liver` | 0.00% | Continuous |
| `LBXSAL` | Albumin | g/dL | `BIOPRO_L` | `liver` | 0.00% | Continuous |
| `LBXSTB` | Total Bilirubin | mg/dL | `BIOPRO_L` | `liver` | 0.05% | Continuous |
| `LBXSAPSI` | Alkaline Phosphatase (ALP) | U/L | `BIOPRO_L` | `liver` | 0.00% | Continuous |
| `LUXSMED` | Liver Stiffness Median (FibroScan) | kPa | `LUX_L` | `liver` | 6.21% | Continuous |
| `LUXCAPM` | Controlled Attenuation Parameter (CAP) | dB/m | `LUX_L` | `liver` | 6.21% | Continuous |

### Kidney (6 Features)

| NHANES Code | Meaning | Unit | Source File | Node Type | Cohort Missing % | Type |
|:---|:---|:---|:---|:---|---:|:---|
| `LBXSCR` | Serum Creatinine | mg/dL | `BIOPRO_L` | `kidney` | 0.03% | Continuous |
| `LBXSBU` | Blood Urea Nitrogen (BUN) | mg/dL | `BIOPRO_L` | `kidney` | 0.05% | Continuous |
| `LBXSUA` | Uric Acid | mg/dL | `BIOPRO_L` | `kidney` | 0.00% | Continuous |
| `URXUMA` | Urine Albumin (Microalbumin) | µg/mL | `ALB_CR_L` | `kidney` | 1.97% | Continuous |
| `URXUCR` | Urine Creatinine | mg/dL | `ALB_CR_L` | `kidney` | 1.96% | Continuous |
| `KIQ022` | Ever Told Kidney Disease (1=Yes, 2=No) | Binary Categorical | `KIQ_U_L` | `kidney` | 13.98% | Categorical |

### Heart / Cardiovascular (8 Features)

| NHANES Code | Meaning | Unit | Source File | Node Type | Cohort Missing % | Type |
|:---|:---|:---|:---|:---|---:|:---|
| `BPXOSY1` | Systolic Blood Pressure Reading 1 | mmHg | `BPXO_L` | `heart` | 3.07% | Continuous |
| `BPXODI1` | Diastolic Blood Pressure Reading 1 | mmHg | `BPXO_L` | `heart` | 3.07% | Continuous |
| `BPXOPLS1` | Pulse Rate Reading 1 | bpm | `BPXO_L` | `heart` | 3.07% | Continuous |
| `LBDHDD` | Direct HDL Cholesterol | mg/dL | `HDL_L` | `heart` | 0.00% | Continuous |
| `LBXTC` | Total Cholesterol | mg/dL | `TCHOL_L` | `heart` | 0.00% | Continuous |
| `BPQ020` | Ever Told High Blood Pressure (1=Yes, 2=No) | Binary Categorical | `BPQ_L` | `heart` | 7.07% | Categorical |
| `MCQ160C` | Ever Told Coronary Heart Disease (1=Yes, 2=No) | Binary Categorical | `MCQ_L` | `heart` | 13.99% | Categorical |
| `MCQ160E` | Ever Told Heart Attack (1=Yes, 2=No) | Binary Categorical | `MCQ_L` | `heart` | 13.99% | Categorical |

### Biomarker / Systemic (4 Features)

| NHANES Code | Meaning | Unit | Source File | Node Type | Cohort Missing % | Type |
|:---|:---|:---|:---|:---|---:|:---|
| `LBXWBCSI` | White Blood Cell Count | 10⁹/L | `CBC_L` | `biomarker` | 0.00% | Continuous |
| `LBXRBCSI` | Red Blood Cell Count | 10¹²/L | `CBC_L` | `biomarker` | 0.00% | Continuous |
| `LBXHGB` | Hemoglobin | g/dL | `CBC_L` | `biomarker` | 0.00% | Continuous |
| `LBXHSCRP` | High-Sensitivity C-Reactive Protein (hs-CRP) | mg/L | `HSCRP_L` | `biomarker` | 0.00% | Continuous |

> [!CAUTION]
> Double-check that `RIDAGEYR` (Age), `LBXSASSI` (AST), `LBXSATSI` (ALT), and `LBXPLTSI` (Platelets) are NOT present in this list. Their inclusion would constitute mathematical target leakage.

---

## Section 10 — Leakage Control Experiments

### 10.1 Why This Investigation Was Necessary

FIB-4 is **not** a measured biomarker — it is a number **mathematically computed from** Age, AST, ALT, and Platelets. If any of these four inputs are available as model features, a machine learning model can reconstruct FIB-4 purely through the formula without learning anything about multi-organ biology. This is called **direct mathematical target leakage**.

Three controlled experiments were designed to quantify the severity of this leakage.

### 10.2 Experiment Design

All three experiments used the same evaluation protocol:
- **5-fold cross-validation**, patient-level splits.
- **4 tabular models**: Ridge Regression, Random Forest, XGBoost, MLP Regressor.
- **Same preprocessing**: fold-safe median imputation + StandardScaler.

The only thing that changed between experiments was **which features were included**.

### 10.3 Experiment Results (Source: `reports/leakage_audit_report.md`)

#### Experiment 1: All Features (29 features — includes all 4 FIB-4 inputs)

| Model | MAE | RMSE | $R^2$ |
|:---|---:|---:|---:|
| Ridge Regression | 0.2105 ± 0.0039 | 0.3832 ± 0.0448 | **0.7550 ± 0.0323** |
| Random Forest | 0.1060 ± 0.0061 | 0.2304 ± 0.0509 | **0.9105 ± 0.0310** |
| XGBoost | 0.0897 ± 0.0024 | 0.2031 ± 0.0474 | **0.9302 ± 0.0259** |
| MLP Regressor | 0.0912 ± 0.0051 | 0.2012 ± 0.0414 | **0.9313 ± 0.0226** |

**Interpretation**: $R^2 \approx 0.93$ reflects near-perfect algebraic reconstruction of the FIB-4 formula, not biological prediction. This confirms severe mathematical identity leakage.

#### Experiment 2: Remove ALT, AST, Platelets (retain Age — 26 features)

| Model | MAE | RMSE | $R^2$ |
|:---|---:|---:|---:|
| Ridge Regression | 0.3058 ± 0.0045 | 0.5098 ± 0.0376 | **0.5662 ± 0.0209** |
| Random Forest | 0.2850 ± 0.0070 | 0.4956 ± 0.0419 | **0.5900 ± 0.0306** |
| XGBoost | 0.2783 ± 0.0044 | 0.4844 ± 0.0369 | **0.6081 ± 0.0265** |
| MLP Regressor | 0.3647 ± 0.0120 | 0.5849 ± 0.0347 | **0.4236 ± 0.0774** |

**Interpretation**: Retaining Age alone is still sufficient for partial leakage ($R^2 \approx 0.61$) because Age is the FIB-4 numerator. Age must also be excluded.

#### Experiment 3: Complete Leakage-Free (remove all 4 FIB-4 inputs — 25 features)

| Model | MAE | RMSE | $R^2$ |
|:---|---:|---:|---:|
| Ridge Regression | 0.4065 ± 0.0094 | 0.6058 ± 0.0386 | **0.3869 ± 0.0222** |
| Random Forest | 0.3862 ± 0.0095 | 0.5956 ± 0.0404 | **0.4066 ± 0.0434** |
| XGBoost | 0.3821 ± 0.0098 | 0.5785 ± 0.0404 | **0.4408 ± 0.0316** |
| MLP Regressor | 0.4658 ± 0.0246 | 0.7230 ± 0.0804 | **0.1258 ± 0.1217** |

**Interpretation**: Direct mathematical target leakage from the FIB-4 algebraic components has been controlled. Models must now genuinely predict FIB-4 from non-FIB-4 multi-organ biomarkers.

> [!WARNING]
> **What the leakage audit establishes vs. does NOT establish:**
> - ✅ **Does establish**: Direct mathematical leakage from `RIDAGEYR`, `LBXSASSI`, `LBXSATSI`, `LBXPLTSI` has been controlled under the tested experimental configuration.
> - ❌ **Does NOT establish**: Absence of ALL possible indirect/confounded leakage pathways (e.g., variables correlated with excluded ones). Does not establish that remaining features carry no statistical correlation with the excluded variables. Does not establish clinical validity, causation, biological mechanism, or generalizability to other populations.

### 10.4 Experiment 3 Locked as Primary Configuration

Based on this audit, **Experiment 3 (Complete Leakage-Free)** was locked as the sole primary scientific benchmark for all HSGIN training, baseline comparisons, ablation studies, and Y-randomization validation.

### 10.5 Y-Randomization Control

**What it is**: An additional sanity check where the **target labels (FIB-4 values)** are randomly shuffled **within each training fold**, breaking any relationship between features and target. Models are trained on these shuffled labels but evaluated on the **true, un-shuffled validation targets**.

**How it was done**:
1. Within each fold, the FIB-4 target vector for the training set was permuted randomly.
2. The model was trained on shuffled $Y$ but with the real $X$ features.
3. Evaluation used the real, un-shuffled $Y$ on the validation set.

**Result** (from `data/experiment_results.json` → `y_randomization`):

| Metric | Value |
|:---|---:|
| MAE | 0.5569 ± 0.0070 |
| RMSE | 0.7838 ± 0.0351 |
| **$R^2$** | **−0.0281 ± 0.0291** |

**Interpretation**: $R^2 \approx -0.028 \approx 0$. A model trained on randomized targets cannot predict the true validation targets, as expected. This supports the claim that the residual $R^2 = 0.4976$ achieved by HSGIN under Experiment 3 conditions is not explained by trivial feature-target correlations detectable under the tested configuration. It does not constitute proof of zero leakage or proof of a causal biological mechanism.

---

## Section 11 — Final Dataset Structure and Generated Artifacts

The following files are the outputs of the data pipeline. All are stored in the `data/` directory.

| Artifact File | Type | Size | Description | How Generated | Use |
|:---|:---|---:|:---|:---|:---|
| `master_patient.csv` | Intermediate | ~11.5 MB | All 11,933 NHANES participants × all extracted variables, SEQN-merged | SEQN left-join of all 27 raw XPT files | Starting point for cohort filtering |
| `final_cohort.csv` | Final | ~8.2 MB | 6,277 filtered patients × 29 variables (25 model features + 4 target-construction variables) | Sequential inclusion filter applied to `master_patient.csv` | Primary input to graph construction and model training |
| `feature_manifest.json` | Final | 4,956 B | Complete feature manifest including description, raw and cohort-level missingness % for all 29 variables | Generated during missingness audit | Reference for reproducibility; consumed by pipeline scripts |
| `experiment_results.json` | Final | 8,506 B | All model performance metrics (tabular baselines, HGNN, HSGIN, ablation A–D, Y-randomization, HSGIN organ ablation A–D) | Accumulated by training pipeline and ablation scripts | Primary results artifact |
| `leakage_audit_results.json` | Final | 6,114 B | Detailed metrics for all 12 model × experiment combinations in the leakage audit (Exp 1/2/3 × 4 models) | Generated by leakage audit script | Supports Section 10 of this report |
| `fib4_target_validation.json` | Final | 570 B | FIB-4 target statistics: N, mean, std, median, min, max, IQR, skewness, unit verification block, validation gates status | Generated during target computation validation | Confirms correct FIB-4 formula and data |
| `cohort_flow.csv` | Final | 451 B | 6-step attrition table with N remaining and N excluded per step | Generated during cohort construction | Reproducibility audit trail |
| `missingness_report.csv` | Final | 2,709 B | Per-variable missingness at raw-file level and final-cohort level for all 29 variables | Generated during missingness audit | Used to confirm < 30% threshold for all retained variables |
| `ingestion_summary.csv` | Final | 1,708 B | Per-file metadata: file key, description, category, row count, unique SEQN count, is_seqn_unique flag, column count | Generated during data ingestion | Confirms uniqueness of SEQN across all 27 source files |
| `hsgin_ablation_cache.json` | Intermediate | 2,050 B | Fold-level metrics cache for HSGIN organ ablation (Configs A–D, 5 folds each), used for resumable training | Written incrementally by `src/hsgin_ablation.py` during training | Allows ablation to resume without retraining completed folds |

**Note**: The `graphs/patient_graphs.pt` file (PyTorch Geometric graph dataset) is stored in the `graphs/` directory, not `data/`. See Section 12.

---

## Section 12 — Conversion to HSGIN Graph Dataset

### 12.1 Overview: One Patient = One Graph

After creating `final_cohort.csv`, the pipeline converts each of the 6,277 patients into an independent **PyTorch Geometric `HeteroData` object** — a heterogeneous graph that encodes the patient's multi-organ data as interconnected nodes.

All 6,277 graphs are stored as a Python list serialized to: `graphs/patient_graphs.pt`

### 12.2 The 5 Node Types

Each patient graph has exactly **5 nodes** (one node of each type):

| Node Type | Feature Vector Content | Feature Dimension | Variables |
|:---|:---|---:|:---|
| `patient` | Gender | **1** | `RIAGENDR` |
| `liver` | Hepatic function and imaging markers | **6** | `LBXSGTSI`, `LBXSAL`, `LBXSTB`, `LBXSAPSI`, `LUXSMED`, `LUXCAPM` |
| `kidney` | Renal filtration and disease markers | **6** | `LBXSCR`, `LBXSBU`, `LBXSUA`, `URXUMA`, `URXUCR`, `KIQ022` |
| `heart` | Cardiovascular hemodynamics and lipid markers | **8** | `BPXOSY1`, `BPXODI1`, `BPXOPLS1`, `LBDHDD`, `LBXTC`, `BPQ020`, `MCQ160C`, `MCQ160E` |
| `biomarker` | Systemic hematologic and inflammatory markers | **4** | `LBXWBCSI`, `LBXRBCSI`, `LBXHGB`, `LBXHSCRP` |

**Total features per patient**: 1 + 6 + 6 + 8 + 4 = **25 features** ✅ (matches the Experiment 3 manifest exactly).

Each node's feature vector is a 1D tensor (one row, since each node represents exactly one patient's measurements in that domain).

### 12.3 The 14 Edge Types

Edges in the graph encode **relationships between organ systems**. There are two categories of edges:

**Category A: Patient–Organ Edges (8 edges, 4 bidirectional pairs)**

These connect the `patient` node to each organ/domain node:

| Direction | Edge Name | Meaning |
|:---|:---|:---|
| `patient` → `liver` | `pertains_to` | Patient's liver measurements belong to this patient |
| `liver` → `patient` | `rev_pertains_to` | Reverse of above (for message passing) |
| `patient` → `kidney` | `pertains_to` | Patient's kidney measurements belong to this patient |
| `kidney` → `patient` | `rev_pertains_to` | Reverse |
| `patient` → `heart` | `pertains_to` | Patient's heart measurements belong to this patient |
| `heart` → `patient` | `rev_pertains_to` | Reverse |
| `patient` → `biomarker` | `pertains_to` | Patient's biomarker measurements belong to this patient |
| `biomarker` → `patient` | `rev_pertains_to` | Reverse |

**Category B: Inter-Organ Edges (6 edges, 3 bidirectional pairs)**

These connect organ nodes directly to each other, encoding physiological inter-organ crosstalk:

| Direction | Edge Name | Physiological Basis |
|:---|:---|:---|
| `liver` → `kidney` | `interacts_with` | Hepatorenal syndrome; shared metabolic pathways |
| `kidney` → `liver` | `interacts_with` | Reverse |
| `liver` → `heart` | `interacts_with` | Metabolic liver disease and cardiovascular risk interaction |
| `heart` → `liver` | `interacts_with` | Reverse |
| `kidney` → `heart` | `interacts_with` | Cardiorenal syndrome; hypertension and kidney disease linkage |
| `heart` → `kidney` | `interacts_with` | Reverse |

**Total: 8 patient–organ + 6 inter-organ = 14 directed edge types** ✅

> [!NOTE]
> There are **no edges** between:
> - `patient` ↔ `patient` (patients are independent graphs)
> - `biomarker` ↔ any organ directly (biomarker only connects to `patient`)
> - `liver` ↔ `biomarker`, `kidney` ↔ `biomarker`, `heart` ↔ `biomarker`

**Why no Brain/Gut nodes**: The original project concept envisioned 5 organs (Liver + Kidney + Heart + Gut + Brain). However, the NHANES August 2021–August 2023 cycle **does not contain** validated patient-level gut microbiome composition or neuroimaging/cognitive assessment variables that can be linked via SEQN. These two organs were deferred to future work.

### 12.4 Graph-Level Target Assignment

The continuous FIB-4 score for each patient is stored in:

```python
data['patient'].y  # tensor of shape [1] containing the patient's FIB-4 score
```

The target is assigned to the `patient` node as a scalar regression target.

### 12.5 ASCII Diagram of One Patient's Graph

```
                 [Patient Node]
                  (1 feature: RIAGENDR)
                 / |        |       \
                /  |        |        \
               ↓   ↓        ↓         ↓
         [Liver]  [Kidney] [Heart]  [Biomarker]
         (6 feat) (6 feat) (8 feat)  (4 feat)
            ↕         ↕        ↕
         (inter-organ interacts_with edges)
```

All arrows are bidirectional (separate forward and reverse edge types).

---

## Section 13 — Complete Reproduction Workflow

The following is a step-by-step guide to reproducing the entire dataset from scratch.

```
PHASE 1: DATA ACQUISITION
═══════════════════════════════════════════════════════════════════
1.  Go to: https://www.cdc.gov/nchs/nhanes/
2.  Navigate to: Data Files → NHANES August 2021–August 2023
3.  Download exactly 12 XPT files:
      Demographics:   DEMO_L.xpt
      Laboratory:     BIOPRO_L.xpt, CBC_L.xpt, ALB_CR_L.xpt,
                      HDL_L.xpt, TCHOL_L.xpt, HSCRP_L.xpt
      Examination:    BPXO_L.xpt, LUX_L.xpt
      Questionnaire:  BPQ_L.xpt, KIQ_U_L.xpt, MCQ_L.xpt
4.  Organize into subdirectories: DEMO G/, LABORATORY/, EXAMINATION/, QUESTIONNAIRE/

PHASE 2: DATA INGESTION
═══════════════════════════════════════════════════════════════════
5.  Load each XPT file using: pd.read_sas(file, format="xport", encoding="utf-8")
6.  Verify SEQN uniqueness in each file (all should be unique)
7.  Save ingestion summary → data/ingestion_summary.csv

PHASE 3: SEQN-BASED INTEGRATION
═══════════════════════════════════════════════════════════════════
8.  Start from DEMO_L as the base (11,933 rows, one per participant)
9.  Left-merge each subsequent file on SEQN:
      base.merge(BIOPRO_L[['SEQN', 'LBXSATSI', 'LBXSASSI', ...]], on='SEQN', how='left')
      base.merge(CBC_L[['SEQN', 'LBXWBCSI', 'LBXRBCSI', ...]], on='SEQN', how='left')
      ... (repeat for all 11 files)
10. Save merged table → data/master_patient.csv (11,933 rows × all variables)

PHASE 4: MISSINGNESS AUDIT
═══════════════════════════════════════════════════════════════════
11. For each of the 29 tracked variables, compute:
      raw_missing_pct = (11933 - raw_available) / 11933 * 100
      cohort_missing_pct = calculated after cohort filtering
12. Retain all variables with cohort missingness < 30%
13. Save missingness report → data/missingness_report.csv

PHASE 5: COHORT FILTERING (Sequential Inclusion)
═══════════════════════════════════════════════════════════════════
14. Filter: ALT (LBXSATSI) complete AND > 0  → 6,308 remain
15. Filter: AST (LBXSASSI) complete AND > 0  → 6,308 (already filtered by co-presence)
16. Filter: Platelets (LBXPLTSI) complete AND > 0 → 6,282 remain
17. Filter: Creatinine (LBXSCR) AND BUN (LBXSBU) complete → 6,277 remain
18. Filter: HDL (LBDHDD) AND Total Cholesterol (LBXTC) complete → 6,277 remain (no change)
19. Assign patient_uid = P_000001 ... P_006277
20. Save cohort flow → data/cohort_flow.csv
21. Save filtered data → data/final_cohort.csv (6,277 rows)

PHASE 6: FIB-4 TARGET CONSTRUCTION
═══════════════════════════════════════════════════════════════════
22. Compute: fib4 = (RIDAGEYR * LBXSASSI) / (LBXPLTSI * sqrt(LBXSATSI))
23. Validate: check no NaN, no Inf, verify statistics match:
      Mean=1.0590, Std=0.7748, Median=0.9028, Min=0.0634, Max=13.9971
24. Save target validation → data/fib4_target_validation.json

PHASE 7: FEATURE LOCKING (Leakage Control)
═══════════════════════════════════════════════════════════════════
25. Exclude from model inputs: RIDAGEYR, LBXSASSI, LBXSATSI, LBXPLTSI
26. Confirm 25-feature model manifest (Experiment 3)
27. Save manifest → data/feature_manifest.json

PHASE 8: FEATURE PREPROCESSING
═══════════════════════════════════════════════════════════════════
28. For each of 5 cross-validation folds:
    a. Split patients into training/validation at patient_uid level
    b. Fit median imputation on training fold only
    c. Apply imputation to both training and validation folds
    d. Fit StandardScaler on training fold only
    e. Apply scaling to both training and validation folds
    (This prevents validation data from influencing preprocessing)

PHASE 9: GRAPH CONSTRUCTION
═══════════════════════════════════════════════════════════════════
29. For each patient in final_cohort.csv:
    a. Create PyTorch Geometric HeteroData object
    b. Assign patient node:   x = tensor([RIAGENDR])
    c. Assign liver node:     x = tensor([GGT, Albumin, Bilirubin, ALP, LUXSMED, LUXCAPM])
    d. Assign kidney node:    x = tensor([Creatinine, BUN, UricAcid, UrineAlb, UrineCr, KIQ022])
    e. Assign heart node:     x = tensor([SysolicBP, DiastolicBP, PulseRate, HDL, TotalChol, BPQ020, MCQ160C, MCQ160E])
    f. Assign biomarker node: x = tensor([WBC, RBC, Hemoglobin, hsCRP])
    g. Create all 14 edge connections (8 patient-organ + 6 inter-organ)
    h. Assign target: data['patient'].y = tensor([fib4_score])
30. Save list of 6,277 HeteroData graphs → graphs/patient_graphs.pt
```

---

## Section 14 — Final Validation Checklist

Use this checklist to verify that a recreated dataset exactly matches the HSGIN project dataset.

### Data Acquisition

- [ ] NHANES cycle is **August 2021–August 2023** (file suffix `_L`)
- [ ] 12 specific XPT files downloaded (DEMO_L, BIOPRO_L, CBC_L, ALB_CR_L, HDL_L, TCHOL_L, HSCRP_L, BPXO_L, LUX_L, BPQ_L, KIQ_U_L, MCQ_L)

### Data Integration

- [ ] All 12 files (plus optional audit-only files) confirm `is_seqn_unique = True`
- [ ] Master patient table has **11,933 rows** before filtering
- [ ] All files merged via left-join on `SEQN`

### Cohort Attrition (check each step)

- [ ] After Step 1 (initial): N = **11,933**
- [ ] After Step 2 (demographics): N = **11,933** (no change)
- [ ] After Step 3 (liver enzymes ALT & AST complete & > 0): N = **6,308**
- [ ] After Step 4 (Platelets complete & > 0): N = **6,282**
- [ ] After Step 5 (Creatinine & BUN complete): N = **6,277**
- [ ] After Step 6 (HDL & Total Cholesterol): N = **6,277** (no change)
- [ ] **Final cohort: N = 6,277** ✅

### FIB-4 Target

- [ ] Formula is: `FIB-4 = (RIDAGEYR × LBXSASSI) / (LBXPLTSI × √LBXSATSI)`
- [ ] N = **6,277** patients have valid FIB-4 scores
- [ ] Mean ≈ **1.0590** ± 0.7748
- [ ] Median ≈ **0.9028**
- [ ] Min ≈ **0.0634**, Max ≈ **13.9971**
- [ ] Skewness ≈ **2.9236**
- [ ] No NaN, no Inf values in target

### Leakage Control

- [ ] `RIDAGEYR` (Age) is **NOT** in the model input feature matrix
- [ ] `LBXSASSI` (AST) is **NOT** in the model input feature matrix
- [ ] `LBXSATSI` (ALT) is **NOT** in the model input feature matrix
- [ ] `LBXPLTSI` (Platelets) is **NOT** in the model input feature matrix
- [ ] Model input feature count = **25** (Experiment 3 locked)

### Feature Manifest

- [ ] 1 Demographics feature: `RIAGENDR`
- [ ] 6 Liver features: `LBXSGTSI`, `LBXSAL`, `LBXSTB`, `LBXSAPSI`, `LUXSMED`, `LUXCAPM`
- [ ] 6 Kidney features: `LBXSCR`, `LBXSBU`, `LBXSUA`, `URXUMA`, `URXUCR`, `KIQ022`
- [ ] 8 Heart features: `BPXOSY1`, `BPXODI1`, `BPXOPLS1`, `LBDHDD`, `LBXTC`, `BPQ020`, `MCQ160C`, `MCQ160E`
- [ ] 4 Biomarker features: `LBXWBCSI`, `LBXRBCSI`, `LBXHGB`, `LBXHSCRP`

### Graph Dataset

- [ ] **5 node types**: `patient` (dim=1), `liver` (dim=6), `kidney` (dim=6), `heart` (dim=8), `biomarker` (dim=4)
- [ ] **14 directed edge types**: 8 patient–organ (bidirectional) + 6 inter-organ (bidirectional liver↔kidney, liver↔heart, kidney↔heart)
- [ ] **No** direct biomarker ↔ organ inter-edges
- [ ] **No** Brain or Gut node types
- [ ] **6,277 graphs** in `graphs/patient_graphs.pt`
- [ ] Each graph has `data['patient'].y` containing the continuous FIB-4 score

### Generated Artifacts

- [ ] `data/master_patient.csv` exists (~11.5 MB)
- [ ] `data/final_cohort.csv` exists (~8.2 MB, 6,277 rows)
- [ ] `data/feature_manifest.json` exists
- [ ] `data/fib4_target_validation.json` exists (validation_gates_passed = true)
- [ ] `data/cohort_flow.csv` exists (6 steps, final N = 6,277)
- [ ] `data/missingness_report.csv` exists (29 variables, all < 30% cohort missing)
- [ ] `data/ingestion_summary.csv` exists (all files show is_seqn_unique = True)
- [ ] `data/experiment_results.json` exists
- [ ] `data/leakage_audit_results.json` exists
- [ ] `graphs/patient_graphs.pt` exists (6,277 HeteroData objects)

---

*Report compiled from project source files: `dataset_report.md`, `FINAL_MASTER_HANDOVER.md`, `leakage_audit_report.md`, `feature_manifest.json`, `cohort_flow.csv`, `missingness_report.csv`, `fib4_target_validation.json`, `ingestion_summary.csv`. Official NHANES website referenced for cycle identification and file format context. All statistics reproduced exactly from project artifacts without modification.*
