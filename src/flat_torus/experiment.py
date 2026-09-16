"""Shared experiment contract for the geometry portfolio.

The contract is deliberately small. It describes one run without
pretending that a torus, a Jacobi field, and a covariance geodesic
are interchangeable objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CheckRecord:
    name: str
    passed: bool
    details: str
    tolerance: float | None = None


@dataclass
class ExperimentRecord:
    """Four-part record used across the geometry testbeds."""

    title: str
    mathematical_specification: dict[str, Any]
    experiment_specification: dict[str, Any]
    result: dict[str, Any]
    verification: list[CheckRecord] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.verification)

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "mathematical_specification": self.mathematical_specification,
            "experiment_specification": self.experiment_specification,
            "result": self.result,
            "verification": [
                {
                    "name": check.name,
                    "passed": check.passed,
                    "details": check.details,
                    "tolerance": check.tolerance,
                }
                for check in self.verification
            ],
            "limitations": list(self.limitations),
        }
