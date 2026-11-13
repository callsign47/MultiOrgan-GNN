"""
ORGANIX Base Experiment Interface.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional
from organix.core.logging import get_logger
from organix.utils.paths import get_paths


class BaseExperiment(ABC):
    """
    Standardized Abstract Base Class for all ORGANIX Experiments (Exp0 through Exp9).
    Enforces reproducible execution, input/output artifact resolution, and metric logging.
    """
    def __init__(self, experiment_id: str, name: str, description: str):
        self.experiment_id = experiment_id
        self.name = name
        self.description = description
        self.logger = get_logger(f"organix.experiments.{experiment_id}")
        self.paths = get_paths()

    @property
    def output_dir(self) -> Path:
        """Returns the canonical output directory for this experiment."""
        return self.paths.results_dir / "experiments" / self.experiment_id

    @property
    def config_path(self) -> Path:
        """Returns the configuration file path for this experiment."""
        return self.paths.configs_dir / "experiments" / f"{self.experiment_id}.json"

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Executes the experiment pipeline."""
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Returns reproducibility metadata and input/output specifications."""
        pass
