"""Closed-loop lengths on an area-one flat torus.

For a nonzero integer winding pair (m, n) the corresponding closed
geodesic has length

    ell_{m,n}(tau) = |m + n tau| / sqrt(y) = |m omega1 + n omega2|.

These are non-contractible loops. The pair (0, 0) is rejected: it is
the constant path, not a closed geodesic of this family.
"""

from __future__ import annotations

from dataclasses import dataclass

from .lattice import NormalizedLattice, ShapeParameter, normalized_lattice


@dataclass(frozen=True)
class Winding:
    """Integer homology class of a closed geodesic on T_tau."""

    m: int
    n: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "m", int(self.m))
        object.__setattr__(self, "n", int(self.n))
        if self.m == 0 and self.n == 0:
            raise ValueError("winding (0, 0) is the constant path, not a closed geodesic")

    def as_tuple(self) -> tuple[int, int]:
        return self.m, self.n


def loop_length(
    tau: complex | float | ShapeParameter | NormalizedLattice,
    m: int,
    n: int,
) -> float:
    """Exact length of the closed geodesic in class (m, n)."""
    winding = Winding(m, n)
    lattice = tau if isinstance(tau, NormalizedLattice) else normalized_lattice(tau)
    return abs(lattice.lattice_vector(winding.m, winding.n))


def primitive_generator_lengths(
    tau: complex | float | ShapeParameter | NormalizedLattice,
) -> tuple[float, float]:
    """Lengths of the two lattice generators (1,0) and (0,1)."""
    return loop_length(tau, 1, 0), loop_length(tau, 0, 1)


REFERENCE_CASES: tuple[dict[str, object], ...] = (
    {
        "name": "square",
        "tau": 1j,
        "generator_lengths": (1.0, 1.0),
        "area": 1.0,
    },
    {
        "name": "elongated",
        "tau": 4j,
        "generator_lengths": (0.5, 2.0),
        "area": 1.0,
    },
)
