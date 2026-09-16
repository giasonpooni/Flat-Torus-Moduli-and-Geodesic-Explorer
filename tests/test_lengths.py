from __future__ import annotations

import pytest

from flat_torus import Winding, loop_length, primitive_generator_lengths


def test_formula_matches_generator_norm() -> None:
    tau = 0.25 + 2.0j
    y = tau.imag
    m, n = 3, -2
    expected = abs(m + n * tau) / (y**0.5)
    assert loop_length(tau, m, n) == pytest.approx(expected)


def test_square_versus_elongated_shortest_loop() -> None:
    square = primitive_generator_lengths(1j)
    long = primitive_generator_lengths(4j)
    assert min(square) == pytest.approx(1.0)
    assert min(long) == pytest.approx(0.5)
    assert min(long) < min(square)


def test_rejects_contractible_label() -> None:
    with pytest.raises(ValueError):
        Winding(0, 0)
    with pytest.raises(ValueError):
        loop_length(1j, 0, 0)
