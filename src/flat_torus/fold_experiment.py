"""Experiment: fold a general SL(2, Z) word and keep the loop length."""

from __future__ import annotations

from .checks import check_unit_area
from .declaration import TorusDeclaration, default_path, load
from .experiment import CheckRecord, ExperimentRecord
from .fold import fold_to_fundamental_domain, in_fundamental_domain, word_from_matrix
from .lattice import ShapeParameter, normalized_lattice
from .lengths import Winding, loop_length
from .modular import (
    IDENTITY,
    MINUS_IDENTITY,
    S_GENERATOR,
    T_GENERATOR,
    ModularMatrix,
    act_on_tau,
    act_on_winding,
    length_after_basis_change,
)

LENGTH_TOL = 1e-12


def check_defining_relations() -> list[CheckRecord]:
    s2 = S_GENERATOR * S_GENERATOR
    st = S_GENERATOR * T_GENERATOR
    st3 = st * st * st
    return [
        CheckRecord(name="S^2 = -I", passed=s2 == MINUS_IDENTITY, details=f"S^2 = {s2.as_tuple()}"),
        CheckRecord(name="(ST)^3 = -I", passed=st3 == MINUS_IDENTITY, details=f"(ST)^3 = {st3.as_tuple()}"),
        CheckRecord(
            name="-I acts as the identity on tau",
            passed=act_on_tau(MINUS_IDENTITY, ShapeParameter(0.3, 1.2)).tau == ShapeParameter(0.3, 1.2).tau,
            details="(-I).tau = tau",
        ),
    ]


def check_fold_in_domain(shape: ShapeParameter) -> CheckRecord:
    result = fold_to_fundamental_domain(shape)
    return CheckRecord(
        name=f"fold of tau={shape.tau} lands in the domain",
        passed=in_fundamental_domain(result.reduced),
        details=f"reduced={result.reduced.tau}, word={result.word.as_pairs()}",
    )


def check_fold_length(shape: ShapeParameter, winding: Winding, *, tol: float = LENGTH_TOL) -> CheckRecord:
    result = fold_to_fundamental_domain(shape, winding)
    original, reduced = result.length_pair()
    return CheckRecord(
        name="fold preserves ell after labels move",
        passed=abs(original - reduced) <= tol,
        details=(
            f"ell_{winding.as_tuple()}({shape.tau}) = {original:.16f}, "
            f"ell_{result.reduced_winding.as_tuple()}({result.reduced.tau}) = {reduced:.16f}"
        ),
        tolerance=tol,
    )


def check_word_recovers_matrix(matrix: ModularMatrix) -> CheckRecord:
    word = word_from_matrix(matrix)
    got = word.matrix()
    return CheckRecord(
        name=f"word recovers {matrix.as_tuple()}",
        passed=got == matrix,
        details=f"word={word.as_pairs()} product={got.as_tuple()}",
    )


def check_word_agrees_with_matrix(shape, winding, matrix, *, tol: float = LENGTH_TOL) -> CheckRecord:
    word = word_from_matrix(matrix)
    tau_word = word.apply_tau(shape)
    tau_mat = act_on_tau(matrix, shape)
    wind_word = word.apply_winding(winding)
    wind_mat = act_on_winding(matrix, winding)
    original, transformed = length_after_basis_change(shape, winding, matrix)
    ok = abs(tau_word.tau - tau_mat.tau) <= tol and wind_word == wind_mat and abs(original - transformed) <= tol
    return CheckRecord(
        name="letter-by-letter action matches the matrix",
        passed=ok,
        details=f"word winding={wind_word.as_tuple()}, matrix winding={wind_mat.as_tuple()}",
        tolerance=tol,
    )


def run_fold_experiment(
    *,
    declaration: TorusDeclaration | None = None,
    tau: complex | None = None,
    m: int | None = None,
    n: int | None = None,
    extra: ModularMatrix | None = None,
) -> ExperimentRecord:
    declared = declaration
    if declared is None and tau is None and m is None and n is None and extra is None:
        declared = load(default_path("fold"))
    if declared is not None:
        tau = declared.tau if tau is None else tau
        m = declared.winding.m if m is None else m
        n = declared.winding.n if n is None else n
        extra = declared.representation.matrix() if extra is None else extra
    tau = 2.4 + 0.35j if tau is None else tau
    m = 3 if m is None else m
    n = 2 if n is None else n
    shape = ShapeParameter.from_tau(tau)
    winding = Winding(m, n)
    extra = extra or (T_GENERATOR * T_GENERATOR * S_GENERATOR * T_GENERATOR)
    after_extra = act_on_tau(extra, shape)
    after_extra_winding = act_on_winding(extra, winding)
    folded = fold_to_fundamental_domain(after_extra, after_extra_winding)
    lattice = normalized_lattice(folded.reduced)
    verification = [
        *check_defining_relations(),
        check_unit_area(lattice),
        check_word_recovers_matrix(IDENTITY),
        check_word_recovers_matrix(T_GENERATOR),
        check_word_recovers_matrix(S_GENERATOR),
        check_word_recovers_matrix(MINUS_IDENTITY),
        check_word_recovers_matrix(extra),
        check_word_agrees_with_matrix(shape, winding, extra),
        check_fold_in_domain(shape),
        check_fold_in_domain(after_extra),
        check_fold_length(shape, winding),
        check_fold_length(after_extra, after_extra_winding),
    ]
    original_length = loop_length(shape, m, n)
    extra_length = loop_length(after_extra, *after_extra_winding.as_tuple())
    folded_pair = folded.length_pair()
    folded_length = folded_pair[1] if folded_pair else None
    return ExperimentRecord(
        title=(declared.title if declared is not None else "SL(2, Z) word and fundamental-domain fold"),
        mathematical_specification={
            "object": "area-one flat torus, described by any tau in the upper half-plane",
            "domain": "|Re(tau)| <= 1/2 and |tau| >= 1",
            "group": "SL(2, Z) generated by T and S, with S^2 = (ST)^3 = -I",
            "labels": "m' = a m - b n, n' = -c m + d n",
            "length_formula": "ell_{m,n}(tau) = |m + n tau| / sqrt(y)",
        },
        experiment_specification={
            "tau": str(tau),
            "winding": winding.as_tuple(),
            "applied_matrix": extra.as_tuple(),
            "applied_word": word_from_matrix(extra).as_pairs(),
            "declaration": None if declared is None else declared.as_dict(),
        },
        result={
            "tau_after_matrix": after_extra.tau,
            "winding_after_matrix": after_extra_winding.as_tuple(),
            "reduced_tau": folded.reduced.tau,
            "reduced_winding": None if folded.reduced_winding is None else folded.reduced_winding.as_tuple(),
            "fold_word": folded.word.as_pairs(),
            "fold_matrix": folded.matrix.as_tuple(),
            "original_length": original_length,
            "length_after_matrix": extra_length,
            "length_after_fold": folded_length,
            "in_domain": in_fundamental_domain(folded.reduced),
        },
        verification=verification,
        limitations=[
            "The fold is a discrete T/S word, not a hyperbolic geodesic in moduli space.",
            "Boundary points are identified; the canonical representative maps Re=+1/2 to Re=-1/2.",
            "S^2 = -I flips winding sign without changing tau or length.",
        ],
    )
