"""Area-normalized flat tori and their lattice representations.

The mathematical object is the quotient

    T_tau = C / Lambda_tau,    Lambda_tau = y^{-1/2} (Z + tau Z),    tau = x + i y, y > 0.

The factor y^{-1/2} fixes the fundamental parallelogram at area one, so
tau parametrizes *shape*, not size. Two different tau may still describe
the same lattice after an SL(2, Z) change of basis; that equivalence
lives in ``flat_torus.modular``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

_MIN_IMAG = 1e-15


def _as_complex(value: complex | float | np.complexfloating) -> complex:
    return complex(value)


@dataclass(frozen=True)
class ShapeParameter:
    """Point tau = x + i y in the upper half-plane."""

    x: float
    y: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", float(self.x))
        object.__setattr__(self, "y", float(self.y))
        if not np.isfinite(self.x) or not np.isfinite(self.y):
            raise ValueError("shape parameter components must be finite")
        if self.y <= _MIN_IMAG:
            raise ValueError(f"Im(tau) must be positive, got y={self.y}")

    @classmethod
    def from_tau(cls, tau: complex | float) -> ShapeParameter:
        tau = _as_complex(tau)
        return cls(x=tau.real, y=tau.imag)

    @property
    def tau(self) -> complex:
        return complex(self.x, self.y)

    @property
    def modulus(self) -> float:
        return float(abs(self.tau))


@dataclass(frozen=True)
class NormalizedLattice:
    """Generators of the area-one lattice Lambda_tau.

    ``omega1`` corresponds to 1, ``omega2`` to tau, both scaled by y^{-1/2}.
    A lattice vector is ``m * omega1 + n * omega2`` for integers m, n.
    """

    shape: ShapeParameter
    omega1: complex
    omega2: complex

    @classmethod
    def from_shape(cls, shape: ShapeParameter) -> NormalizedLattice:
        scale = 1.0 / np.sqrt(shape.y)
        return cls(
            shape=shape,
            omega1=complex(scale, 0.0),
            omega2=complex(scale * shape.x, scale * shape.y),
        )

    @classmethod
    def from_tau(cls, tau: complex | float) -> NormalizedLattice:
        return cls.from_shape(ShapeParameter.from_tau(tau))

    @property
    def scale(self) -> float:
        return 1.0 / np.sqrt(self.shape.y)

    @property
    def generators(self) -> tuple[complex, complex]:
        return self.omega1, self.omega2

    def area(self) -> float:
        """Signed area of the fundamental parallelogram. Equals 1 by construction."""
        return float(np.imag(np.conjugate(self.omega1) * self.omega2))

    def generator_lengths(self) -> tuple[float, float]:
        return float(abs(self.omega1)), float(abs(self.omega2))

    def lattice_vector(self, m: int, n: int) -> complex:
        return m * self.omega1 + n * self.omega2

    def cover_coordinates(self, z: complex | float) -> tuple[float, float]:
        """Coefficients (alpha, beta) in the basis (omega1, omega2)."""
        z = _as_complex(z)
        matrix = np.array(
            [
                [self.omega1.real, self.omega2.real],
                [self.omega1.imag, self.omega2.imag],
            ],
            dtype=float,
        )
        coeffs = np.linalg.solve(matrix, np.array([z.real, z.imag], dtype=float))
        return float(coeffs[0]), float(coeffs[1])

    def from_cover_coordinates(self, alpha: float, beta: float) -> complex:
        return alpha * self.omega1 + beta * self.omega2

    def reduce(self, z: complex | float) -> complex:
        """Unique representative in the half-open fundamental parallelogram."""
        alpha, beta = self.cover_coordinates(z)
        return self.from_cover_coordinates(alpha % 1.0, beta % 1.0)

    def lattice_displacement(self, z: complex | float) -> tuple[int, int]:
        """Integers (k, ell) such that z - k omega1 - ell omega2 is in the cell."""
        alpha, beta = self.cover_coordinates(z)
        return int(np.floor(alpha)), int(np.floor(beta))


def normalized_lattice(tau: complex | float | ShapeParameter) -> NormalizedLattice:
    if isinstance(tau, ShapeParameter):
        return NormalizedLattice.from_shape(tau)
    return NormalizedLattice.from_tau(tau)


SQUARE_TORUS = NormalizedLattice.from_tau(1j)
ELONGATED_TORUS = NormalizedLattice.from_tau(4j)
