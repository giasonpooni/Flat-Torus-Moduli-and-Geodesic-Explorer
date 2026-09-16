"""First-release demonstration: one torus, one loop, one basis change."""

from __future__ import annotations

from pathlib import Path

from flat_torus.declaration import default_path, load
from flat_torus import (
    format_record,
    loop_length,
    normalized_lattice,
    run_first_release,
    trace_closed_geodesic,
    translate_tau,
    translate_winding,
    write_report,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "results" / "quickstart.md"


def main() -> None:
    record = run_first_release(declaration=load(default_path("first_release")))
    write_report(REPORT, record)
    print(format_record(record))

    lattice = normalized_lattice(4j)
    print("Reference comparison")
    print(f"  tau = i   generators {normalized_lattice(1j).generator_lengths()}")
    print(f"  tau = 4i  generators {lattice.generator_lengths()}")
    print(f"  both areas {normalized_lattice(1j).area()}, {lattice.area()}")

    traj = trace_closed_geodesic(lattice, 1, 1, start=0.15 + 0.22j)
    shifted = translate_winding(traj.winding)
    print(
        f"  trajectory ({traj.winding.m}, {traj.winding.n}) length {traj.length:.12f}, "
        f"closed={traj.closed}, crossings={len(traj.crossings)}"
    )
    print(
        f"  after T: tau={translate_tau(lattice.shape).tau}, "
        f"winding={shifted.as_tuple()}, "
        f"length={loop_length(translate_tau(lattice.shape), *shifted.as_tuple()):.12f}"
    )
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
