"""Fold a general SL(2, Z) word into the standard fundamental domain."""

from __future__ import annotations

from pathlib import Path

from flat_torus import format_record, run_fold_experiment, write_report
from flat_torus.declaration import default_path, load
from flat_torus.fold import fold_to_fundamental_domain
from flat_torus.visualize import draw_fold_path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "results" / "fold.md"
FIGURE = ROOT / "results" / "fold.png"


def main() -> None:
    declared = load(default_path("fold"))
    record = run_fold_experiment(declaration=declared)
    write_report(REPORT, record)
    print(format_record(record))
    folded = fold_to_fundamental_domain(declared.shape, declared.winding)
    try:
        draw_fold_path(folded, path=FIGURE)
        print(f"Wrote {FIGURE}")
    except ImportError as exc:
        print(f"Skipped figure: {exc}")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
