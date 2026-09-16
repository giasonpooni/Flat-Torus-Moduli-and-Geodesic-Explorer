from __future__ import annotations

import pytest

from flat_torus import (
    ModularMatrix,
    ShapeParameter,
    Winding,
    act_on_tau,
    act_on_winding,
    loop_length,
    translate_tau,
    translate_winding,
)


def test_translation_identity_on_the_same_trajectory() -> None:
    shape = ShapeParameter(0.4, 1.3)
    winding = Winding(3, 2)
    new_shape = translate_tau(shape)
    new_winding = translate_winding(winding)
    assert new_shape.tau == pytest.approx(shape.tau + 1)
    assert new_winding.as_tuple() == (3 - 2, 2)
    assert loop_length(new_shape, *new_winding.as_tuple()) == pytest.approx(
        loop_length(shape, *winding.as_tuple())
    )


def test_same_labels_after_T_are_a_different_trajectory() -> None:
    shape = ShapeParameter(0.4, 1.3)
    before = loop_length(shape, 3, 2)
    after_same_labels = loop_length(translate_tau(shape), 3, 2)
    assert after_same_labels != pytest.approx(before)


def test_s_invariance() -> None:
    shape = ShapeParameter(0.4, 1.3)
    winding = Winding(3, 2)
    s = ModularMatrix(0, -1, 1, 0)
    new_shape = act_on_tau(s, shape)
    new_winding = act_on_winding(s, winding)
    assert new_winding.as_tuple() == (2, -3)
    assert loop_length(new_shape, *new_winding.as_tuple()) == pytest.approx(
        loop_length(shape, *winding.as_tuple())
    )


def test_rejects_non_sl2() -> None:
    with pytest.raises(ValueError):
        ModularMatrix(2, 0, 0, 2)
