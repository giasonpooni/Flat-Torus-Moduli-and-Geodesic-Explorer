from __future__ import annotations

import pytest

from flat_torus import (
    IDENTITY,
    MINUS_IDENTITY,
    S_GENERATOR,
    T_GENERATOR,
    ModularMatrix,
    ShapeParameter,
    Winding,
    act_on_tau,
    act_on_winding,
    fold_to_fundamental_domain,
    in_fundamental_domain,
    loop_length,
    run_fold_experiment,
    word_from_matrix,
)


def test_defining_relations() -> None:
    assert S_GENERATOR * S_GENERATOR == MINUS_IDENTITY
    st = S_GENERATOR * T_GENERATOR
    assert st * st * st == MINUS_IDENTITY


@pytest.mark.parametrize(
    "tau",
    [1j, 0.3 + 1.1j, 2.4 + 0.35j, -3.7 + 0.2j, 0.1 + 0.2j, 0.5 + 0.9j],
)
def test_fold_lands_in_domain(tau: complex) -> None:
    shape = ShapeParameter.from_tau(tau)
    result = fold_to_fundamental_domain(shape)
    assert in_fundamental_domain(result.reduced)
    assert result.word.apply_tau(shape).tau == pytest.approx(result.reduced.tau)
    assert act_on_tau(result.matrix, shape).tau == pytest.approx(result.reduced.tau)


@pytest.mark.parametrize(
    "tau",
    [1j, 2.4 + 0.35j, -3.7 + 0.2j, 0.1 + 0.2j],
)
def test_fold_preserves_length(tau: complex) -> None:
    shape = ShapeParameter.from_tau(tau)
    winding = Winding(3, 2)
    result = fold_to_fundamental_domain(shape, winding)
    assert result.reduced_winding is not None
    assert loop_length(result.reduced, *result.reduced_winding.as_tuple()) == pytest.approx(
        loop_length(shape, *winding.as_tuple())
    )


def test_already_reduced_is_identity_word() -> None:
    shape = ShapeParameter(0.2, 1.3)
    result = fold_to_fundamental_domain(shape)
    assert result.matrix == IDENTITY
    assert result.word.as_pairs() == ()
    assert result.reduced.tau == pytest.approx(shape.tau)


@pytest.mark.parametrize(
    "matrix",
    [
        IDENTITY,
        T_GENERATOR,
        S_GENERATOR,
        MINUS_IDENTITY,
        T_GENERATOR * T_GENERATOR * S_GENERATOR * T_GENERATOR,
        S_GENERATOR * T_GENERATOR * S_GENERATOR,
        ModularMatrix(5, 2, 2, 1),
        ModularMatrix(2, 1, 1, 1),
        ModularMatrix(3, -5, -1, 2),
    ],
)
def test_word_recovers_matrix(matrix: ModularMatrix) -> None:
    word = word_from_matrix(matrix)
    assert word.matrix() == matrix


def test_word_action_matches_matrix() -> None:
    shape = ShapeParameter(0.4, 1.3)
    winding = Winding(3, 2)
    matrix = T_GENERATOR * T_GENERATOR * S_GENERATOR * T_GENERATOR
    word = word_from_matrix(matrix)
    assert word.apply_tau(shape).tau == pytest.approx(act_on_tau(matrix, shape).tau)
    assert word.apply_winding(winding) == act_on_winding(matrix, winding)


def test_minus_identity_flips_winding_only() -> None:
    shape = ShapeParameter(0.3, 1.2)
    winding = Winding(2, 1)
    assert act_on_tau(MINUS_IDENTITY, shape).tau == pytest.approx(shape.tau)
    assert act_on_winding(MINUS_IDENTITY, winding).as_tuple() == (-2, -1)
    assert loop_length(shape, -2, -1) == pytest.approx(loop_length(shape, 2, 1))


def test_fold_experiment_passes() -> None:
    record = run_fold_experiment()
    assert record.passed
    assert record.result["length_after_matrix"] == pytest.approx(
        record.result["original_length"]
    )
    assert record.result["length_after_fold"] == pytest.approx(
        record.result["original_length"]
    )
