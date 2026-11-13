"""
ORGANIX Heterogeneous Organ Interaction Graph Schema Specification.
"""

from typing import Dict, List, Tuple, Any
from organix.core.constants import NODE_TYPES, EDGE_TYPES, NODE_FEATURE_DIMS, FEATURE_DOMAINS


def get_hetero_schema() -> Dict[str, Any]:
    """Returns the complete specification of the multi-organ graph topology."""
    return {
        "node_types": NODE_TYPES,
        "edge_types": EDGE_TYPES,
        "node_feature_dimensions": NODE_FEATURE_DIMS,
        "feature_domains": FEATURE_DOMAINS,
    }
