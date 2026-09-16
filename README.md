# Flat-Torus Moduli and Geodesic Explorer

An interactive computational testbed for area-one flat tori, demonstrating
geodesic trajectories, closed-loop lengths, and invariance under changes of
lattice representation.

Short name **FTMGE**. The reusable library import is `flat_torus`.

This is the first project in the portfolio

> Computational Geometry, Geodesic Dynamics, and Invariant Representations

The organizing question is:

> What belongs to the underlying mathematical object, what belongs to its
> representation, and what changes when the object itself changes?

## What is in the first release

| Responsibility | What the testbed demonstrates |
| --- | --- |
| Normalized lattice | Area-one generators `\u03c9\u2081 = y^{-1/2}`, `\u03c9\u2082 = \u03c4 y^{-1/2}`. |
| Closed-loop lengths | Exact formula `\u2113_{m,n}(\u03c4) = \\|m + n \u03c4\\| / \u221ay`. |
| Periodic trajectories | Straight lines in the cover, wrapped through the parallelogram, with recorded edge crossings. |
| Equivalent descriptions | `\u03c4 \u21a6 \u03c4+1` with matching labels `(m, n) \u21a6 (m\u2212n, n)` leaves the length unchanged. |
| Linked explorer | A figure drawn from the same objects the tests use. |

The first-release claim is small and checkable:

> Construct one normalized torus, trace one closed trajectory, change its
> representation, and demonstrate that the corresponding intrinsic result
> survives.

## The mathematical object

```text
\u03c4 = x + i y,    y > 0
\u039b_\u03c4 = y^{-1/2} (\u2124 + \u03c4 \u2124)
T_\u03c4 = \u2102 / \u039b_\u03c4
\u2113_{m,n}(\u03c4) = |m + n \u03c4| / \u221ay
```

`\u03c4` determines lattice *shape*. The factor `y^{-1/2}` removes area as a
variable. The torus is the quotient obtained by identifying points that
differ by a lattice vector.

Reference cases from the project brief, same area, different shape:

| Shape parameter | First generating length | Second generating length | Fundamental area |
| --- | --- | --- | --- |
| `\u03c4 = i` | `1` | `1` | `1` |
| `\u03c4 = 4i` | `1/2` | `2` | `1` |

The second torus has a shorter non-contractible loop despite having the
same area.

A basis change is not a shape change. After `\u03c4' = \u03c4 + 1` the winding
labels must move with the basis,

```text
(m', n') = (m \u2212 n, n)
\u2113_{m\u2212n, n}(\u03c4 + 1) = \u2113_{m, n}(\u03c4)
```

Comparing the same integer labels before and after a basis change does
not necessarily compare the same trajectory.

## Install and run

Python 3.12 or 3.13 and NumPy are required. [uv](https://docs.astral.sh/uv/)
is the supported runner; a plain virtual environment also works.

```bash
git clone https://github.com/giasonpooni/Flat-Torus-Moduli-and-Geodesic-Explorer.git
cd Flat-Torus-Moduli-and-Geodesic-Explorer
uv run --python 3.13 python examples/quickstart.py
uv run --python 3.13 --with pytest pytest -q
```

Without uv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e . pytest
PYTHONPATH=src python examples/quickstart.py
PYTHONPATH=src pytest -q
```

The quickstart writes `results/quickstart.md`.

To draw the parallelogram view (optional matplotlib extra):

```bash
uv run --python 3.13 --with matplotlib python examples/explorer.py
```

That writes `results/explorer.png` from the same `ClosedTrajectory` object
the tests close against. The doughnut picture of a torus is not used as
geometry.

## Library layout

```text
Normalized lattice and loop lengths
        +
Wrapped trajectories and edge crossings
        +
Modular changes of representation
        +
Experiment contract and reports
```

```text
from flat_torus import (
    normalized_lattice,
    loop_length,
    trace_closed_geodesic,
    translate_tau,
    translate_winding,
    run_first_release,
)
```

## Scope and limits

First release: one family of area-one flat tori, exact loop lengths,
integer windings, the generators `T` and `S` of SL(2, \u2124), and a
parallelogram renderer that does not own the metric.

Not in this release:

- Paths through moduli space, or the hyperbolic metric on the upper half-plane.
- Translation surfaces beyond the square torus (that is the next surface project).
- Jacobi fields and nearby-geodesic sensitivity (companion testbed).
- Covariance-manifold interpolation, or intrinsic geodesics on triangle meshes.

The authoritative geometry remains the identified flat parallelogram.

See [docs/SCOPE.md](docs/SCOPE.md) and [docs/METHODS.md](docs/METHODS.md).

## Portfolio

| Project | Role |
| --- | --- |
| Flat-Torus Moduli and Geodesic Explorer | Starting project: geometry, equivalence, and spaces of shapes. |
| [Geodesic Flow and Jacobi-Field Testbed](https://github.com/giasonpooni/Geodesic-Flow-and-Jacobi-Field-Testbed) | Numerical companion: sensitivity of nearby geodesics. |
| Translation-Surface Dynamics Explorer | Planned: explicit polygon gluing. |
| Covariance Geometry and Geodesic Testbed | Planned independent branch. |
| Intrinsic Surface Geodesics Testbed | Planned discrete-geometry branch. |

## License

MIT. See [LICENSE](LICENSE).
