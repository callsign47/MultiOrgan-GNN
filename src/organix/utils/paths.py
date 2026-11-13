"""
ORGANIX Path Resolution Helpers.
"""

from pathlib import Path
from organix.core.config import get_config, PathConfig


def get_paths() -> PathConfig:
    """Returns the PathConfig instance from active configuration."""
    return get_config().paths
