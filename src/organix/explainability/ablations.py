"""
ORGANIX Physiological Domain and Graph Architecture Ablations.
"""

from typing import Dict, List, Set, Any
from organix.core.constants import FEATURE_DOMAINS, get_locked_feature_list


def get_leave_one_domain_out_feature_sets() -> Dict[str, List[str]]:
    """
    Returns feature subsets for Leave-One-Domain-Out (LODO) ablation:
      - LOO_Demographics (24 features)
      - LOO_Liver (19 features)
      - LOO_Kidney (19 features)
      - LOO_Heart (17 features)
      - LOO_Biomarker (21 features)
    """
    all_feats = get_locked_feature_list()
    ablation_sets = {}
    for domain, excluded in FEATURE_DOMAINS.items():
        ex_set = set(excluded)
        ablation_sets[f"LOO_{domain}"] = [f for f in all_feats if f not in ex_set]
    return ablation_sets


def get_single_domain_feature_sets() -> Dict[str, List[str]]:
    """
    Returns single-domain feature subsets for standalone domain models.
    """
    return {f"ONLY_{dom}": feats for dom, feats in FEATURE_DOMAINS.items()}
