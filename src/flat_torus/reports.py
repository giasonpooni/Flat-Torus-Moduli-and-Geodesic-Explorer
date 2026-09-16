"""Plain-text experiment reports and a record-integrity digest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .experiment import ExperimentRecord

REPORT_SCHEMA = "torus-report-commitment-v1"
CLAIM_SCOPE = "record-integrity-only"


def jsonable(value: object) -> object:
    """JSON payload for a pinned report. Complex -> {re, im}. Numpy scalars -> Python."""
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, complex):
        return {"re": float(value.real), "im": float(value.imag)}
    if hasattr(value, "item") and not isinstance(value, (bytes, bytearray)):
        try:
            return jsonable(value.item())
        except (AttributeError, ValueError):
            pass
    if isinstance(value, int) and not isinstance(value, bool):
        return int(value)
    if isinstance(value, float):
        return float(value)
    raise TypeError(f"report payload cannot encode {type(value).__name__}")


def canonical_digest(value: object) -> str:
    encoded = json.dumps(
        jsonable(value),
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def report_commitment(record: ExperimentRecord) -> dict[str, object]:
    payload = jsonable(record.as_dict())
    return {
        "schema": REPORT_SCHEMA,
        "kind": "torus-report",
        "claim_scope": CLAIM_SCOPE,
        "payload": payload,
        "digest": canonical_digest(payload),
    }


def format_record(record: ExperimentRecord) -> str:
    status = "PASS" if record.passed else "FAIL"
    lines = [
        f"# {record.title}",
        "",
        f"Overall: {status}",
        "",
        "## Mathematical specification",
        "",
    ]
    for key, value in record.mathematical_specification.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Experiment specification", ""])
    for key, value in record.experiment_specification.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Result", ""])
    for key, value in record.result.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Verification", ""])
    for check in record.verification:
        mark = "PASS" if check.passed else "FAIL"
        tol = "" if check.tolerance is None else f" (tol={check.tolerance:g})"
        lines.append(f"- [{mark}] {check.name}: {check.details}{tol}")
    if record.limitations:
        lines.extend(["", "## Limitations", ""])
        for note in record.limitations:
            lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def write_report(path: Path, record: ExperimentRecord) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_record(record), encoding="utf-8")
    return path
