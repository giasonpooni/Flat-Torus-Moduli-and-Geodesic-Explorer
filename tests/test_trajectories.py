from __future__ import annotations

import pytest

from flat_torus import loop_length, normalized_lattice, trace_closed_geodesic


@pytest.mark.parametrize("tau", [1j, 4j, 0.3 + 1.1j])
@pytest.mark.parametrize("winding", [(1, 0), (0, 1), (1, 1), (2, -1)])
def test_integer_windings_close(tau: complex, winding: tuple[int, int]) -> None:
    m, n = winding
    traj = trace_closed_geodesic(tau, m, n, start=0.17 + 0.09j, samples=48)
    assert traj.closed
    assert traj.parallelogram_points[0] == pytest.approx(traj.parallelogram_points[-1])
    assert traj.length == pytest.approx(loop_length(tau, m, n))


def test_cover_endpoint_is_start_plus_lattice_vector() -> None:
    lattice = normalized_lattice(0.2 + 1.4j)
    traj = trace_closed_geodesic(lattice, 2, 1, start=0.1 + 0.2j)
    expected = traj.start + lattice.lattice_vector(2, 1)
    assert traj.cover_points[-1] == pytest.approx(expected)


def test_wrapped_points_stay_in_parallelogram() -> None:
    lattice = normalized_lattice(0.5 + 1.8j)
    traj = trace_closed_geodesic(lattice, 3, 2, samples=80)
    for z in traj.parallelogram_points:
        alpha, beta = lattice.cover_coordinates(z)
        assert -1e-12 <= alpha < 1.0 + 1e-12
        assert -1e-12 <= beta < 1.0 + 1e-12


def test_crossings_are_recorded() -> None:
    traj = trace_closed_geodesic(1j, 1, 1, start=0.1 + 0.2j)
    assert len(traj.crossings) >= 2
    assert all(0.0 < c.parameter <= 1.0 + 1e-12 for c in traj.crossings)
