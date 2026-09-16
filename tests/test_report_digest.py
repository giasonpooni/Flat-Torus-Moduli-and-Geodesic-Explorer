from flat_torus.experiment import CheckRecord, ExperimentRecord
from flat_torus.reports import CLAIM_SCOPE, REPORT_SCHEMA, report_commitment


def test_report_commitment_is_stable():
    record = ExperimentRecord(
        title="first-release",
        mathematical_specification={"object": "area-one flat torus"},
        experiment_specification={"tau": "4i"},
        result={"length": 4.123105625617661},
        verification=[CheckRecord("closure", True, "returns to start")],
    )
    first = report_commitment(record)
    second = report_commitment(record)
    assert first["schema"] == REPORT_SCHEMA
    assert first["claim_scope"] == CLAIM_SCOPE
    assert first["digest"] == second["digest"]
    assert len(first["digest"]) == 64
