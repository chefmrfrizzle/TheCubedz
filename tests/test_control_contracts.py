from copy import deepcopy
from datetime import UTC, datetime
from hashlib import sha256
import json

from research_core.control import validate_control_document

HASH = "sha256:" + "a" * 64
NOW = datetime(2026, 8, 7, 12, 0, tzinfo=UTC)


def task():
    return {
        "schema_version": "1.0.0",
        "task_id": "TASK-000001",
        "title": "Validate a bounded research artifact",
        "classification": "VALIDATION",
        "authority_tier": "WORKING",
        "objective": "Validate one immutable candidate with declared checks.",
        "inputs": [{"path": "candidates/CANDIDATE-000001.json", "sha256": HASH, "read_only": True}],
        "required_gates": ["TESTS", "HUMAN_PROMOTION"],
        "created_by": {"type": "HUMAN", "id": "ChefMrFrizzle"},
        "created_at": "2026-08-07T11:00:00Z",
        "human_promotion_required": True,
    }


def capability():
    return {
        "schema_version": "1.0.0",
        "capability_id": "CAP-000001",
        "task_id": "TASK-000001",
        "actor": {"type": "AGENT", "id": "build-1", "role": "BUILD"},
        "allowed_tools": ["READ_FILES", "WRITE_WORKSPACE", "RUN_TESTS"],
        "read_paths": ["candidates", "src", "tests"],
        "write_paths": ["work/TASK-000001"],
        "network": {"mode": "DENY", "destinations": []},
        "quotas": {"cpu_seconds": 300, "memory_mb": 1024, "wall_seconds": 600, "disk_mb": 1024, "output_mb": 32, "processes": 8},
        "issued_at": "2026-08-07T11:00:00Z",
        "expires_at": "2026-08-07T13:00:00Z",
        "issued_by": {"type": "HUMAN", "id": "ChefMrFrizzle"},
    }


def promotion():
    return {
        "schema_version": "1.0.0",
        "decision_id": "DECISION-000001",
        "task_id": "TASK-000001",
        "bundle_digest": HASH,
        "decision": "APPROVE",
        "reviewed_by": {"type": "HUMAN", "id": "reviewer-1"},
        "proposed_by": {"type": "AGENT", "id": "build-1"},
        "rationale": "All declared gates passed and residual risk is accepted.",
        "decided_at": "2026-08-07T12:00:00Z",
    }


def test_valid_task_requires_human_promotion():
    assert validate_control_document("task", task()) == []
    invalid = deepcopy(task())
    invalid["required_gates"] = ["TESTS"]
    assert "HUMAN_PROMOTION is mandatory" in " ".join(validate_control_document("task", invalid))


def test_capability_rejects_expiry_network_and_canonical_writes():
    assert validate_control_document("capability", capability(), now=NOW) == []
    expired = deepcopy(capability())
    expired["expires_at"] = "2026-08-07T11:30:00Z"
    assert "expired" in " ".join(validate_control_document("capability", expired, now=NOW))
    networked = deepcopy(capability())
    networked["network"]["destinations"] = ["https://example.com"]
    assert "DENY mode" in " ".join(validate_control_document("capability", networked, now=NOW))
    for path in ["candidates/new.json", "artifacts/results/result.json", "data/ledger/events.jsonl", "../outside"]:
        invalid = deepcopy(capability())
        invalid["write_paths"] = [path]
        assert validate_control_document("capability", invalid, now=NOW)
    for path in ["C:/outside", "/etc/passwd", "\\\\server\\share"]:
        invalid = deepcopy(capability())
        invalid["read_paths"] = [path]
        assert "workspace-relative" in " ".join(validate_control_document("capability", invalid, now=NOW))


def test_agent_run_cannot_claim_release_or_write_canonical_state():
    base = {
        "schema_version": "1.0.0", "run_id": "RUN-000001", "task_id": "TASK-000001", "capability_id": "CAP-000001",
        "actor": {"type": "AGENT", "id": "build-1", "role": "BUILD"}, "status": "REVIEW_REQUIRED",
        "prompt": {"id": "build", "version": "1", "sha256": HASH},
        "model": {"provider": "local", "id": "test", "version": "1"}, "source_commit": "a" * 40,
        "input_hashes": [HASH], "output_hashes": [HASH], "started_at": "2026-08-07T11:00:00Z", "finished_at": "2026-08-07T11:10:00Z",
        "canonical_write_performed": False,
    }
    assert validate_control_document("run", base) == []
    released = deepcopy(base)
    released["status"] = "RELEASED"
    assert validate_control_document("run", released)
    wrote = deepcopy(base)
    wrote["canonical_write_performed"] = True
    assert validate_control_document("run", wrote)


def test_promotion_requires_a_distinct_human_reviewer():
    assert validate_control_document("promotion", promotion()) == []
    self_approved = deepcopy(promotion())
    self_approved["proposed_by"] = {"type": "HUMAN", "id": "reviewer-1"}
    assert "cannot approve" in " ".join(validate_control_document("promotion", self_approved))
    agent_review = deepcopy(promotion())
    agent_review["reviewed_by"] = {"type": "AGENT", "id": "reviewer-2"}
    assert validate_control_document("promotion", agent_review)


def test_evidence_bundle_digest_is_content_addressed():
    evidence = {
        "schema_version": "1.0.0", "bundle_id": "BUNDLE-000001", "task_id": "TASK-000001", "run_ids": ["RUN-000001"],
        "source_commit": "a" * 40,
        "environment": {"os": "test", "architecture": "x86_64", "python": "3.12", "node": "22", "dependency_lock_sha256": HASH},
        "artifacts": [{"path": "work/result.json", "media_type": "application/json", "sha256": HASH, "bytes": 42}],
        "gate_results": [{"gate": "TESTS", "status": "PASS", "evidence": [HASH]}],
        "limitations": ["Synthetic fixture only."], "created_at": "2026-08-07T12:00:00Z",
    }
    canonical = json.dumps(evidence, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    evidence["bundle_digest"] = f"sha256:{sha256(canonical).hexdigest()}"
    assert validate_control_document("evidence", evidence) == []
    evidence["artifacts"][0]["bytes"] = 43
    assert "does not match" in " ".join(validate_control_document("evidence", evidence))
