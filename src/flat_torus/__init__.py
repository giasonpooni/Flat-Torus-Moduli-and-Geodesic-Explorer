"""Reusable kernel for area-one flat tori and their closed geodesics."""

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
from .fold import (
    FoldResult,
    ModularLetter,
    ModularWord,
    fold_to_fundamental_domain,
    in_fundamental_domain,
    word_from_matrix,
)
from .fold_experiment import run_fold_experiment
from .lattice import (
    ELONGATED_TORUS,
    SQUARE_TORUS,
    NormalizedLattice,
    ShapeParameter,
    normalized_lattice,
)
from .lengths import Winding, loop_length, primitive_generator_lengths
from .modular import (
    IDENTITY,
    MINUS_IDENTITY,
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
    translation_matrix,
)
from .reports import format_record, write_report
from .trajectories import ClosedTrajectory, EdgeCrossing, trace_closed_geodesic

__all__ = [
    "ELONGATED_TORUS",
    "IDENTITY",
    "MINUS_IDENTITY",
    "SQUARE_TORUS",
    "CheckRecord",
    "ClosedTrajectory",
    "EdgeCrossing",
    "ExperimentRecord",
    "FoldResult",
    "ModularLetter",
    "ModularMatrix",
    "ModularWord",
    "NormalizedLattice",
    "S_GENERATOR",
    "ShapeParameter",
    "T_GENERATOR",
    "Winding",
    "act_on_tau",
    "act_on_winding",
    "fold_to_fundamental_domain",
    "in_fundamental_domain",
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
    "run_fold_experiment",
    "trace_closed_geodesic",
    "translate_tau",
    "translate_winding",
    "translation_matrix",
    "word_from_matrix",
    "write_report",
]

__version__ = "0.1.0"
