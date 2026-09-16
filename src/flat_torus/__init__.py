"""Reusable kernel for area-one flat tori and their closed geodesics.

This package is the importable mathematical fragment. Experiments,
figures, and reports live beside it in the repository.
"""

from .checks import (
    check_closure,
    check_inversion_invariance,
    check_length_matches_cover,
    check_reference_generators,
    check_translation_invariance,
    check_unit_area,
)
from .experiment import CheckRecord, ExperimentRecord
from .first_release import run_first_release
from .lattice import (
    ELONGATED_TORUS,
    SQUARE_TORUS,
    NormalizedLattice,
    ShapeParameter,
    normalized_lattice,
)
from .lengths import Winding, loop_length, primitive_generator_lengths
from .modular import (
    S_GENERATOR,
    T_GENERATOR,
    ModularMatrix,
    act_on_tau,
    act_on_winding,
    invert_tau,
    invert_winding,
    length_after_basis_change,
    translate_tau,
    translate_winding,
)
from .reports import format_record, write_report
from .trajectories import ClosedTrajectory, EdgeCrossing, trace_closed_geodesic

__all__ = [
    "ELONGATED_TORUS",
    "SQUARE_TORUS",
    "CheckRecord",
    "ClosedTrajectory",
    "EdgeCrossing",
    "ExperimentRecord",
    "ModularMatrix",
    "NormalizedLattice",
    "S_GENERATOR",
    "ShapeParameter",
    "T_GENERATOR",
    "Winding",
    "act_on_tau",
    "act_on_winding",
    "check_closure",
    "check_inversion_invariance",
    "check_length_matches_cover",
    "check_reference_generators",
    "check_translation_invariance",
    "check_unit_area",
    "format_record",
    "invert_tau",
    "invert_winding",
    "length_after_basis_change",
    "loop_length",
    "normalized_lattice",
    "primitive_generator_lengths",
    "run_first_release",
    "trace_closed_geodesic",
    "translate_tau",
    "translate_winding",
    "write_report",
]

__version__ = "0.1.0"
