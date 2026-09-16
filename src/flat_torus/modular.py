"""Changes of lattice representation and the matching winding labels.

An SL(2, Z) matrix g = [[a, b], [c, d]] acts on the shape parameter by

    tau' = (a tau + b) / (c tau + d).

For that same g the labels of the same closed geodesic are

    m' = a m - b n,    n' = -c m + d n.

That rule agrees with T and S individually. Using g^{-1} on the labels
instead preserves length for one generator and fails for a composed word.
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

    def compose(self, other: ModularMatrix) -> ModularMatrix:
        """Return ``self * other`` (apply ``other`` first)."""
        return ModularMatrix(
            self.a * other.a + self.b * other.c,
            self.a * other.b + self.b * other.d,
            self.c * other.a + self.d * other.c,
            self.c * other.b + self.d * other.d,
        )

    def __mul__(self, other: ModularMatrix) -> ModularMatrix:
        if not isinstance(other, ModularMatrix):
            return NotImplemented
        return self.compose(other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModularMatrix):
            return NotImplemented
        return (self.a, self.b, self.c, self.d) == (other.a, other.b, other.c, other.d)

    def __hash__(self) -> int:
        return hash((self.a, self.b, self.c, self.d))

    def as_tuple(self) -> tuple[int, int, int, int]:
        return self.a, self.b, self.c, self.d

    @property
    def is_identity(self) -> bool:
        return self.as_tuple() == (1, 0, 0, 1)

    @property
    def is_minus_identity(self) -> bool:
        return self.as_tuple() == (-1, 0, 0, -1)


IDENTITY = ModularMatrix(1, 0, 0, 1)
MINUS_IDENTITY = ModularMatrix(-1, 0, 0, -1)
T_GENERATOR = ModularMatrix(1, 1, 0, 1)
S_GENERATOR = ModularMatrix(0, -1, 1, 0)


def translation_matrix(shift: int) -> ModularMatrix:
    """T^k = [[1, k], [0, 1]], sending tau |-> tau + k."""
    return ModularMatrix(1, int(shift), 0, 1)


def act_on_tau(matrix: ModularMatrix, shape: ShapeParameter) -> ShapeParameter:
    tau = shape.tau
    denom = matrix.c * tau + matrix.d
    if abs(denom) == 0:
        raise ZeroDivisionError("modular action hit a pole")
    return ShapeParameter.from_tau((matrix.a * tau + matrix.b) / denom)


def act_on_winding(matrix: ModularMatrix, winding: Winding) -> Winding:
    """Return the winding labels of the same geodesic after tau' = g.tau."""
    m_new = matrix.a * winding.m - matrix.b * winding.n
    n_new = -matrix.c * winding.m + matrix.d * winding.n
    return Winding(m_new, n_new)


def translate_tau(shape: ShapeParameter) -> ShapeParameter:
    return act_on_tau(T_GENERATOR, shape)


def translate_winding(winding: Winding) -> Winding:
    return act_on_winding(T_GENERATOR, winding)


def invert_tau(shape: ShapeParameter) -> ShapeParameter:
    return act_on_tau(S_GENERATOR, shape)


def invert_winding(winding: Winding) -> Winding:
    return act_on_winding(S_GENERATOR, winding)


def length_after_basis_change(
    shape: ShapeParameter,
    winding: Winding,
    matrix: ModularMatrix,
) -> tuple[float, float]:
    original = loop_length(shape, winding.m, winding.n)
    new_shape = act_on_tau(matrix, shape)
    new_winding = act_on_winding(matrix, winding)
    transformed = loop_length(new_shape, new_winding.m, new_winding.n)
    return original, transformed
