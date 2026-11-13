# Complete Repository Folder and File Tree Manifest

**Evaluation Scope**: Full Repository Audit | **Base Path**: `c:\Users\admin_fix\Downloads\3 ORGAN`  
**Total Monitored Files**: 297 | **Integrity Standard**: SHA-256 Cryptographic Fingerprints  
**Status**: `VERIFIED-ON-DISK` (Read-Only Inspection)  

---

## 1. Directory Summary Statistics

| Top-Level Directory | File Count | Total Size (Bytes) | Human-Readable Size | Architectural Role |
| :--- | :---: | :---: | :---: | :--- |
| `NHANES AUG'21 - AUG'23` | 27 | 24,502,480 | 23.37 MB | CDC NHANES 2021-2023 SAS transport (.xpt) source datasets |
| `Root` | 6 | 95,577 | 0.09 MB | Root configuration, requirements, and master PRD markdown files |
| `backups` | 78 | 64,890,374 | 61.88 MB | Immutable baseline snapshot (baseline_v1) and isolation audit scripts |
| `configs` | 6 | 4,402 | 0.00 MB | Experiment-specific JSON hyperparameters and model selection configs |
| `data` | 10 | 20,940,601 | 19.97 MB | Raw and processed patient cohort CSVs, feature manifests, and split JSONs |
| `graphs` | 5 | 20,302,687 | 19.36 MB | Serialized PyG HeteroData graphs (.pt) and topology schema diagrams |
| `reports` | 5 | 121,743 | 0.12 MB | Phase 1/Phase 2 dataset reports, leakage audits, and handover documents |
| `results` | 112 | 25,848,552 | 24.65 MB | Phase 0-9 experiment results JSONs, OOF prediction CSVs, and statistical tests |
| `src` | 45 | 438,846 | 0.42 MB | End-to-end Python source pipeline, models, adapters, and experiment runners |
| `tests` | 3 | 3,884 | 0.00 MB | Automated unit test suite verifying leakage, splits, and preservation |

---

## 2. Visual Directory Hierarchy

```text
3 ORGAN/
├── backups/                          # Snapshot preservation & audits
│   ├── baseline_v1/                  # Immutable snapshot of 68 baseline assets (100% matched)
│   └── *.py                          # Phase 3-5 isolation and verification scripts
├── configs/                          # Experiment configuration files
│   └── comparative/                  # Subdirectories for Exp 3, 4, 5, 6, 7, 8
├── data/                             # Data artifacts
│   ├── comparative/                  # Versioned patient fold splits (folds_v1.json)
│   ├── final_cohort.csv              # Locked 6,277-patient cohort
│   ├── master_patient.csv            # Joined 11,933-patient raw table
│   └── *.csv / *.json                # Manifests, cohort flow, leakage reports
├── graphs/                           # Graph representations
│   ├── patient_graphs.pt             # Serialized HeteroData for 6,277 patients (19.39 MB)
│   └── *.png / *.html                # Schema visualizers and interactive graphs
├── NHANES AUG'21 - AUG'23/          # Raw CDC SAS Transport files (27 XPT files)
│   ├── DEMO G/                       # Demographics (DEMO_L.xpt)
│   ├── EXAMINATION/                  # Examination modules (BMX, BPXO, LUX)
│   ├── LABORATORY/                   # Laboratory panels (14 files: enzymes, CBC, etc.)
│   └── QUESTIONNAIRE/                # Clinical questionnaires (9 files: BPQ, MCQ, etc.)
├── reports/                          # Narrative reports and historical handovers
├── results/                          # Comparative experiment outputs
│   └── comparative/                  # Exp 0 to Exp 9 results JSONs and OOF CSVs
├── src/                              # Core codebase
│   ├── comparative/                  # Experiments 0-9 runners, adapters, metrics, splits
│   ├── models/                       # HSGIN & baseline model definitions
│   └── *.py                          # Data ingestion, cohort, target, graph pipeline
├── tests/                            # Automated unit tests (leakage, splits, preservation)
├── technical_evidence_package/       # Read-only authoritative technical evidence package
└── *.md / *.txt / *.py               # Top-level PRD, README, requirements
```

---

## 3. Complete File Inventory and Cryptographic Fingerprints

| # | Relative File Path | Size (Bytes) | SHA-256 Checksum | Category |
| :---: | :--- | :---: | :--- | :--- |
| 1 | [`.gitignore`](file:///.gitignore) | 325 | `e0c55daf2f5c03310f55b4cb743464dd34a309893f799de3875968fb1c3d4812` | Root |
| 2 | [`HSGIN_3_Organ_Training_Pipeline_PRD.md`](file:///HSGIN_3_Organ_Training_Pipeline_PRD.md) | 12,101 | `b7761b731db0799f374f775330e716a1cc8de44cac2fc45ada676be4dff519bd` | Root |
| 3 | [`NHANES AUG'21 - AUG'23/DEMO G/DEMO_L.xpt`](file:///NHANES AUG'21 - AUG'23/DEMO G/DEMO_L.xpt) | 2,582,160 | `ca4374a158b493b8b0163e1388da21d57a18d1b9cecff2aa4e2fa2bec494fe23` | NHANES AUG'21 - AUG'23 |
| 4 | [`NHANES AUG'21 - AUG'23/EXAMINATION/BMX_L.xpt`](file:///NHANES AUG'21 - AUG'23/EXAMINATION/BMX_L.xpt) | 1,563,200 | `44440c416d9ad709e8b1708a5975378ab4d5b18edc39eb5015c2ae7186500170` | NHANES AUG'21 - AUG'23 |
| 5 | [`NHANES AUG'21 - AUG'23/EXAMINATION/BPXO_L.xpt`](file:///NHANES AUG'21 - AUG'23/EXAMINATION/BPXO_L.xpt) | 696,720 | `189aa9bed689d2c69cf8d780b01de85073276fea5694dd52cdf696229f9054a6` | NHANES AUG'21 - AUG'23 |
| 6 | [`NHANES AUG'21 - AUG'23/EXAMINATION/LUX_L.xpt`](file:///NHANES AUG'21 - AUG'23/EXAMINATION/LUX_L.xpt) | 765,680 | `40e49c5f1b58054e4787cd59cdeb224cd7658784b760274c3449bd4c1eb64c34` | NHANES AUG'21 - AUG'23 |
| 7 | [`NHANES AUG'21 - AUG'23/LABORATORY/ALB_CR_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/ALB_CR_L.xpt) | 545,440 | `fc011a80d14419884559372a3196f0a268b494f4f2fa972d00be1f3a23ba3c41` | NHANES AUG'21 - AUG'23 |
| 8 | [`NHANES AUG'21 - AUG'23/LABORATORY/BIOPRO_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/BIOPRO_L.xpt) | 2,425,520 | `912b345aad6b71d53a3bc299a7f3bb0d5530e9fa5b6e76d2d00103979861a476` | NHANES AUG'21 - AUG'23 |
| 9 | [`NHANES AUG'21 - AUG'23/LABORATORY/CBC_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/CBC_L.xpt) | 1,609,840 | `4405da2a5899dcd11e3ef4dbec0b4d2fca6d736a3efa7a85afee668baa95923f` | NHANES AUG'21 - AUG'23 |
| 10 | [`NHANES AUG'21 - AUG'23/LABORATORY/GHB_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/GHB_L.xpt) | 174,000 | `67aee0353160e2392dc0a33bece99b90764a630c76d82415ac4639105ad9dd03` | NHANES AUG'21 - AUG'23 |
| 11 | [`NHANES AUG'21 - AUG'23/LABORATORY/GLU_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/GLU_L.xpt) | 129,200 | `70f773ab37e3d8485341f32137e280e05b9279e5fe9b6f0362e4052d8fe9a201` | NHANES AUG'21 - AUG'23 |
| 12 | [`NHANES AUG'21 - AUG'23/LABORATORY/HDL_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/HDL_L.xpt) | 259,520 | `c1bb43df5ca366f470b411c043f4aee7ae6552a7f4bca1178bc87b24fb9a7300` | NHANES AUG'21 - AUG'23 |
| 13 | [`NHANES AUG'21 - AUG'23/LABORATORY/HEPA_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/HEPA_L.xpt) | 207,920 | `0eacb9b1b0bce97ac85aa5df1f95f78aca36bff72c9f07ba70a9d381579b5517` | NHANES AUG'21 - AUG'23 |
| 14 | [`NHANES AUG'21 - AUG'23/LABORATORY/HEPBD_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/HEPBD_L.xpt) | 324,160 | `e2828da40dbca482a784a5aa2971bb7923fe43b4199bf7953290a3fb9ff01982` | NHANES AUG'21 - AUG'23 |
| 15 | [`NHANES AUG'21 - AUG'23/LABORATORY/HEPC_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/HEPC_L.xpt) | 324,160 | `ccdbbec2d51adc948fc4db9f328721c734ed74eac4b33dbba6ed643870231b83` | NHANES AUG'21 - AUG'23 |
| 16 | [`NHANES AUG'21 - AUG'23/LABORATORY/HEPE_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/HEPE_L.xpt) | 259,520 | `6753e7540a7a76a0e2e16aaf85b036e38ac34b9c6e620aebec95592724f5194b` | NHANES AUG'21 - AUG'23 |
| 17 | [`NHANES AUG'21 - AUG'23/LABORATORY/HSCRP_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/HSCRP_L.xpt) | 280,560 | `c56098d7c33509087a4645dfdf39936c14213d9123e1e718831a10d5bc4e3a1b` | NHANES AUG'21 - AUG'23 |
| 18 | [`NHANES AUG'21 - AUG'23/LABORATORY/INS_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/INS_L.xpt) | 161,280 | `cdbf53b644805e5e67725c81ee32048dad3c06687689435b042a7a144cb9ec65` | NHANES AUG'21 - AUG'23 |
| 19 | [`NHANES AUG'21 - AUG'23/LABORATORY/TCHOL_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/TCHOL_L.xpt) | 259,520 | `5c3312e555bb0706fd97cbd63fcbc9e78f00bda8d2d149732d9dd368169b25d3` | NHANES AUG'21 - AUG'23 |
| 20 | [`NHANES AUG'21 - AUG'23/LABORATORY/TRIGLY_L.xpt`](file:///NHANES AUG'21 - AUG'23/LABORATORY/TRIGLY_L.xpt) | 321,840 | `77679864c33b98d9b6db528f3a0ac0a15ea34bde9731c04d23bc9801277975f4` | NHANES AUG'21 - AUG'23 |
| 21 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/BPQ_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/BPQ_L.xpt) | 409,680 | `0acde3af0526c375942fe0735e3bf69a0422bcbc606f98a478209d2f47baa4b5` | NHANES AUG'21 - AUG'23 |
| 22 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DBQ_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DBQ_L.xpt) | 2,582,160 | `774ead4e3b8d4ec90e464dc77d8eed3fb20e5eb2899e78dc98b3100ab98d1c88` | NHANES AUG'21 - AUG'23 |
| 23 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DIQ_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DIQ_L.xpt) | 847,600 | `9535a023673ae869afae19d842d8679e06f6a464606ac15900686b41ef05090f` | NHANES AUG'21 - AUG'23 |
| 24 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DPQ_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DPQ_L.xpt) | 560,000 | `25605a02685035fe997477b31a0991cca2776b0f72f24a8e61ac5b018456304b` | NHANES AUG'21 - AUG'23 |
| 25 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/FNQ_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/FNQ_L.xpt) | 2,806,400 | `d140701b0ae0e6a1711bd63a2f64589ca9cb59c6247603e80c0b9d7dcc24eb29` | NHANES AUG'21 - AUG'23 |
| 26 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/HEQ_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/HEQ_L.xpt) | 172,240 | `0d515ca8d8666618b6d007d1a29185266ab4f6ee4ecaa4db92cab53d453eb541` | NHANES AUG'21 - AUG'23 |
| 27 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/KIQ_U_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/KIQ_U_L.xpt) | 564,320 | `2f114aeee6e9c7bc9381729b95a6685e28f35c3fbc26558ca8b9458bf4bf3437` | NHANES AUG'21 - AUG'23 |
| 28 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/MCQ_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/MCQ_L.xpt) | 3,294,000 | `0889bb3eaa5adedf1a11c4af2d4776fc4c4c3cfdeea24fcedb77c4636b478f61` | NHANES AUG'21 - AUG'23 |
| 29 | [`NHANES AUG'21 - AUG'23/QUESTIONNAIRE/SLQ_L.xpt`](file:///NHANES AUG'21 - AUG'23/QUESTIONNAIRE/SLQ_L.xpt) | 375,840 | `918c3258b2f466ac1cae55ea45330c736dbdc573ee4dc72306e3d2b222764741` | NHANES AUG'21 - AUG'23 |
| 30 | [`PRD Comparative Evaluation of Machine Learning, Deep Learning, and Graph Neural.md`](file:///PRD Comparative Evaluation of Machine Learning, Deep Learning, and Graph Neural.md) | 67,849 | `1ba2b61b79e7b6b3e7e39ffde3a8b9e71c1ecfb8da4c87c2278000fe328850da` | Root |
| 31 | [`README.md`](file:///README.md) | 9,331 | `9f56e4c82cf120793505d350cb3ccda67fcab3830c284135a81b52a3946c5e59` | Root |
| 32 | [`backups/audit_outer_fold_isolation.py`](file:///backups/audit_outer_fold_isolation.py) | 2,913 | `f6068afe60430f510861432f0370021e1fbdc8bca8a0c5bb7e5d435fe75c663b` | backups |
| 33 | [`backups/baseline_v1/.gitignore`](file:///backups/baseline_v1/.gitignore) | 203 | `97200ba2bb7fd311a79895f2718b0a66ebccd48b75bedb2882eab274e5e9aa03` | backups |
| 34 | [`backups/baseline_v1/HSGIN_3_Organ_Training_Pipeline_PRD.md`](file:///backups/baseline_v1/HSGIN_3_Organ_Training_Pipeline_PRD.md) | 12,101 | `b7761b731db0799f374f775330e716a1cc8de44cac2fc45ada676be4dff519bd` | backups |
| 35 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/DEMO G/DEMO_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/DEMO G/DEMO_L.xpt) | 2,582,160 | `ca4374a158b493b8b0163e1388da21d57a18d1b9cecff2aa4e2fa2bec494fe23` | backups |
| 36 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/EXAMINATION/BMX_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/EXAMINATION/BMX_L.xpt) | 1,563,200 | `44440c416d9ad709e8b1708a5975378ab4d5b18edc39eb5015c2ae7186500170` | backups |
| 37 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/EXAMINATION/BPXO_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/EXAMINATION/BPXO_L.xpt) | 696,720 | `189aa9bed689d2c69cf8d780b01de85073276fea5694dd52cdf696229f9054a6` | backups |
| 38 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/EXAMINATION/LUX_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/EXAMINATION/LUX_L.xpt) | 765,680 | `40e49c5f1b58054e4787cd59cdeb224cd7658784b760274c3449bd4c1eb64c34` | backups |
| 39 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/ALB_CR_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/ALB_CR_L.xpt) | 545,440 | `fc011a80d14419884559372a3196f0a268b494f4f2fa972d00be1f3a23ba3c41` | backups |
| 40 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/BIOPRO_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/BIOPRO_L.xpt) | 2,425,520 | `912b345aad6b71d53a3bc299a7f3bb0d5530e9fa5b6e76d2d00103979861a476` | backups |
| 41 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/CBC_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/CBC_L.xpt) | 1,609,840 | `4405da2a5899dcd11e3ef4dbec0b4d2fca6d736a3efa7a85afee668baa95923f` | backups |
| 42 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/GHB_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/GHB_L.xpt) | 174,000 | `67aee0353160e2392dc0a33bece99b90764a630c76d82415ac4639105ad9dd03` | backups |
| 43 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/GLU_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/GLU_L.xpt) | 129,200 | `70f773ab37e3d8485341f32137e280e05b9279e5fe9b6f0362e4052d8fe9a201` | backups |
| 44 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HDL_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HDL_L.xpt) | 259,520 | `c1bb43df5ca366f470b411c043f4aee7ae6552a7f4bca1178bc87b24fb9a7300` | backups |
| 45 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HEPA_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HEPA_L.xpt) | 207,920 | `0eacb9b1b0bce97ac85aa5df1f95f78aca36bff72c9f07ba70a9d381579b5517` | backups |
| 46 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HEPBD_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HEPBD_L.xpt) | 324,160 | `e2828da40dbca482a784a5aa2971bb7923fe43b4199bf7953290a3fb9ff01982` | backups |
| 47 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HEPC_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HEPC_L.xpt) | 324,160 | `ccdbbec2d51adc948fc4db9f328721c734ed74eac4b33dbba6ed643870231b83` | backups |
| 48 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HEPE_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HEPE_L.xpt) | 259,520 | `6753e7540a7a76a0e2e16aaf85b036e38ac34b9c6e620aebec95592724f5194b` | backups |
| 49 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HSCRP_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/HSCRP_L.xpt) | 280,560 | `c56098d7c33509087a4645dfdf39936c14213d9123e1e718831a10d5bc4e3a1b` | backups |
| 50 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/INS_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/INS_L.xpt) | 161,280 | `cdbf53b644805e5e67725c81ee32048dad3c06687689435b042a7a144cb9ec65` | backups |
| 51 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/TCHOL_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/TCHOL_L.xpt) | 259,520 | `5c3312e555bb0706fd97cbd63fcbc9e78f00bda8d2d149732d9dd368169b25d3` | backups |
| 52 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/TRIGLY_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/LABORATORY/TRIGLY_L.xpt) | 321,840 | `77679864c33b98d9b6db528f3a0ac0a15ea34bde9731c04d23bc9801277975f4` | backups |
| 53 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/BPQ_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/BPQ_L.xpt) | 409,680 | `0acde3af0526c375942fe0735e3bf69a0422bcbc606f98a478209d2f47baa4b5` | backups |
| 54 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DBQ_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DBQ_L.xpt) | 2,582,160 | `774ead4e3b8d4ec90e464dc77d8eed3fb20e5eb2899e78dc98b3100ab98d1c88` | backups |
| 55 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DIQ_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DIQ_L.xpt) | 847,600 | `9535a023673ae869afae19d842d8679e06f6a464606ac15900686b41ef05090f` | backups |
| 56 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DPQ_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DPQ_L.xpt) | 560,000 | `25605a02685035fe997477b31a0991cca2776b0f72f24a8e61ac5b018456304b` | backups |
| 57 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/FNQ_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/FNQ_L.xpt) | 2,806,400 | `d140701b0ae0e6a1711bd63a2f64589ca9cb59c6247603e80c0b9d7dcc24eb29` | backups |
| 58 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/HEQ_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/HEQ_L.xpt) | 172,240 | `0d515ca8d8666618b6d007d1a29185266ab4f6ee4ecaa4db92cab53d453eb541` | backups |
| 59 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/KIQ_U_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/KIQ_U_L.xpt) | 564,320 | `2f114aeee6e9c7bc9381729b95a6685e28f35c3fbc26558ca8b9458bf4bf3437` | backups |
| 60 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/MCQ_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/MCQ_L.xpt) | 3,294,000 | `0889bb3eaa5adedf1a11c4af2d4776fc4c4c3cfdeea24fcedb77c4636b478f61` | backups |
| 61 | [`backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/SLQ_L.xpt`](file:///backups/baseline_v1/NHANES AUG'21 - AUG'23/QUESTIONNAIRE/SLQ_L.xpt) | 375,840 | `918c3258b2f466ac1cae55ea45330c736dbdc573ee4dc72306e3d2b222764741` | backups |
| 62 | [`backups/baseline_v1/PRD Comparative Evaluation of Machine Learning, Deep Learning, and Graph Neural.md`](file:///backups/baseline_v1/PRD Comparative Evaluation of Machine Learning, Deep Learning, and Graph Neural.md) | 67,849 | `1ba2b61b79e7b6b3e7e39ffde3a8b9e71c1ecfb8da4c87c2278000fe328850da` | backups |
| 63 | [`backups/baseline_v1/README.md`](file:///backups/baseline_v1/README.md) | 9,331 | `9f56e4c82cf120793505d350cb3ccda67fcab3830c284135a81b52a3946c5e59` | backups |
| 64 | [`backups/baseline_v1/checksum_report.md`](file:///backups/baseline_v1/checksum_report.md) | 16,202 | `8a45b21f1278c3f8fd3ffd31b73bd4aefb40589a74bf32a3a1fbe53d6bc1716f` | backups |
| 65 | [`backups/baseline_v1/data/cohort_flow.csv`](file:///backups/baseline_v1/data/cohort_flow.csv) | 451 | `c2c6ad7d54929caa1cdb13c6f0576fd60f85705afeae243ef9e42da71e7305c1` | backups |
| 66 | [`backups/baseline_v1/data/experiment_results.json`](file:///backups/baseline_v1/data/experiment_results.json) | 8,506 | `a9db2276afc1f50d2e9817724e14da88a6b62914feec059c0117dabe3271315d` | backups |
| 67 | [`backups/baseline_v1/data/feature_manifest.json`](file:///backups/baseline_v1/data/feature_manifest.json) | 4,956 | `6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22` | backups |
| 68 | [`backups/baseline_v1/data/fib4_target_validation.json`](file:///backups/baseline_v1/data/fib4_target_validation.json) | 570 | `85560c93d75d3990a8d2bb2f984439004aaeb8b9d28d6e63bbc94bb1e5346e9d` | backups |
| 69 | [`backups/baseline_v1/data/final_cohort.csv`](file:///backups/baseline_v1/data/final_cohort.csv) | 8,183,972 | `7d9f30deb21b4c49683b96a62d6866fedd8877f3c60b8c03d208f699c6c5ca1f` | backups |
| 70 | [`backups/baseline_v1/data/ingestion_summary.csv`](file:///backups/baseline_v1/data/ingestion_summary.csv) | 1,708 | `d87cba4449124fdccd2f7bd3aadf34c9a3de363c76d00fcf6efe2cb4ea365cda` | backups |
| 71 | [`backups/baseline_v1/data/leakage_audit_results.json`](file:///backups/baseline_v1/data/leakage_audit_results.json) | 6,114 | `8708f98f9a383357c739b4d6f71e7cdb99a5a7ed08080bdde19a935e6995cd9b` | backups |
| 72 | [`backups/baseline_v1/data/master_patient.csv`](file:///backups/baseline_v1/data/master_patient.csv) | 11,537,773 | `b1682cb1d0ad083a2d8e7749f826a9c078169925a8f9914eae2460f12d1a111d` | backups |
| 73 | [`backups/baseline_v1/data/missingness_report.csv`](file:///backups/baseline_v1/data/missingness_report.csv) | 2,709 | `d53a9ab11a44aac59660bda612fbabdfa9eeee1833c6cd64cf2753298735a5d7` | backups |
| 74 | [`backups/baseline_v1/generate_dataset_report.py`](file:///backups/baseline_v1/generate_dataset_report.py) | 5,823 | `425be2f2933c71f547b32fe95acc8a0f44692f6e1fec9f73c55d2b53c6e44b8b` | backups |
| 75 | [`backups/baseline_v1/graphs/.gitkeep`](file:///backups/baseline_v1/graphs/.gitkeep) | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | backups |
| 76 | [`backups/baseline_v1/graphs/hsgin_hetero_schema.png`](file:///backups/baseline_v1/graphs/hsgin_hetero_schema.png) | 381,983 | `83e0a0a40d093c35311f66028f809a661168d37873e93ea06931e4ac397822d1` | backups |
| 77 | [`backups/baseline_v1/graphs/hsgin_interactive_graph.html`](file:///backups/baseline_v1/graphs/hsgin_interactive_graph.html) | 5,304 | `f16071babdb2de5c9a272cf625ea472c07253eab589adca847c25366e0da39ff` | backups |
| 78 | [`backups/baseline_v1/graphs/patient_graph_sample.png`](file:///backups/baseline_v1/graphs/patient_graph_sample.png) | 522,237 | `ad7273010a6d5fbdcb8403851cce3fc6f59d543bb952c5160294a5165473680d` | backups |
| 79 | [`backups/baseline_v1/graphs/patient_graphs.pt`](file:///backups/baseline_v1/graphs/patient_graphs.pt) | 19,393,163 | `4bffe0406004b951b3db848c7d92bd4183d4b2530a523a38f885e6dc21324145` | backups |
| 80 | [`backups/baseline_v1/reports/FINAL_MASTER_HANDOVER.md`](file:///backups/baseline_v1/reports/FINAL_MASTER_HANDOVER.md) | 39,121 | `d0e5921534f0b389222487fb1f36f4efa33e692c5bbf3a2033a3f23c3227fb87` | backups |
| 81 | [`backups/baseline_v1/reports/NHANES_Dataset_Report.md`](file:///backups/baseline_v1/reports/NHANES_Dataset_Report.md) | 56,683 | `158a6c74837a3d0c3bb61c442e161173b842014d2f8c16a7ffd0efa97e7142ad` | backups |
| 82 | [`backups/baseline_v1/reports/dataset_report.md`](file:///backups/baseline_v1/reports/dataset_report.md) | 8,498 | `13e916e007c91109da53fcc3e1ab69152251e26faa323494b14e793ea2ee9f74` | backups |
| 83 | [`backups/baseline_v1/reports/experiment_report.md`](file:///backups/baseline_v1/reports/experiment_report.md) | 10,431 | `5b3beab98a0a6ed77c4fabcf76c1cd372076b425608a85a240934ab5268ca81f` | backups |
| 84 | [`backups/baseline_v1/reports/leakage_audit_report.md`](file:///backups/baseline_v1/reports/leakage_audit_report.md) | 7,010 | `0a0be1d62e2a7fcf09481ba145123eb51e0613cabb5bb1ed0a5ee8b60fc1ec3e` | backups |
| 85 | [`backups/baseline_v1/requirements.txt`](file:///backups/baseline_v1/requirements.txt) | 148 | `1905b7e1b7d7c9896723e378bd7575cd3359cb39d1f80035c0e821d596c80d5f` | backups |
| 86 | [`backups/baseline_v1/src/ablation.py`](file:///backups/baseline_v1/src/ablation.py) | 3,182 | `60b8f96b3ef57652ef975a8c2702ef7d1f12d7d18683da8ee6664820c7fba9a6` | backups |
| 87 | [`backups/baseline_v1/src/audit.py`](file:///backups/baseline_v1/src/audit.py) | 5,124 | `89c97e7b72ee7fe033e58e304a7ee818f8c21f9e3be4954ff018ad20d5f7ccd8` | backups |
| 88 | [`backups/baseline_v1/src/cohort.py`](file:///backups/baseline_v1/src/cohort.py) | 3,417 | `3dce6eb21e6e6010c8d278617cc6dff3a0493c7bbc5032b2ce4c7af47ff8bb98` | backups |
| 89 | [`backups/baseline_v1/src/dataset.py`](file:///backups/baseline_v1/src/dataset.py) | 5,121 | `15e8c409fd854a5b0b6225ceda32b46760010daae0e4fa2a814513011a3bd3a1` | backups |
| 90 | [`backups/baseline_v1/src/draw_schema_diagram.py`](file:///backups/baseline_v1/src/draw_schema_diagram.py) | 3,468 | `bab78eac5e82d6602325a4e6ae661916e165f6eef5a434d5dc2abba86fe14205` | backups |
| 91 | [`backups/baseline_v1/src/graph_builder.py`](file:///backups/baseline_v1/src/graph_builder.py) | 4,692 | `b4ee2b472d52c77964c164344bcaf8268540c2af62e459d98e05d06f07f9e69e` | backups |
| 92 | [`backups/baseline_v1/src/hsgin_ablation.py`](file:///backups/baseline_v1/src/hsgin_ablation.py) | 7,308 | `a437f2b4582d60048e7bd7709760adbab888de4dc03446bb6734cfd71ea7e793` | backups |
| 93 | [`backups/baseline_v1/src/leakage_audit.py`](file:///backups/baseline_v1/src/leakage_audit.py) | 11,338 | `ac908022cc2818e450cce322714c10e9961cf2923363f1322cf81c2d6199a500` | backups |
| 94 | [`backups/baseline_v1/src/models/baselines.py`](file:///backups/baseline_v1/src/models/baselines.py) | 3,903 | `2e24f4e6b8cedfa0a0c949847b66e8be9925478cbdd9de394d0422161c51a39e` | backups |
| 95 | [`backups/baseline_v1/src/models/hsgin.py`](file:///backups/baseline_v1/src/models/hsgin.py) | 4,720 | `4d9bd5a8372e3eb9d234701fb7d8885efa2f087ddb95f807488e04ad9ac65b6d` | backups |
| 96 | [`backups/baseline_v1/src/pipeline.py`](file:///backups/baseline_v1/src/pipeline.py) | 3,660 | `24d33b42b5971d98016765434ecefd703f0e65c97fcd518f43c3378c3a0ae328` | backups |
| 97 | [`backups/baseline_v1/src/target.py`](file:///backups/baseline_v1/src/target.py) | 3,714 | `680b957a2c93813ca04e7b65c393c06461a6efb1521ed92473fe66fa4d8dd26c` | backups |
| 98 | [`backups/baseline_v1/src/train.py`](file:///backups/baseline_v1/src/train.py) | 10,711 | `a0e466d39ae83d0893b11333e61ae0d7908882ae31eaa353d2d05a5d559bdcce` | backups |
| 99 | [`backups/baseline_v1/src/visualize_graph.py`](file:///backups/baseline_v1/src/visualize_graph.py) | 3,649 | `7ae9e3e3a5d0206c8a9631dd83586b92ea32ae147b62f3a65852c5816f49c159` | backups |
| 100 | [`backups/baseline_v1/src/visualize_interactive.py`](file:///backups/baseline_v1/src/visualize_interactive.py) | 6,267 | `3d849fffdb5a8361ca9bcb8366137ab9c230ed1b6e1785af5e5006b489e49c23` | backups |
| 101 | [`backups/baseline_v1/src/y_randomization.py`](file:///backups/baseline_v1/src/y_randomization.py) | 2,607 | `3c0b0379243e07be14d4933300c1a61630e34fbfdd5acf873cfc2f39b44b70e9` | backups |
| 102 | [`backups/check_exp5_json.py`](file:///backups/check_exp5_json.py) | 395 | `0bb28c0cb8f1b69d87e64ab6cf87b842db8202d8be6a68e51bda52e9107f398c` | backups |
| 103 | [`backups/check_metrics.py`](file:///backups/check_metrics.py) | 1,606 | `0fb333bff5a97aa3d747c12b9503e7e51097397628f2e37b3728f151f2d1e1e0` | backups |
| 104 | [`backups/test_inner_fitting.py`](file:///backups/test_inner_fitting.py) | 3,057 | `b3d50ce1cb88ff413cf329d1d797a8dddde5931a415c10a366c29a9e50185b5f` | backups |
| 105 | [`backups/test_stacking_leakage.py`](file:///backups/test_stacking_leakage.py) | 6,092 | `47b07921ef3e377476008af019e72675e9b4cff594a3c977ae654ffec69b2666` | backups |
| 106 | [`backups/update_ft_inner_predictions.py`](file:///backups/update_ft_inner_predictions.py) | 3,742 | `d47e9e812470bdda375cdb6343dd8ae374bacadeeb620292e307dd49ed243096` | backups |
| 107 | [`backups/verify_exp1.py`](file:///backups/verify_exp1.py) | 1,795 | `b1a4c6010ae5ebc522b3f5d8bbe064d22e5c83f4ee2c250a5865d5304e60b87e` | backups |
| 108 | [`backups/verify_exp2.py`](file:///backups/verify_exp2.py) | 1,597 | `bf3538f7aeee1e517e68ba8580f3fad2536ba16021f7d263e2439b82689dcab9` | backups |
| 109 | [`backups/verify_phase3_pre.py`](file:///backups/verify_phase3_pre.py) | 970 | `17bc9584cb2a3d298561e75ac41a39593367b248c57a07814e75d31d21062c46` | backups |
| 110 | [`configs/comparative/exp3_deep_tabular/deep_tabular_configs.json`](file:///configs/comparative/exp3_deep_tabular/deep_tabular_configs.json) | 612 | `23db568088767124b33057fe25cd127820fcd991eca57ba59321d73cb73b4005` | configs |
| 111 | [`configs/comparative/exp4_gnn/gnn_configs.json`](file:///configs/comparative/exp4_gnn/gnn_configs.json) | 292 | `5ac98dfdd1d189889c3ae1eb2cc0f8599792775997f759f1c2bb9603b86fc532` | configs |
| 112 | [`configs/comparative/exp5_ensemble/base_model_selection.json`](file:///configs/comparative/exp5_ensemble/base_model_selection.json) | 728 | `6d56f58e7b120e1f12d84fdf132ac376a5d90999dc4a0373911bc9477e4752b1` | configs |
| 113 | [`configs/comparative/exp6_ablations/exp6_config.json`](file:///configs/comparative/exp6_ablations/exp6_config.json) | 593 | `26627822f75c89cc18360dbb220d8117493133c55a97e01c5d7510c27d059553` | configs |
| 114 | [`configs/comparative/exp6_ablations/exp7_config.json`](file:///configs/comparative/exp6_ablations/exp7_config.json) | 1,395 | `5a4fb6cca78acc9a7bc80ae813628e274966b3ef7370e2bcc8c9480153fce96c` | configs |
| 115 | [`configs/comparative/exp8_controls/exp8_config.json`](file:///configs/comparative/exp8_controls/exp8_config.json) | 782 | `9ef32f848509febc5d20682da356559009e37ab6e01aabec76e90a7d737729fe` | configs |
| 116 | [`data/cohort_flow.csv`](file:///data/cohort_flow.csv) | 451 | `c2c6ad7d54929caa1cdb13c6f0576fd60f85705afeae243ef9e42da71e7305c1` | data |
| 117 | [`data/comparative/folds_v1.json`](file:///data/comparative/folds_v1.json) | 1,193,842 | `226b731be71e246942c3378c02182b9de5a9a1a02cf2742418fa0d343152cfe8` | data |
| 118 | [`data/experiment_results.json`](file:///data/experiment_results.json) | 8,506 | `a9db2276afc1f50d2e9817724e14da88a6b62914feec059c0117dabe3271315d` | data |
| 119 | [`data/feature_manifest.json`](file:///data/feature_manifest.json) | 4,956 | `6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22` | data |
| 120 | [`data/fib4_target_validation.json`](file:///data/fib4_target_validation.json) | 570 | `85560c93d75d3990a8d2bb2f984439004aaeb8b9d28d6e63bbc94bb1e5346e9d` | data |
| 121 | [`data/final_cohort.csv`](file:///data/final_cohort.csv) | 8,183,972 | `7d9f30deb21b4c49683b96a62d6866fedd8877f3c60b8c03d208f699c6c5ca1f` | data |
| 122 | [`data/ingestion_summary.csv`](file:///data/ingestion_summary.csv) | 1,708 | `d87cba4449124fdccd2f7bd3aadf34c9a3de363c76d00fcf6efe2cb4ea365cda` | data |
| 123 | [`data/leakage_audit_results.json`](file:///data/leakage_audit_results.json) | 6,114 | `8708f98f9a383357c739b4d6f71e7cdb99a5a7ed08080bdde19a935e6995cd9b` | data |
| 124 | [`data/master_patient.csv`](file:///data/master_patient.csv) | 11,537,773 | `b1682cb1d0ad083a2d8e7749f826a9c078169925a8f9914eae2460f12d1a111d` | data |
| 125 | [`data/missingness_report.csv`](file:///data/missingness_report.csv) | 2,709 | `d53a9ab11a44aac59660bda612fbabdfa9eeee1833c6cd64cf2753298735a5d7` | data |
| 126 | [`generate_dataset_report.py`](file:///generate_dataset_report.py) | 5,823 | `425be2f2933c71f547b32fe95acc8a0f44692f6e1fec9f73c55d2b53c6e44b8b` | Root |
| 127 | [`graphs/.gitkeep`](file:///graphs/.gitkeep) | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | graphs |
| 128 | [`graphs/hsgin_hetero_schema.png`](file:///graphs/hsgin_hetero_schema.png) | 381,983 | `83e0a0a40d093c35311f66028f809a661168d37873e93ea06931e4ac397822d1` | graphs |
| 129 | [`graphs/hsgin_interactive_graph.html`](file:///graphs/hsgin_interactive_graph.html) | 5,304 | `f16071babdb2de5c9a272cf625ea472c07253eab589adca847c25366e0da39ff` | graphs |
| 130 | [`graphs/patient_graph_sample.png`](file:///graphs/patient_graph_sample.png) | 522,237 | `ad7273010a6d5fbdcb8403851cce3fc6f59d543bb952c5160294a5165473680d` | graphs |
| 131 | [`graphs/patient_graphs.pt`](file:///graphs/patient_graphs.pt) | 19,393,163 | `4bffe0406004b951b3db848c7d92bd4183d4b2530a523a38f885e6dc21324145` | graphs |
| 132 | [`reports/FINAL_MASTER_HANDOVER.md`](file:///reports/FINAL_MASTER_HANDOVER.md) | 39,121 | `d0e5921534f0b389222487fb1f36f4efa33e692c5bbf3a2033a3f23c3227fb87` | reports |
| 133 | [`reports/NHANES_Dataset_Report.md`](file:///reports/NHANES_Dataset_Report.md) | 56,683 | `158a6c74837a3d0c3bb61c442e161173b842014d2f8c16a7ffd0efa97e7142ad` | reports |
| 134 | [`reports/dataset_report.md`](file:///reports/dataset_report.md) | 8,498 | `13e916e007c91109da53fcc3e1ab69152251e26faa323494b14e793ea2ee9f74` | reports |
| 135 | [`reports/experiment_report.md`](file:///reports/experiment_report.md) | 10,431 | `5b3beab98a0a6ed77c4fabcf76c1cd372076b425608a85a240934ab5268ca81f` | reports |
| 136 | [`reports/leakage_audit_report.md`](file:///reports/leakage_audit_report.md) | 7,010 | `0a0be1d62e2a7fcf09481ba145123eb51e0613cabb5bb1ed0a5ee8b60fc1ec3e` | reports |
| 137 | [`requirements.txt`](file:///requirements.txt) | 148 | `1905b7e1b7d7c9896723e378bd7575cd3359cb39d1f80035c0e821d596c80d5f` | Root |
| 138 | [`results/comparative/exp0_reproduction/Classical_HGNN_oof_predictions.csv`](file:///results/comparative/exp0_reproduction/Classical_HGNN_oof_predictions.csv) | 356,385 | `9f73c2b45a72c1dbe75c31e9a2369852583562e082439f39bec32b7cb1f86ca3` | results |
| 139 | [`results/comparative/exp0_reproduction/HSGIN_oof_predictions.csv`](file:///results/comparative/exp0_reproduction/HSGIN_oof_predictions.csv) | 356,487 | `f77905f95b8d944ff53ddac99b72aca88b3b367889978036c2e6858c1e6b11d8` | results |
| 140 | [`results/comparative/exp0_reproduction/MLP_Regressor_oof_predictions.csv`](file:///results/comparative/exp0_reproduction/MLP_Regressor_oof_predictions.csv) | 355,431 | `5eab3f9121644d0a8cde7a39a5c840433de72d5b4a571d09e805b8af47c2ff0d` | results |
| 141 | [`results/comparative/exp0_reproduction/Random_Forest_oof_predictions.csv`](file:///results/comparative/exp0_reproduction/Random_Forest_oof_predictions.csv) | 354,772 | `8c383e74ee3ba355418845bac98456e54bc834ec1a4f9536da4ab98d950fca55` | results |
| 142 | [`results/comparative/exp0_reproduction/Ridge_Regression_oof_predictions.csv`](file:///results/comparative/exp0_reproduction/Ridge_Regression_oof_predictions.csv) | 355,010 | `02d3e58b2f082d2aee135e8d9d67439319a452d7daeeb27370a2202fa1cc30bc` | results |
| 143 | [`results/comparative/exp0_reproduction/XGBoost_oof_predictions.csv`](file:///results/comparative/exp0_reproduction/XGBoost_oof_predictions.csv) | 354,955 | `7cd9a2fa02a07c91865ce92ad6cf9eb02717009511d5370ff8e341ac78e4ac78` | results |
| 144 | [`results/comparative/exp0_reproduction/reproduction_comparison.md`](file:///results/comparative/exp0_reproduction/reproduction_comparison.md) | 1,676 | `0dbec66077075e5d29a23ee32bb893386ab42a0a03dd0ada4a15b24c514849ac` | results |
| 145 | [`results/comparative/exp0_reproduction/reproduction_report.json`](file:///results/comparative/exp0_reproduction/reproduction_report.json) | 7,885 | `d77584fdbcf8fe5fc63f9244b71ea125e618708d3773443ac30a862777eeeba8` | results |
| 146 | [`results/comparative/exp1_linear_trees/ElasticNet_oof_predictions.csv`](file:///results/comparative/exp1_linear_trees/ElasticNet_oof_predictions.csv) | 354,936 | `7565573255e04229c888be93b46598224e8d61bcf98be72c16338dfd97ce310f` | results |
| 147 | [`results/comparative/exp1_linear_trees/ExtraTrees_oof_predictions.csv`](file:///results/comparative/exp1_linear_trees/ExtraTrees_oof_predictions.csv) | 354,861 | `2617847951d1a4715e59ffd21eef70de302177ac0dee87a80d3f4925e14802b5` | results |
| 148 | [`results/comparative/exp1_linear_trees/RandomForest_oof_predictions.csv`](file:///results/comparative/exp1_linear_trees/RandomForest_oof_predictions.csv) | 354,859 | `20234c320d2a6ca7d02122ee49ef5f97c5600efc8f68b55dc14e19bc5fde902c` | results |
| 149 | [`results/comparative/exp1_linear_trees/Ridge_oof_predictions.csv`](file:///results/comparative/exp1_linear_trees/Ridge_oof_predictions.csv) | 355,006 | `bd77d29baf1bf6de01707e5fdc8a43ad255079e332e8614c4996f0e626b2a073` | results |
| 150 | [`results/comparative/exp1_linear_trees/exp1_results.json`](file:///results/comparative/exp1_linear_trees/exp1_results.json) | 9,477 | `a5a1ab40f6835718d10b0542c4b5484b6118f8bfc098617ab4c3638a82756284` | results |
| 151 | [`results/comparative/exp1_linear_trees/exp1_summary.md`](file:///results/comparative/exp1_linear_trees/exp1_summary.md) | 824 | `65e528ee05459a31dac78c27878ccd36fb48bd41f6a2f3bc23d8d09aba73dd8f` | results |
| 152 | [`results/comparative/exp2_boosting/CatBoost_oof_predictions.csv`](file:///results/comparative/exp2_boosting/CatBoost_oof_predictions.csv) | 355,054 | `004376dacac9a968413b77d20c54d0b611e2f0e8b80ad554303a7d1637d7937c` | results |
| 153 | [`results/comparative/exp2_boosting/HistGradientBoosting_oof_predictions.csv`](file:///results/comparative/exp2_boosting/HistGradientBoosting_oof_predictions.csv) | 355,003 | `ec2fc3c1efa1d564aebc32730f44e0b4b2f12af259017ee628b04f0bace256b7` | results |
| 154 | [`results/comparative/exp2_boosting/LightGBM_oof_predictions.csv`](file:///results/comparative/exp2_boosting/LightGBM_oof_predictions.csv) | 354,849 | `1c707b96031fb1ae48f98218f48f318e099ded61cf408c5476806140637f8505` | results |
| 155 | [`results/comparative/exp2_boosting/XGBoost_tuned_oof_predictions.csv`](file:///results/comparative/exp2_boosting/XGBoost_tuned_oof_predictions.csv) | 355,002 | `76a1561e96c993ea123f60d6d2cf2114ca6c49204838ce0a796e6b1eb506ac7f` | results |
| 156 | [`results/comparative/exp2_boosting/exp2_results.json`](file:///results/comparative/exp2_boosting/exp2_results.json) | 8,865 | `34918fe64fce61986640c4b4f6867ace73e7c00adc6aed410249667b7d371871` | results |
| 157 | [`results/comparative/exp2_boosting/exp2_summary.md`](file:///results/comparative/exp2_boosting/exp2_summary.md) | 820 | `db96001f1c5d27cc60aa6c1e506f41ccccbfec6549abc5d89776d1b6d7850ba4` | results |
| 158 | [`results/comparative/exp3_deep_tabular/FT_Transformer_ensemble_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/FT_Transformer_ensemble_oof_predictions.csv) | 355,060 | `dc0f0f855cb2bf714122e947b78237358ce8fd967bb3f0eb1144b2ec31619790` | results |
| 159 | [`results/comparative/exp3_deep_tabular/FT_Transformer_seed42_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/FT_Transformer_seed42_oof_predictions.csv) | 355,068 | `d6b5e29779be4a98ae25d6efac5a70f32eb104cc82cb88ced4eaa59e7afc48d2` | results |
| 160 | [`results/comparative/exp3_deep_tabular/FT_Transformer_seed43_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/FT_Transformer_seed43_oof_predictions.csv) | 355,043 | `a5e47b64630d5a94347d0ac4d04622c18ce8e6737be1b046e852e14342d21c85` | results |
| 161 | [`results/comparative/exp3_deep_tabular/FT_Transformer_seed44_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/FT_Transformer_seed44_oof_predictions.csv) | 355,121 | `c8257e135173b942d9a58989e996b4aa7ac5ab04020d895962a2bf4334ff7747` | results |
| 162 | [`results/comparative/exp3_deep_tabular/MLP_Retuned_ensemble_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/MLP_Retuned_ensemble_oof_predictions.csv) | 355,103 | `7404ddb71206ac13d233a604a3c566da6eaeaae837fb987c129b56ce4689eee7` | results |
| 163 | [`results/comparative/exp3_deep_tabular/MLP_Retuned_seed42_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/MLP_Retuned_seed42_oof_predictions.csv) | 355,081 | `35db65051ea0ea9290b1fdaa97fda3e15281e3caa15dfe5863f0e23082058071` | results |
| 164 | [`results/comparative/exp3_deep_tabular/MLP_Retuned_seed43_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/MLP_Retuned_seed43_oof_predictions.csv) | 355,083 | `2b3fa30e33258ae0a14829db180f696175195a671765e81ed68c622a2b7d3f80` | results |
| 165 | [`results/comparative/exp3_deep_tabular/MLP_Retuned_seed44_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/MLP_Retuned_seed44_oof_predictions.csv) | 355,022 | `1ec9f9250858be57d6a6cfad5c81e93d7699cad0c3c9cb388cfac8ea88c7c3c9` | results |
| 166 | [`results/comparative/exp3_deep_tabular/TabNet_ensemble_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/TabNet_ensemble_oof_predictions.csv) | 354,771 | `fd1d70905b2dd6ca9e534dd1c3f598d59d767991daf06625f0047e92d3a4df15` | results |
| 167 | [`results/comparative/exp3_deep_tabular/TabNet_seed42_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/TabNet_seed42_oof_predictions.csv) | 354,763 | `215317164f8263f0775b87cd49d42873cf4b95e27346bdb37e8c16b9ed3e4b77` | results |
| 168 | [`results/comparative/exp3_deep_tabular/TabNet_seed43_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/TabNet_seed43_oof_predictions.csv) | 354,790 | `9faf7fc0130e8c5678a888187c6f87e49ce2b6fcc45fd7f64623d4fe79d37f48` | results |
| 169 | [`results/comparative/exp3_deep_tabular/TabNet_seed44_oof_predictions.csv`](file:///results/comparative/exp3_deep_tabular/TabNet_seed44_oof_predictions.csv) | 354,887 | `a292a9b2e5b651d619ae6f8cb49b1e2ef193779d234033ec7bcc918b6fae3090` | results |
| 170 | [`results/comparative/exp3_deep_tabular/exp3_results.json`](file:///results/comparative/exp3_deep_tabular/exp3_results.json) | 14,796 | `423c529b85786f4a722fb2f8e30687cd86e387945c624e86b5bb7bce2d31469d` | results |
| 171 | [`results/comparative/exp3_deep_tabular/exp3_summary.md`](file:///results/comparative/exp3_deep_tabular/exp3_summary.md) | 669 | `6860de210dc4cba9b088914aad9b3f5565bc7682f569f787e947c469e675e942` | results |
| 172 | [`results/comparative/exp4_gnn/Classical_HGNN_ensemble_oof_predictions.csv`](file:///results/comparative/exp4_gnn/Classical_HGNN_ensemble_oof_predictions.csv) | 356,318 | `2a9ebbcd27b9df8c5bafccf4b19b2c8f0be1cb425b4e0eb6c41ca4ed5f869648` | results |
| 173 | [`results/comparative/exp4_gnn/Classical_HGNN_seed42_oof_predictions.csv`](file:///results/comparative/exp4_gnn/Classical_HGNN_seed42_oof_predictions.csv) | 356,385 | `9f73c2b45a72c1dbe75c31e9a2369852583562e082439f39bec32b7cb1f86ca3` | results |
| 174 | [`results/comparative/exp4_gnn/Classical_HGNN_seed43_oof_predictions.csv`](file:///results/comparative/exp4_gnn/Classical_HGNN_seed43_oof_predictions.csv) | 356,301 | `a7090332314987411fdf2b3ad53bc1a5680d28aaa3769d031da2cb7bf9dab8fc` | results |
| 175 | [`results/comparative/exp4_gnn/Classical_HGNN_seed44_oof_predictions.csv`](file:///results/comparative/exp4_gnn/Classical_HGNN_seed44_oof_predictions.csv) | 356,420 | `db893747d964c3bcab9580bef7c9a913bd7f10548c18d00948cb7519c0d5161b` | results |
| 176 | [`results/comparative/exp4_gnn/HSGIN_ensemble_oof_predictions.csv`](file:///results/comparative/exp4_gnn/HSGIN_ensemble_oof_predictions.csv) | 356,547 | `176a168930c4e3ba969772ac3871e553d4eec977a6c2b30469ff210b87b529fc` | results |
| 177 | [`results/comparative/exp4_gnn/HSGIN_seed42_oof_predictions.csv`](file:///results/comparative/exp4_gnn/HSGIN_seed42_oof_predictions.csv) | 356,487 | `f77905f95b8d944ff53ddac99b72aca88b3b367889978036c2e6858c1e6b11d8` | results |
| 178 | [`results/comparative/exp4_gnn/HSGIN_seed43_oof_predictions.csv`](file:///results/comparative/exp4_gnn/HSGIN_seed43_oof_predictions.csv) | 356,661 | `8c99486cd19ce9565fa13f79d4c589fbbdc0791d1ca953acab92e89fa0380663` | results |
| 179 | [`results/comparative/exp4_gnn/HSGIN_seed44_oof_predictions.csv`](file:///results/comparative/exp4_gnn/HSGIN_seed44_oof_predictions.csv) | 356,416 | `40704f3da7e7b587e81eaefd32ea041ed53d564c5a1a932c18d4f6891fc56d93` | results |
| 180 | [`results/comparative/exp4_gnn/exp4_results.json`](file:///results/comparative/exp4_gnn/exp4_results.json) | 9,734 | `17d5376d4615c0a2937f7114bac3a6fd4445ff169a09e91622ddd9d58fda059d` | results |
| 181 | [`results/comparative/exp4_gnn/exp4_summary.md`](file:///results/comparative/exp4_gnn/exp4_summary.md) | 591 | `25e9e87de8b107a0377c9ae879ce71880e1e614b03713016085f1aa50c0d2656` | results |
| 182 | [`results/comparative/exp5_ensemble/NNW_Blend_oof_predictions.csv`](file:///results/comparative/exp5_ensemble/NNW_Blend_oof_predictions.csv) | 311,078 | `1b4a094e7639814ba79238df80de752d5d2dea9a0c9804588d299f49ed4b439b` | results |
| 183 | [`results/comparative/exp5_ensemble/RidgeStacking_oof_predictions.csv`](file:///results/comparative/exp5_ensemble/RidgeStacking_oof_predictions.csv) | 311,105 | `7e8f13f1bcd541e73c6f1062984e112520ababfb1cdb2e68fb0cd0abb408f41f` | results |
| 184 | [`results/comparative/exp5_ensemble/SimpleAverage_oof_predictions.csv`](file:///results/comparative/exp5_ensemble/SimpleAverage_oof_predictions.csv) | 311,062 | `1ae36a75bc80ae6c71301790af05cadbcf47b88b06e43b8d5da12e6a13b15bcf` | results |
| 185 | [`results/comparative/exp5_ensemble/diversity_analysis.json`](file:///results/comparative/exp5_ensemble/diversity_analysis.json) | 1,208 | `a5ccf2ba88ab0b69c30cd7736f1e806df39cbed07357155e504af2d444122925` | results |
| 186 | [`results/comparative/exp5_ensemble/exp5_results.json`](file:///results/comparative/exp5_ensemble/exp5_results.json) | 13,798 | `4ba4d190c47da04d17cdb47796ce7c0ab917db301b05afbb0c31f388e998293b` | results |
| 187 | [`results/comparative/exp5_ensemble/exp5_summary.md`](file:///results/comparative/exp5_ensemble/exp5_summary.md) | 2,657 | `3ffbd4efc306a22cb12f0e3946030ba194f717d1c87f5030bc7baec4401a9a70` | results |
| 188 | [`results/comparative/exp5_ensemble/inner_meta_predictions.npz`](file:///results/comparative/exp5_ensemble/inner_meta_predictions.npz) | 804,698 | `5c02b71c565c85796504f9511e62594ec239f52561c84b9d6f1d8c9750f2c690` | results |
| 189 | [`results/comparative/exp5_ensemble/meta_leakage_audit.json`](file:///results/comparative/exp5_ensemble/meta_leakage_audit.json) | 3,882 | `b93747da1df3a10e4e8c8a6811f35a1cf86cf9bab1295fd0af4e3652bbbaa48e` | results |
| 190 | [`results/comparative/exp6_ablations/HSGIN_FULL_25_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_FULL_25_oof.csv) | 354,465 | `5c68903040be46fa5ac19d63f85d6401612fef258aa0943940c82b273a56d80c` | results |
| 191 | [`results/comparative/exp6_ablations/HSGIN_LOO_Biomarker_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_LOO_Biomarker_oof.csv) | 356,435 | `68bd027d4a35fcf120e4f6da59c337a2d9f7f299e5da44ad3b8a50071a2271a0` | results |
| 192 | [`results/comparative/exp6_ablations/HSGIN_LOO_Demographics_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_LOO_Demographics_oof.csv) | 356,374 | `e0c01fe631dcbb5d8fa12e93364cf840aa928ee8d71cb256192efed032dfffbf` | results |
| 193 | [`results/comparative/exp6_ablations/HSGIN_LOO_Heart_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_LOO_Heart_oof.csv) | 356,277 | `469808bbba710b66bedb4e2cfe51a83ca2702afb14b34bf218c082374ff0531f` | results |
| 194 | [`results/comparative/exp6_ablations/HSGIN_LOO_Kidney_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_LOO_Kidney_oof.csv) | 356,350 | `5d2308661f4900be91018d4760dd70423f6f407930fa2294e0e9123db03cd362` | results |
| 195 | [`results/comparative/exp6_ablations/HSGIN_LOO_Liver_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_LOO_Liver_oof.csv) | 356,423 | `8948672412c9d1be1252457c2ea672f09afd247dbba6d829e6b79aaad1170bae` | results |
| 196 | [`results/comparative/exp6_ablations/HSGIN_Variant_FlatReadout_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_Variant_FlatReadout_oof.csv) | 356,515 | `375bd297750d16dd601a71767e91dea2bc3c06636ffebc60cf93aacde0be1bd9` | results |
| 197 | [`results/comparative/exp6_ablations/HSGIN_Variant_HomoGNN_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_Variant_HomoGNN_oof.csv) | 356,411 | `e824ec0a81e4ff39be0d1fc0165f6e8b015e2ff10b792477d14307fced1510f6` | results |
| 198 | [`results/comparative/exp6_ablations/HSGIN_Variant_NoCrossTalk_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_Variant_NoCrossTalk_oof.csv) | 356,365 | `3f0bd0c16f2bbff38cb39c3d6f987cd8d8878a53b17162cbed181db1583d07ec` | results |
| 199 | [`results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_ensemble_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_ensemble_oof.csv) | 355,290 | `d480581d2d9f9eee624db2f1684226fb6e5294381847bc9c8217259428c11895` | results |
| 200 | [`results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_oof.csv) | 356,458 | `5b35b59867d805dfb7e5d2e9d966e23e4a2346b1539c4a75b8287aaa9718ce8d` | results |
| 201 | [`results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_seed43_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_seed43_oof.csv) | 356,477 | `d2ec7c92d2b9d6e9ffaa9b19e67d2c58e7e70fb038a1c974503130484bd73481` | results |
| 202 | [`results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_seed44_oof.csv`](file:///results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_seed44_oof.csv) | 356,470 | `15e80b7741664f2166986be7985f85ae206e7c106c093b107e7b68ad2750b599` | results |
| 203 | [`results/comparative/exp6_ablations/XGBoost_FULL_25_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_FULL_25_oof.csv) | 367,608 | `aeb581c446259c72daf657c90751b2b361ce60763f10a0eee24cd2d5d45ad45e` | results |
| 204 | [`results/comparative/exp6_ablations/XGBoost_LOO_Biomarker_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_LOO_Biomarker_oof.csv) | 367,581 | `2c01ab99fb1e8b7f4ea8d185acf3fe761727a0b5de54d0d0714f22490e09b29f` | results |
| 205 | [`results/comparative/exp6_ablations/XGBoost_LOO_Demographics_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_LOO_Demographics_oof.csv) | 367,440 | `373102333e395f770d1736cfffd1190b903facb9a8606869de7a7fd69ff8695b` | results |
| 206 | [`results/comparative/exp6_ablations/XGBoost_LOO_Heart_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_LOO_Heart_oof.csv) | 367,398 | `6ce197006af88b8bd54b50dd52895060025eeaef8d73476d252c4503ed08a6a6` | results |
| 207 | [`results/comparative/exp6_ablations/XGBoost_LOO_Kidney_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_LOO_Kidney_oof.csv) | 367,505 | `47bd62ced136ca13c284da4897134735eee553157bf1ce3741ff1af663377b3b` | results |
| 208 | [`results/comparative/exp6_ablations/XGBoost_LOO_Liver_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_LOO_Liver_oof.csv) | 367,547 | `3eb1a399544f763be36066b86b2be132e53a247e6de43fb55bb7fdf0f43242d7` | results |
| 209 | [`results/comparative/exp6_ablations/XGBoost_ONLY_Biomarker_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_ONLY_Biomarker_oof.csv) | 367,203 | `8fddd7281135f2825cc8faa1db124bb45afaee3436a4f703237345ca611000f0` | results |
| 210 | [`results/comparative/exp6_ablations/XGBoost_ONLY_Demographics_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_ONLY_Demographics_oof.csv) | 366,940 | `7f3720c1ce2f904b711f3825d69e5a981e274eb62ec4d77778a36f027ece5503` | results |
| 211 | [`results/comparative/exp6_ablations/XGBoost_ONLY_Heart_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_ONLY_Heart_oof.csv) | 367,320 | `6aa0860e7f6040982def44699c1730b669ecd5d412feca459051a0396938a3a2` | results |
| 212 | [`results/comparative/exp6_ablations/XGBoost_ONLY_Kidney_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_ONLY_Kidney_oof.csv) | 367,247 | `c815f7aa263cd6ec38b414b964094a40b16e94ecb3e1597800de7fb16bde2435` | results |
| 213 | [`results/comparative/exp6_ablations/XGBoost_ONLY_Liver_oof.csv`](file:///results/comparative/exp6_ablations/XGBoost_ONLY_Liver_oof.csv) | 367,247 | `8a8a322cbe974871e9a58b10101f210f2cab4d91397bcb7a7dd67aa0f2435589` | results |
| 214 | [`results/comparative/exp6_ablations/exp6_hsgin_results.json`](file:///results/comparative/exp6_ablations/exp6_hsgin_results.json) | 11,544 | `8a8d64f567da6c80d301c5e980cba23d76d14dbec72858890788c557884d2f69` | results |
| 215 | [`results/comparative/exp6_ablations/exp6_xgboost_results.json`](file:///results/comparative/exp6_ablations/exp6_xgboost_results.json) | 26,208 | `4f9561f9477632df874491950c3e93c7e228036c9b056c53049414e9a1a14663` | results |
| 216 | [`results/comparative/exp6_ablations/exp6_xgboost_summary.md`](file:///results/comparative/exp6_ablations/exp6_xgboost_summary.md) | 3,635 | `012dc43e3c6b9db118ef096fc4d1a097ae30ef2aea4617b7d42a8289fb5bd79e` | results |
| 217 | [`results/comparative/exp6_ablations/exp6a_bootstrap_holm.json`](file:///results/comparative/exp6_ablations/exp6a_bootstrap_holm.json) | 5,840 | `ea2bfb344213a9bf2cf94c9f8df6b5df7ef83a388a29d25e01f25180b21da09d` | results |
| 218 | [`results/comparative/exp6_ablations/exp6b_bootstrap_holm.json`](file:///results/comparative/exp6_ablations/exp6b_bootstrap_holm.json) | 2,940 | `4319ffcf47af1ba4ecc1aa4f86c195846acbe3037761a4ff1e5060ca81bb7fd4` | results |
| 219 | [`results/comparative/exp6_ablations/exp7_bootstrap_holm.json`](file:///results/comparative/exp6_ablations/exp7_bootstrap_holm.json) | 2,382 | `30e1f2c0ffdd4ba07bf9f9fffe69e612f4ea8ef2079e86f3d5d79d6ab0b5ebd4` | results |
| 220 | [`results/comparative/exp6_ablations/exp7_graph_ablation_results.json`](file:///results/comparative/exp6_ablations/exp7_graph_ablation_results.json) | 10,130 | `5b7265e51b43c8bd89151956dac2b859b37386b686bf43c9a4d65c6d7843cbeb` | results |
| 221 | [`results/comparative/exp6_ablations/exp7_random_edges_multiseed_results.json`](file:///results/comparative/exp6_ablations/exp7_random_edges_multiseed_results.json) | 2,304 | `cf324712e6c7bc02f9f38aa8d9ad0a82f70f448286ecc95c5e897ea0386e4ac2` | results |
| 222 | [`results/comparative/exp8_controls/LEAKY_DEMO_Exact_LogFormula_Ridge_oof.csv`](file:///results/comparative/exp8_controls/LEAKY_DEMO_Exact_LogFormula_Ridge_oof.csv) | 298,783 | `0cad5211d97de7f4cd45e897a25dd88544cc9d10b9cfc8dc809abd840b157e40` | results |
| 223 | [`results/comparative/exp8_controls/LEAKY_DEMO_MLP_Leaky_Full29_oof.csv`](file:///results/comparative/exp8_controls/LEAKY_DEMO_MLP_Leaky_Full29_oof.csv) | 299,000 | `bb9be251c33104594173df45d419452dfa3c10fe2001733a5df5b440da3d16d2` | results |
| 224 | [`results/comparative/exp8_controls/LEAKY_DEMO_MLP_Leaky_Raw4_oof.csv`](file:///results/comparative/exp8_controls/LEAKY_DEMO_MLP_Leaky_Raw4_oof.csv) | 298,854 | `1f51def95e7472315694164cad3cb50b7beb6a1591ed1a306e76c86c91575f0c` | results |
| 225 | [`results/comparative/exp8_controls/LEAKY_DEMO_Ridge_Leaky_Full29_oof.csv`](file:///results/comparative/exp8_controls/LEAKY_DEMO_Ridge_Leaky_Full29_oof.csv) | 299,266 | `e3f1d97411dd8b86eac95a434e0f35b97b0a49f2e40aada5932cd7e902ba24c1` | results |
| 226 | [`results/comparative/exp8_controls/LEAKY_DEMO_Ridge_Leaky_Raw4_oof.csv`](file:///results/comparative/exp8_controls/LEAKY_DEMO_Ridge_Leaky_Raw4_oof.csv) | 299,264 | `575948b215004f26c617b24142ad3c6870d68788e83a0d25f0ecd3753dea99c9` | results |
| 227 | [`results/comparative/exp8_controls/LEAKY_DEMO_XGBoost_Leaky_Full29_oof.csv`](file:///results/comparative/exp8_controls/LEAKY_DEMO_XGBoost_Leaky_Full29_oof.csv) | 298,724 | `f667c04f0873ddb8c304cb9a7ac959b2a3f5ebb56f801bfb05b71c685813700b` | results |
| 228 | [`results/comparative/exp8_controls/LEAKY_DEMO_XGBoost_Leaky_Raw4_oof.csv`](file:///results/comparative/exp8_controls/LEAKY_DEMO_XGBoost_Leaky_Raw4_oof.csv) | 298,742 | `9a0f279c5f0bc7443bc31ffe55a3552273ff1e0f6c2fe8ee11f0b7b7d20f81c6` | results |
| 229 | [`results/comparative/exp8_controls/exp8_controls_results.json`](file:///results/comparative/exp8_controls/exp8_controls_results.json) | 22,370 | `71202439cee2f616290a0cdf477f3a29adad61f20fa6efc8e290e49e2c6b9d74` | results |
| 230 | [`results/comparative/exp8_controls/exp8_controls_summary.md`](file:///results/comparative/exp8_controls/exp8_controls_summary.md) | 2,449 | `60ce6ad827e597985c48eb78bc56a6d831d93624c61fe8bb1137f63527265e40` | results |
| 231 | [`results/comparative/exp8_controls/hsgin_100perms_distribution.json`](file:///results/comparative/exp8_controls/hsgin_100perms_distribution.json) | 1,890 | `21e84015928c6e9173c1c8cc47946996863a18decba51c0d6fb97794c6cb08d4` | results |
| 232 | [`results/comparative/exp8_controls/parts/hsgin_perms_11_25.json`](file:///results/comparative/exp8_controls/parts/hsgin_perms_11_25.json) | 287 | `fc97acfc67836e3580611902f1d7af266e8da10f895822820123b3d19d5c71e8` | results |
| 233 | [`results/comparative/exp8_controls/parts/hsgin_perms_26_40.json`](file:///results/comparative/exp8_controls/parts/hsgin_perms_26_40.json) | 286 | `e985a1c233173237a2e81f834088fffce0b27cbf9e7cf4e8a7086237624dda58` | results |
| 234 | [`results/comparative/exp8_controls/parts/hsgin_perms_41_55.json`](file:///results/comparative/exp8_controls/parts/hsgin_perms_41_55.json) | 288 | `ff7e92db40ce49412bf606d2188642ff1e8502e12de85387ab5b242846a2a4f2` | results |
| 235 | [`results/comparative/exp8_controls/parts/hsgin_perms_56_70.json`](file:///results/comparative/exp8_controls/parts/hsgin_perms_56_70.json) | 287 | `ec79b9cdd408ff0836d83580d984bb0ef92cbaef72ab61be3a8b841936a31bce` | results |
| 236 | [`results/comparative/exp8_controls/parts/hsgin_perms_71_85.json`](file:///results/comparative/exp8_controls/parts/hsgin_perms_71_85.json) | 287 | `5b81db293a33db9ea6ef65e30ae8713ab9391bfd16440b0f68c8130be8e683a0` | results |
| 237 | [`results/comparative/exp8_controls/parts/hsgin_perms_86_100.json`](file:///results/comparative/exp8_controls/parts/hsgin_perms_86_100.json) | 287 | `4870652ddbea1d024b01e1d40bbabe820948c625a82c175c05dd484c1737c337` | results |
| 238 | [`results/comparative/exp9_subgroups/exp9_subgroup_results.json`](file:///results/comparative/exp9_subgroups/exp9_subgroup_results.json) | 57,896 | `e4f55a2ce1f8b30c7d4c014756c5245f5d3899db7a706c489d18e5040cc997a5` | results |
| 239 | [`results/comparative/exp9_subgroups/exp9_subgroups_summary.md`](file:///results/comparative/exp9_subgroups/exp9_subgroups_summary.md) | 3,324 | `8e57d13aa1d6872715b69ddda4bfc40fd2f3541b22093c75f43481324fb242b3` | results |
| 240 | [`results/comparative/exp9_subgroups/subgroup_patient_evaluations.csv`](file:///results/comparative/exp9_subgroups/subgroup_patient_evaluations.csv) | 977,990 | `c727619b8581189f5feb9b9e2d5b1002653e835f968120a2a7577b42e6e78c4e` | results |
| 241 | [`results/comparative/explainability/domain_importance_summary.csv`](file:///results/comparative/explainability/domain_importance_summary.csv) | 324 | `fbe6d9c8379699e955a211cdad5a115c8a5a086126503fa6913c4668b4bb7946` | results |
| 242 | [`results/comparative/explainability/explainability_results.json`](file:///results/comparative/explainability/explainability_results.json) | 5,878 | `973b17c9090155fcdf4f3dc99ce49f285a2652794579599260f98a0e7491db3b` | results |
| 243 | [`results/comparative/explainability/feature_permutation_importance.csv`](file:///results/comparative/explainability/feature_permutation_importance.csv) | 5,678 | `4c0cd4d8209169bf9b7639ba4d29eb90e6343d5faea7cf8ad5d3eeb7f7e7ff18` | results |
| 244 | [`results/comparative/explainability/reconciled_domain_attribution.json`](file:///results/comparative/explainability/reconciled_domain_attribution.json) | 2,755 | `5cf6c0eb4111ab7a45333ea18ba42f4df9993853bde052ec89a7fc4e423db2f8` | results |
| 245 | [`results/comparative/final_benchmark_summary.json`](file:///results/comparative/final_benchmark_summary.json) | 16,815 | `64e10d0f60a69f0ed14af6ea1827bc26f5af07b43b403aff44ca3962fcf22c0e` | results |
| 246 | [`results/comparative/leakage_gate_report.json`](file:///results/comparative/leakage_gate_report.json) | 5,048 | `d6cf8b6b02893751f16eed1b598fb4ce522db413dbf54ff42d1f79774df64504` | results |
| 247 | [`results/comparative/paired_bootstrap_phase3.json`](file:///results/comparative/paired_bootstrap_phase3.json) | 6,759 | `34eedfdc0310e404b833535ce1cc5f8e3a57e24d9855925210f66bea1d1319be` | results |
| 248 | [`results/comparative/paired_bootstrap_phase4.json`](file:///results/comparative/paired_bootstrap_phase4.json) | 6,261 | `9f57402e7268aff6399bac8a5c3be411f83e6e060724348ab673399918351b75` | results |
| 249 | [`results/comparative/paired_bootstrap_phase5.json`](file:///results/comparative/paired_bootstrap_phase5.json) | 3,669 | `140ae9bc0484dcb4800008fcec5292670138d3a76addaf538faa01b6f3efa4c4` | results |
| 250 | [`src/ablation.py`](file:///src/ablation.py) | 3,182 | `60b8f96b3ef57652ef975a8c2702ef7d1f12d7d18683da8ee6664820c7fba9a6` | src |
| 251 | [`src/audit.py`](file:///src/audit.py) | 5,124 | `89c97e7b72ee7fe033e58e304a7ee818f8c21f9e3be4954ff018ad20d5f7ccd8` | src |
| 252 | [`src/cohort.py`](file:///src/cohort.py) | 3,417 | `3dce6eb21e6e6010c8d278617cc6dff3a0493c7bbc5032b2ce4c7af47ff8bb98` | src |
| 253 | [`src/comparative/__init__.py`](file:///src/comparative/__init__.py) | 88 | `8e5966f59193d8c0e8c727cb6702ce52dd1dd7499f2165bdaf0433d272c50b32` | src |
| 254 | [`src/comparative/base_adapter.py`](file:///src/comparative/base_adapter.py) | 2,165 | `aeda3d2167652b1b506b547860c12bb4f67af1200012f8d41959bc6bb4fc1902` | src |
| 255 | [`src/comparative/compute_multiple_corrections.py`](file:///src/comparative/compute_multiple_corrections.py) | 6,716 | `d00e22e33e6c2fb8dbc28df7266a7e73f8f636bd5a99e64db47cb7fd210bb701` | src |
| 256 | [`src/comparative/deep_tabular.py`](file:///src/comparative/deep_tabular.py) | 2,683 | `3ae58255efb8be0eff88edaec4dfcaef37bfc94664fa21f944b0944dcf1d79f5` | src |
| 257 | [`src/comparative/exp0_reproduction.py`](file:///src/comparative/exp0_reproduction.py) | 13,338 | `6c2eef53935fab8fa48c7f6a08ef8aaf0b8a113640146d246b9e06de8c2c52a9` | src |
| 258 | [`src/comparative/exp1_linear_trees.py`](file:///src/comparative/exp1_linear_trees.py) | 8,339 | `7bc09a8ec0029877d497b88d2e08bfc814b67b8654bd225571290e4ac110c13d` | src |
| 259 | [`src/comparative/exp2_boosting.py`](file:///src/comparative/exp2_boosting.py) | 10,559 | `ea1dabeec52aadcae37a06a6046239785e24f681757a19c1bb03e792ef734ca3` | src |
| 260 | [`src/comparative/exp3_deep_tabular.py`](file:///src/comparative/exp3_deep_tabular.py) | 13,436 | `9ab092e0aca4eba78d4d388bd083c8f76c6447937a4eb2cce2a1721c6fd40fdf` | src |
| 261 | [`src/comparative/exp4_gnn.py`](file:///src/comparative/exp4_gnn.py) | 9,968 | `a38d9df0aba9c34b1ea1b9354b67279b498d6cc8356d138092e62a3c0bf2d5a6` | src |
| 262 | [`src/comparative/exp5_ensemble.py`](file:///src/comparative/exp5_ensemble.py) | 29,747 | `94834f87cd139eea1cfeab7deb6b628f856328cbc10bb408347c56a14186d782` | src |
| 263 | [`src/comparative/exp6_ablations.py`](file:///src/comparative/exp6_ablations.py) | 43,048 | `e447909545d47c0a2b5a6a790c876b85cec0333dfdd5959513e7e1aadcddb281` | src |
| 264 | [`src/comparative/finalize_phase6_audit.py`](file:///src/comparative/finalize_phase6_audit.py) | 30,943 | `c98bddc482fccfc710ca171c0577cc522a5300de0505f2c4233546f65b5ea696` | src |
| 265 | [`src/comparative/finalize_phase7_report.py`](file:///src/comparative/finalize_phase7_report.py) | 21,144 | `5b8ab77a7c642dbbb2b13cdbf40a7f5b79123b20c70af8a93b622bbcf9dee64e` | src |
| 266 | [`src/comparative/leakage_gate.py`](file:///src/comparative/leakage_gate.py) | 7,090 | `b987e544b67e877e4b300508bdfdf0f0010cad160b67256535acc25f2f3dbc11` | src |
| 267 | [`src/comparative/metrics.py`](file:///src/comparative/metrics.py) | 3,004 | `5899ea08d9d0d5bf28f175a38cd546f7ee0a119cf8e884c2f758c15ff85d9104` | src |
| 268 | [`src/comparative/paired_tests.py`](file:///src/comparative/paired_tests.py) | 3,235 | `6a7a6e2e6a570432711ce3e6c22ce01307f39d7eb9b7b9fcb385eac1dfbe905f` | src |
| 269 | [`src/comparative/reconcile_liver_contribution.py`](file:///src/comparative/reconcile_liver_contribution.py) | 4,296 | `8f9ce1ba4bbe06073e6d6366748bc4b57424a6e01600a580f857b38515351112` | src |
| 270 | [`src/comparative/rerun_exp7_random_edges.py`](file:///src/comparative/rerun_exp7_random_edges.py) | 9,923 | `d6bb16ccc04da9d8b535f4555c9899492926a68081e0c4541227ebc1d024dde6` | src |
| 271 | [`src/comparative/run_exp6_xgboost.py`](file:///src/comparative/run_exp6_xgboost.py) | 5,926 | `6ec109c8c9c79a336baa5509f1518c32e9c6515c7eb54b7cf3b3fa493b44f9d1` | src |
| 272 | [`src/comparative/run_exp6b_hsgin.py`](file:///src/comparative/run_exp6b_hsgin.py) | 8,231 | `29c791b994a9a2dab3ab1fbe14408fb4698951278b551226dd8bb3e5f06e4665` | src |
| 273 | [`src/comparative/run_exp7_graph_ablations.py`](file:///src/comparative/run_exp7_graph_ablations.py) | 15,252 | `2436036594c7357e0d620b9879a1693dea9bf92981a79bfbe6718ebdc239296e` | src |
| 274 | [`src/comparative/run_exp7_random_edges_multiseed.py`](file:///src/comparative/run_exp7_random_edges_multiseed.py) | 13,250 | `45586918b0521294a1a5114746321853210c3adf82fbb11a61b0310afb63b2b9` | src |
| 275 | [`src/comparative/run_exp8_controls.py`](file:///src/comparative/run_exp8_controls.py) | 20,568 | `927d8278886ef13142e040db7454642d166d063efe8aef64688335e40ebd0099` | src |
| 276 | [`src/comparative/run_exp8_hsgin_100perms.py`](file:///src/comparative/run_exp8_hsgin_100perms.py) | 7,798 | `73244b07757814b72668922264f2d7f9737cdd52590a95b5d85e7fd9d5379495` | src |
| 277 | [`src/comparative/run_exp8_multiprocess.py`](file:///src/comparative/run_exp8_multiprocess.py) | 4,637 | `838eff5d0b120b59d09abca89052bb02b8958b8a47e16d8d0d635757433690b3` | src |
| 278 | [`src/comparative/run_exp8_worker.py`](file:///src/comparative/run_exp8_worker.py) | 4,677 | `29a7321387b700dd732f0161931a919215fa56a2894305a390329ec51d53a7c7` | src |
| 279 | [`src/comparative/run_exp9_subgroups.py`](file:///src/comparative/run_exp9_subgroups.py) | 13,224 | `cf16f102b120c8576f6bd3b10e695ca02d9379c5e6dfbb80ef9b34d9237a55ab` | src |
| 280 | [`src/comparative/run_phase8_synthesis.py`](file:///src/comparative/run_phase8_synthesis.py) | 40,142 | `9c08ac34943db5b1b1325e877b3ac316100c52155f758924476204a36bca654f` | src |
| 281 | [`src/comparative/split.py`](file:///src/comparative/split.py) | 2,538 | `de0d6e197f98a2e40ad23a32365295af709e0dcecae23d30d0de48187e4e07ba` | src |
| 282 | [`src/dataset.py`](file:///src/dataset.py) | 5,121 | `15e8c409fd854a5b0b6225ceda32b46760010daae0e4fa2a814513011a3bd3a1` | src |
| 283 | [`src/draw_schema_diagram.py`](file:///src/draw_schema_diagram.py) | 3,468 | `bab78eac5e82d6602325a4e6ae661916e165f6eef5a434d5dc2abba86fe14205` | src |
| 284 | [`src/graph_builder.py`](file:///src/graph_builder.py) | 4,692 | `b4ee2b472d52c77964c164344bcaf8268540c2af62e459d98e05d06f07f9e69e` | src |
| 285 | [`src/hsgin_ablation.py`](file:///src/hsgin_ablation.py) | 7,308 | `a437f2b4582d60048e7bd7709760adbab888de4dc03446bb6734cfd71ea7e793` | src |
| 286 | [`src/leakage_audit.py`](file:///src/leakage_audit.py) | 11,338 | `ac908022cc2818e450cce322714c10e9961cf2923363f1322cf81c2d6199a500` | src |
| 287 | [`src/models/baselines.py`](file:///src/models/baselines.py) | 3,903 | `2e24f4e6b8cedfa0a0c949847b66e8be9925478cbdd9de394d0422161c51a39e` | src |
| 288 | [`src/models/hsgin.py`](file:///src/models/hsgin.py) | 4,720 | `4d9bd5a8372e3eb9d234701fb7d8885efa2f087ddb95f807488e04ad9ac65b6d` | src |
| 289 | [`src/pipeline.py`](file:///src/pipeline.py) | 3,660 | `24d33b42b5971d98016765434ecefd703f0e65c97fcd518f43c3378c3a0ae328` | src |
| 290 | [`src/target.py`](file:///src/target.py) | 3,714 | `680b957a2c93813ca04e7b65c393c06461a6efb1521ed92473fe66fa4d8dd26c` | src |
| 291 | [`src/train.py`](file:///src/train.py) | 10,711 | `a0e466d39ae83d0893b11333e61ae0d7908882ae31eaa353d2d05a5d559bdcce` | src |
| 292 | [`src/visualize_graph.py`](file:///src/visualize_graph.py) | 3,649 | `7ae9e3e3a5d0206c8a9631dd83586b92ea32ae147b62f3a65852c5816f49c159` | src |
| 293 | [`src/visualize_interactive.py`](file:///src/visualize_interactive.py) | 6,267 | `3d849fffdb5a8361ca9bcb8366137ab9c230ed1b6e1785af5e5006b489e49c23` | src |
| 294 | [`src/y_randomization.py`](file:///src/y_randomization.py) | 2,607 | `3c0b0379243e07be14d4933300c1a61630e34fbfdd5acf873cfc2f39b44b70e9` | src |
| 295 | [`tests/test_leakage_gate.py`](file:///tests/test_leakage_gate.py) | 663 | `7151b140eb28192dc4057ae9ba08811bfa185570e773b135a2789b2224667bcb` | tests |
| 296 | [`tests/test_preservation.py`](file:///tests/test_preservation.py) | 1,965 | `ee52caee57da62dbb0de146e965ec64a5c6eba2ff05b4c41273a30597d29a8b2` | tests |
| 297 | [`tests/test_splits.py`](file:///tests/test_splits.py) | 1,256 | `7cc072fb1af477281d1250401e6ff68a92ef09f5e9a751b0cc44e1c0f7b323f8` | tests |