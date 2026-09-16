"""First-release experiment: one torus, one loop, one change of representation."""

from __future__ import annotations

from .checks import (
    check_closure,
    check_inversion_invariance,
    check_length_matches_cover,
    check_reference_generators,
    check_translation_invariance,
    check_unit_area,
)
from .experiment import ExperimentRecord
from .lattice import normalized_lattice
from .lengths import Winding, loop_length
from .modular import T_GENERATOR, act_on_tau, act_on_winding, translate_tau, translate_winding
from .trajectories import trace_closed_geodesic


def run_first_release(
    *,
    tau: complex = 4j,
    m: int = 1,
    n: int = 1,
    start: complex = 0j,
) -> ExperimentRecord:
    """Construct one normalized torus, trace one closed trajectory, change basis."""
    lattice = normalized_lattice(tau)
    winding = Winding(m, n)
    length = loop_length(lattice, winding.m, winding.n)
    traj = trace_closed_geodesic(lattice, winding.m, winding.n, start=start)
    shifted_shape = translate_tau(lattice.shape)
    shifted_winding = translate_winding(winding)
    shifted_length = loop_length(shifted_shape, shifted_winding.m, shifted_winding.n)

    verification = [
        check_unit_area(lattice),
        *check_reference_generators(),
        check_length_matches_cover(tau, m, n),
        check_closure(tau, m, n, start=start),
        check_translation_invariance(lattice.shape, winding),
        check_inversion_invariance(lattice.shape, winding),
        check_translation_invariance(lattice.shape, Winding(2, 1)),
        check_inversion_invariance(lattice.shape, Winding(2, 1)),
    ]

    return ExperimentRecord(
        title="First release: normalized torus, closed geodesic, modular invariance",
        mathematical_specification={
            "object": "area-one flat torus T_tau = C / Lambda_tau",
            "metric": "flat Euclidean metric on the parallelogram, identified by Lambda_tau",
            "coordinates": "tau = x + i y in the upper half-plane; lattice coords (alpha, beta)",
            "identifications": "z ~ z + m omega1 + n omega2",
            "admissible_parameters": "y > 0; winding (m, n) in Z^2 minus {(0, 0)}",
            "length_formula": "ell_{m,n}(tau) = |m + n tau| / sqrt(y)",
        },
        experiment_specification={
            "tau": str(tau),
            "winding": winding.as_tuple(),
            "start": str(start),
            "basis_change": "T: tau |-> tau+1 with (m, n) |-> (m-n, n)",
            "samples": int(traj.times.size),
        },
        result={
            "omega1": lattice.omega1,
            "omega2": lattice.omega2,
            "generator_lengths": lattice.generator_lengths(),
            "area": lattice.area(),
            "loop_length": length,
            "crossings": len(traj.crossings),
            "closed": traj.closed,
            "tau_after_T": shifted_shape.tau,
            "winding_after_T": shifted_winding.as_tuple(),
            "loop_length_after_T": shifted_length,
            "T_matrix": T_GENERATOR.matrix.tolist(),
        },
        verification=verification,
        limitations=[
            "Lengths are exact algebraic evaluations, not integrator outputs.",
            "A doughnut rendering is topological illustration only; the metric is flat.",
            "Modular invariance is checked for T and S, not a full fundamental-domain fold.",
            "Motion through moduli space (hyperbolic geodesics in tau) is not in this release.",
        ],
    )


__all__ = ["run_first_release", "act_on_tau", "act_on_winding"]
