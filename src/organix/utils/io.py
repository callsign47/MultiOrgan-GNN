"""
ORGANIX Input/Output and Checksum Utilities.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Union
import pandas as pd


def compute_file_sha256(filepath: Union[str, Path]) -> str:
    """Computes standard SHA-256 hash for a file."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_json(filepath: Union[str, Path]) -> Any:
    """Safely loads JSON document with UTF-8 encoding."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, filepath: Union[str, Path], indent: int = 2) -> None:
    """Safely saves JSON document creating parent directories if needed."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)


def load_dataframe(filepath: Union[str, Path]) -> pd.DataFrame:
    """Loads CSV dataset."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Dataset CSV not found: {path}")
    return pd.read_csv(path)
