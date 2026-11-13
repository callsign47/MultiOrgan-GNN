"""
ORGANIX NHANES SAS Transport (.XPT) File Ingestion and Provenance.
"""

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from organix.core.logging import get_logger
from organix.utils.paths import get_paths

logger = get_logger("organix.data.ingestion")


def load_xpt_file(filepath: Path) -> pd.DataFrame:
    """Reads a SAS transport file into a pandas DataFrame."""
    if not filepath.is_file():
        raise FileNotFoundError(f"XPT file not found: {filepath}")
    return pd.read_sas(filepath, format="xport", encoding="utf-8")


def discover_raw_xpt_files(raw_dir: Optional[Path] = None) -> Dict[str, Path]:
    """Finds all raw NHANES 2021-2023 XPT files in the directory."""
    dir_path = raw_dir or get_paths().raw_data_dir
    files = {}
    for p in dir_path.glob("**/*.xpt"):
        files[p.stem.upper()] = p
    for p in dir_path.glob("**/*.XPT"):
        files[p.stem.upper()] = p
    return files
