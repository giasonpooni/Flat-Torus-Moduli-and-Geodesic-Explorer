from __future__ import annotations

import numpy as np
import pytest

from flat_torus import ShapeParameter, normalized_lattice


def test_reference_areas_and_generators() -> None:
    square = normalized_lattice(1j)
    long = normalized_lattice(4j)
    assert square.area() == pytest.approx(1.0)
    assert long.area() == pytest.approx(1.0)
    assert square.generator_lengths() == pytest.approx((1.0, 1.0))
    assert long.generator_lengths() == pytest.approx((0.5, 2.0))


def test_rejects_closed_half_plane() -> None:
    with pytest.raises(ValueError):
        ShapeParameter(0.0, 0.0)
    with pytest.raises(ValueError):
        normalized_lattice(1 + 0j)


def test_reduce_is_idempotent_and_in_cell() -> None:
    lattice = normalized_lattice(0.3 + 1.7j)
    z = 4.2 * lattice.omega1 - 3.1 * lattice.omega2 + 0.11 + 0.07j
    reduced = lattice.reduce(z)
    alpha, beta = lattice.cover_coordinates(reduced)
    assert 0.0 <= alpha < 1.0
    assert 0.0 <= beta < 1.0
    assert lattice.reduce(reduced) == pytest.approx(reduced)
    k, ell = lattice.lattice_displacement(z)
    assert lattice.reduce(z - k * lattice.omega1 - ell * lattice.omega2) == pytest.approx(reduced)


def test_cover_round_trip() -> None:
    lattice = normalized_lattice(-0.4 + 2.5j)
    z = 0.2 + 0.5j
    alpha, beta = lattice.cover_coordinates(z)
    assert lattice.from_cover_coordinates(alpha, beta) == pytest.approx(z)
    assert np.isfinite(alpha) and np.isfinite(beta)
