from __future__ import annotations

from flat_torus import run_first_release


def test_first_release_experiment_passes() -> None:
    record = run_first_release(tau=4j, m=1, n=1)
    assert record.passed
    assert record.result["area"] == 1.0
    assert record.result["loop_length"] == record.result["loop_length_after_T"]
    assert record.result["winding_after_T"] == (0, 1)
