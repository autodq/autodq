"""Public interface for the AutoDQ statistical engine."""

from .checks import check
from .profiling import profile
from .rules import fit, review

__all__ = ["check", "fit", "profile", "review"]
