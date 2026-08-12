from __future__ import annotations

import base64
from copy import deepcopy
from datetime import UTC, datetime
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from research_core.canonical import canonical_bytes
from research_core.cli import main
from research_core.quiet_compute import (
    allocate_replications,
    build_isolated_execution_plan,
    compare_measurements,
    evaluate_consensus,
    score_evidence_reputation,
    seal_measurement,
    seal_passport,
    seal_reproduction,
    seal_submission,
    signed_job_payload,
    validate_measurement,
    validate_passport,
    validate_submission,
    verify_and_claim_job_envelope,
    verify_job_envelope,
)


HASH = "sha256:" + "a" * 64
IMAGE = "sha256:" + "b" * 64
ATTESTATION = "sha256:" + "c" * 64
NOW = datetime(2026, 8, 12, 12, 0, tzinfo=UTC)
ROOT = Path(__file__).resolve().parents[1]


def passport():
    return seal_passport({
        "schema_version": "1.0.0",
        "passport_id": "QC-PASSPORT-000001",
        "version": "1.0.0",
        "challenge_id": "CHALLENGE-QUIET-000001",
        "status": "DRAFT",
        "boundary": "SERVER",
        "matched_workload": {
            "exact_fields": ["workload_id", "version", "input_digest", "command_digest", "throughput.unit", "service_target.metric", "service_target.target", "service_target.unit"],
            "max_relative_throughput_difference": 0.02,
            "max_relative_latency_difference": 0.05,
            "max_relative_duration_difference": 0.05,
        },
        "matched_environment": {"require_same_microphone_position": True, "require_same_microphone_orientation": True, "max_microphone_distance_difference_m": 0.02, "max_background_difference_db": 3.0, "max_absolute_sensor_clock_offset_ms": 100.0},
        "acoustic": {"minimum_improvement_db": 3.0, "confidence_multiplier": 2.0, "minimum_background_separation_db": 6.0},
        "guardrails": {
            "maximum_component_temperature_c": 85.0,
            "maximum_relative_energy_increase": 0.05,
            "maximum_relative_water_increase": 0.05,
            "allow_unknown_water": False,
            "maximum_errors": 0,
            "maximum_throttling_seconds": 0,
            "maximum_relative_cost_increase": 0.10,
            "allow_unknown_cost": False,
        },
        "replication": {
            "minimum_results": 3,
            "minimum_independent_operators": 3,
            "minimum_independence_groups": 3,
            "minimum_os_families": 2,
            "minimum_hardware_families": 2,
        },
        "consensus": {
            "require_every_guardrail_pass": True,
            "metric_tolerances": {"acoustic_improvement_db": 0.8, "energy_relative_change": 0.03, "component_max_c": 2.0},
        },
        "review": {"created_by": "ChefMrFrizzle", "created_at": "2026-08-12T10:00:00Z", "human_promotion_required": True},
    })


def measurement(*, identifier="QC-MEAS-000001", kind="BASELINE", baseline_id=None, dba=72.0, energy=100000.0, throughput=100.0, latency=10.0, component_max=75.0, background=45.0):
    return seal_measurement({
        "schema_version": "1.0.0",
        "measurement_id": identifier,
        "challenge_id": "CHALLENGE-QUIET-000001",
        "kind": kind,
        "passport_id": "QC-PASSPORT-000001",
        "baseline_measurement_id": baseline_id,
        "operator": {"operator_id": "operator-one", "independence_group": "group-one", "conflict_of_interest": "No financial conflict declared."},
        "system": {
            "system_id": "server-one",
            "hardware_family": "x86-reference",
            "cpu": "Reference CPU",
            "accelerators": [],
            "memory_gb": 64,
            "os": {"family": "LINUX", "version": "test", "architecture": "x86_64"},
            "cooling": {"primary_path": "AIR", "fan_control": "Automatic firmware curve", "facility_boundary": "One server at one metre; facility cooling is reported separately."},
        },
        "workload": {
            "workload_id": "qc-reference-workload",
            "version": "1.0.0",
            "input_digest": HASH,
            "command_digest": "sha256:" + "d" * 64,
            "duration_seconds": 600,
            "throughput": {"value": throughput, "unit": "jobs/s"},
            "latency_ms": latency,
            "service_target": {"metric": "minimum-throughput", "target": 95, "unit": "jobs/s"},
        },
        "environment": {"boundary": "SERVER", "description": "Synthetic contract fixture in a declared test room.", "microphone": {"distance_m": 1.0, "position": "Front-centre at server midline", "orientation": "Normal incidence toward the server"}, "background_dba": background},
        "sensors": [
            {"sensor_id": "sound-1", "type": "ACOUSTIC", "model": "Test class-1 meter", "calibration_id": "CAL-SOUND-1", "calibrated_at": "2026-08-01T00:00:00Z", "sampling_hz": 48000, "clock_offset_ms": 2},
            {"sensor_id": "temp-1", "type": "TEMPERATURE", "model": "Test thermocouple", "calibration_id": "CAL-TEMP-1", "calibrated_at": "2026-08-01T00:00:00Z", "sampling_hz": 1, "clock_offset_ms": 4},
            {"sensor_id": "power-1", "type": "POWER", "model": "Test power meter", "calibration_id": "CAL-POWER-1", "calibrated_at": "2026-08-01T00:00:00Z", "sampling_hz": 1, "clock_offset_ms": 3},
        ],
        "observations": {
            "acoustic": {"dba_leq": dba, "uncertainty_db": 0.3, "spectrum_digest": "sha256:" + "e" * 64, "clipping_detected": False},
            "thermal": {"inlet_c": 22, "outlet_c": 31, "component_max_c": component_max, "uncertainty_c": 0.5},
            "energy": {"joules": energy, "uncertainty_percent": 1.0},
            "water": {"status": "NOT_APPLICABLE", "liters": None},
            "reliability": {"completed": True, "errors": 0, "throttling_seconds": 0},
            "cost": {"status": "MEASURED", "usd": 1.0},
        },
        "raw_artifacts": [
            {"path": "raw/sound.csv", "media_type": "text/csv", "sha256": "sha256:" + "1" * 64, "bytes": 1000},
            {"path": "raw/thermal.csv", "media_type": "text/csv", "sha256": "sha256:" + "2" * 64, "bytes": 1000},
            {"path": "raw/power.csv", "media_type": "text/csv", "sha256": "sha256:" + "3" * 64, "bytes": 1000},
        ],
        "provenance": {"source_commit": "f" * 40, "software_version": "0.3.0", "commands": ["research-core quiet validate-measurement measurement.json"], "recorded_at": "2026-08-12T10:00:00Z"},
        "publication": {"scope": "PUBLIC_RAW_ARTIFACTS", "contains_personal_data": False, "contains_secrets": False, "commercial_use": "SEPARATE_AGREEMENT_REQUIRED"},
    })


def intervention(**overrides):
    values = {"identifier": "QC-MEAS-000002", "kind": "INTERVENTION", "baseline_id": "QC-MEAS-000001", "dba": 67.0, "energy": 102000.0, "component_max": 76.0}
    values.update(overrides)
    result = measurement(**values)
    result["operator"] = {"operator_id": "operator-one", "independence_group": "group-one", "conflict_of_interest": "Operator designed the intervention."}
    return seal_measurement(result)


def key_material():
    private_key = Ed25519PrivateKey.generate()
    public = private_key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    trust = {
        "schema_version": "1.0.0",
        "keys": [{"key_id": "QC-KEY-project-1", "algorithm": "Ed25519", "public_key_base64": base64.b64encode(public).decode(), "status": "ACTIVE", "not_before": "2026-08-01T00:00:00Z", "not_after": "2027-08-01T00:00:00Z"}],
    }
    return private_key, trust


def manifest():
    return {
        "schema_version": "1.0.0",
        "job_id": "QC-JOB-000001",
        "task_id": "TASK-000001",
        "challenge_id": "CHALLENGE-QUIET-000001",
        "operation": "VALIDATE_MEASUREMENT",
        "issued_at": "2026-08-12T11:00:00Z",
        "expires_at": "2026-08-12T13:00:00Z",
        "nonce": "abcdefghijklmnopqrstuv",
        "runtime": {"image_digest": IMAGE, "entrypoint_id": "QC_VALIDATE_V1"},
        "inputs": [{"name": "measurement.json", "sha256": HASH, "bytes": 1000, "expanded_bytes": 1000, "media_type": "application/json"}],
        "resources": {"cpu_cores": 1, "memory_mb": 512, "disk_mb": 128, "wall_seconds": 300, "output_mb": 8, "processes": 4, "gpu_count": 0},
        "isolation": {"network": "DENY", "rootless": True, "read_only_root": True, "read_only_inputs": True, "ephemeral_scratch": True, "privileged": False, "host_mounts": [], "capabilities": []},
    }


def envelope(private_key, document=None):
    document = document or manifest()
    unsigned = {"schema_version": "1.0.0", "algorithm": "Ed25519", "key_id": "QC-KEY-project-1", "manifest": document}
    return {**unsigned, "signature": base64.b64encode(private_key.sign(signed_job_payload(unsigned))).decode()}


def worker(number=1, *, operator=None, group=None, os_family="LINUX", hardware="x86-reference", sensor="sensor-a"):
    result_public = result_key(number).public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return {
        "schema_version": "1.0.0",
        "worker_id": f"QC-WORKER-{number:06d}",
        "operator_id": operator or f"operator-{number}",
        "independence_group": group or f"group-{number}",
        "status": "ACTIVE",
        "os_family": os_family,
        "hardware_family": hardware,
        "sensor_stack": sensor,
        "operations": ["VALIDATE_MEASUREMENT", "COMPARE_MEASUREMENTS", "REPRODUCE_FROZEN_BENCHMARK"],
        "trusted_key_ids": ["QC-KEY-project-1"],
        "approved_runtime_digests": [IMAGE],
        "result_public_key_base64": base64.b64encode(result_public).decode(),
        "capacity": {"cpu_cores": 8, "memory_mb": 16384, "disk_mb": 10000, "wall_seconds": 3600, "output_mb": 100, "processes": 32, "gpu_count": 1},
        "sandbox_attestation": {"runtime": "ROOTLESS_DOCKER", "rootless": True, "network_deny_enforced": True, "read_only_root_enforced": True, "no_new_privileges": True, "capabilities_dropped": True, "attested_at": "2026-08-10T00:00:00Z", "attestation_digest": ATTESTATION},
    }


def result_key(number):
    return Ed25519PrivateKey.from_private_bytes(bytes([number]) * 32)


def reproduction(number, *, acoustic=4.5, energy=0.02, temperature=76.0, operator=None, group=None, os_family="LINUX", hardware="x86-reference"):
    return seal_reproduction({
        "schema_version": "1.0.0",
        "result_id": f"QC-REPRO-{number:06d}",
        "job_id": "QC-JOB-000001",
        "measurement_id": "QC-MEAS-000002",
        "input_digest": HASH,
        "passport_id": "QC-PASSPORT-000001",
        "operator_id": operator or f"operator-{number}",
        "independence_group": group or f"group-{number}",
        "worker_id": f"QC-WORKER-{number:06d}",
        "os_family": os_family,
        "hardware_family": hardware,
        "comparison_status": "PASS",
        "guardrails_all_pass": True,
        "metrics": {"acoustic_improvement_db": acoustic, "energy_relative_change": energy, "component_max_c": temperature},
        "provenance_complete": True,
    })


def signed_reproduction(number, **overrides):
    result = reproduction(number, **overrides)
    return {"schema_version": "1.0.0", "algorithm": "Ed25519", "worker_id": result["worker_id"], "result": result, "signature": base64.b64encode(result_key(number).sign(canonical_bytes(result))).decode()}


def test_measurement_and_deliberate_submission_are_content_addressed():
    baseline = measurement()
    assert validate_measurement(baseline) == []
    tampered = deepcopy(baseline)
    tampered["observations"]["energy"]["joules"] += 1
    assert "does not match" in " ".join(validate_measurement(tampered))
    unsafe = deepcopy(baseline)
    unsafe["raw_artifacts"][0]["path"] = "../secret.txt"
    unsafe = seal_measurement(unsafe)
    assert "unsafe" in " ".join(validate_measurement(unsafe))

    submission = seal_submission({
        "schema_version": "1.0.0",
        "submission_id": "QC-SUB-000001",
        "measurement": baseline,
        "selected_artifacts": [baseline["raw_artifacts"][0]["sha256"]],
        "authorization": {"operator_confirmed": True, "automatic_upload": False, "credentials_included": False, "remote_access_granted": False, "terms_version": "1.0.0"},
        "created_at": "2026-08-12T12:00:00Z",
    })
    assert validate_submission(submission) == []
    submission["selected_artifacts"] = ["sha256:" + "9" * 64]
    submission = seal_submission(submission)
    assert "undeclared artifact" in " ".join(validate_submission(submission))


def test_comparison_requires_matched_work_and_every_guardrail():
    result = compare_measurements(measurement(), intervention(), passport())
    assert result["overall_status"] == "PASS"
    assert result["metrics"]["acoustic_conservative_improvement_db"] > 3

    throttled = intervention(throughput=80)
    assert compare_measurements(measurement(), throttled, passport())["overall_status"] == "FAIL"
    expensive_energy = intervention(energy=120000)
    assert compare_measurements(measurement(), expensive_energy, passport())["overall_status"] == "FAIL"
    hidden_by_background = intervention(background=64)
    assert compare_measurements(measurement(), hidden_by_background, passport())["overall_status"] == "FAIL"
    moved_microphone = intervention()
    moved_microphone["environment"]["microphone"]["distance_m"] = 2.0
    moved_microphone = seal_measurement(moved_microphone)
    assert compare_measurements(measurement(), moved_microphone, passport())["overall_status"] == "FAIL"
    clipped = intervention()
    clipped["observations"]["acoustic"]["clipping_detected"] = True
    clipped = seal_measurement(clipped)
    assert compare_measurements(measurement(), clipped, passport())["overall_status"] == "FAIL"
    drifting_clock = intervention()
    drifting_clock["sensors"][0]["clock_offset_ms"] = 500
    drifting_clock = seal_measurement(drifting_clock)
    assert compare_measurements(measurement(), drifting_clock, passport())["overall_status"] == "FAIL"


def test_passport_rejects_impossible_replication_requirements():
    document = passport()
    document["replication"]["minimum_os_families"] = 4
    document = seal_passport(document)
    assert "cannot exceed" in " ".join(validate_passport(document))


def test_signed_job_is_verified_against_external_trust_and_replay_state():
    private_key, trust = key_material()
    signed = envelope(private_key)
    seen = set()
    decision = verify_job_envelope(signed, trust, worker(), now=NOW, seen_nonces=seen)
    assert decision["status"] == "ACCEPT"
    assert signed["manifest"]["nonce"] in seen
    replay = verify_job_envelope(signed, trust, worker(), now=NOW, seen_nonces=seen)
    assert "REPLAYED_NONCE" in replay["reasons"]

    tampered = deepcopy(signed)
    tampered["manifest"]["resources"]["memory_mb"] = 999999
    rejected = verify_job_envelope(tampered, trust, worker(), now=NOW)
    assert rejected["status"] == "REJECT"
    assert "INVALID_SIGNATURE" in rejected["reasons"]
    assert "RESOURCE_EXCEEDS_CAPACITY:memory_mb" in rejected["reasons"]

    unknown = deepcopy(signed)
    unknown["key_id"] = "QC-KEY-attacker"
    assert "UNKNOWN_SIGNING_KEY" in verify_job_envelope(unknown, trust, worker(), now=NOW)["reasons"]


def test_job_admission_rejects_network_privilege_bombs_substitution_and_revocation():
    private_key, trust = key_material()

    networked_manifest = manifest()
    networked_manifest["isolation"]["network"] = "ALLOW"
    networked = envelope(private_key, networked_manifest)
    assert any(reason.startswith("MANIFEST_SCHEMA") for reason in verify_job_envelope(networked, trust, worker(), now=NOW)["reasons"])

    privileged_manifest = manifest()
    privileged_manifest["isolation"]["privileged"] = True
    privileged = envelope(private_key, privileged_manifest)
    assert any(reason.startswith("MANIFEST_SCHEMA") for reason in verify_job_envelope(privileged, trust, worker(), now=NOW)["reasons"])

    bomb_manifest = manifest()
    bomb_manifest["inputs"][0]["expanded_bytes"] = 200_000_000
    bomb = envelope(private_key, bomb_manifest)
    bomb_reasons = verify_job_envelope(bomb, trust, worker(), now=NOW)["reasons"]
    assert "EXPANDED_INPUT_EXCEEDS_DISK_QUOTA" in bomb_reasons
    assert "INPUT_EXPANSION_RATIO_EXCEEDS_LIMIT" in bomb_reasons

    substituted_manifest = manifest()
    substituted_manifest["runtime"]["image_digest"] = "sha256:" + "9" * 64
    substituted = envelope(private_key, substituted_manifest)
    assert "UNAPPROVED_RUNTIME_DIGEST" in verify_job_envelope(substituted, trust, worker(), now=NOW)["reasons"]

    revoked = deepcopy(trust)
    revoked["keys"][0]["status"] = "REVOKED"
    assert "SIGNING_KEY_REVOKED" in verify_job_envelope(envelope(private_key), revoked, worker(), now=NOW)["reasons"]


def test_job_plan_is_fail_closed_and_never_executes():
    plan = build_isolated_execution_plan(manifest(), worker())
    assert plan["status"] == "PLAN_ONLY"
    assert plan["public_execution_enabled"] is False
    assert plan["sandbox"]["network"] == "NONE"
    assert plan["sandbox"]["root_filesystem"] == "READ_ONLY"
    assert plan["sandbox"]["capabilities"] == []
    assert "does not execute" in plan["execution_boundary"]


def test_persistent_replay_claim_is_atomic_and_local(tmp_path):
    private_key, trust = key_material()
    signed = envelope(private_key)
    first = verify_and_claim_job_envelope(signed, trust, worker(), tmp_path / "nonces", now=NOW)
    assert first["status"] == "ACCEPT"
    assert (tmp_path / "nonces").is_dir()
    second = verify_and_claim_job_envelope(signed, trust, worker(), tmp_path / "nonces", now=NOW)
    assert second["status"] == "REJECT"
    assert second["reasons"] == ["REPLAYED_NONCE"]


def test_replication_allocator_maximizes_declared_independence():
    private_key, trust = key_material()
    workers = [
        worker(1, os_family="LINUX", hardware="x86-a", sensor="sensor-a"),
        worker(2, os_family="WINDOWS", hardware="x86-b", sensor="sensor-b"),
        worker(3, os_family="LINUX", hardware="arm-a", sensor="sensor-c"),
        worker(4, operator="operator-1", group="group-1", os_family="LINUX", hardware="x86-a", sensor="sensor-a"),
    ]
    allocation = allocate_replications(envelope(private_key), trust, workers, passport()["replication"], now=NOW)
    assert allocation["status"] == "ALLOCATED"
    assert allocation["assignments"] == ["QC-WORKER-000001", "QC-WORKER-000002", "QC-WORKER-000003"]
    assert allocation["diversity"]["independence_groups"] == 3

    collapsed = [worker(number, operator="same-operator", group="same-group") for number in range(1, 5)]
    failed = allocate_replications(envelope(private_key), trust, collapsed, passport()["replication"], now=NOW)
    assert failed["status"] == "INSUFFICIENT_CAPACITY"
    assert "independence_groups" in failed["unmet_requirements"]


def test_consensus_requires_unanimous_contract_and_tolerance_agreement():
    results = [
        signed_reproduction(1, acoustic=4.4, energy=0.02, temperature=76, os_family="LINUX", hardware="x86-a"),
        signed_reproduction(2, acoustic=4.6, energy=0.025, temperature=77, os_family="WINDOWS", hardware="x86-b"),
        signed_reproduction(3, acoustic=4.5, energy=0.021, temperature=76.5, os_family="LINUX", hardware="arm-a"),
    ]
    profiles = [worker(1, os_family="LINUX", hardware="x86-a"), worker(2, os_family="WINDOWS", hardware="x86-b"), worker(3, os_family="LINUX", hardware="arm-a")]
    consensus = evaluate_consensus(results, profiles, passport())
    assert consensus["status"] == "CONSENSUS"
    assert "majority voting is not used" in consensus["decision_rule"]

    outlier = deepcopy(results)
    outlier[2] = signed_reproduction(3, acoustic=7.0, energy=0.021, temperature=76.5, os_family="LINUX", hardware="arm-a")
    mismatch = evaluate_consensus(outlier, profiles, passport())
    assert mismatch["status"] == "MISMATCH"
    assert "TOLERANCE_MISMATCH:acoustic_improvement_db" in mismatch["reasons"]

    repeated_owner = [signed_reproduction(number, operator="same", group="same") for number in range(1, 4)]
    insufficient = evaluate_consensus(repeated_owner, profiles, passport())
    assert insufficient["status"] == "INSUFFICIENT_EVIDENCE"

    forged = deepcopy(results)
    forged[2]["result"]["metrics"]["acoustic_improvement_db"] = 4.8
    forged_result = evaluate_consensus(forged, profiles, passport())
    assert forged_result["status"] == "MISMATCH"
    assert any(reason.startswith("SIGNED_RESULT_INVALID") for reason in forged_result["reasons"])


def test_reputation_rewards_evidence_not_money_or_compute():
    events = [
        {"schema_version": "1.0.0", "event_id": "QC-REP-000001", "contributor_id": "contributor-one", "type": "VERIFIED_REPRODUCTION", "evidence_digest": "sha256:" + "1" * 64, "verified": True, "occurred_at": "2026-08-12T12:00:00Z"},
        {"schema_version": "1.0.0", "event_id": "QC-REP-000002", "contributor_id": "contributor-one", "type": "USEFUL_NEGATIVE_RESULT", "evidence_digest": "sha256:" + "2" * 64, "verified": True, "occurred_at": "2026-08-12T12:01:00Z"},
        {"schema_version": "1.0.0", "event_id": "QC-REP-000003", "contributor_id": "contributor-one", "type": "FUNDING", "evidence_digest": "sha256:" + "3" * 64, "verified": True, "occurred_at": "2026-08-12T12:02:00Z"},
        {"schema_version": "1.0.0", "event_id": "QC-REP-000004", "contributor_id": "contributor-one", "type": "DONATED_COMPUTE", "evidence_digest": "sha256:" + "4" * 64, "verified": True, "occurred_at": "2026-08-12T12:03:00Z"},
        {"schema_version": "1.0.0", "event_id": "QC-REP-000005", "contributor_id": "contributor-one", "type": "COMPLETE_PROVENANCE", "evidence_digest": "sha256:" + "5" * 64, "verified": False, "occurred_at": "2026-08-12T12:04:00Z"},
    ]
    output = score_evidence_reputation(events)
    assert output["scores"] == [{"contributor_id": "contributor-one", "score": 28, "tier": "CONTRIBUTOR", "scientific_authority": False}]
    assert [item["weight"] for item in output["counted_events"]][-2:] == [0, 0]
    assert output["excluded_events"] == [{"event_id": "QC-REP-000005", "reason": "UNVERIFIED"}]


def test_quiet_cli_validates_a_sealed_measurement(tmp_path, capsys):
    path = tmp_path / "measurement.json"
    path.write_text(json.dumps(measurement()), encoding="utf-8")
    assert main(["quiet", "validate-measurement", str(path)]) == 0
    assert "locally sealed" in capsys.readouterr().out


def test_public_templates_seal_but_remain_explicitly_non_evidentiary():
    measurement_template = json.loads((ROOT / "templates/quiet-compute/MEASUREMENT.template.json").read_text(encoding="utf-8"))
    passport_template = json.loads((ROOT / "templates/quiet-compute/PASSPORT-ROUND-0.template.json").read_text(encoding="utf-8"))
    assert validate_measurement(seal_measurement(measurement_template)) == []
    assert validate_passport(seal_passport(passport_template)) == []
    assert measurement_template["operator"]["operator_id"] == "TEMPLATE-OPERATOR"
    assert passport_template["status"] == "DRAFT"
