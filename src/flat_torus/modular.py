"""Changes of lattice representation and the matching winding labels.

An SL(2, Z) matrix g = [[a, b], [c, d]] acts on the shape parameter by

    tau' = (a tau + b) / (c tau + d).

The same closed geodesic is then described by a transformed winding.
If the un-normalized bases are related by

    (omega1', omega2') = (omega1, omega2) g,

the labels transform as

    (m, n)^T = g (m', n')^T,
    (m', n')^T = g^{-1} (m, n)^T.

The first-release unit test is the translation generator

    T: tau |-> tau + 1,    g = [[1, 1], [0, 1]],    (m', n') = (m - n, n),

which leaves the lattice itself unchanged and therefore leaves every
loop length unchanged once the labels move with the basis:

    ell_{m-n, n}(tau + 1) = ell_{m, n}(tau).

Comparing the *same* integer labels before and after a basis change
does not compare the same trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .lattice import ShapeParameter
from .lengths import Winding, loop_length


def _require_sl2z(a: int, b: int, c: int, d: int) -> None:
    if a * d - b * c != 1:
        raise ValueError(f"matrix [[{a}, {b}], [{c}, {d}]] is not in SL(2, Z)")


@dataclass(frozen=True)
class ModularMatrix:
    """An element of SL(2, Z)."""

    a: int
    b: int
    c: int
    d: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", int(self.a))
        object.__setattr__(self, "b", int(self.b))
        object.__setattr__(self, "c", int(self.c))
        object.__setattr__(self, "d", int(self.d))
        _require_sl2z(self.a, self.b, self.c, self.d)

    @property
    def matrix(self) -> np.ndarray:
        return np.array([[self.a, self.b], [self.c, self.d]], dtype=int)

    def inverse(self) -> ModularMatrix:
        return ModularMatrix(self.d, -self.b, -self.c, self.a)


T_GENERATOR = ModularMatrix(1, 1, 0, 1)
S_GENERATOR = ModularMatrix(0, -1, 1, 0)


def act_on_tau(matrix: ModularMatrix, shape: ShapeParameter) -> ShapeParameter:
    tau = shape.tau
    denom = matrix.c * tau + matrix.d
    if abs(denom) == 0:
        raise ZeroDivisionError("modular action hit a pole")
    return ShapeParameter.from_tau((matrix.a * tau + matrix.b) / denom)


def act_on_winding(matrix: ModularMatrix, winding: Winding) -> Winding:
    """Return the winding labels of the same geodesic in the new basis.

    (m', n')^T = g^{-1} (m, n)^T.
    """
    inv = matrix.inverse()
    m_new = inv.a * winding.m + inv.b * winding.n
    n_new = inv.c * winding.m + inv.d * winding.n
    return Winding(m_new, n_new)


def translate_tau(shape: ShapeParameter) -> ShapeParameter:
    """T: tau |-> tau + 1."""
    return act_on_tau(T_GENERATOR, shape)


def translate_winding(winding: Winding) -> Winding:
    """Matching label change for T: (m, n) |-> (m - n, n)."""
    return act_on_winding(T_GENERATOR, winding)


def invert_tau(shape: ShapeParameter) -> ShapeParameter:
    """S: tau |-> -1/tau."""
    return act_on_tau(S_GENERATOR, shape)


def invert_winding(winding: Winding) -> Winding:
    """Matching label change for S: (m, n) |-> (n, -m)."""
    return act_on_winding(S_GENERATOR, winding)


def length_after_basis_change(
    shape: ShapeParameter,
    winding: Winding,
    matrix: ModularMatrix,
) -> tuple[float, float]:
    """Return (original length, transformed-description length)."""
    original = loop_length(shape, winding.m, winding.n)
    new_shape = act_on_tau(matrix, shape)
    new_winding = act_on_winding(matrix, winding)
    transformed = loop_length(new_shape, new_winding.m, new_winding.n)
    return original, transformed
