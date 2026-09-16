"""Parallelogram drawings that consume the same geometry as the tests."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .lattice import NormalizedLattice
from .trajectories import ClosedTrajectory


def _require_matplotlib():
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "matplotlib is required for the explorer. "
            "Install with: pip install 'flat-torus-moduli-and-geodesic-explorer[viz]'"
        ) from exc
    return plt


def parallelogram_vertices(lattice: NormalizedLattice) -> np.ndarray:
    o, w1, w2 = 0j, lattice.omega1, lattice.omega2
    corners = [o, w1, w1 + w2, w2, o]
    return np.array([[z.real, z.imag] for z in corners], dtype=float)


def draw_trajectory(
    trajectory: ClosedTrajectory,
    *,
    path: Path | None = None,
    show_cover: bool = True,
) -> Path | None:
    plt = _require_matplotlib()
    lattice = trajectory.lattice
    fig, axes = plt.subplots(1, 2 if show_cover else 1, figsize=(10 if show_cover else 5, 4.5))
    if not show_cover:
        axes = [axes]
    poly = parallelogram_vertices(lattice)
    ax = axes[0]
    ax.plot(poly[:, 0], poly[:, 1], color="black", lw=1.2)
    pts = trajectory.parallelogram_points
    coords = np.column_stack([pts.real, pts.imag])
    diffs = np.linalg.norm(np.diff(coords, axis=0), axis=1)
    threshold = 0.25 * min(abs(lattice.omega1), abs(lattice.omega2))
    breaks = np.where(diffs > threshold)[0]
    start = 0
    first = True
    for brk in list(breaks) + [len(coords) - 1]:
        sl = coords[start : brk + 1]
        if sl.shape[0] >= 2:
            ax.plot(sl[:, 0], sl[:, 1], color="C0", lw=1.8, label="wrapped geodesic" if first else None)
            first = False
        start = brk + 1
    ax.scatter([pts[0].real], [pts[0].imag], color="C3", zorder=3, label="start")
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Identified parallelogram")
    ax.set_xlabel("Re z")
    ax.set_ylabel("Im z")
    ax.legend(loc="upper right", fontsize=8)
    if show_cover:
        ax = axes[1]
        cover = trajectory.cover_points
        ax.plot(cover.real, cover.imag, color="C0", lw=1.8, label="cover geodesic")
        ax.plot(poly[:, 0], poly[:, 1], color="black", lw=1.0, alpha=0.6)
        ax.scatter([cover[0].real], [cover[0].imag], color="C3", zorder=3, label="start")
        ax.scatter([cover[-1].real], [cover[-1].imag], color="C2", zorder=3, label="end = start + lattice")
        ax.set_aspect("equal", adjustable="box")
        ax.set_title("Universal cover")
        ax.set_xlabel("Re z")
        ax.set_ylabel("Im z")
        ax.legend(loc="best", fontsize=8)
    m, n = trajectory.winding_tuple
    fig.suptitle(
        f"tau={lattice.shape.tau}, winding=({m},{n}), "
        f"ell={trajectory.length:.6g}, area={lattice.area():.6g}"
    )
    fig.tight_layout()
    if path is None:
        plt.close(fig)
        return None
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def draw_fold_path(result, *, path: Path | None = None) -> Path | None:
    plt = _require_matplotlib()
    from .fold import DOMAIN_RE_BOUND

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    arc = np.linspace(np.pi / 3, 2 * np.pi / 3, 80)
    ax.plot(np.cos(arc), np.sin(arc), color="black", lw=1.2)
    ymax = max(3.0, max(s.y for s in result.path) + 0.4)
    ax.plot([-DOMAIN_RE_BOUND, -DOMAIN_RE_BOUND], [np.sqrt(0.75), ymax], color="black", lw=1.2)
    ax.plot([DOMAIN_RE_BOUND, DOMAIN_RE_BOUND], [np.sqrt(0.75), ymax], color="black", lw=1.2)
    xs = [s.x for s in result.path]
    ys = [s.y for s in result.path]
    ax.plot(xs, ys, color="C0", marker="o", lw=1.4, label="T/S word")
    ax.scatter([xs[0]], [ys[0]], color="C3", zorder=3, label="start")
    ax.scatter([xs[-1]], [ys[-1]], color="C2", zorder=3, label="reduced")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(0.0, ymax)
    ax.set_xlabel("Re tau")
    ax.set_ylabel("Im tau")
    ax.set_title("Fundamental-domain fold (discrete word)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    if path is None:
        plt.close(fig)
        return None
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path
