"""A torus experiment declared as data instead of as example defaults.

tau, the winding, the start point, and the modular word are the object
or its representation. They do not belong in JSPT and they are not
UI preferences. A misspelled key must not silently become a default.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from .fold import ModularLetter, ModularWord
from .lattice import ShapeParameter
from .lengths import Winding
from .modular import IDENTITY, S_GENERATOR, T_GENERATOR, ModularMatrix

SCHEMA = "flat-torus-declaration-v1"

_OBJECT_KEYS = {"tau_x", "tau_y", "reason"}
_LOOP_KEYS = {"m", "n", "start_re", "start_im"}
_REP_KEYS = {"kind", "letters", "reason"}
_LETTER_KEYS = {"kind", "power"}
_TOP_KEYS = {"schema", "title", "object", "loop", "representation", "notes"}
_REP_KINDS = {"identity", "T", "S", "modular-word"}


def _str(value, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{what} must be a non-empty string, got {value!r}")
    return value.strip()


def _float(value, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{what} must be a number, got {value!r}")
    value = float(value)
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError(f"{what} must be finite, got {value!r}")
    return value


def _int(value, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{what} must be an integer, got {value!r}")
    return int(value)


def _table(value, what: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{what} must be a table, got {type(value).__name__}")
    return value


def _only(table: dict, allowed: set[str], what: str) -> None:
    unknown = sorted(set(table) - allowed)
    if unknown:
        raise ValueError(f"{what} has unknown key(s) {unknown}; allowed: {sorted(allowed)}")


@dataclass(frozen=True)
class Representation:
    kind: str
    word: ModularWord
    reason: str

    def matrix(self) -> ModularMatrix:
        if self.kind == "identity":
            return IDENTITY
        if self.kind == "T":
            return T_GENERATOR
        if self.kind == "S":
            return S_GENERATOR
        return self.word.matrix()


@dataclass(frozen=True)
class TorusDeclaration:
    title: str
    shape: ShapeParameter
    object_reason: str
    winding: Winding
    start: complex
    representation: Representation
    notes: str

    @property
    def tau(self) -> complex:
        return self.shape.tau

    def as_dict(self) -> dict[str, object]:
        return {
            "schema": SCHEMA,
            "title": self.title,
            "tau": str(self.tau),
            "winding": self.winding.as_tuple(),
            "start": str(self.start),
            "representation": {
                "kind": self.representation.kind,
                "letters": list(self.representation.word.as_pairs()),
                "reason": self.representation.reason,
            },
            "object_reason": self.object_reason,
            "notes": self.notes,
        }


def _parse_letters(raw) -> ModularWord:
    if not isinstance(raw, list) or not raw:
        raise ValueError("representation.letters must be a non-empty array of tables")
    letters = []
    for index, item in enumerate(raw):
        table = _table(item, f"representation.letters[{index}]")
        _only(table, _LETTER_KEYS, f"representation.letters[{index}]")
        letters.append(
            ModularLetter(
                _str(table.get("kind"), f"representation.letters[{index}].kind"),
                _int(table.get("power", 1), f"representation.letters[{index}].power"),
            )
        )
    return ModularWord(letters=tuple(letters))


def loads(text: str) -> TorusDeclaration:
    data = tomllib.loads(text)
    _only(data, _TOP_KEYS, "declaration")
    schema = _str(data.get("schema"), "schema")
    if schema != SCHEMA:
        raise ValueError(f"schema must be {SCHEMA!r}, got {schema!r}")
    title = _str(data.get("title"), "title")
    obj = _table(data.get("object"), "object")
    _only(obj, _OBJECT_KEYS, "object")
    shape = ShapeParameter(
        _float(obj.get("tau_x"), "object.tau_x"),
        _float(obj.get("tau_y"), "object.tau_y"),
    )
    object_reason = _str(obj.get("reason"), "object.reason")
    loop = _table(data.get("loop"), "loop")
    _only(loop, _LOOP_KEYS, "loop")
    winding = Winding(_int(loop.get("m"), "loop.m"), _int(loop.get("n"), "loop.n"))
    start = complex(
        _float(loop.get("start_re"), "loop.start_re"),
        _float(loop.get("start_im"), "loop.start_im"),
    )
    rep = _table(data.get("representation"), "representation")
    _only(rep, _REP_KEYS, "representation")
    kind = _str(rep.get("kind"), "representation.kind")
    if kind not in _REP_KINDS:
        raise ValueError(f"representation.kind must be one of {sorted(_REP_KINDS)}, got {kind!r}")
    reason = _str(rep.get("reason"), "representation.reason")
    if kind == "modular-word":
        word = _parse_letters(rep.get("letters"))
    else:
        if "letters" in rep:
            raise ValueError(f"representation.kind {kind!r} does not take letters; omit them")
        if kind == "T":
            word = ModularWord(letters=(ModularLetter("T", 1),))
        elif kind == "S":
            word = ModularWord(letters=(ModularLetter("S", 1),))
        else:
            word = ModularWord()
    notes = _str(data["notes"], "notes") if "notes" in data else ""
    return TorusDeclaration(
        title=title,
        shape=shape,
        object_reason=object_reason,
        winding=winding,
        start=start,
        representation=Representation(kind=kind, word=word, reason=reason),
        notes=notes,
    )


def load(path: str | Path) -> TorusDeclaration:
    return loads(Path(path).read_text(encoding="utf-8"))


def default_path(name: str) -> Path:
    filename = f"{name}.toml"
    here = Path(__file__).resolve()
    candidates = (
        Path.cwd() / "declarations" / filename,
        here.parents[2] / "declarations" / filename,
        here.parent / "declarations" / filename,
    )
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(
        f"declaration {filename!r} not found; looked in {[str(p) for p in candidates]}"
    )
