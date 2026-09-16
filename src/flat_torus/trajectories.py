"""Geodesics on the identified flat parallelogram.

A unit-speed geodesic on T_tau lifts to a straight line in C. In lattice
coordinates (alpha, beta), the closed geodesic of class (m, n) starting at
(alpha0, beta0) is

    alpha(t) = alpha0 + m t,    beta(t) = beta0 + n t,    t in [0, 1],

then reduced modulo 1. Each time alpha or beta crosses an integer the path
hits an edge of the fundamental parallelogram and re-enters on the
identified opposite edge.

The renderer must consume these reduced points. A doughnut embedding
may illustrate topology, but it does not replace the flat metric.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .lattice import NormalizedLattice, normalized_lattice
from .lengths import Winding, loop_length


@dataclass(frozen=True)
class EdgeCrossing:
    """A hit on the boundary of the fundamental parallelogram."""

    parameter: float
    edge: str
    incoming: complex
    outgoing: complex
    lattice_step: tuple[int, int]


@dataclass(frozen=True)
class ClosedTrajectory:
    """One closed geodesic, sampled in the parallelogram and on the cover."""

    lattice: NormalizedLattice
    winding: Winding
    start: complex
    length: float
    times: np.ndarray
    parallelogram_points: np.ndarray
    cover_points: np.ndarray
    crossings: tuple[EdgeCrossing, ...]
    closed: bool
    notes: str = ""

    @property
    def winding_tuple(self) -> tuple[int, int]:
        return self.winding.as_tuple()


def _edge_name(da: int, db: int) -> str:
    if da == 1 and db == 0:
        return "omega1+"
    if da == -1 and db == 0:
        return "omega1-"
    if da == 0 and db == 1:
        return "omega2+"
    if da == 0 and db == -1:
        return "omega2-"
    return f"corner({da},{db})"


def _crossing_parameters(m: int, n: int, alpha0: float, beta0: float) -> list[float]:
    """Parameter values t in (0, 1] where the path hits a lattice line."""
    hits: set[float] = set()
    if m != 0:
        direction = 1 if m > 0 else -1
        first = np.ceil(alpha0 + 1e-15) if direction > 0 else np.floor(alpha0 - 1e-15)
        k = int(first)
        while True:
            t = (k - alpha0) / m
            if t > 1.0 + 1e-14:
                break
            if t > 1e-14:
                hits.add(float(t))
            k += direction
    if n != 0:
        direction = 1 if n > 0 else -1
        first = np.ceil(beta0 + 1e-15) if direction > 0 else np.floor(beta0 - 1e-15)
        k = int(first)
        while True:
            t = (k - beta0) / n
            if t > 1.0 + 1e-14:
                break
            if t > 1e-14:
                hits.add(float(t))
            k += direction
    return sorted(hits)


def trace_closed_geodesic(
    tau: complex | float | NormalizedLattice,
    m: int,
    n: int,
    *,
    start: complex = 0j,
    samples: int = 256,
) -> ClosedTrajectory:
    """Trace the (m, n) geodesic through the fundamental parallelogram."""
    if samples < 2:
        raise ValueError("samples must be at least 2")
    winding = Winding(m, n)
    lattice = tau if isinstance(tau, NormalizedLattice) else normalized_lattice(tau)
    start = lattice.reduce(start)
    alpha0, beta0 = lattice.cover_coordinates(start)
    length = loop_length(lattice, winding.m, winding.n)

    times = np.linspace(0.0, 1.0, samples)
    cover = np.empty(samples, dtype=complex)
    wrapped = np.empty(samples, dtype=complex)
    for i, t in enumerate(times):
        alpha = alpha0 + winding.m * t
        beta = beta0 + winding.n * t
        cover[i] = lattice.from_cover_coordinates(alpha, beta)
        wrapped[i] = lattice.from_cover_coordinates(alpha % 1.0, beta % 1.0)

    crossings: list[EdgeCrossing] = []
    for t in _crossing_parameters(winding.m, winding.n, alpha0, beta0):
        if t > 1.0 + 1e-12:
            continue
        t_clip = min(t, 1.0)
        alpha = alpha0 + winding.m * t_clip
        beta = beta0 + winding.n * t_clip
        incoming = lattice.from_cover_coordinates(alpha, beta)
        eps = 1e-12
        a_in = alpha0 + winding.m * max(t_clip - eps, 0.0)
        b_in = beta0 + winding.n * max(t_clip - eps, 0.0)
        a_out = alpha0 + winding.m * min(t_clip + eps, 1.0)
        b_out = beta0 + winding.n * min(t_clip + eps, 1.0)
        step = (int(np.floor(a_out)) - int(np.floor(a_in)), int(np.floor(b_out)) - int(np.floor(b_in)))
        outgoing = lattice.from_cover_coordinates(a_out % 1.0, b_out % 1.0)
        crossings.append(
            EdgeCrossing(
                parameter=float(t_clip),
                edge=_edge_name(*step) if step != (0, 0) else "tangent",
                incoming=incoming,
                outgoing=outgoing,
                lattice_step=step,
            )
        )

    end_cover = lattice.from_cover_coordinates(alpha0 + winding.m, beta0 + winding.n)
    expected_end = start + lattice.lattice_vector(winding.m, winding.n)
    closed = abs(end_cover - expected_end) < 1e-12 and abs(wrapped[-1] - start) < 1e-10
    notes = (
        "Path is a straight line in the cover and a broken line in the "
        "identified parallelogram. Closure is exact for integer windings."
    )
    return ClosedTrajectory(
        lattice=lattice,
        winding=winding,
        start=start,
        length=length,
        times=times,
        parallelogram_points=wrapped,
        cover_points=cover,
        crossings=tuple(crossings),
        closed=closed,
        notes=notes,
    )


def expected_crossing_count(m: int, n: int) -> int:
    winding = Winding(m, n)
    return abs(winding.m) + abs(winding.n)
