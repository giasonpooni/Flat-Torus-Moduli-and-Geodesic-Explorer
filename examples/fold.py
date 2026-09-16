"""Fold a general SL(2, Z) word into the standard fundamental domain."""

from __future__ import annotations

from pathlib import Path

from flat_torus import format_record, run_fold_experiment, write_report
from flat_torus.fold import fold_to_fundamental_domain
from flat_torus.lattice import ShapeParameter
from flat_torus.lengths import Winding
from flat_torus.visualize import draw_fold_path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "results" / "fold.md"
FIGURE = ROOT / "results" / "fold.png"


def main() -> None:
    record = run_fold_experiment(tau=2.4 + 0.35j, m=3, n=2)
    write_report(REPORT, record)
    print(format_record(record))
    folded = fold_to_fundamental_domain(
        ShapeParameter.from_tau(2.4 + 0.35j),
        Winding(3, 2),
    )
    try:
        draw_fold_path(folded, path=FIGURE)
        print(f"Wrote {FIGURE}")
    except ImportError as exc:
        print(f"Skipped figure: {exc}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
