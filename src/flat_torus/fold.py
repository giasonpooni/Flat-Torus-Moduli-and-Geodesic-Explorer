"""Fundamental-domain fold for a general SL(2, Z) word."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor

from .lattice import ShapeParameter
from .lengths import Winding, loop_length
from .modular import (
    IDENTITY,
    MINUS_IDENTITY,
    S_GENERATOR,
    ModularMatrix,
    act_on_tau,
    act_on_winding,
    translation_matrix,
)

DOMAIN_RE_BOUND = 0.5
IN_DISK_TOL = 1e-12
RE_TOL = 1e-12
MAX_FOLD_STEPS = 10_000


@dataclass(frozen=True)
class ModularLetter:
    kind: str
    power: int = 1

    def __post_init__(self) -> None:
        kind = str(self.kind)
        if kind not in {"T", "S"}:
            raise ValueError(f"letter kind must be 'T' or 'S', got {kind!r}")
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "power", int(self.power))
        if kind == "S" and self.power != 1:
            raise ValueError("record S^2 as two S letters, or as -I separately")
        if kind == "T" and self.power == 0:
            raise ValueError("T^0 is the identity and is omitted from a word")

    def matrix(self) -> ModularMatrix:
        if self.kind == "T":
            return translation_matrix(self.power)
        return S_GENERATOR

    def as_pair(self) -> tuple[str, int]:
        return self.kind, self.power


@dataclass(frozen=True)
class ModularWord:
    letters: tuple[ModularLetter, ...] = ()

    @classmethod
    def from_pairs(cls, pairs):
        letters = tuple(ModularLetter(kind, power) for kind, power in pairs)
        return cls(letters=letters)

    def __len__(self) -> int:
        return len(self.letters)

    def matrix(self) -> ModularMatrix:
        acc = IDENTITY
        for letter in self.letters:
            acc = letter.matrix() * acc
        return acc

    def as_pairs(self):
        return tuple(letter.as_pair() for letter in self.letters)

    def apply_tau(self, shape: ShapeParameter) -> ShapeParameter:
        current = shape
        for letter in self.letters:
            current = act_on_tau(letter.matrix(), current)
        return current

    def apply_winding(self, winding: Winding) -> Winding:
        current = winding
        for letter in self.letters:
            current = act_on_winding(letter.matrix(), current)
        return current


@dataclass(frozen=True)
class FoldResult:
    original: ShapeParameter
    reduced: ShapeParameter
    matrix: ModularMatrix
    word: ModularWord
    path: tuple[ShapeParameter, ...]
    original_winding: Winding | None = None
    reduced_winding: Winding | None = None

    def length_pair(self):
        if self.original_winding is None or self.reduced_winding is None:
            return None
        return (
            loop_length(self.original, *self.original_winding.as_tuple()),
            loop_length(self.reduced, *self.reduced_winding.as_tuple()),
        )


def in_fundamental_domain(shape: ShapeParameter, *, re_tol: float = RE_TOL, disk_tol: float = IN_DISK_TOL) -> bool:
    return abs(shape.x) <= DOMAIN_RE_BOUND + re_tol and shape.modulus >= 1.0 - disk_tol


def _nearest_translation(real_part: float) -> int:
    if real_part > DOMAIN_RE_BOUND + RE_TOL:
        return int(floor(real_part + 0.5))
    if real_part < -DOMAIN_RE_BOUND - RE_TOL:
        return int(ceil(real_part - 0.5))
    return 0


def fold_to_fundamental_domain(shape: ShapeParameter, winding: Winding | None = None, *, canonical_boundary: bool = True) -> FoldResult:
    current = shape
    acc = IDENTITY
    pairs: list[tuple[str, int]] = []
    path: list[ShapeParameter] = [current]
    for _ in range(MAX_FOLD_STEPS):
        shifted = False
        k = _nearest_translation(current.x)
        if k != 0:
            step = translation_matrix(-k)
            current = act_on_tau(step, current)
            acc = step * acc
            pairs.append(("T", -k))
            path.append(current)
            shifted = True
        if current.modulus < 1.0 - IN_DISK_TOL:
            current = act_on_tau(S_GENERATOR, current)
            acc = S_GENERATOR * acc
            pairs.append(("S", 1))
            path.append(current)
            continue
        if not shifted:
            break
    else:
        raise RuntimeError("fold did not terminate; tau is not in the upper half-plane")
    if canonical_boundary:
        current, acc, pairs, path = _canonicalize_boundary(current, acc, pairs, path)
    if not in_fundamental_domain(current):
        raise RuntimeError(f"fold left the domain: tau={current.tau}, |tau|={current.modulus}")
    word = ModularWord.from_pairs(pairs) if pairs else ModularWord()
    reduced_winding = act_on_winding(acc, winding) if winding is not None else None
    return FoldResult(original=shape, reduced=current, matrix=acc, word=word, path=tuple(path), original_winding=winding, reduced_winding=reduced_winding)


def _canonicalize_boundary(current, acc, pairs, path):
    if abs(current.x - DOMAIN_RE_BOUND) <= RE_TOL:
        step = translation_matrix(-1)
        current = act_on_tau(step, current)
        acc = step * acc
        pairs.append(("T", -1))
        path.append(current)
    on_arc = abs(current.modulus - 1.0) <= IN_DISK_TOL
    if on_arc and current.x < -RE_TOL:
        current = act_on_tau(S_GENERATOR, current)
        acc = S_GENERATOR * acc
        pairs.append(("S", 1))
        path.append(current)
    return current, acc, pairs, path


def word_from_matrix(matrix: ModularMatrix) -> ModularWord:
    current = matrix
    reducing: list[ModularLetter] = []
    guard = 0
    while current.c != 0:
        guard += 1
        if guard > MAX_FOLD_STEPS:
            raise RuntimeError("word decomposition did not terminate")
        if abs(current.c) > abs(current.a):
            reducing.append(ModularLetter("S", 1))
            current = S_GENERATOR * current
            continue
        q, rem = divmod(current.a, current.c)
        if q != 0:
            reducing.append(ModularLetter("T", -q))
            current = translation_matrix(-q) * current
        if current.c != 0:
            reducing.append(ModularLetter("S", 1))
            current = S_GENERATOR * current
    if current.a == -1:
        reducing.append(ModularLetter("S", 1))
        reducing.append(ModularLetter("S", 1))
        current = MINUS_IDENTITY * current
    if current.b != 0:
        reducing.append(ModularLetter("T", -current.b))
        current = translation_matrix(-current.b) * current
    if current != IDENTITY:
        raise RuntimeError(f"decomposition leftover {current.as_tuple()}")
    reconstructed: list[ModularLetter] = []
    for letter in reversed(reducing):
        if letter.kind == "T":
            reconstructed.append(ModularLetter("T", -letter.power))
        else:
            reconstructed.extend([ModularLetter("S", 1), ModularLetter("S", 1), ModularLetter("S", 1)])
    compressed = _compress_s_runs(reconstructed)
    word = ModularWord(letters=tuple(compressed))
    got = word.matrix()
    if got != matrix:
        raise RuntimeError(f"word matrix {got.as_tuple()} != requested {matrix.as_tuple()}")
    return word


def _compress_s_runs(letters: list[ModularLetter]) -> list[ModularLetter]:
    out: list[ModularLetter] = []
    for letter in letters:
        if letter.kind == "T" and out and out[-1].kind == "T":
            power = out[-1].power + letter.power
            if power == 0:
                out.pop()
            else:
                out[-1] = ModularLetter("T", power)
            continue
        out.append(letter)
        while len(out) >= 4 and all(item.kind == "S" for item in out[-4:]):
            del out[-4:]
    return out
