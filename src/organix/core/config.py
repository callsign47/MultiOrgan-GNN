"""
ORGANIX Centralized Configuration & Path Management using pathlib.Path.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any
import json
import os


def find_repository_root(start_path: Optional[Path] = None) -> Path:
    """
    Locates the project root directory containing pyproject.toml or MIGRATION_MANIFEST.md.
    """
    current = (start_path or Path.cwd()).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() or (parent / "MIGRATION_MANIFEST.md").exists() or (parent / "requirements.txt").exists():
            return parent
    return current


@dataclass(frozen=True)
class PathConfig:
    """Project-wide paths resolved from the repository root."""
    root: Path = field(default_factory=find_repository_root)
    
    @property
    def data_dir(self) -> Path:
        return self.root / "data"

    @property
    def raw_data_dir(self) -> Path:
        return self.data_dir / "raw" / "nhanes_2021_2023"

    @property
    def processed_data_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def splits_dir(self) -> Path:
        return self.data_dir / "splits"

    @property
    def metadata_dir(self) -> Path:
        return self.data_dir / "metadata"

    @property
    def artifacts_dir(self) -> Path:
        return self.root / "artifacts"

    @property
    def graphs_dir(self) -> Path:
        return self.artifacts_dir / "graphs"

    @property
    def checkpoints_dir(self) -> Path:
        return self.artifacts_dir / "checkpoints"

    @property
    def results_dir(self) -> Path:
        return self.artifacts_dir / "results"

    @property
    def configs_dir(self) -> Path:
        return self.root / "configs"

    @property
    def docs_dir(self) -> Path:
        return self.root / "docs"

    # Canonical file paths
    @property
    def final_cohort_path(self) -> Path:
        return self.processed_data_dir / "final_cohort.csv"

    @property
    def master_patient_path(self) -> Path:
        return self.processed_data_dir / "master_patient.csv"

    @property
    def folds_path(self) -> Path:
        return self.splits_dir / "folds_v1.json"

    @property
    def manifest_path(self) -> Path:
        return self.metadata_dir / "feature_manifest.json"

    @property
    def patient_graphs_path(self) -> Path:
        return self.graphs_dir / "patient_graphs.pt"

    @property
    def leakage_gate_report_path(self) -> Path:
        return self.results_dir / "leakage_gate" / "leakage_gate_report.json"

    @property
    def final_benchmark_summary_path(self) -> Path:
        return self.results_dir / "benchmarks" / "final_benchmark_summary.json"


@dataclass
class OrganixConfig:
    """Master ORGANIX runtime and experiment configuration."""
    paths: PathConfig = field(default_factory=PathConfig)
    n_splits: int = 5
    seed: int = 42
    target_column: str = "fib4_target"
    batch_size: int = 64
    epochs: int = 50
    lr: float = 0.001
    weight_decay: float = 1e-4

    @classmethod
    def load_from_file(cls, config_path: Path) -> "OrganixConfig":
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)


_DEFAULT_CONFIG: Optional[OrganixConfig] = None


def get_config() -> OrganixConfig:
    """Retrieve global default configuration singleton."""
    global _DEFAULT_CONFIG
    if _DEFAULT_CONFIG is None:
        _DEFAULT_CONFIG = OrganixConfig()
    return _DEFAULT_CONFIG
