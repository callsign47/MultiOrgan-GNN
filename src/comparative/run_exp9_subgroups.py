import os, sys, json
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.abspath('.'))
from src.comparative.pipeline import FINAL_COHORT_PATH
from src.comparative.metrics import compute_regression_metrics

OUT_DIR = r"results/comparative/exp9_subgroups"
CFG_DIR = r"configs/comparative/exp9_subgroups"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CFG_DIR, exist_ok=True)

OOF_PATHS = {
    "HSGIN": r"results/comparative/exp4_gnn/HSGIN_seed42_oof_predictions.csv",
    "XGBoost": r"results/comparative/exp2_boosting/XGBoost_tuned_oof_predictions.csv",
    "NNW_Blend": r"results/comparative/exp5_ensemble/NNW_Blend_oof_predictions.csv",
    "Ridge": r"results/comparative/exp1_linear_trees/Ridge_oof_predictions.csv"
}

def bootstrap_subgroup_ci(y_true, y_pred, n_bootstraps=2000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    if n < 5:
        return {"r2_ci": [None, None], "rmse_ci": [None, None], "mae_ci": [None, None]}

    boot_r2, boot_rmse, boot_mae = [], [], []
    for _ in range(n_bootstraps):
        idx = rng.choice(n, size=n, replace=True)
        yt_b, yp_b = y_true[idx], y_pred[idx]
        m = compute_regression_metrics(yt_b, yp_b)
        boot_r2.append(m["r2"])
        boot_rmse.append(m["rmse"])
        boot_mae.append(m["mae"])

    return {
        "r2_ci": [float(np.percentile(boot_r2, 2.5)), float(np.percentile(boot_r2, 97.5))],
        "rmse_ci": [float(np.percentile(boot_rmse, 2.5)), float(np.percentile(boot_rmse, 97.5))],
        "mae_ci": [float(np.percentile(boot_mae, 2.5)), float(np.percentile(boot_mae, 97.5))]
    }

def compute_extended_metrics(y_true, y_pred, seed=42):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    n = len(y_true)

    base = compute_regression_metrics(y_true, y_pred)
    bias = float(np.mean(y_pred - y_true))

    # Correlation metrics
    if n > 2 and np.std(y_true) > 1e-9 and np.std(y_pred) > 1e-9:
        pearson_r, _ = stats.pearsonr(y_true, y_pred)
        spearman_rho, _ = stats.spearmanr(y_true, y_pred)
    else:
        pearson_r, spearman_rho = 0.0, 0.0

    ci = bootstrap_subgroup_ci(y_true, y_pred, n_bootstraps=2000, seed=seed)

    return {
        "n": int(n),
        "r2": float(base["r2"]),
        "r2_ci": ci["r2_ci"],
        "rmse": float(base["rmse"]),
        "rmse_ci": ci["rmse_ci"],
        "mae": float(base["mae"]),
        "mae_ci": ci["mae_ci"],
        "pearson_r": float(pearson_r),
        "spearman_rho": float(spearman_rho),
        "bias": bias,
        "true_mean": float(np.mean(y_true)),
        "true_std": float(np.std(y_true)),
        "pred_mean": float(np.mean(y_pred)),
        "pred_std": float(np.std(y_pred))
    }

def compute_clinical_classification_metrics(y_true, y_pred):
    """
    Evaluates clinical risk categorization performance:
    Threshold 1: Low Risk rule-out (< 1.30)
    Threshold 2: High Risk rule-in (> 2.67)
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    # Threshold 1.30 (Low vs Not-Low)
    true_low = (y_true < 1.30)
    pred_low = (y_pred < 1.30)
    tp_low = np.sum(pred_low & true_low)
    fp_low = np.sum(pred_low & ~true_low)
    fn_low = np.sum(~pred_low & true_low)
    tn_low = np.sum(~pred_low & ~true_low)

    sens_low = tp_low / (tp_low + fn_low) if (tp_low + fn_low) > 0 else 0.0
    spec_low = tn_low / (tn_low + fp_low) if (tn_low + fp_low) > 0 else 0.0
    npv_low  = tn_low / (tn_low + fn_low) if (tn_low + fn_low) > 0 else 0.0
    acc_low  = (tp_low + tn_low) / len(y_true)

    # Threshold 2.67 (High vs Not-High)
    true_high = (y_true > 2.67)
    pred_high = (y_pred > 2.67)
    tp_high = np.sum(pred_high & true_high)
    fp_high = np.sum(pred_high & ~true_high)
    fn_high = np.sum(~pred_high & true_high)
    tn_high = np.sum(~pred_high & ~true_high)

    sens_high = tp_high / (tp_high + fn_high) if (tp_high + fn_high) > 0 else 0.0
    spec_high = tn_high / (tn_high + fp_high) if (tn_high + fp_high) > 0 else 0.0
    ppv_high  = tp_high / (tp_high + fp_high) if (tp_high + fp_high) > 0 else 0.0
    acc_high  = (tp_high + tn_high) / len(y_true)

    # 3-class concordance (Low, Indeterminate, High)
    true_cat = np.where(y_true < 1.30, 0, np.where(y_true <= 2.67, 1, 2))
    pred_cat = np.where(y_pred < 1.30, 0, np.where(y_pred <= 2.67, 1, 2))
    concordance = float(np.mean(true_cat == pred_cat))

    return {
        "rule_out_1_30": {
            "sensitivity": float(sens_low),
            "specificity": float(spec_low),
            "npv": float(npv_low),
            "accuracy": float(acc_low)
        },
        "rule_in_2_67": {
            "sensitivity": float(sens_high),
            "specificity": float(spec_high),
            "ppv": float(ppv_high),
            "accuracy": float(acc_high)
        },
        "overall_3class_concordance": concordance
    }

def main():
    print("=" * 74)
    print("  EXPERIMENT 9: CLINICAL ROBUSTNESS & SUBGROUP ANALYSIS")
    print("=" * 74)

    # 1. Load cohort data
    print("Loading cohort data...")
    cohort_df = pd.read_csv(FINAL_COHORT_PATH)
    print(f"Cohort loaded: {len(cohort_df)} patients, {cohort_df.shape[1]} columns.")

    # 2. Load out-of-fold predictions
    oof_dfs = {}
    for mname, p in OOF_PATHS.items():
        df = pd.read_csv(p)
        df = df.sort_values("SEQN").reset_index(drop=True)
        oof_dfs[mname] = df
        print(f"Loaded OOF for {mname}: {len(df)} rows.")

    # Validate alignment
    ref_seqns = cohort_df["SEQN"].values
    ref_df = cohort_df.sort_values("SEQN").reset_index(drop=True)
    for mname, df in oof_dfs.items():
        assert np.array_equal(df["SEQN"].values, ref_df["SEQN"].values), f"SEQN mismatch in {mname}"
        assert np.allclose(df["y_true"].values, ref_df["fib4_target"].values), f"y_true mismatch in {mname}"
    print("Alignment verified across all models: 100% exact match.")

    # Create master merged analysis dataframe
    merged = ref_df.copy()
    for mname, df in oof_dfs.items():
        merged[f"pred_{mname}"] = df["y_pred"].values

    # Define Subgroups
    subgroups_dict = {}

    # A. Clinical FIB-4 Strata
    merged["stratum_fib4"] = np.where(
        merged["fib4_target"] < 1.30, "Low (<1.30)",
        np.where(merged["fib4_target"] <= 2.67, "Indeterminate (1.30-2.67)", "High (>2.67)")
    )
    for cat in ["Low (<1.30)", "Indeterminate (1.30-2.67)", "High (>2.67)"]:
        subgroups_dict[f"Clinical_FIB4_{cat}"] = (merged["stratum_fib4"] == cat)

    # B. Demographics: Sex
    subgroups_dict["Sex_Male"]   = (merged["RIAGENDR"] == 1)
    subgroups_dict["Sex_Female"] = (merged["RIAGENDR"] == 2)

    # C. Demographics: Age Bands (Evaluated as subgroup; NOT used as predictor)
    subgroups_dict["Age_Young_<45"]       = (merged["RIDAGEYR"] < 45)
    subgroups_dict["Age_Middle_45_to_64"] = (merged["RIDAGEYR"] >= 45) & (merged["RIDAGEYR"] < 65)
    subgroups_dict["Age_Elderly_65+"]     = (merged["RIDAGEYR"] >= 65)

    # D. Metabolic Comorbidities: Hypertension
    subgroups_dict["Hypertension_Yes"] = (merged["BPQ020"] == 1)
    subgroups_dict["Hypertension_No"]  = (merged["BPQ020"] == 2)

    # E. Metabolic Comorbidities: Diabetes
    subgroups_dict["Diabetes_Yes"] = (merged["DIQ010"] == 1)
    subgroups_dict["Diabetes_No"]  = (merged["DIQ010"] == 2)

    # F. Liver Steatosis (CAP Score threshold 248 dB/m for S1+ steatosis)
    cap_valid = merged["LUXCAPM"].notna()
    subgroups_dict["Steatosis_Normal_<248"]   = cap_valid & (merged["LUXCAPM"] < 248)
    subgroups_dict["Steatosis_Elevated_248+"] = cap_valid & (merged["LUXCAPM"] >= 248)

    # G. Body Mass Index (BMI)
    bmi_valid = merged["BMXBMI"].notna()
    subgroups_dict["BMI_Normal_<25"]     = bmi_valid & (merged["BMXBMI"] < 25)
    subgroups_dict["BMI_Overweight_25-29"] = bmi_valid & (merged["BMXBMI"] >= 25) & (merged["BMXBMI"] < 30)
    subgroups_dict["BMI_Obese_30+"]       = bmi_valid & (merged["BMXBMI"] >= 30)

    # Save patient-level subgroup evaluation CSV
    eval_csv = os.path.join(OUT_DIR, "subgroup_patient_evaluations.csv")
    cols_to_save = [
        "SEQN", "patient_uid", "fib4_target", "stratum_fib4",
        "RIAGENDR", "RIDAGEYR", "BPQ020", "DIQ010", "LUXCAPM", "BMXBMI",
        "pred_HSGIN", "pred_XGBoost", "pred_NNW_Blend", "pred_Ridge"
    ]
    merged[cols_to_save].to_csv(eval_csv, index=False)
    print(f"Saved patient-level subgroup CSV: {eval_csv}")

    # Compute Subgroup Performance & Clinical Classification Concordance
    results = {
        "experiment": "Exp9_ClinicalRobustness_Subgroups",
        "cohort_size": int(len(merged)),
        "subgroups": {},
        "clinical_classification_concordance": {}
    }

    # Evaluate Clinical Concordance for each model overall
    for mname in OOF_PATHS.keys():
        cc = compute_clinical_classification_metrics(merged["fib4_target"].values, merged[f"pred_{mname}"].values)
        results["clinical_classification_concordance"][mname] = cc

    print("\n--- Subgroup Evaluation ---")
    for sname, mask in subgroups_dict.items():
        sub_df = merged[mask]
        n_sub = len(sub_df)
        pct_sub = (n_sub / len(merged)) * 100

        sub_res = {
            "sample_size": n_sub,
            "percentage_cohort": round(pct_sub, 2),
            "evaluable": bool(n_sub >= 100),
            "models": {}
        }

        if n_sub < 100:
            print(f"  [{sname}] N={n_sub} (<100) -> Flagged NOT EVALUABLE.")
            results["subgroups"][sname] = sub_res
            continue

        y_true_sub = sub_df["fib4_target"].values
        for mname in OOF_PATHS.keys():
            y_pred_sub = sub_df[f"pred_{mname}"].values
            ext_m = compute_extended_metrics(y_true_sub, y_pred_sub, seed=42)
            sub_res["models"][mname] = ext_m

        results["subgroups"][sname] = sub_res
        hsgin_m = sub_res["models"]["HSGIN"]
        xgb_m   = sub_res["models"]["XGBoost"]
        nnw_m   = sub_res["models"]["NNW_Blend"]
        print(f"  {sname:30s} | N={n_sub:4d} ({pct_sub:4.1f}%) | HSGIN R2={hsgin_m['r2']:+.4f} (RMSE={hsgin_m['rmse']:.3f}) | XGB R2={xgb_m['r2']:+.4f} | NNW R2={nnw_m['r2']:+.4f}")

    # Save results JSON
    res_json = os.path.join(OUT_DIR, "exp9_subgroup_results.json")
    with open(res_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nMaster JSON saved: {res_json}")

    # Generate Summary Markdown
    summary_md = os.path.join(OUT_DIR, "exp9_subgroups_summary.md")
    with open(summary_md, "w", encoding="utf-8") as f:
        f.write("# Experiment 9: Clinical Robustness & Subgroup Analysis Summary\n\n")
        f.write(f"**Cohort Size**: $N = {len(merged)}$ patients (NHANES 2017\u20132020 pre-pandemic)\n\n")

        f.write("## 1. Clinical FIB-4 Risk Stratification & Classification Concordance\n\n")
        f.write("| Model | Low-Risk Rule-Out (<1.30) Sens / Spec / NPV | High-Risk Rule-In (>2.67) Sens / Spec / PPV | 3-Class Concordance |\n")
        f.write("| :--- | :---: | :---: | :---: |\n")
        for mname in ["HSGIN", "XGBoost", "NNW_Blend", "Ridge"]:
            cc = results["clinical_classification_concordance"][mname]
            r_out = cc["rule_out_1_30"]
            r_in  = cc["rule_in_2_67"]
            f.write(f"| **{mname}** | {r_out['sensitivity']*100:.1f}% / {r_out['specificity']*100:.1f}% / **{r_out['npv']*100:.1f}%** | {r_in['sensitivity']*100:.1f}% / {r_in['specificity']*100:.1f}% / **{r_in['ppv']*100:.1f}%** | **{cc['overall_3class_concordance']*100:.1f}%** |\n")

        f.write("\n---\n\n## 2. Demographic & Comorbidity Subgroup Performance Table\n\n")
        f.write("| Subgroup Category | Subgroup Name | Sample Size ($N$) | Cohort % | HSGIN Pooled $R^2$ [95% CI] | XGBoost Pooled $R^2$ [95% CI] | NNW Blend Pooled $R^2$ | Ridge Pooled $R^2$ |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n")

        cat_names = {
            "Clinical_FIB4": "Clinical Risk Strata",
            "Sex": "Biological Sex",
            "Age": "Age Cohort",
            "Hypertension": "Hypertension History",
            "Diabetes": "Diabetes History",
            "Steatosis": "Liver Steatosis (CAP)",
            "BMI": "Body Mass Index"
        }

        for sname, sdata in results["subgroups"].items():
            if not sdata["evaluable"]:
                continue
            cat = sname.split("_")[0]
            cat_display = cat_names.get(cat, cat)
            clean_name = sname.replace(f"{cat}_", "")
            h_m = sdata["models"]["HSGIN"]
            x_m = sdata["models"]["XGBoost"]
            n_m = sdata["models"]["NNW_Blend"]
            r_m = sdata["models"]["Ridge"]

            h_ci = f"[{h_m['r2_ci'][0]:+.3f}, {h_m['r2_ci'][1]:+.3f}]" if h_m['r2_ci'][0] is not None else "N/A"
            x_ci = f"[{x_m['r2_ci'][0]:+.3f}, {x_m['r2_ci'][1]:+.3f}]" if x_m['r2_ci'][0] is not None else "N/A"

            f.write(f"| {cat_display} | **{clean_name}** | {sdata['sample_size']:,} | {sdata['percentage_cohort']:.1f}% | **{h_m['r2']:+.4f}** {h_ci} | {x_m['r2']:+.4f} {x_ci} | **{n_m['r2']:+.4f}** | {r_m['r2']:+.4f} |\n")

    print(f"Summary markdown saved: {summary_md}")

if __name__ == "__main__":
    main()
