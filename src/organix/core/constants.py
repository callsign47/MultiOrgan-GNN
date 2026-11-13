"""
ORGANIX Core Constants and Clinical Specification.
"""

from typing import Dict, List, Set, Tuple

# Excluded direct algebraic components of the FIB-4 index
# FIB-4 = (Age * AST) / (Platelet * sqrt(ALT))
EXCLUDED_FEATURES: Set[str] = {
    "RIDAGEYR",  # Age in years
    "LBXSASSI",  # Aspartate Aminotransferase (AST) in U/L
    "LBXSATSI",  # Alanine Aminotransferase (ALT) in U/L
    "LBXPLTSI",  # Platelet count in 10^9/L
}

# 25 Locked Leakage-Free Manifest Features grouped by physiological domain
FEATURE_DOMAINS: Dict[str, List[str]] = {
    "Demographics": ["RIAGENDR"],
    "Liver": [
        "LBXSGTSI",  # Gamma-glutamyl transferase (GGT)
        "LBXSAL",    # Albumin
        "LBXSTB",    # Total bilirubin
        "LBXSAPSI",  # Alkaline phosphatase (ALP)
        "LUXSMED",   # Liver stiffness median (FibroScan elastography, kPa)
        "LUXCAPM",   # Controlled attenuation parameter median (steatosis, dB/m)
    ],
    "Kidney": [
        "LBXSCR",    # Serum creatinine
        "LBXSBU",    # Blood urea nitrogen (BUN)
        "LBXSUA",    # Serum uric acid
        "URXUMA",    # Urine microalbumin
        "URXUCR",    # Urine creatinine
        "KIQ022",    # Questionnaire: Kidney failure / weakened kidneys
    ],
    "Heart": [
        "BPXOSY1",   # Oscillometric systolic blood pressure (first reading)
        "BPXODI1",   # Oscillometric diastolic blood pressure (first reading)
        "BPXOPLS1",  # Oscillometric pulse (first reading)
        "LBDHDD",    # HDL cholesterol
        "LBXTC",     # Total cholesterol
        "BPQ020",    # Questionnaire: Ever told high blood pressure
        "MCQ160C",   # Questionnaire: Ever told coronary heart disease
        "MCQ160E",   # Questionnaire: Ever told heart attack / MI
    ],
    "Biomarker": [
        "LBXWBCSI",  # White blood cell count
        "LBXRBCSI",  # Red blood cell count
        "LBXHGB",    # Hemoglobin
        "LBXHSCRP",  # High-sensitivity C-reactive protein (systemic inflammation)
    ],
}

# Ordered flat list of all 25 locked features
def get_locked_feature_list() -> List[str]:
    features: List[str] = []
    for domain in ["Demographics", "Liver", "Kidney", "Heart", "Biomarker"]:
        features.extend(FEATURE_DOMAINS[domain])
    return features

# Verified cohort and dataset invariant specifications
EXPECTED_COHORT_SIZE: int = 6277
EXPECTED_RAW_PATIENTS: int = 11933
EXPECTED_FEATURE_COUNT: int = 25
EXPECTED_FOLDS_COUNT: int = 5
RANDOM_SEED: int = 42

# SHA-256 Checksum for the locked 25-feature manifest
EXPECTED_MANIFEST_HASH: str = "6712e1575dc12c36e2345e08cc1112a3ae90be283fce882dcf681e59862cbe22"

# Heterogeneous Graph Schema
NODE_TYPES: List[str] = ["patient", "liver", "kidney", "heart", "biomarker"]

# 14 Canonical Directed Relations
EDGE_TYPES: List[Tuple[str, str, str]] = [
    ("patient", "pertains_to", "liver"),
    ("liver", "rev_pertains_to", "patient"),
    ("patient", "pertains_to", "kidney"),
    ("kidney", "rev_pertains_to", "patient"),
    ("patient", "pertains_to", "heart"),
    ("heart", "rev_pertains_to", "patient"),
    ("patient", "pertains_to", "biomarker"),
    ("biomarker", "rev_pertains_to", "patient"),
    ("liver", "interacts_with", "kidney"),
    ("kidney", "interacts_with", "liver"),
    ("liver", "interacts_with", "heart"),
    ("heart", "interacts_with", "liver"),
    ("kidney", "interacts_with", "heart"),
    ("heart", "interacts_with", "kidney"),
]

# Canonical Node Feature Dimensionality (raw features per node type)
NODE_FEATURE_DIMS: Dict[str, int] = {
    "patient": 1,    # RIAGENDR
    "liver": 6,      # LBXSGTSI, LBXSAL, LBXSTB, LBXSAPSI, LUXSMED, LUXCAPM
    "kidney": 6,     # LBXSCR, LBXSBU, LBXSUA, URXUMA, URXUCR, KIQ022
    "heart": 8,      # BPXOSY1, BPXODI1, BPXOPLS1, LBDHDD, LBXTC, BPQ020, MCQ160C, MCQ160E
    "biomarker": 4,  # LBXWBCSI, LBXRBCSI, LBXHGB, LBXHSCRP
}
