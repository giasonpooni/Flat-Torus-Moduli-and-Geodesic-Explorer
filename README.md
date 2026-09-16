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

## What is delivered

| Responsibility | What the testbed demonstrates |
| --- | --- |
| Normalized lattice | Area-one generators `omega1 = y^{-1/2}`, `omega2 = tau * y^{-1/2}`. |
| Closed-loop lengths | Exact formula `ell_{m,n}(tau) = |m + n tau| / sqrt(y)`. |
| Periodic trajectories | Straight lines in the cover, wrapped through the parallelogram, with recorded edge crossings. |
| Equivalent descriptions | `tau -> tau+1` with matching labels `(m, n) -> (m-n, n)` leaves the length unchanged. |
| Fundamental-domain fold | A general SL(2, Z) word in T and S reduces tau to `|Re tau| <= 1/2`, `|tau| >= 1`, with labels moving with the word. |
| Linked explorer | A figure drawn from the same objects the tests use. |

The first-release claim remains:

> Construct one normalized torus, trace one closed trajectory, change its
> representation, and demonstrate that the corresponding intrinsic result
> survives.

The fold increment adds: the same claim for an arbitrary SL(2, Z) word,
not only the generators T and S.

## The mathematical object

```text
tau = x + i y,    y > 0
Lambda_tau = y^{-1/2} (Z + tau Z)
T_tau = C / Lambda_tau
ell_{m,n}(tau) = |m + n tau| / sqrt(y)
```

`tau` determines lattice *shape*. The factor `y^{-1/2}` removes area as a
variable. The torus is the quotient obtained by identifying points that
differ by a lattice vector.

Reference cases from the project brief, same area, different shape:

| Shape parameter | First generating length | Second generating length | Fundamental area |
| --- | --- | --- | --- |
| `tau = i` | `1` | `1` | `1` |
| `tau = 4i` | `1/2` | `2` | `1` |

The second torus has a shorter non-contractible loop despite having the
same area.

A basis change is not a shape change. After `tau' = tau + 1` the winding
labels must move with the basis,

```text
(m', n') = (m - n, n)
ell_{m-n, n}(tau + 1) = ell_{m, n}(tau)
```

For a general matrix `g = [[a, b], [c, d]]` with `tau' = g . tau`,

```text
m' = a m - b n,    n' = -c m + d n
```

Comparing the same integer labels before and after a basis change does
not necessarily compare the same trajectory. Using `g^{-1}` on the labels
is correct for a single generator and wrong for a composed word.

## Install and run

Python 3.12 or 3.13 and NumPy are required. [uv](https://docs.astral.sh/uv/)
is the supported runner; a plain virtual environment also works.

```bash
git clone https://github.com/giasonpooni/Flat-Torus-Moduli-and-Geodesic-Explorer.git
cd Flat-Torus-Moduli-and-Geodesic-Explorer
uv run --python 3.13 python examples/quickstart.py
uv run --python 3.13 python examples/fold.py
uv run --python 3.13 python examples/write_validation.py
uv run --python 3.13 --with pytest pytest -q
```

Without uv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e . pytest
PYTHONPATH=src python examples/quickstart.py
PYTHONPATH=src python examples/fold.py
PYTHONPATH=src python examples/write_validation.py
PYTHONPATH=src pytest -q
```

The quickstart writes `results/quickstart.md`. The fold example writes
`results/fold.md`. `write_validation.py` writes JSON commitments under
`validation/` for the CSE experiment harness.

To draw views (optional matplotlib extra):

```bash
uv run --python 3.13 --with matplotlib python examples/explorer.py
uv run --python 3.13 --with matplotlib python examples/fold.py
```

The explorer writes `results/explorer.png` from the same `ClosedTrajectory`
the tests close against. The fold figure is a discrete T/S word against
the standard domain, not a hyperbolic geodesic in moduli space.

## Bind a report in the CSE harness

This repo does not import GAT and does not prove. After
`examples/write_validation.py` you can hand the commitment file to CSE:

```bash
python -m gat.demo.experiment_harness \
  --disposition validation/beam-b1-disposition-v1.json \
  --commit path/to/torus-first-release-commitment-v1.json \
  -o out/harness-bundle.json
```

The harness records the digest. It does not change the torus object and
it does not put this algebra in an SP1 guest. Lengths are already
replayable by re-running the experiment.

## Library layout

```text
Normalized lattice and loop lengths
        +
Wrapped trajectories and edge crossings
        +
Modular changes of representation
        +
SL(2, Z) words and fundamental-domain fold
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
    fold_to_fundamental_domain,
    word_from_matrix,
    run_first_release,
    run_fold_experiment,
)
```

## Scope and limits

Delivered: one family of area-one flat tori, exact loop lengths, integer
windings, the generators T and S, general SL(2, Z) words, a fundamental-
domain fold, and a parallelogram renderer that does not own the metric.

Not in this repository yet:

- Continuous paths through moduli space, or the hyperbolic metric on the upper half-plane.
- Translation surfaces beyond the square torus.
- Jacobi fields and nearby-geodesic sensitivity (companion testbed).
- Covariance-manifold interpolation, or intrinsic geodesics on triangle meshes.

The authoritative geometry remains the identified flat parallelogram.

See [docs/SCOPE.md](docs/SCOPE.md) and [docs/METHODS.md](docs/METHODS.md).

## Portfolio

| Project | Role |
| --- | --- |
| Flat-Torus Moduli and Geodesic Explorer | Starting project: geometry, equivalence, and spaces of shapes. |
| [Geodesic Flow and Jacobi-Field Testbed](https://github.com/giasonpooni/Geodesic-Flow-and-Jacobi-Field-Testbed) | Numerical companion: sensitivity of nearby geodesics. |
| [Construction State Estimator](https://github.com/giasonpooni/Construction-State-Estimator-for-BIM) | Consumer of report digests via the experiment harness. |
| Translation-Surface Dynamics Explorer | Planned: explicit polygon gluing. |
| Covariance Geometry and Geodesic Testbed | Planned independent branch. |
| Intrinsic Surface Geodesics Testbed | Planned discrete-geometry branch. |

## License

MIT. See [LICENSE](LICENSE).
