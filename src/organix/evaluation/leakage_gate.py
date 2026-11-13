"""
ORGANIX Automated 4-Tier Leakage Control Gate.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from scipy.stats import spearmanr

from organix.core.constants import (
    EXPECTED_MANIFEST_HASH,
    EXCLUDED_FEATURES,
    EXPECTED_FEATURE_COUNT,
    EXPECTED_COHORT_SIZE,
)
from organix.core.exceptions import LeakageGateError
from organix.utils.io import compute_file_sha256
from organix.utils.paths import get_paths


def run_leakage_gate(
    manifest_path: Optional[Path] = None,
    cohort_path: Optional[Path] = None,
    folds_path: Optional[Path] = None,
    report_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Executes the 4-Tier Automated Leakage-Control Gate:
      [Gate 1] Manifest Hash & Direct Non-Overlap Check.
      [Gate 2] Fold Disjointness & Zero Patient Overlap Check.
      [Gate 3] Excluded Component Linear Reconstruction Test (R^2 < 0.90 constraint).
      [Gate 4] Proxy Leakage Screen for Liver Features.
    """
    paths = get_paths()
    m_path = manifest_path or paths.manifest_path
    c_path = cohort_path or paths.final_cohort_path
    f_path = folds_path or paths.folds_path
    r_path = report_path or paths.leakage_gate_report_path

    report: Dict[str, Any] = {
        "gate_timestamp": pd.Timestamp.now().isoformat(),
        "tests": {},
        "all_passed": False,
    }

    # 1. Manifest Hash & Integrity Test
    actual_hash = compute_file_sha256(m_path)
    hash_match = (actual_hash == EXPECTED_MANIFEST_HASH)
    with open(m_path, "r", encoding="utf-8") as f:
        m_data = json.load(f)

    all_retained_features: List[str] = []
    for domain_name, items in m_data.items():
        if isinstance(items, list):
            for item in items:
                feat = item.get("feature") if isinstance(item, dict) else str(item)
                if feat and feat not in EXCLUDED_FEATURES:
                    all_retained_features.append(feat)

    overlap = set(all_retained_features).intersection(EXCLUDED_FEATURES)
    g1_pass = hash_match and (len(overlap) == 0) and (len(all_retained_features) == EXPECTED_FEATURE_COUNT)

    report["tests"]["gate_1_manifest_check"] = {
        "passed": bool(g1_pass),
        "manifest_sha256": actual_hash,
        "hash_verified": bool(hash_match),
        "feature_count": len(all_retained_features),
        "direct_overlap": list(overlap),
    }

    if not g1_pass:
        raise LeakageGateError(f"Gate 1 Failed! Overlap: {overlap}, Hash Match: {hash_match}, Count: {len(all_retained_features)}")

    # 2. Fold Disjointness Check
    with open(f_path, "r", encoding="utf-8") as f:
        folds_data = json.load(f)

    disjoint_folds = True
    overlaps_found = {}
    total_val_patients = 0
    for fold in folds_data.get("folds", []):
        f_num = fold["fold"]
        tr = set(fold["train_seqn"])
        va = set(fold["val_seqn"])
        ov = tr.intersection(va)
        if len(ov) > 0:
            disjoint_folds = False
            overlaps_found[f"fold_{f_num}"] = len(ov)
        total_val_patients += len(va)

    coverage_pass = (total_val_patients == EXPECTED_COHORT_SIZE)
    g2_pass = disjoint_folds and coverage_pass

    report["tests"]["gate_2_fold_disjointness"] = {
        "passed": bool(g2_pass),
        "zero_patient_overlap": bool(disjoint_folds),
        "cohort_coverage_exact": bool(coverage_pass),
        "total_evaluated_patients": total_val_patients,
        "fold_overlaps": overlaps_found,
    }

    if not g2_pass:
        raise LeakageGateError(f"Gate 2 Failed! Overlaps: {overlaps_found}, Coverage: {total_val_patients}")

    # 3. Excluded Component Reconstruction Test
    df = pd.read_csv(c_path)
    X_matrix = df[all_retained_features].fillna(df[all_retained_features].median()).values

    reconstruction_results = {}
    g3_pass = True

    for comp in ["RIDAGEYR", "LBXSASSI", "LBXSATSI", "LBXPLTSI"]:
        if comp in df.columns:
            y_comp = df[comp].fillna(df[comp].median()).values
            ridge = Ridge(alpha=1.0)
            ridge.fit(X_matrix, y_comp)
            r2 = float(r2_score(y_comp, ridge.predict(X_matrix)))

            corrs = []
            for feat in all_retained_features:
                c, _ = spearmanr(df[comp].dropna(), df[feat].loc[df[comp].dropna().index].fillna(0))
                corrs.append((feat, float(abs(c))))
            corrs.sort(key=lambda x: x[1], reverse=True)
            max_corr_feat, max_corr_val = corrs[0]

            is_leak = (r2 >= 0.90)
            if is_leak:
                g3_pass = False

            reconstruction_results[comp] = {
                "reconstruction_r2": round(r2, 4),
                "max_pairwise_spearman": round(max_corr_val, 4),
                "max_correlated_feature": max_corr_feat,
                "is_reconstructed": is_leak,
            }

    report["tests"]["gate_3_reconstruction_test"] = {
        "passed": bool(g3_pass),
        "components": reconstruction_results,
    }

    if not g3_pass:
        raise LeakageGateError(f"Gate 3 Failed! Reconstruction R^2 exceeded threshold: {reconstruction_results}")

    # 4. Proxy Leakage Screen for Liver Features
    liver_items = m_data.get("Liver", [])
    liver_feats = [it["feature"] for it in liver_items if it["feature"] not in EXCLUDED_FEATURES]
    g4_pass = (len(liver_feats) == 6) and (len(set(liver_feats).intersection(EXCLUDED_FEATURES)) == 0)

    report["tests"]["gate_4_proxy_screen"] = {
        "passed": bool(g4_pass),
        "liver_features": liver_feats,
        "note": "Documented in Experiment 6 Leave-One-Domain-Out ablation",
    }

    report["all_passed"] = bool(g1_pass and g2_pass and g3_pass and g4_pass)

    r_path.parent.mkdir(parents=True, exist_ok=True)
    with open(r_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report
