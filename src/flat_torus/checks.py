"""Reference comparisons that the first release must pass."""

from __future__ import annotations

from .experiment import CheckRecord
from .lattice import NormalizedLattice, ShapeParameter, normalized_lattice
from .lengths import REFERENCE_CASES, Winding, loop_length, primitive_generator_lengths
from .modular import (
    S_GENERATOR,
    T_GENERATOR,
    act_on_tau,
    act_on_winding,
    length_after_basis_change,
)
from .trajectories import expected_crossing_count, trace_closed_geodesic


AREA_TOL = 1e-12
LENGTH_TOL = 1e-12
WRAP_TOL = 1e-10


def check_unit_area(lattice: NormalizedLattice, *, tol: float = AREA_TOL) -> CheckRecord:
    area = lattice.area()
    ok = abs(area - 1.0) <= tol
    return CheckRecord(
        name="unit area",
        passed=ok,
        details=f"area={area:.16f} (expected 1)",
        tolerance=tol,
    )


def check_reference_generators(*, tol: float = LENGTH_TOL) -> list[CheckRecord]:
    records: list[CheckRecord] = []
    for case in REFERENCE_CASES:
        tau = case["tau"]
        expected = case["generator_lengths"]
        got = primitive_generator_lengths(tau)
        lattice = normalized_lattice(tau)
        area_check = check_unit_area(lattice, tol=AREA_TOL)
        records.append(area_check)
        match = abs(got[0] - expected[0]) <= tol and abs(got[1] - expected[1]) <= tol
        records.append(
            CheckRecord(
                name=f"reference generators tau={tau}",
                passed=match,
                details=(
                    f"got {got[0]:.16f}, {got[1]:.16f}; "
                    f"expected {expected[0]}, {expected[1]}"
                ),
                tolerance=tol,
            )
        )
    return records


def check_translation_invariance(
    shape: ShapeParameter,
    winding: Winding,
    *,
    tol: float = LENGTH_TOL,
) -> CheckRecord:
    original, transformed = length_after_basis_change(shape, winding, T_GENERATOR)
    ok = abs(original - transformed) <= tol
    new_winding = act_on_winding(T_GENERATOR, winding)
    new_shape = act_on_tau(T_GENERATOR, shape)
    return CheckRecord(
        name="T: ell_{m-n,n}(tau+1) = ell_{m,n}(tau)",
        passed=ok,
        details=(
            f"ell_{winding.as_tuple()}({shape.tau}) = {original:.16f}, "
            f"ell_{new_winding.as_tuple()}({new_shape.tau}) = {transformed:.16f}"
        ),
        tolerance=tol,
    )


def check_inversion_invariance(
    shape: ShapeParameter,
    winding: Winding,
    *,
    tol: float = LENGTH_TOL,
) -> CheckRecord:
    original, transformed = length_after_basis_change(shape, winding, S_GENERATOR)
    ok = abs(original - transformed) <= tol
    new_winding = act_on_winding(S_GENERATOR, winding)
    new_shape = act_on_tau(S_GENERATOR, shape)
    return CheckRecord(
        name="S: ell_{n,-m}(-1/tau) = ell_{m,n}(tau)",
        passed=ok,
        details=(
            f"ell_{winding.as_tuple()}({shape.tau}) = {original:.16f}, "
            f"ell_{new_winding.as_tuple()}({new_shape.tau}) = {transformed:.16f}"
        ),
        tolerance=tol,
    )


def check_closure(
    tau: complex,
    m: int,
    n: int,
    *,
    start: complex = 0j,
    samples: int = 64,
    tol: float = WRAP_TOL,
) -> CheckRecord:
    traj = trace_closed_geodesic(tau, m, n, start=start, samples=samples)
    start_wrap = traj.parallelogram_points[0]
    end_wrap = traj.parallelogram_points[-1]
    wrap_gap = abs(end_wrap - start_wrap)
    ok = traj.closed and wrap_gap <= tol
    return CheckRecord(
        name=f"closure of ({m}, {n}) on tau={tau}",
        passed=ok,
        details=(
            f"closed={traj.closed}, wrap gap={wrap_gap:.3e}, "
            f"crossings={len(traj.crossings)}, "
            f"expected crossings >= {expected_crossing_count(m, n) - 1}"
        ),
        tolerance=tol,
    )


def check_length_matches_cover(
    tau: complex,
    m: int,
    n: int,
    *,
    tol: float = LENGTH_TOL,
) -> CheckRecord:
    traj = trace_closed_geodesic(tau, m, n, samples=8)
    analytic = loop_length(tau, m, n)
    cover_span = abs(traj.cover_points[-1] - traj.cover_points[0])
    ok = abs(analytic - cover_span) <= tol and abs(analytic - traj.length) <= tol
    return CheckRecord(
        name=f"cover length of ({m}, {n})",
        passed=ok,
        details=f"analytic={analytic:.16f}, cover span={cover_span:.16f}",
        tolerance=tol,
    )
