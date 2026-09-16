from flat_torus.first_release import run_first_release
from flat_torus.reports import CLAIM_SCOPE, REPORT_SCHEMA, report_commitment


def test_live_first_release_commitment_is_json_and_stable():
    record = run_first_release()
    first = report_commitment(record)
    second = report_commitment(record)
    assert record.passed
    assert first["schema"] == REPORT_SCHEMA
    assert first["claim_scope"] == CLAIM_SCOPE
    assert first["digest"] == second["digest"]
    assert len(first["digest"]) == 64
    assert first["payload"]["result"]["closed"] is True
