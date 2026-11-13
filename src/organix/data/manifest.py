"""
ORGANIX Feature Manifest Loading and Verification.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from organix.core.constants import (
    EXPECTED_MANIFEST_HASH,
    EXPECTED_FEATURE_COUNT,
    EXCLUDED_FEATURES,
    FEATURE_DOMAINS,
    get_locked_feature_list,
)
from organix.core.exceptions import ManifestIntegrityError
from organix.utils.io import compute_file_sha256, load_json
from organix.utils.paths import get_paths


def verify_and_load_manifest(manifest_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Loads and cryptographically validates the locked feature manifest.
    Ensures zero overlap with the 4 excluded algebraic FIB-4 formula components
    and verifies that exactly 25 leakage-free clinical features are retained.
    """
    path = manifest_path or get_paths().manifest_path
    if not path.is_file():
        raise FileNotFoundError(f"Feature manifest not found at: {path}")

    actual_hash = compute_file_sha256(path)
    if actual_hash != EXPECTED_MANIFEST_HASH:
        raise ManifestIntegrityError(
            f"Manifest SHA-256 mismatch! Expected {EXPECTED_MANIFEST_HASH}, found {actual_hash}"
        )

    manifest_data = load_json(path)
    all_retained_features: List[str] = []

    for domain_name, items in manifest_data.items():
        if isinstance(items, list):
            for item in items:
                feat = item.get("feature") if isinstance(item, dict) else str(item)
                if feat and feat not in EXCLUDED_FEATURES:
                    all_retained_features.append(feat)

    # Check feature count
    if len(all_retained_features) != EXPECTED_FEATURE_COUNT:
        raise ManifestIntegrityError(
            f"Expected {EXPECTED_FEATURE_COUNT} retained features in manifest, found {len(all_retained_features)}"
        )

    # Check zero overlap with excluded formula components
    overlap = set(all_retained_features).intersection(EXCLUDED_FEATURES)
    if overlap:
        raise ManifestIntegrityError(
            f"CRITICAL LEAKAGE DETECTED: Direct FIB-4 components in retained features: {overlap}"
        )

    return manifest_data


def get_feature_names() -> List[str]:
    """Returns the ordered 25 locked feature names."""
    return get_locked_feature_list()
