from __future__ import annotations

import base64
from copy import deepcopy
from datetime import UTC, datetime, timedelta
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
from statistics import median
from typing import Any, Iterable

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jsonschema import Draft202012Validator, FormatChecker

from .canonical import canonical_bytes


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_FILES = {
    "measurement": "quiet-compute-measurement.schema.json",
    "passport": "quiet-compute-passport.schema.json",
    "submission": "quiet-compute-submission.schema.json",
    "job_manifest": "quiet-compute-job-manifest.schema.json",
    "signed_job": "quiet-compute-signed-job.schema.json",
    "trust_store": "quiet-compute-trust-store.schema.json",
    "worker": "quiet-compute-worker.schema.json",
    "reproduction": "quiet-compute-reproduction.schema.json",
    "signed_reproduction": "quiet-compute-signed-reproduction.schema.json",
    "reputation_event": "quiet-compute-reputation-event.schema.json",
}
ENTRYPOINTS = {
    "VALIDATE_MEASUREMENT": ("QC_VALIDATE_V1", ["research-core", "quiet", "validate-measurement", "/inputs/measurement.json"]),
    "COMPARE_MEASUREMENTS": ("QC_COMPARE_V1", ["research-core", "quiet", "compare", "/inputs/baseline.json", "/inputs/intervention.json", "/inputs/passport.json"]),
    "REPRODUCE_FROZEN_BENCHMARK": ("FROZEN_BENCHMARK_V1", ["research-core", "benchmark", "--json"]),
}
REPUTATION_WEIGHTS = {
    "VERIFIED_REPRODUCTION": 20,
    "USEFUL_NEGATIVE_RESULT": 8,
    "DISCLOSED_MISMATCH": 10,
    "COMPLETE_PROVENANCE": 5,
    "CONFIRMED_ADVERSARIAL_FINDING": 12,
    "RETRACTION": -20,
    "MISREPRESENTED_INDEPENDENCE": -30,
    "INVALID_PROVENANCE": -15,
    "DONATED_COMPUTE": 0,
    "FUNDING": 0,
}


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def load_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    if not isinstance(document, dict):
        raise ValueError("document root must be an object")
    return document


def _schema_errors(kind: str, document: dict[str, Any]) -> list[str]:
    schema = json.loads((ROOT / "src" / "core" / SCHEMA_FILES[kind]).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: [str(part) for part in item.absolute_path])
    ]


def _digest(document: dict[str, Any], field: str) -> str:
    unsigned = {key: value for key, value in document.items() if key != field}
    return f"sha256:{hashlib.sha256(canonical_bytes(unsigned)).hexdigest()}"


def _seal(document: dict[str, Any], field: str) -> dict[str, Any]:
    sealed = deepcopy(document)
    sealed.pop(field, None)
    sealed[field] = _digest(sealed, field)
    return sealed


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed.astimezone(UTC)


def _unique_errors(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def seal_measurement(document: dict[str, Any]) -> dict[str, Any]:
    return _seal(document, "measurement_digest")


def validate_measurement(document: dict[str, Any]) -> list[str]:
    errors = _schema_errors("measurement", document)
    if errors:
        return errors

    if document["measurement_digest"] != _digest(document, "measurement_digest"):
        errors.append("measurement_digest: does not match the canonical measurement payload")
    if document["kind"] == "BASELINE" and document["baseline_measurement_id"] is not None:
        errors.append("baseline_measurement_id: a baseline must not reference another baseline")
    if document["kind"] == "INTERVENTION" and document["baseline_measurement_id"] is None:
        errors.append("baseline_measurement_id: an intervention must reference its frozen baseline")
    if document["baseline_measurement_id"] == document["measurement_id"]:
        errors.append("baseline_measurement_id: a measurement cannot reference itself")

    sensor_types = {sensor["type"] for sensor in document["sensors"]}
    for required in ("ACOUSTIC", "TEMPERATURE", "POWER"):
        if required not in sensor_types:
            errors.append(f"sensors: a {required} sensor is required")
    sensor_ids = [sensor["sensor_id"] for sensor in document["sensors"]]
    if len(sensor_ids) != len(set(sensor_ids)):
        errors.append("sensors: sensor_id values must be unique")

    paths = [artifact["path"] for artifact in document["raw_artifacts"]]
    if len(paths) != len(set(paths)):
        errors.append("raw_artifacts: paths must be unique")
    for raw_path in paths:
        path = PurePosixPath(raw_path.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"raw_artifacts: unsafe workspace-relative path ({raw_path})")

    acoustic = document["observations"]["acoustic"]
    if acoustic["dba_leq"] < document["environment"]["background_dba"]:
        errors.append("observations.acoustic.dba_leq: cannot be below the declared background level")
    for name in ("water", "cost"):
        value = document["observations"][name]
        amount = value["liters" if name == "water" else "usd"]
        if value["status"] == "MEASURED" and amount is None:
            errors.append(f"observations.{name}: MEASURED requires a numeric amount")
        if value["status"] != "MEASURED" and amount is not None:
            errors.append(f"observations.{name}: an unmeasured amount must be null")
    return _unique_errors(errors)


def seal_passport(document: dict[str, Any]) -> dict[str, Any]:
    return _seal(document, "passport_digest")


def validate_passport(document: dict[str, Any]) -> list[str]:
    errors = _schema_errors("passport", document)
    if errors:
        return errors
    if document["passport_digest"] != _digest(document, "passport_digest"):
        errors.append("passport_digest: does not match the canonical passport payload")
    replication = document["replication"]
    for field in ("minimum_independent_operators", "minimum_independence_groups", "minimum_os_families", "minimum_hardware_families"):
        if replication[field] > replication["minimum_results"]:
            errors.append(f"replication.{field}: cannot exceed minimum_results")
    return errors


def seal_submission(document: dict[str, Any]) -> dict[str, Any]:
    return _seal(document, "submission_digest")


def validate_submission(document: dict[str, Any]) -> list[str]:
    errors = _schema_errors("submission", document)
    if errors:
        return errors
    errors.extend(f"measurement.{error}" for error in validate_measurement(document["measurement"]))
    available = {item["sha256"] for item in document["measurement"]["raw_artifacts"]}
    unknown = sorted(set(document["selected_artifacts"]) - available)
    if unknown:
        errors.append(f"selected_artifacts: undeclared artifact digests: {', '.join(unknown)}")
    if document["submission_digest"] != _digest(document, "submission_digest"):
        errors.append("submission_digest: does not match the canonical deliberate-submission payload")
    return errors


def _require_valid(label: str, errors: list[str]) -> None:
    if errors:
        raise ValueError(f"invalid {label}: " + "; ".join(errors))


def _nested(document: dict[str, Any], dotted: str) -> Any:
    value: Any = document
    for part in dotted.split("."):
        value = value[part]
    return value


def _relative_difference(baseline: float, observed: float) -> float:
    return abs(observed - baseline) / max(abs(baseline), 1e-12)


def _relative_change(baseline: float, observed: float) -> float:
    return (observed - baseline) / max(abs(baseline), 1e-12)


def compare_measurements(baseline: dict[str, Any], intervention: dict[str, Any], passport: dict[str, Any]) -> dict[str, Any]:
    _require_valid("baseline measurement", validate_measurement(baseline))
    _require_valid("intervention measurement", validate_measurement(intervention))
    _require_valid("comparison passport", validate_passport(passport))
    if baseline["kind"] != "BASELINE":
        raise ValueError("invalid baseline measurement: kind must be BASELINE")
    if intervention["kind"] != "INTERVENTION":
        raise ValueError("invalid intervention measurement: kind must be INTERVENTION")
    if intervention["baseline_measurement_id"] != baseline["measurement_id"]:
        raise ValueError("invalid intervention measurement: frozen baseline reference does not match")
    if baseline["passport_id"] != passport["passport_id"] or intervention["passport_id"] != passport["passport_id"]:
        raise ValueError("passport_id: both measurements must be bound to the supplied passport")
    if baseline["environment"]["boundary"] != passport["boundary"] or intervention["environment"]["boundary"] != passport["boundary"]:
        raise ValueError("boundary: measurements do not match the passport boundary")

    checks: list[dict[str, Any]] = []

    def check(identifier: str, passed: bool, observed: Any, limit: Any) -> None:
        checks.append({"id": identifier, "status": "PASS" if passed else "FAIL", "observed": observed, "limit": limit})

    match = passport["matched_workload"]
    for field in match["exact_fields"]:
        left = _nested(baseline["workload"], field)
        right = _nested(intervention["workload"], field)
        check(f"workload.exact.{field}", left == right, {"baseline": left, "intervention": right}, "EXACT")
    for field, tolerance in (
        ("throughput.value", match["max_relative_throughput_difference"]),
        ("latency_ms", match["max_relative_latency_difference"]),
        ("duration_seconds", match["max_relative_duration_difference"]),
    ):
        left = float(_nested(baseline["workload"], field))
        right = float(_nested(intervention["workload"], field))
        difference = _relative_difference(left, right)
        check(f"workload.relative.{field}", difference <= tolerance, difference, tolerance)

    environment_rule = passport["matched_environment"]
    left_microphone = baseline["environment"]["microphone"]
    right_microphone = intervention["environment"]["microphone"]
    check("environment.microphone.position", left_microphone["position"] == right_microphone["position"], {"baseline": left_microphone["position"], "intervention": right_microphone["position"]}, "EXACT")
    check("environment.microphone.orientation", left_microphone["orientation"] == right_microphone["orientation"], {"baseline": left_microphone["orientation"], "intervention": right_microphone["orientation"]}, "EXACT")
    distance_difference = abs(left_microphone["distance_m"] - right_microphone["distance_m"])
    check("environment.microphone.distance", distance_difference <= environment_rule["max_microphone_distance_difference_m"], distance_difference, environment_rule["max_microphone_distance_difference_m"])
    background_difference = abs(baseline["environment"]["background_dba"] - intervention["environment"]["background_dba"])
    check("environment.background", background_difference <= environment_rule["max_background_difference_db"], background_difference, environment_rule["max_background_difference_db"])
    for label, measurement in (("baseline", baseline), ("intervention", intervention)):
        maximum_clock_offset = max(abs(sensor["clock_offset_ms"]) for sensor in measurement["sensors"])
        check(f"environment.sensor_clock.{label}", maximum_clock_offset <= environment_rule["max_absolute_sensor_clock_offset_ms"], maximum_clock_offset, environment_rule["max_absolute_sensor_clock_offset_ms"])
        check(f"acoustic.clipping.{label}", not measurement["observations"]["acoustic"]["clipping_detected"], measurement["observations"]["acoustic"]["clipping_detected"], False)

    acoustic_rule = passport["acoustic"]
    for label, measurement in (("baseline", baseline), ("intervention", intervention)):
        separation = measurement["observations"]["acoustic"]["dba_leq"] - measurement["environment"]["background_dba"]
        check(f"acoustic.background_separation.{label}", separation >= acoustic_rule["minimum_background_separation_db"], separation, acoustic_rule["minimum_background_separation_db"])
    acoustic_improvement = baseline["observations"]["acoustic"]["dba_leq"] - intervention["observations"]["acoustic"]["dba_leq"]
    combined_uncertainty = math.hypot(baseline["observations"]["acoustic"]["uncertainty_db"], intervention["observations"]["acoustic"]["uncertainty_db"])
    conservative_improvement = acoustic_improvement - acoustic_rule["confidence_multiplier"] * combined_uncertainty
    check("acoustic.improvement", conservative_improvement >= acoustic_rule["minimum_improvement_db"], {"point_estimate_db": acoustic_improvement, "conservative_db": conservative_improvement}, acoustic_rule["minimum_improvement_db"])

    guardrails = passport["guardrails"]
    component_max = intervention["observations"]["thermal"]["component_max_c"]
    check("guardrail.thermal", component_max <= guardrails["maximum_component_temperature_c"], component_max, guardrails["maximum_component_temperature_c"])
    energy_change = _relative_change(baseline["observations"]["energy"]["joules"], intervention["observations"]["energy"]["joules"])
    check("guardrail.energy", energy_change <= guardrails["maximum_relative_energy_increase"], energy_change, guardrails["maximum_relative_energy_increase"])

    for name, amount, maximum, allow_unknown in (
        ("water", "liters", "maximum_relative_water_increase", "allow_unknown_water"),
        ("cost", "usd", "maximum_relative_cost_increase", "allow_unknown_cost"),
    ):
        left = baseline["observations"][name]
        right = intervention["observations"][name]
        if left["status"] == right["status"] == "MEASURED":
            change = _relative_change(float(left[amount]), float(right[amount]))
            check(f"guardrail.{name}", change <= guardrails[maximum], change, guardrails[maximum])
        elif left["status"] == right["status"] == "NOT_APPLICABLE":
            check(f"guardrail.{name}", True, "NOT_APPLICABLE", "MATCHED_NOT_APPLICABLE")
        else:
            allowed = guardrails[allow_unknown] and "UNKNOWN" in {left["status"], right["status"]}
            check(f"guardrail.{name}", allowed, {"baseline": left["status"], "intervention": right["status"]}, "DECLARED_AND_ALLOWED")

    reliability = intervention["observations"]["reliability"]
    check("guardrail.reliability.completed", reliability["completed"], reliability["completed"], True)
    check("guardrail.reliability.errors", reliability["errors"] <= guardrails["maximum_errors"], reliability["errors"], guardrails["maximum_errors"])
    check("guardrail.reliability.throttling", reliability["throttling_seconds"] <= guardrails["maximum_throttling_seconds"], reliability["throttling_seconds"], guardrails["maximum_throttling_seconds"])

    result = {
        "schema_version": "1.0.0",
        "baseline_measurement_id": baseline["measurement_id"],
        "intervention_measurement_id": intervention["measurement_id"],
        "passport": {"passport_id": passport["passport_id"], "version": passport["version"], "status": passport["status"], "digest": passport["passport_digest"]},
        "checks": checks,
        "metrics": {
            "acoustic_improvement_db": acoustic_improvement,
            "acoustic_conservative_improvement_db": conservative_improvement,
            "energy_relative_change": energy_change,
            "component_max_c": component_max,
        },
        "overall_status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
        "claim_boundary": "A passing comparison applies only to the declared systems, workload, environment, passport, and intervention.",
        "human_promotion_required": True,
    }
    result["comparison_digest"] = _digest(result, "comparison_digest")
    return result


def _validate_trust_store(document: dict[str, Any]) -> list[str]:
    errors = _schema_errors("trust_store", document)
    if errors:
        return errors
    ids = [item["key_id"] for item in document["keys"]]
    if len(ids) != len(set(ids)):
        errors.append("keys: key_id values must be unique")
    return errors


def _validate_worker(document: dict[str, Any]) -> list[str]:
    return _schema_errors("worker", document)


def signed_job_payload(envelope: dict[str, Any]) -> bytes:
    return canonical_bytes({
        "schema_version": envelope["schema_version"],
        "algorithm": envelope["algorithm"],
        "key_id": envelope["key_id"],
        "manifest": envelope["manifest"],
    })


def verify_job_envelope(
    envelope: dict[str, Any],
    trust_store: dict[str, Any],
    worker: dict[str, Any],
    *,
    now: datetime | None = None,
    seen_nonces: set[str] | None = None,
) -> dict[str, Any]:
    reasons: list[str] = []
    reasons.extend(f"ENVELOPE_SCHEMA:{error}" for error in _schema_errors("signed_job", envelope))
    if not reasons:
        reasons.extend(f"MANIFEST_SCHEMA:{error}" for error in _schema_errors("job_manifest", envelope["manifest"]))
    reasons.extend(f"TRUST_STORE:{error}" for error in _validate_trust_store(trust_store))
    reasons.extend(f"WORKER:{error}" for error in _validate_worker(worker))
    if reasons:
        return {"status": "REJECT", "reasons": reasons, "signature_verified": False, "eligibility_verified": False}

    current = (now or datetime.now(UTC)).astimezone(UTC)
    manifest = envelope["manifest"]
    key = next((item for item in trust_store["keys"] if item["key_id"] == envelope["key_id"]), None)
    signature_verified = False
    if key is None:
        reasons.append("UNKNOWN_SIGNING_KEY")
    else:
        if key["status"] != "ACTIVE":
            reasons.append("SIGNING_KEY_REVOKED")
        if not (_parse_time(key["not_before"]) <= current <= _parse_time(key["not_after"])):
            reasons.append("SIGNING_KEY_OUTSIDE_VALIDITY_WINDOW")
        try:
            public_bytes = base64.b64decode(key["public_key_base64"], validate=True)
            signature = base64.b64decode(envelope["signature"], validate=True)
            Ed25519PublicKey.from_public_bytes(public_bytes).verify(signature, signed_job_payload(envelope))
            signature_verified = True
        except (ValueError, InvalidSignature):
            reasons.append("INVALID_SIGNATURE")

    issued_at = _parse_time(manifest["issued_at"])
    expires_at = _parse_time(manifest["expires_at"])
    if expires_at <= issued_at:
        reasons.append("INVALID_JOB_VALIDITY_WINDOW")
    if current > expires_at:
        reasons.append("JOB_EXPIRED")
    if issued_at > current + timedelta(minutes=5):
        reasons.append("JOB_ISSUED_TOO_FAR_IN_FUTURE")
    if seen_nonces is not None and manifest["nonce"] in seen_nonces:
        reasons.append("REPLAYED_NONCE")
    if worker["status"] != "ACTIVE":
        reasons.append(f"WORKER_{worker['status']}")
    if envelope["key_id"] not in worker["trusted_key_ids"]:
        reasons.append("WORKER_DOES_NOT_TRUST_SIGNING_KEY")
    if manifest["operation"] not in worker["operations"]:
        reasons.append("UNSUPPORTED_OPERATION")
    expected_entrypoint = ENTRYPOINTS[manifest["operation"]][0]
    if manifest["runtime"]["entrypoint_id"] != expected_entrypoint:
        reasons.append("OPERATION_ENTRYPOINT_MISMATCH")
    if manifest["runtime"]["image_digest"] not in worker["approved_runtime_digests"]:
        reasons.append("UNAPPROVED_RUNTIME_DIGEST")
    expanded_bytes = sum(item["expanded_bytes"] for item in manifest["inputs"])
    if expanded_bytes > manifest["resources"]["disk_mb"] * 1024 * 1024:
        reasons.append("EXPANDED_INPUT_EXCEEDS_DISK_QUOTA")
    if any(item["expanded_bytes"] < item["bytes"] for item in manifest["inputs"]):
        reasons.append("EXPANDED_INPUT_SMALLER_THAN_TRANSFER")
    if any(item["expanded_bytes"] / item["bytes"] > 100 for item in manifest["inputs"]):
        reasons.append("INPUT_EXPANSION_RATIO_EXCEEDS_LIMIT")
    for field, requested in manifest["resources"].items():
        if requested > worker["capacity"][field]:
            reasons.append(f"RESOURCE_EXCEEDS_CAPACITY:{field}")
    attested_at = _parse_time(worker["sandbox_attestation"]["attested_at"])
    if attested_at > current + timedelta(minutes=5):
        reasons.append("SANDBOX_ATTESTATION_FROM_FUTURE")
    if current - attested_at > timedelta(days=90):
        reasons.append("SANDBOX_ATTESTATION_STALE")

    accepted = not reasons and signature_verified
    if accepted and seen_nonces is not None:
        seen_nonces.add(manifest["nonce"])
    return {
        "status": "ACCEPT" if accepted else "REJECT",
        "reasons": reasons,
        "signature_verified": signature_verified,
        "eligibility_verified": accepted,
        "job_id": manifest["job_id"],
        "worker_id": worker["worker_id"],
        "manifest_digest": f"sha256:{hashlib.sha256(canonical_bytes(manifest)).hexdigest()}",
    }


def verify_and_claim_job_envelope(
    envelope: dict[str, Any],
    trust_store: dict[str, Any],
    worker: dict[str, Any],
    replay_directory: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    manifest = envelope.get("manifest") if isinstance(envelope, dict) else None
    nonce = manifest.get("nonce") if isinstance(manifest, dict) else None
    if not isinstance(nonce, str):
        return verify_job_envelope(envelope, trust_store, worker, now=now)
    nonce_key = hashlib.sha256(nonce.encode("utf-8")).hexdigest()
    record_path = replay_directory / f"{nonce_key}.json"
    seen = {nonce} if record_path.exists() else set()
    decision = verify_job_envelope(envelope, trust_store, worker, now=now, seen_nonces=seen)
    if decision["status"] != "ACCEPT":
        return decision

    replay_directory.mkdir(parents=True, exist_ok=True)
    record = {
        "schema_version": "1.0.0",
        "job_id": manifest["job_id"],
        "worker_id": worker["worker_id"],
        "nonce_sha256": f"sha256:{nonce_key}",
        "manifest_digest": decision["manifest_digest"],
        "claimed_at": (now or datetime.now(UTC)).astimezone(UTC).isoformat().replace("+00:00", "Z"),
    }
    try:
        with record_path.open("x", encoding="utf-8") as handle:
            json.dump(record, handle, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            handle.write("\n")
    except FileExistsError:
        return {**decision, "status": "REJECT", "eligibility_verified": False, "reasons": ["REPLAYED_NONCE"]}
    return {**decision, "replay_claim": record_path.name}


def build_isolated_execution_plan(manifest: dict[str, Any], worker: dict[str, Any]) -> dict[str, Any]:
    _require_valid("job manifest", _schema_errors("job_manifest", manifest))
    _require_valid("worker profile", _validate_worker(worker))
    if worker["status"] != "ACTIVE":
        raise ValueError("worker is not active")
    if manifest["operation"] not in worker["operations"]:
        raise ValueError("worker does not support the requested operation")
    if manifest["runtime"]["image_digest"] not in worker["approved_runtime_digests"]:
        raise ValueError("worker has not approved the immutable runtime digest")
    for field, requested in manifest["resources"].items():
        if requested > worker["capacity"][field]:
            raise ValueError(f"requested {field} exceeds worker capacity")
    expected_entrypoint, argv = ENTRYPOINTS[manifest["operation"]]
    if manifest["runtime"]["entrypoint_id"] != expected_entrypoint:
        raise ValueError("operation and entrypoint do not match")
    return {
        "status": "PLAN_ONLY",
        "public_execution_enabled": False,
        "job_id": manifest["job_id"],
        "worker_id": worker["worker_id"],
        "immutable_image_digest": manifest["runtime"]["image_digest"],
        "argv": argv,
        "sandbox": {
            "rootless": True,
            "network": "NONE",
            "root_filesystem": "READ_ONLY",
            "inputs": "READ_ONLY",
            "scratch": "EPHEMERAL_TMPFS_NOEXEC_NOSUID_NODEV",
            "user": "65532:65532",
            "capabilities": [],
            "privileged": False,
            "no_new_privileges": True,
            "host_mounts": [],
            "limits": manifest["resources"],
        },
        "required_external_attestation": worker["sandbox_attestation"]["attestation_digest"],
        "execution_boundary": "A reviewed sandbox adapter must enforce this plan. This library does not execute the job.",
    }


def allocate_replications(
    envelope: dict[str, Any],
    trust_store: dict[str, Any],
    workers: list[dict[str, Any]],
    replication_requirements: dict[str, int],
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    requested = replication_requirements["minimum_results"]
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for worker in sorted(workers, key=lambda item: item.get("worker_id", "")):
        decision = verify_job_envelope(envelope, trust_store, worker, now=now)
        if decision["status"] == "ACCEPT":
            accepted.append(worker)
        else:
            rejected.append({"worker_id": worker.get("worker_id", "UNKNOWN"), "reasons": decision["reasons"]})

    selected: list[dict[str, Any]] = []
    remaining = accepted[:]
    dimensions = ("independence_group", "operator_id", "os_family", "hardware_family", "sensor_stack")
    while remaining and len(selected) < requested:
        used = {dimension: {item[dimension] for item in selected} for dimension in dimensions}
        scored = [
            (tuple(int(worker[dimension] not in used[dimension]) for dimension in dimensions), worker)
            for worker in remaining
        ]
        best_score = max(score for score, _ in scored)
        chosen = next(worker for score, worker in scored if score == best_score)
        selected.append(chosen)
        remaining.remove(chosen)

    diversity = {
        "results": len(selected),
        "independent_operators": len({item["operator_id"] for item in selected}),
        "independence_groups": len({item["independence_group"] for item in selected}),
        "os_families": len({item["os_family"] for item in selected}),
        "hardware_families": len({item["hardware_family"] for item in selected}),
        "sensor_stacks": len({item["sensor_stack"] for item in selected}),
    }
    requirement_map = {
        "results": "minimum_results",
        "independent_operators": "minimum_independent_operators",
        "independence_groups": "minimum_independence_groups",
        "os_families": "minimum_os_families",
        "hardware_families": "minimum_hardware_families",
    }
    unmet = [name for name, requirement in requirement_map.items() if diversity[name] < replication_requirements[requirement]]
    result = {
        "status": "ALLOCATED" if not unmet else "INSUFFICIENT_CAPACITY",
        "job_id": envelope.get("manifest", {}).get("job_id", "UNKNOWN"),
        "assignments": [item["worker_id"] for item in selected],
        "diversity": diversity,
        "unmet_requirements": unmet,
        "rejected_workers": rejected,
        "selection_rule": "Maximize independence group, operator, OS, hardware, and sensor diversity in that order; break ties by worker_id.",
    }
    result["allocation_digest"] = _digest(result, "allocation_digest")
    return result


def validate_reproduction(document: dict[str, Any]) -> list[str]:
    errors = _schema_errors("reproduction", document)
    if errors:
        return errors
    if document["result_digest"] != _digest(document, "result_digest"):
        errors.append("result_digest: does not match the canonical reproduction payload")
    return errors


def seal_reproduction(document: dict[str, Any]) -> dict[str, Any]:
    return _seal(document, "result_digest")


def verify_reproduction_envelope(envelope: dict[str, Any], worker: dict[str, Any]) -> list[str]:
    errors = _schema_errors("signed_reproduction", envelope)
    errors.extend(f"worker:{error}" for error in _validate_worker(worker))
    if errors:
        return errors
    result = envelope["result"]
    errors.extend(f"result:{error}" for error in validate_reproduction(result))
    if envelope["worker_id"] != worker["worker_id"] or result.get("worker_id") != worker["worker_id"]:
        errors.append("worker_id: envelope, result, and registered worker must match")
    if worker["status"] != "ACTIVE":
        errors.append(f"worker.status: {worker['status']} results are not eligible for consensus")
    try:
        public_bytes = base64.b64decode(worker["result_public_key_base64"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        Ed25519PublicKey.from_public_bytes(public_bytes).verify(signature, canonical_bytes(result))
    except (ValueError, InvalidSignature):
        errors.append("signature: invalid reproduction signature")
    return errors


def evaluate_consensus(signed_results: list[dict[str, Any]], workers: list[dict[str, Any]], passport: dict[str, Any]) -> dict[str, Any]:
    _require_valid("comparison passport", validate_passport(passport))
    if not signed_results:
        raise ValueError("at least one reproduction result is required")
    worker_by_id: dict[str, dict[str, Any]] = {}
    for worker in workers:
        _require_valid("worker profile", _validate_worker(worker))
        if worker["worker_id"] in worker_by_id:
            raise ValueError(f"duplicate worker profile: {worker['worker_id']}")
        worker_by_id[worker["worker_id"]] = worker
    results: list[dict[str, Any]] = []
    signature_reasons: list[str] = []
    for index, envelope in enumerate(signed_results):
        envelope_schema_errors = _schema_errors("signed_reproduction", envelope)
        if envelope_schema_errors:
            raise ValueError(f"invalid signed reproduction {index}: {'; '.join(envelope_schema_errors)}")
        worker_id = envelope.get("worker_id")
        worker = worker_by_id.get(worker_id)
        if worker is None:
            raise ValueError(f"signed reproduction {index}: unknown worker_id {worker_id}")
        signature_errors = verify_reproduction_envelope(envelope, worker)
        signature_reasons.extend(f"SIGNED_RESULT_INVALID:{worker_id}:{error}" for error in signature_errors)
        results.append(envelope["result"])

    reasons: list[str] = signature_reasons
    for field in ("job_id", "measurement_id", "input_digest", "passport_id"):
        values = {item[field] for item in results}
        if len(values) != 1:
            reasons.append(f"CONTRACT_MISMATCH:{field}")
    if {item["passport_id"] for item in results} != {passport["passport_id"]}:
        reasons.append("CONTRACT_MISMATCH:passport_id")

    replication = passport["replication"]
    diversity = {
        "results": len(results),
        "independent_operators": len({item["operator_id"] for item in results}),
        "independence_groups": len({item["independence_group"] for item in results}),
        "os_families": len({item["os_family"] for item in results}),
        "hardware_families": len({item["hardware_family"] for item in results}),
    }
    for observed, required in (
        ("results", "minimum_results"),
        ("independent_operators", "minimum_independent_operators"),
        ("independence_groups", "minimum_independence_groups"),
        ("os_families", "minimum_os_families"),
        ("hardware_families", "minimum_hardware_families"),
    ):
        if diversity[observed] < replication[required]:
            reasons.append(f"INSUFFICIENT_DIVERSITY:{observed}")

    if any(not item["provenance_complete"] for item in results):
        reasons.append("INCOMPLETE_PROVENANCE")
    if any(item["comparison_status"] != "PASS" for item in results):
        reasons.append("NOT_EVERY_COMPARISON_PASSED")
    if any(not item["guardrails_all_pass"] for item in results):
        reasons.append("NOT_EVERY_GUARDRAIL_PASSED")

    spreads: dict[str, dict[str, float]] = {}
    for metric, tolerance in passport["consensus"]["metric_tolerances"].items():
        values = [float(item["metrics"][metric]) for item in results]
        spread = max(values) - min(values)
        spreads[metric] = {"minimum": min(values), "median": median(values), "maximum": max(values), "spread": spread, "tolerance": tolerance}
        if spread > tolerance:
            reasons.append(f"TOLERANCE_MISMATCH:{metric}")

    if any(reason.startswith("INSUFFICIENT_DIVERSITY") for reason in reasons):
        status = "INSUFFICIENT_EVIDENCE"
    elif reasons:
        status = "MISMATCH"
    else:
        status = "CONSENSUS"
    output = {
        "schema_version": "1.0.0",
        "status": status,
        "passport_id": passport["passport_id"],
        "result_ids": [item["result_id"] for item in sorted(results, key=lambda item: item["result_id"])],
        "diversity": diversity,
        "metric_spreads": spreads,
        "reasons": _unique_errors(reasons),
        "decision_rule": "Every contract, guardrail, independence minimum, signature, provenance requirement, and numeric tolerance must pass; majority voting is not used.",
        "human_promotion_required": True,
    }
    output["consensus_digest"] = _digest(output, "consensus_digest")
    return output


def score_evidence_reputation(events: list[dict[str, Any]]) -> dict[str, Any]:
    seen_ids: set[str] = set()
    seen_evidence_events: set[tuple[str, str]] = set()
    contributions: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    totals: dict[str, int] = {}
    for index, event in enumerate(events):
        errors = _schema_errors("reputation_event", event)
        if errors:
            raise ValueError(f"invalid reputation event {index}: {'; '.join(errors)}")
        if event["event_id"] in seen_ids:
            raise ValueError(f"duplicate reputation event_id: {event['event_id']}")
        seen_ids.add(event["event_id"])
        key = (event["type"], event["evidence_digest"])
        if key in seen_evidence_events:
            excluded.append({"event_id": event["event_id"], "reason": "DUPLICATE_EVIDENCE_EVENT"})
            continue
        seen_evidence_events.add(key)
        if not event["verified"]:
            excluded.append({"event_id": event["event_id"], "reason": "UNVERIFIED"})
            continue
        weight = REPUTATION_WEIGHTS[event["type"]]
        totals[event["contributor_id"]] = totals.get(event["contributor_id"], 0) + weight
        contributions.append({"event_id": event["event_id"], "contributor_id": event["contributor_id"], "type": event["type"], "weight": weight})

    scores = []
    for contributor_id, raw_score in sorted(totals.items()):
        score = min(100, max(0, raw_score))
        tier = "ROBUST_EVIDENCE_CONTRIBUTOR" if score >= 60 else "REPRODUCER" if score >= 30 else "CONTRIBUTOR" if score >= 10 else "NEW"
        scores.append({"contributor_id": contributor_id, "score": score, "tier": tier, "scientific_authority": False})
    output = {
        "schema_version": "1.0.0",
        "scores": scores,
        "counted_events": contributions,
        "excluded_events": excluded,
        "policy": "Only verified evidence quality affects reputation. Funding and donated compute have zero weight. Reputation never grants scientific authority.",
    }
    output["reputation_digest"] = _digest(output, "reputation_digest")
    return output
