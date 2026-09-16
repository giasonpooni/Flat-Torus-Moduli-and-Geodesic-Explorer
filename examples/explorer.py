"""Parallelogram view of the same trajectory the tests close against."""

from __future__ import annotations

from pathlib import Path

from flat_torus import run_first_release, trace_closed_geodesic
from flat_torus.visualize import draw_trajectory

ROOT = Path(__file__).resolve().parents[1]
FIGURE = ROOT / "results" / "explorer.png"
REPORT = ROOT / "results" / "explorer.md"


def main() -> None:
    record = run_first_release(tau=4j, m=1, n=1, start=0.15 + 0.22j)
    traj = trace_closed_geodesic(4j, 1, 1, start=0.15 + 0.22j)
    draw_trajectory(traj, path=FIGURE)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "\n".join(
            [
                "# Explorer figure",
                "",
                f"Figure: `{FIGURE.relative_to(ROOT)}`",
                "",
                "Drawn from `trace_closed_geodesic(4j, 1, 1)`, not from a",
                "separate geometric model. The doughnut embedding of a torus",
                "is not used.",
                "",
                f"First-release experiment passed: {record.passed}",
                f"Loop length: {traj.length}",
                f"Crossings: {len(traj.crossings)}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {FIGURE}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
