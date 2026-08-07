# Federated reproduction protocol

## Purpose

Allow outside contributors to reproduce results without granting a central service authority over their environment or automatically trusting returned files.

## V0

A contributor runs the repository locally and submits a reproduction record through a pull request or issue. No public remote code execution exists.

## Minimum reproduction record

```json
{
  "reproduction_id": "REPRODUCTION-...",
  "candidate_id": "CANDIDATE-000001",
  "source_result_id": "RESULT-...",
  "contributor": "...",
  "independence": {
    "separate_environment": true,
    "separate_implementation": false,
    "separate_solver": false
  },
  "environment": {
    "operating_system": "...",
    "architecture": "...",
    "python": "...",
    "source_commit": "..."
  },
  "command": "...",
  "observed_digest": "sha256:...",
  "comparison": "MATCH | MISMATCH | PARTIAL",
  "discrepancies": [],
  "artifacts": []
}
```

## Independence levels

| Level | Meaning |
|---|---|
| R0 | Same implementation, same environment, repeated run |
| R1 | Same implementation, clean separate environment |
| R2 | Same method, independent implementation |
| R3 | Different validated method or solver |
| R4 | Independent experimental observation |

R0 and R1 improve software confidence. R2 and R3 provide stronger scientific reproduction. R4 applies only to physical predictions.

## Future signed bundle

```text
job-manifest.json
candidate.json
validator-manifest.json
result.json
stdout.log
stderr.log
environment.json
artifacts/*
checksums.txt
attestation.sig
```

A central verifier should check signatures, hashes, schema conformance, allowed validator identity, resource envelope, and result comparison. It should not automatically promote scientific status.
