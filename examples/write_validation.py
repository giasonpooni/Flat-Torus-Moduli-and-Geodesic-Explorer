"""Write pinned validation commitments from live experiments."""

from pathlib import Path
import json

from flat_torus.first_release import run_first_release
from flat_torus.fold_experiment import run_fold_experiment
from flat_torus.reports import report_commitment, write_report


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "validation"
    root.mkdir(parents=True, exist_ok=True)
    first = run_first_release()
    fold = run_fold_experiment()
    for name, record in ("torus-first-release", first), ("torus-fold", fold):
        commitment = report_commitment(record)
        (root / f"{name}-commitment-v1.json").write_text(
            json.dumps(commitment, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        write_report(root / f"{name}.md", record)
        print(name, record.passed, commitment["digest"])


if __name__ == "__main__":
    main()
