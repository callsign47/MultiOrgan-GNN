# ORGANIX Repository Migration Manifest

Authoritative mapping of all pre-migration assets in `3 ORGAN` to their destinations in `ORGANIX`.

| Original Path | New Path | Category | Action | SHA-256 (prefix) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.gitignore` | `.gitignore` | PROJECT_ROOT | UPDATE | `e0c55daf2f5c...` | PRESERVED |
| `PRD Comparative Evaluation of Machine Learning, Deep Learning, and Graph Neural.md` | `docs/PRD_Comparative_Evaluation_v1.1.md` | PROJECT_ROOT | REFACTOR | `1ba2b61b79e7...` | PRESERVED |
| `README.md` | `docs/LEGACY_README.md` | PROJECT_ROOT | ARCHIVE_AND_SUPERSEDE | `9f56e4c82cf1...` | PRESERVED |
| `requirements.txt` | `requirements.txt` | PROJECT_ROOT | UPDATE | `1905b7e1b7d7...` | PRESERVED |
| `technical_evidence_package.zip` | `docs/technical_evidence/technical_evidence_package.zip` | ARCHIVE_EVIDENCE | REFACTOR | `00dca4a5f35c...` | PRESERVED |
| `configs/comparative/exp3_deep_tabular/deep_tabular_configs.json` | `configs/experiments/deep_tabular_configs.json` | CONFIG | MOVE | `23db56808876...` | PRESERVED |
| `configs/comparative/exp4_gnn/gnn_configs.json` | `configs/experiments/gnn_configs.json` | CONFIG | MOVE | `5ac98dfdd1d1...` | PRESERVED |
| `configs/comparative/exp5_ensemble/base_model_selection.json` | `configs/experiments/base_model_selection.json` | CONFIG | MOVE | `6d56f58e7b12...` | PRESERVED |
| `configs/comparative/exp6_ablations/exp6_config.json` | `configs/experiments/exp6_config.json` | CONFIG | MOVE | `26627822f75c...` | PRESERVED |
| `configs/comparative/exp6_ablations/exp7_config.json` | `configs/experiments/exp7_config.json` | CONFIG | MOVE | `5a4fb6cca78a...` | PRESERVED |
| `configs/comparative/exp8_controls/exp8_config.json` | `configs/experiments/exp8_config.json` | CONFIG | MOVE | `9ef32f848509...` | PRESERVED |
| `data/artifact_checksums.json` | `data/metadata/artifact_checksums.json` | DATA_METADATA | MOVE | `b2b3968228f7...` | CRITICAL_VERIFIED |
| `data/feature_manifest.json` | `data/metadata/feature_manifest.json` | DATA_METADATA | MOVE | `6712e1575dc1...` | CRITICAL_VERIFIED |
| `data/feature_preprocessing_audit.json` | `data/metadata/feature_preprocessing_audit.json` | DATA_METADATA | MOVE | `3b371acaf6e2...` | CRITICAL_VERIFIED |
| `data/file_mapping_analysis.json` | `data/metadata/file_mapping_analysis.json` | DATA_METADATA | MOVE | `63ce3c6c503c...` | CRITICAL_VERIFIED |
| `data/final_cohort.csv` | `data/processed/final_cohort.csv` | DATA_PROCESSED | MOVE | `7d9f30deb21b...` | CRITICAL_VERIFIED |
| `data/hsgin_architecture_audit.json` | `data/metadata/hsgin_architecture_audit.json` | DATA_METADATA | MOVE | `a43a6ec185b7...` | CRITICAL_VERIFIED |
| `data/master_patient.csv` | `data/processed/master_patient.csv` | DATA_PROCESSED | MOVE | `b1682cb1d0ad...` | CRITICAL_VERIFIED |
| `data/raw_file_audit.json` | `data/metadata/raw_file_audit.json` | DATA_METADATA | MOVE | `6e318ce429af...` | CRITICAL_VERIFIED |
| `data/table_inventory.json` | `data/metadata/table_inventory.json` | DATA_METADATA | MOVE | `891e5d45f4ea...` | CRITICAL_VERIFIED |
| `data/comparative/folds_v1.json` | `data/splits/folds_v1.json` | DATA_SPLITS | MOVE | `226b731be71e...` | CRITICAL_VERIFIED |
| `graphs/.gitkeep` | `artifacts/graphs/.gitkeep` | ARTIFACT_MISC | REFACTOR | `e3b0c44298fc...` | PRESERVED |
| `graphs/patient_graphs.pt` | `artifacts/graphs/patient_graphs.pt` | ARTIFACT_GRAPH | MOVE | `4bffe0406004...` | CRITICAL_VERIFIED |
| `NHANES AUG'21 - AUG'23/DEMO G/DEMO_L.xpt` | `data/raw/nhanes_2021_2023/DEMO_G/DEMO_L.xpt` | DATA_RAW | MOVE | `ca4374a158b4...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/EXAMINATION/BMX_L.xpt` | `data/raw/nhanes_2021_2023/EXAMINATION/BMX_L.xpt` | DATA_RAW | MOVE | `44440c416d9a...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/EXAMINATION/BPXO_L.xpt` | `data/raw/nhanes_2021_2023/EXAMINATION/BPXO_L.xpt` | DATA_RAW | MOVE | `189aa9bed689...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/EXAMINATION/LUX_L.xpt` | `data/raw/nhanes_2021_2023/EXAMINATION/LUX_L.xpt` | DATA_RAW | MOVE | `40e49c5f1b58...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/ALB_CR_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/ALB_CR_L.xpt` | DATA_RAW | MOVE | `fc011a80d144...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/BIOPRO_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/BIOPRO_L.xpt` | DATA_RAW | MOVE | `912b345aad6b...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/CBC_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/CBC_L.xpt` | DATA_RAW | MOVE | `4405da2a5899...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/GHB_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/GHB_L.xpt` | DATA_RAW | MOVE | `67aee0353160...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/GLU_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/GLU_L.xpt` | DATA_RAW | MOVE | `70f773ab37e3...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/HDL_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/HDL_L.xpt` | DATA_RAW | MOVE | `c1bb43df5ca3...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/HEPA_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/HEPA_L.xpt` | DATA_RAW | MOVE | `0eacb9b1b0bc...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/HEPBD_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/HEPBD_L.xpt` | DATA_RAW | MOVE | `e2828da40dbc...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/HEPC_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/HEPC_L.xpt` | DATA_RAW | MOVE | `ccdbbec2d51a...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/HEPE_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/HEPE_L.xpt` | DATA_RAW | MOVE | `6753e7540a7a...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/HSCRP_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/HSCRP_L.xpt` | DATA_RAW | MOVE | `c56098d7c335...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/INS_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/INS_L.xpt` | DATA_RAW | MOVE | `cdbf53b64480...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/TCHOL_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/TCHOL_L.xpt` | DATA_RAW | MOVE | `5c3312e555bb...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/LABORATORY/TRIGLY_L.xpt` | `data/raw/nhanes_2021_2023/LABORATORY/TRIGLY_L.xpt` | DATA_RAW | MOVE | `77679864c33b...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/BPQ_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/BPQ_L.xpt` | DATA_RAW | MOVE | `0acde3af0526...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DBQ_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/DBQ_L.xpt` | DATA_RAW | MOVE | `774ead4e3b8d...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DIQ_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/DIQ_L.xpt` | DATA_RAW | MOVE | `9535a023673a...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/DPQ_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/DPQ_L.xpt` | DATA_RAW | MOVE | `25605a026850...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/FNQ_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/FNQ_L.xpt` | DATA_RAW | MOVE | `d140701b0ae0...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/HEQ_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/HEQ_L.xpt` | DATA_RAW | MOVE | `0d515ca8d866...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/KIQ_U_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/KIQ_U_L.xpt` | DATA_RAW | MOVE | `2f114aeee6e9...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/MCQ_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/MCQ_L.xpt` | DATA_RAW | MOVE | `0889bb3eaa5a...` | PRESERVED |
| `NHANES AUG'21 - AUG'23/QUESTIONNAIRE/SLQ_L.xpt` | `data/raw/nhanes_2021_2023/QUESTIONNAIRE/SLQ_L.xpt` | DATA_RAW | MOVE | `918c3258b2f4...` | PRESERVED |
| `results/comparative/final_benchmark_summary.json` | `artifacts/results/final_benchmark_summary.json` | ARTIFACT_RESULTS | MOVE | `64e10d0f60a6...` | PRESERVED |
| `results/comparative/leakage_gate_report.json` | `artifacts/results/leakage_gate_report.json` | ARTIFACT_RESULTS | MOVE | `f8b11479ed17...` | PRESERVED |
| `results/comparative/paired_bootstrap_phase3.json` | `artifacts/results/paired_bootstrap_phase3.json` | ARTIFACT_RESULTS | MOVE | `34eedfdc0310...` | PRESERVED |
| `results/comparative/paired_bootstrap_phase4.json` | `artifacts/results/paired_bootstrap_phase4.json` | ARTIFACT_RESULTS | MOVE | `9f57402e7268...` | PRESERVED |
| `results/comparative/paired_bootstrap_phase5.json` | `artifacts/results/paired_bootstrap_phase5.json` | ARTIFACT_RESULTS | MOVE | `140ae9bc0484...` | PRESERVED |
| `results/comparative/exp0_reproduction/Classical_HGNN_oof_predictions.csv` | `artifacts/results/exp0_reproduction/Classical_HGNN_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `9f73c2b45a72...` | PRESERVED |
| `results/comparative/exp0_reproduction/HSGIN_oof_predictions.csv` | `artifacts/results/exp0_reproduction/HSGIN_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `f77905f95b8d...` | PRESERVED |
| `results/comparative/exp0_reproduction/MLP_Regressor_oof_predictions.csv` | `artifacts/results/exp0_reproduction/MLP_Regressor_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `5eab3f912164...` | PRESERVED |
| `results/comparative/exp0_reproduction/Random_Forest_oof_predictions.csv` | `artifacts/results/exp0_reproduction/Random_Forest_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `8c383e74ee3b...` | PRESERVED |
| `results/comparative/exp0_reproduction/reproduction_comparison.md` | `artifacts/results/exp0_reproduction/reproduction_comparison.md` | ARTIFACT_RESULTS | MOVE | `0dbec6607707...` | PRESERVED |
| `results/comparative/exp0_reproduction/reproduction_report.json` | `artifacts/results/exp0_reproduction/reproduction_report.json` | ARTIFACT_RESULTS | MOVE | `d77584fdbcf8...` | PRESERVED |
| `results/comparative/exp0_reproduction/Ridge_Regression_oof_predictions.csv` | `artifacts/results/exp0_reproduction/Ridge_Regression_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `02d3e58b2f08...` | PRESERVED |
| `results/comparative/exp0_reproduction/XGBoost_oof_predictions.csv` | `artifacts/results/exp0_reproduction/XGBoost_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `7cd9a2fa02a0...` | PRESERVED |
| `results/comparative/exp1_linear_trees/ElasticNet_oof_predictions.csv` | `artifacts/results/exp1_linear_trees/ElasticNet_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `7565573255e0...` | PRESERVED |
| `results/comparative/exp1_linear_trees/exp1_results.json` | `artifacts/results/exp1_linear_trees/exp1_results.json` | ARTIFACT_RESULTS | MOVE | `a5a1ab40f683...` | PRESERVED |
| `results/comparative/exp1_linear_trees/exp1_summary.md` | `artifacts/results/exp1_linear_trees/exp1_summary.md` | ARTIFACT_RESULTS | MOVE | `65e528ee0545...` | PRESERVED |
| `results/comparative/exp1_linear_trees/ExtraTrees_oof_predictions.csv` | `artifacts/results/exp1_linear_trees/ExtraTrees_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `2617847951d1...` | PRESERVED |
| `results/comparative/exp1_linear_trees/RandomForest_oof_predictions.csv` | `artifacts/results/exp1_linear_trees/RandomForest_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `20234c320d2a...` | PRESERVED |
| `results/comparative/exp1_linear_trees/Ridge_oof_predictions.csv` | `artifacts/results/exp1_linear_trees/Ridge_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `bd77d29baf1b...` | PRESERVED |
| `results/comparative/exp2_boosting/CatBoost_oof_predictions.csv` | `artifacts/results/exp2_boosting/CatBoost_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `004376dacac9...` | PRESERVED |
| `results/comparative/exp2_boosting/exp2_results.json` | `artifacts/results/exp2_boosting/exp2_results.json` | ARTIFACT_RESULTS | MOVE | `34918fe64fce...` | PRESERVED |
| `results/comparative/exp2_boosting/exp2_summary.md` | `artifacts/results/exp2_boosting/exp2_summary.md` | ARTIFACT_RESULTS | MOVE | `db96001f1c5d...` | PRESERVED |
| `results/comparative/exp2_boosting/HistGradientBoosting_oof_predictions.csv` | `artifacts/results/exp2_boosting/HistGradientBoosting_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `ec2fc3c1efa1...` | PRESERVED |
| `results/comparative/exp2_boosting/LightGBM_oof_predictions.csv` | `artifacts/results/exp2_boosting/LightGBM_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `1c707b96031f...` | PRESERVED |
| `results/comparative/exp2_boosting/XGBoost_tuned_oof_predictions.csv` | `artifacts/results/exp2_boosting/XGBoost_tuned_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `76a1561e96c9...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/exp3_results.json` | `artifacts/results/exp3_deep_tabular/exp3_results.json` | ARTIFACT_RESULTS | MOVE | `423c529b8578...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/exp3_summary.md` | `artifacts/results/exp3_deep_tabular/exp3_summary.md` | ARTIFACT_RESULTS | MOVE | `6860de210dc4...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/FT_Transformer_ensemble_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/FT_Transformer_ensemble_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `dc0f0f855cb2...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/FT_Transformer_seed42_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/FT_Transformer_seed42_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `d6b5e29779be...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/FT_Transformer_seed43_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/FT_Transformer_seed43_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `a5e47b64630d...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/FT_Transformer_seed44_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/FT_Transformer_seed44_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `c8257e135173...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/MLP_Retuned_ensemble_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/MLP_Retuned_ensemble_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `7404ddb71206...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/MLP_Retuned_seed42_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/MLP_Retuned_seed42_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `35db65051ea0...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/MLP_Retuned_seed43_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/MLP_Retuned_seed43_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `2b3fa30e3325...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/MLP_Retuned_seed44_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/MLP_Retuned_seed44_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `1ec9f9250858...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/TabNet_ensemble_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/TabNet_ensemble_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `fd1d70905b2d...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/TabNet_seed42_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/TabNet_seed42_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `215317164f82...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/TabNet_seed43_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/TabNet_seed43_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `9faf7fc0130e...` | PRESERVED |
| `results/comparative/exp3_deep_tabular/TabNet_seed44_oof_predictions.csv` | `artifacts/results/exp3_deep_tabular/TabNet_seed44_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `a292a9b2e5b6...` | PRESERVED |
| `results/comparative/exp4_gnn/Classical_HGNN_ensemble_oof_predictions.csv` | `artifacts/results/exp4_gnn/Classical_HGNN_ensemble_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `2a9ebbcd27b9...` | PRESERVED |
| `results/comparative/exp4_gnn/Classical_HGNN_seed42_oof_predictions.csv` | `artifacts/results/exp4_gnn/Classical_HGNN_seed42_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `9f73c2b45a72...` | PRESERVED |
| `results/comparative/exp4_gnn/Classical_HGNN_seed43_oof_predictions.csv` | `artifacts/results/exp4_gnn/Classical_HGNN_seed43_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `a70903323149...` | PRESERVED |
| `results/comparative/exp4_gnn/Classical_HGNN_seed44_oof_predictions.csv` | `artifacts/results/exp4_gnn/Classical_HGNN_seed44_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `db893747d964...` | PRESERVED |
| `results/comparative/exp4_gnn/exp4_results.json` | `artifacts/results/exp4_gnn/exp4_results.json` | ARTIFACT_RESULTS | MOVE | `17d5376d4615...` | PRESERVED |
| `results/comparative/exp4_gnn/exp4_summary.md` | `artifacts/results/exp4_gnn/exp4_summary.md` | ARTIFACT_RESULTS | MOVE | `25e9e87de8b1...` | PRESERVED |
| `results/comparative/exp4_gnn/HSGIN_ensemble_oof_predictions.csv` | `artifacts/results/exp4_gnn/HSGIN_ensemble_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `176a168930c4...` | PRESERVED |
| `results/comparative/exp4_gnn/HSGIN_seed42_oof_predictions.csv` | `artifacts/results/exp4_gnn/HSGIN_seed42_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `f77905f95b8d...` | PRESERVED |
| `results/comparative/exp4_gnn/HSGIN_seed43_oof_predictions.csv` | `artifacts/results/exp4_gnn/HSGIN_seed43_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `8c99486cd19c...` | PRESERVED |
| `results/comparative/exp4_gnn/HSGIN_seed44_oof_predictions.csv` | `artifacts/results/exp4_gnn/HSGIN_seed44_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `40704f3da7e7...` | PRESERVED |
| `results/comparative/exp5_ensemble/diversity_analysis.json` | `artifacts/results/exp5_ensemble/diversity_analysis.json` | ARTIFACT_RESULTS | MOVE | `a5ccf2ba88ab...` | PRESERVED |
| `results/comparative/exp5_ensemble/exp5_results.json` | `artifacts/results/exp5_ensemble/exp5_results.json` | ARTIFACT_RESULTS | MOVE | `4ba4d190c47d...` | PRESERVED |
| `results/comparative/exp5_ensemble/exp5_summary.md` | `artifacts/results/exp5_ensemble/exp5_summary.md` | ARTIFACT_RESULTS | MOVE | `3ffbd4efc306...` | PRESERVED |
| `results/comparative/exp5_ensemble/inner_meta_predictions.npz` | `artifacts/results/exp5_ensemble/inner_meta_predictions.npz` | ARTIFACT_RESULTS | MOVE | `5c02b71c565c...` | PRESERVED |
| `results/comparative/exp5_ensemble/meta_leakage_audit.json` | `artifacts/results/exp5_ensemble/meta_leakage_audit.json` | ARTIFACT_RESULTS | MOVE | `b93747da1df3...` | PRESERVED |
| `results/comparative/exp5_ensemble/NNW_Blend_oof_predictions.csv` | `artifacts/results/exp5_ensemble/NNW_Blend_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `1b4a094e7639...` | PRESERVED |
| `results/comparative/exp5_ensemble/RidgeStacking_oof_predictions.csv` | `artifacts/results/exp5_ensemble/RidgeStacking_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `7e8f13f1bcd5...` | PRESERVED |
| `results/comparative/exp5_ensemble/SimpleAverage_oof_predictions.csv` | `artifacts/results/exp5_ensemble/SimpleAverage_oof_predictions.csv` | ARTIFACT_RESULTS | MOVE | `1ae36a75bc80...` | PRESERVED |
| `results/comparative/exp6_ablations/exp6a_bootstrap_holm.json` | `artifacts/results/exp6_ablations/exp6a_bootstrap_holm.json` | ARTIFACT_RESULTS | MOVE | `ea2bfb344213...` | PRESERVED |
| `results/comparative/exp6_ablations/exp6b_bootstrap_holm.json` | `artifacts/results/exp6_ablations/exp6b_bootstrap_holm.json` | ARTIFACT_RESULTS | MOVE | `4319ffcf47af...` | PRESERVED |
| `results/comparative/exp6_ablations/exp6_hsgin_results.json` | `artifacts/results/exp6_ablations/exp6_hsgin_results.json` | ARTIFACT_RESULTS | MOVE | `8a8d64f567da...` | PRESERVED |
| `results/comparative/exp6_ablations/exp6_xgboost_results.json` | `artifacts/results/exp6_ablations/exp6_xgboost_results.json` | ARTIFACT_RESULTS | MOVE | `4f9561f94776...` | PRESERVED |
| `results/comparative/exp6_ablations/exp6_xgboost_summary.md` | `artifacts/results/exp6_ablations/exp6_xgboost_summary.md` | ARTIFACT_RESULTS | MOVE | `012dc43e3c6b...` | PRESERVED |
| `results/comparative/exp6_ablations/exp7_bootstrap_holm.json` | `artifacts/results/exp6_ablations/exp7_bootstrap_holm.json` | ARTIFACT_RESULTS | MOVE | `30e1f2c0ffdd...` | PRESERVED |
| `results/comparative/exp6_ablations/exp7_graph_ablation_results.json` | `artifacts/results/exp6_ablations/exp7_graph_ablation_results.json` | ARTIFACT_RESULTS | MOVE | `5b7265e51b43...` | PRESERVED |
| `results/comparative/exp6_ablations/exp7_random_edges_multiseed_results.json` | `artifacts/results/exp6_ablations/exp7_random_edges_multiseed_results.json` | ARTIFACT_RESULTS | MOVE | `cf324712e6c7...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_FULL_25_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_FULL_25_oof.csv` | ARTIFACT_RESULTS | MOVE | `5c68903040be...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_LOO_Biomarker_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_LOO_Biomarker_oof.csv` | ARTIFACT_RESULTS | MOVE | `68bd027d4a35...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_LOO_Demographics_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_LOO_Demographics_oof.csv` | ARTIFACT_RESULTS | MOVE | `e0c01fe631dc...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_LOO_Heart_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_LOO_Heart_oof.csv` | ARTIFACT_RESULTS | MOVE | `469808bbba71...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_LOO_Kidney_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_LOO_Kidney_oof.csv` | ARTIFACT_RESULTS | MOVE | `5d2308661f49...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_LOO_Liver_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_LOO_Liver_oof.csv` | ARTIFACT_RESULTS | MOVE | `8948672412c9...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_Variant_FlatReadout_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_Variant_FlatReadout_oof.csv` | ARTIFACT_RESULTS | MOVE | `375bd297750d...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_Variant_HomoGNN_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_Variant_HomoGNN_oof.csv` | ARTIFACT_RESULTS | MOVE | `e824ec0a81e4...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_Variant_NoCrossTalk_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_Variant_NoCrossTalk_oof.csv` | ARTIFACT_RESULTS | MOVE | `3f0bd0c16f2b...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_ensemble_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_Variant_RandomEdges_ensemble_oof.csv` | ARTIFACT_RESULTS | MOVE | `d480581d2d9f...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_Variant_RandomEdges_oof.csv` | ARTIFACT_RESULTS | MOVE | `5b35b59867d8...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_seed43_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_Variant_RandomEdges_seed43_oof.csv` | ARTIFACT_RESULTS | MOVE | `d2ec7c92d2b9...` | PRESERVED |
| `results/comparative/exp6_ablations/HSGIN_Variant_RandomEdges_seed44_oof.csv` | `artifacts/results/exp6_ablations/HSGIN_Variant_RandomEdges_seed44_oof.csv` | ARTIFACT_RESULTS | MOVE | `15e80b774166...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_FULL_25_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_FULL_25_oof.csv` | ARTIFACT_RESULTS | MOVE | `aeb581c44625...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_LOO_Biomarker_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_LOO_Biomarker_oof.csv` | ARTIFACT_RESULTS | MOVE | `2c01ab99fb1e...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_LOO_Demographics_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_LOO_Demographics_oof.csv` | ARTIFACT_RESULTS | MOVE | `373102333e39...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_LOO_Heart_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_LOO_Heart_oof.csv` | ARTIFACT_RESULTS | MOVE | `6ce197006af8...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_LOO_Kidney_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_LOO_Kidney_oof.csv` | ARTIFACT_RESULTS | MOVE | `47bd62ced136...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_LOO_Liver_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_LOO_Liver_oof.csv` | ARTIFACT_RESULTS | MOVE | `3eb1a399544f...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_ONLY_Biomarker_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_ONLY_Biomarker_oof.csv` | ARTIFACT_RESULTS | MOVE | `8fddd7281135...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_ONLY_Demographics_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_ONLY_Demographics_oof.csv` | ARTIFACT_RESULTS | MOVE | `7f3720c1ce2f...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_ONLY_Heart_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_ONLY_Heart_oof.csv` | ARTIFACT_RESULTS | MOVE | `6aa0860e7f60...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_ONLY_Kidney_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_ONLY_Kidney_oof.csv` | ARTIFACT_RESULTS | MOVE | `c815f7aa263c...` | PRESERVED |
| `results/comparative/exp6_ablations/XGBoost_ONLY_Liver_oof.csv` | `artifacts/results/exp6_ablations/XGBoost_ONLY_Liver_oof.csv` | ARTIFACT_RESULTS | MOVE | `8a8a322cbe97...` | PRESERVED |
| `results/comparative/exp8_controls/exp8_controls_results.json` | `artifacts/results/exp8_controls/exp8_controls_results.json` | ARTIFACT_RESULTS | MOVE | `71202439cee2...` | PRESERVED |
| `results/comparative/exp8_controls/exp8_controls_summary.md` | `artifacts/results/exp8_controls/exp8_controls_summary.md` | ARTIFACT_RESULTS | MOVE | `60ce6ad827e5...` | PRESERVED |
| `results/comparative/exp8_controls/hsgin_100perms_distribution.json` | `artifacts/results/exp8_controls/hsgin_100perms_distribution.json` | ARTIFACT_RESULTS | MOVE | `21e84015928c...` | PRESERVED |
| `results/comparative/exp8_controls/LEAKY_DEMO_Exact_LogFormula_Ridge_oof.csv` | `artifacts/results/exp8_controls/LEAKY_DEMO_Exact_LogFormula_Ridge_oof.csv` | ARTIFACT_RESULTS | MOVE | `0cad5211d97d...` | PRESERVED |
| `results/comparative/exp8_controls/LEAKY_DEMO_MLP_Leaky_Full29_oof.csv` | `artifacts/results/exp8_controls/LEAKY_DEMO_MLP_Leaky_Full29_oof.csv` | ARTIFACT_RESULTS | MOVE | `bb9be251c331...` | PRESERVED |
| `results/comparative/exp8_controls/LEAKY_DEMO_MLP_Leaky_Raw4_oof.csv` | `artifacts/results/exp8_controls/LEAKY_DEMO_MLP_Leaky_Raw4_oof.csv` | ARTIFACT_RESULTS | MOVE | `1f51def95e74...` | PRESERVED |
| `results/comparative/exp8_controls/LEAKY_DEMO_Ridge_Leaky_Full29_oof.csv` | `artifacts/results/exp8_controls/LEAKY_DEMO_Ridge_Leaky_Full29_oof.csv` | ARTIFACT_RESULTS | MOVE | `e3f1d97411dd...` | PRESERVED |
| `results/comparative/exp8_controls/LEAKY_DEMO_Ridge_Leaky_Raw4_oof.csv` | `artifacts/results/exp8_controls/LEAKY_DEMO_Ridge_Leaky_Raw4_oof.csv` | ARTIFACT_RESULTS | MOVE | `575948b21500...` | PRESERVED |
| `results/comparative/exp8_controls/LEAKY_DEMO_XGBoost_Leaky_Full29_oof.csv` | `artifacts/results/exp8_controls/LEAKY_DEMO_XGBoost_Leaky_Full29_oof.csv` | ARTIFACT_RESULTS | MOVE | `f667c04f0873...` | PRESERVED |
| `results/comparative/exp8_controls/LEAKY_DEMO_XGBoost_Leaky_Raw4_oof.csv` | `artifacts/results/exp8_controls/LEAKY_DEMO_XGBoost_Leaky_Raw4_oof.csv` | ARTIFACT_RESULTS | MOVE | `9a0f279c5f0b...` | PRESERVED |
| `results/comparative/exp8_controls/parts/hsgin_perms_11_25.json` | `artifacts/results/exp8_controls/parts/hsgin_perms_11_25.json` | ARTIFACT_RESULTS | MOVE | `fc97acfc6783...` | PRESERVED |
| `results/comparative/exp8_controls/parts/hsgin_perms_26_40.json` | `artifacts/results/exp8_controls/parts/hsgin_perms_26_40.json` | ARTIFACT_RESULTS | MOVE | `e985a1c23317...` | PRESERVED |
| `results/comparative/exp8_controls/parts/hsgin_perms_41_55.json` | `artifacts/results/exp8_controls/parts/hsgin_perms_41_55.json` | ARTIFACT_RESULTS | MOVE | `ff7e92db40ce...` | PRESERVED |
| `results/comparative/exp8_controls/parts/hsgin_perms_56_70.json` | `artifacts/results/exp8_controls/parts/hsgin_perms_56_70.json` | ARTIFACT_RESULTS | MOVE | `ec79b9cdd408...` | PRESERVED |
| `results/comparative/exp8_controls/parts/hsgin_perms_71_85.json` | `artifacts/results/exp8_controls/parts/hsgin_perms_71_85.json` | ARTIFACT_RESULTS | MOVE | `5b81db293a33...` | PRESERVED |
| `results/comparative/exp8_controls/parts/hsgin_perms_86_100.json` | `artifacts/results/exp8_controls/parts/hsgin_perms_86_100.json` | ARTIFACT_RESULTS | MOVE | `4870652ddbea...` | PRESERVED |
| `results/comparative/exp9_subgroups/exp9_subgroups_summary.md` | `artifacts/results/exp9_subgroups/exp9_subgroups_summary.md` | ARTIFACT_RESULTS | MOVE | `8e57d13aa1d6...` | PRESERVED |
| `results/comparative/exp9_subgroups/exp9_subgroup_results.json` | `artifacts/results/exp9_subgroups/exp9_subgroup_results.json` | ARTIFACT_RESULTS | MOVE | `e4f55a2ce1f8...` | PRESERVED |
| `results/comparative/exp9_subgroups/subgroup_patient_evaluations.csv` | `artifacts/results/exp9_subgroups/subgroup_patient_evaluations.csv` | ARTIFACT_RESULTS | MOVE | `c727619b8581...` | PRESERVED |
| `results/comparative/explainability/domain_importance_summary.csv` | `artifacts/results/explainability/domain_importance_summary.csv` | ARTIFACT_RESULTS | MOVE | `fbe6d9c83796...` | PRESERVED |
| `results/comparative/explainability/explainability_results.json` | `artifacts/results/explainability/explainability_results.json` | ARTIFACT_RESULTS | MOVE | `973b17c90901...` | PRESERVED |
| `results/comparative/explainability/feature_permutation_importance.csv` | `artifacts/results/explainability/feature_permutation_importance.csv` | ARTIFACT_RESULTS | MOVE | `4c0cd4d82091...` | PRESERVED |
| `results/comparative/explainability/reconciled_domain_attribution.json` | `artifacts/results/explainability/reconciled_domain_attribution.json` | ARTIFACT_RESULTS | MOVE | `5cf6c0eb4111...` | PRESERVED |
| `src/comparative/base_adapter.py` | `src/organix/experiments/base_adapter.py` | SOURCE_CODE | REFACTOR | `aeda3d216765...` | PRESERVED |
| `src/comparative/compute_multiple_corrections.py` | `src/organix/experiments/compute_multiple_corrections.py` | SOURCE_CODE | REFACTOR | `d00e22e33e6c...` | PRESERVED |
| `src/comparative/deep_tabular.py` | `src/organix/experiments/deep_tabular.py` | SOURCE_CODE | REFACTOR | `3ae58255efb8...` | PRESERVED |
| `src/comparative/exp0_reproduction.py` | `src/organix/experiments/exp0_reproduction.py` | SOURCE_CODE | REFACTOR | `c6c629f34411...` | PRESERVED |
| `src/comparative/exp1_linear_trees.py` | `src/organix/experiments/exp1_linear_trees.py` | SOURCE_CODE | REFACTOR | `6c61a9dbedf7...` | PRESERVED |
| `src/comparative/exp2_boosting.py` | `src/organix/experiments/exp2_boosting.py` | SOURCE_CODE | REFACTOR | `8ea5017541de...` | PRESERVED |
| `src/comparative/exp3_deep_tabular.py` | `src/organix/experiments/exp3_deep_tabular.py` | SOURCE_CODE | REFACTOR | `f9eaa519776f...` | PRESERVED |
| `src/comparative/exp4_gnn.py` | `src/organix/experiments/exp4_gnn.py` | SOURCE_CODE | REFACTOR | `b90cceb1b28f...` | PRESERVED |
| `src/comparative/exp5_ensemble.py` | `src/organix/experiments/exp5_ensemble.py` | SOURCE_CODE | REFACTOR | `41cc704ca556...` | PRESERVED |
| `src/comparative/exp6_ablations.py` | `src/organix/experiments/exp6_ablations.py` | SOURCE_CODE | REFACTOR | `bc79293ea4d1...` | PRESERVED |
| `src/comparative/finalize_phase6_audit.py` | `src/organix/experiments/finalize_phase6_audit.py` | SOURCE_CODE | REFACTOR | `c98bddc482fc...` | PRESERVED |
| `src/comparative/finalize_phase7_report.py` | `src/organix/experiments/finalize_phase7_report.py` | SOURCE_CODE | REFACTOR | `5b8ab77a7c64...` | PRESERVED |
| `src/comparative/leakage_gate.py` | `src/organix/experiments/leakage_gate.py` | SOURCE_CODE | REFACTOR | `b987e544b67e...` | PRESERVED |
| `src/comparative/metrics.py` | `src/organix/experiments/metrics.py` | SOURCE_CODE | REFACTOR | `5899ea08d9d0...` | PRESERVED |
| `src/comparative/paired_tests.py` | `src/organix/experiments/paired_tests.py` | SOURCE_CODE | REFACTOR | `6a7a6e2e6a57...` | PRESERVED |
| `src/comparative/pipeline.py` | `src/organix/data/pipeline.py` | SOURCE_CODE | REFACTOR | `24d33b42b597...` | PRESERVED |
| `src/comparative/reconcile_liver_contribution.py` | `src/organix/experiments/reconcile_liver_contribution.py` | SOURCE_CODE | REFACTOR | `8f9ce1ba4bbe...` | PRESERVED |
| `src/comparative/rerun_exp7_random_edges.py` | `src/organix/experiments/rerun_exp7_random_edges.py` | SOURCE_CODE | REFACTOR | `ca9681dedcc8...` | PRESERVED |
| `src/comparative/run_exp6b_hsgin.py` | `src/organix/experiments/run_exp6b_hsgin.py` | SOURCE_CODE | REFACTOR | `1b00f85bc278...` | PRESERVED |
| `src/comparative/run_exp6_xgboost.py` | `src/organix/experiments/run_exp6_xgboost.py` | SOURCE_CODE | REFACTOR | `51c2427f55b9...` | PRESERVED |
| `src/comparative/run_exp7_graph_ablations.py` | `src/organix/experiments/run_exp7_graph_ablations.py` | SOURCE_CODE | REFACTOR | `de0ea5328188...` | PRESERVED |
| `src/comparative/run_exp7_random_edges_multiseed.py` | `src/organix/experiments/run_exp7_random_edges_multiseed.py` | SOURCE_CODE | REFACTOR | `d4ec28a95e93...` | PRESERVED |
| `src/comparative/run_exp8_controls.py` | `src/organix/experiments/run_exp8_controls.py` | SOURCE_CODE | REFACTOR | `ad7aa48d2a04...` | PRESERVED |
| `src/comparative/run_exp8_hsgin_100perms.py` | `src/organix/experiments/run_exp8_hsgin_100perms.py` | SOURCE_CODE | REFACTOR | `7beafefa766d...` | PRESERVED |
| `src/comparative/run_exp8_multiprocess.py` | `src/organix/experiments/run_exp8_multiprocess.py` | SOURCE_CODE | REFACTOR | `838eff5d0b12...` | PRESERVED |
| `src/comparative/run_exp8_worker.py` | `src/organix/experiments/run_exp8_worker.py` | SOURCE_CODE | REFACTOR | `c748ffba0d2e...` | PRESERVED |
| `src/comparative/run_exp9_subgroups.py` | `src/organix/experiments/run_exp9_subgroups.py` | SOURCE_CODE | REFACTOR | `cdb7b81aa652...` | PRESERVED |
| `src/comparative/run_phase8_synthesis.py` | `src/organix/experiments/run_phase8_synthesis.py` | SOURCE_CODE | REFACTOR | `72618ff3234a...` | PRESERVED |
| `src/comparative/split.py` | `src/organix/experiments/split.py` | SOURCE_CODE | REFACTOR | `de0d6e197f98...` | PRESERVED |
| `src/comparative/__init__.py` | `src/organix/experiments/__init__.py` | SOURCE_CODE | REFACTOR | `8e5966f59193...` | PRESERVED |
| `src/comparative/models/baselines.py` | `src/organix/models/baselines.py` | SOURCE_CODE | REFACTOR | `2e24f4e6b8ce...` | PRESERVED |
| `src/comparative/models/hsgin.py` | `src/organix/models/hsgin.py` | SOURCE_CODE | REFACTOR | `4d9bd5a8372e...` | PRESERVED |
| `src/comparative/models/__init__.py` | `src/organix/models/__init__.py` | SOURCE_CODE | REFACTOR | `e3b0c44298fc...` | PRESERVED |
| `src/comparative/__pycache__/leakage_gate.cpython-310.pyc` | `src/organix/experiments/leakage_gate.cpython-310.pyc` | SOURCE_CODE | REFACTOR | `6b1a5c83445d...` | PRESERVED |
| `src/comparative/__pycache__/__init__.cpython-310.pyc` | `src/organix/experiments/__init__.cpython-310.pyc` | SOURCE_CODE | REFACTOR | `e196e05e6fe6...` | PRESERVED |
| `technical_evidence_package/README.md` | `docs/technical_evidence/README.md` | DOC_EVIDENCE | MOVE | `3fcb7eabc4d8...` | PRESERVED |
| `technical_evidence_package/01_repository_architecture/01_repository_tree.md` | `docs/technical_evidence/01_repository_architecture/01_repository_tree.md` | DOC_EVIDENCE | MOVE | `df7fd13f6eff...` | PRESERVED |
| `technical_evidence_package/01_repository_architecture/02_python_sources_manifest.md` | `docs/technical_evidence/01_repository_architecture/02_python_sources_manifest.md` | DOC_EVIDENCE | MOVE | `b53826870ba1...` | PRESERVED |
| `technical_evidence_package/02_dataset_and_features/01_dataset_and_provenance.md` | `docs/technical_evidence/02_dataset_and_features/01_dataset_and_provenance.md` | DOC_EVIDENCE | MOVE | `7a34c0c80d01...` | PRESERVED |
| `technical_evidence_package/02_dataset_and_features/02_locked_25_feature_manifest.md` | `docs/technical_evidence/02_dataset_and_features/02_locked_25_feature_manifest.md` | DOC_EVIDENCE | MOVE | `cf8f5af4ee94...` | PRESERVED |
| `technical_evidence_package/03_target_formulation/fib4_target_specification.md` | `docs/technical_evidence/03_target_formulation/fib4_target_specification.md` | DOC_EVIDENCE | MOVE | `0a7bf0e60ec2...` | PRESERVED |
| `technical_evidence_package/04_graph_neural_network_architecture/hsgin_architecture_implementation.md` | `docs/technical_evidence/04_graph_neural_network_architecture/hsgin_architecture_implementation.md` | DOC_EVIDENCE | MOVE | `57fc132e5ecf...` | PRESERVED |
| `technical_evidence_package/05_preprocessing_and_leakage_controls/preprocessing_folds_and_leakage_controls.md` | `docs/technical_evidence/05_preprocessing_and_leakage_controls/preprocessing_folds_and_leakage_controls.md` | DOC_EVIDENCE | MOVE | `146fe1b5ffa8...` | PRESERVED |
| `technical_evidence_package/06_models_and_hyperparameters/model_configurations_and_training_procedures.md` | `docs/technical_evidence/06_models_and_hyperparameters/model_configurations_and_training_procedures.md` | DOC_EVIDENCE | MOVE | `36c805b4671f...` | PRESERVED |
| `technical_evidence_package/07_experiments_0_to_9_implementation/experiments_0_to_9_implementation_details.md` | `docs/technical_evidence/07_experiments_0_to_9_implementation/experiments_0_to_9_implementation_details.md` | DOC_EVIDENCE | MOVE | `658c98b5bcba...` | PRESERVED |
| `technical_evidence_package/08_benchmark_results_and_statistics/benchmark_results_metrics_and_statistical_outputs.md` | `docs/technical_evidence/08_benchmark_results_and_statistics/benchmark_results_metrics_and_statistical_outputs.md` | DOC_EVIDENCE | MOVE | `cbacd6bb0ef5...` | PRESERVED |
| `technical_evidence_package/09_ablations_controls_and_subgroups/y_randomization_ablations_ensembles_and_subgroups.md` | `docs/technical_evidence/09_ablations_controls_and_subgroups/y_randomization_ablations_ensembles_and_subgroups.md` | DOC_EVIDENCE | MOVE | `8a34f123e600...` | PRESERVED |
| `technical_evidence_package/10_verification_and_logs/automated_tests_execution_logs_and_verification.md` | `docs/technical_evidence/10_verification_and_logs/automated_tests_execution_logs_and_verification.md` | DOC_EVIDENCE | MOVE | `68eb45411927...` | PRESERVED |
| `technical_evidence_package/11_environment_and_reproduction/environment_dependencies_and_reproduction.md` | `docs/technical_evidence/11_environment_and_reproduction/environment_dependencies_and_reproduction.md` | DOC_EVIDENCE | MOVE | `5b97aff2ec82...` | PRESERVED |
| `technical_evidence_package/12_checkpoint_and_artifact_inventory/checkpoint_inventory_and_artifact_paths.md` | `docs/technical_evidence/12_checkpoint_and_artifact_inventory/checkpoint_inventory_and_artifact_paths.md` | DOC_EVIDENCE | MOVE | `7968b8e3023b...` | PRESERVED |
| `tests/test_leakage_gate.py` | `tests/test_leakage_gate.py` | TESTS | REFACTOR | `7151b140eb28...` | PRESERVED |
| `tests/test_splits.py` | `tests/test_splits.py` | TESTS | REFACTOR | `7cc072fb1af4...` | PRESERVED |
| `tests/__pycache__/test_leakage_gate.cpython-310.pyc` | `tests/test_leakage_gate.cpython-310.pyc` | TESTS | REFACTOR | `3753b30c78d7...` | PRESERVED |
| `tests/__pycache__/test_splits.cpython-310.pyc` | `tests/test_splits.cpython-310.pyc` | TESTS | REFACTOR | `790dfb46458d...` | PRESERVED |
