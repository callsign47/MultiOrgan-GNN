"""
ORGANIX Domain-Specific Exceptions.
"""

class OrganixError(Exception):
    """Base exception for all ORGANIX operations."""
    pass

class LeakageGateError(OrganixError):
    """Raised when leakage gate detection fails or finds illicit feature overlap."""
    pass

class ManifestIntegrityError(OrganixError):
    """Raised when the feature manifest fails hash or schema verification."""
    pass

class CohortValidationError(OrganixError):
    """Raised when patient cohort filtering, sizing, or column validation fails."""
    pass

class ExperimentExecutionError(OrganixError):
    """Raised when an experiment execution encounters an unrecoverable failure."""
    pass

class GraphConstructionError(OrganixError):
    """Raised when PyG HeteroData graph construction fails."""
    pass
