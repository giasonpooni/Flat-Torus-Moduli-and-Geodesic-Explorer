from __future__ import annotations

from pathlib import Path

import pytest

from flat_torus.declaration import SCHEMA, default_path, load, loads
from flat_torus.first_release import run_first_release
from flat_torus.fold_experiment import run_fold_experiment
from flat_torus.modular import S_GENERATOR, T_GENERATOR


def test_first_release_declaration_is_the_elongated_torus():
    declared = load(default_path("first_release"))
    assert declared.tau == 4j
    assert declared.winding.as_tuple() == (1, 1)
    assert declared.start == 0.15 + 0.22j
    assert declared.representation.kind == "T"
    record = run_first_release(declaration=declared)
    assert record.passed
    assert record.experiment_specification["declaration"]["schema"] == SCHEMA


def test_fold_declaration_recovers_the_existing_word():
    declared = load(default_path("fold"))
    assert declared.tau == 2.4 + 0.35j
    assert declared.winding.as_tuple() == (3, 2)
    assert declared.representation.matrix() == T_GENERATOR * T_GENERATOR * S_GENERATOR * T_GENERATOR
    record = run_fold_experiment(declaration=declared)
    assert record.passed
    assert record.result["original_length"] == pytest.approx(record.result["length_after_matrix"], abs=1e-12)


def test_unknown_key_is_refused():
    text = Path(default_path("first_release")).read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="unknown key"):
        loads(text + "\nbonus = 1\n")


def test_zero_winding_is_refused():
    text = Path(default_path("first_release")).read_text(encoding="utf-8")
    text = text.replace("m = 1\nn = 1", "m = 0\nn = 0")
    with pytest.raises(ValueError, match="constant path"):
        loads(text)


def test_nonpositive_imaginary_part_is_refused():
    text = Path(default_path("first_release")).read_text(encoding="utf-8")
    text = text.replace("tau_y = 4.0", "tau_y = 0.0")
    with pytest.raises(ValueError, match="Im\\(tau\\)"):
        loads(text)


def test_wrong_schema_is_refused():
    with pytest.raises(ValueError, match="schema"):
        loads('schema = "other"\ntitle = "x"\n[object]\ntau_x=0\ntau_y=1\nreason="r"\n')


def test_bare_run_loads_the_committed_declaration():
    record = run_first_release()
    assert record.experiment_specification["tau"] == str(4j)
    assert record.experiment_specification["start"] == str(0.15 + 0.22j)
    assert record.passed
