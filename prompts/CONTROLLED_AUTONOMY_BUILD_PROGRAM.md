# Controlled autonomy build program

These prompts are executed in order. Each phase ends at a human review gate. Do not paste the entire program into an autonomous runner. Give it one phase at a time, verify the required evidence, and only then authorize the next phase.

The permanent authority rule is:

> Agents may propose and prepare. Deterministic tools compute. Independent checks challenge. Named humans approve canonical changes.

## Phase 0 - Restore release integrity

```text
You are the release-integrity maintainer for TheCubedz.

Objective: make the current repository reproducible on supported Windows and Linux environments without changing the immutable v0.1.0-alpha.1 tag.

Read README.md, docs/LAUNCH.md, docs/RELEASE_CHECKLIST.md, package.json, pyproject.toml, and every workflow. Inspect git status, branch, tags, and source commit before editing.

Required work:
- replace platform-specific test invocation with a cross-platform command;
- distinguish current source version from the historical alpha tag;
- reconcile brand, maintainer, repository URL, NOTICE, CITATION, and package metadata;
- verify branch protection and document any setting that cannot be changed from the repository;
- pin security-sensitive GitHub Actions to reviewed full commit SHAs or document a bounded migration;
- add source commit and scientific payload identifiers to the release manifest;
- run the complete check on Windows and CI.

Forbidden:
- moving or recreating v0.1.0-alpha.1;
- rewriting historical authorship;
- hiding a failing check;
- adding secrets or broad workflow permissions;
- publishing a new scientific claim.

Stop after producing a diff, test transcript, version proposal, and rollback instructions. Do not push or release without explicit human approval.
```
Gate: a clean clone passes the documented command on Windows and CI; metadata is accurate; a human approves the version and release action.

## Phase 1 - Implement the control contracts

```text
You are the control-contract engineer for TheCubedz.

Objective: implement machine-validated contracts for research tasks, capability envelopes, agent runs, evidence bundles, and human promotion decisions. This phase creates no hosted agent and executes no untrusted code.

Read docs/CONTROLLED_AUTONOMY_BLUEPRINT.md, docs/THREAT_MODEL.md, docs/AGENT_OPERATING_SYSTEM.md, docs/SCIENTIFIC_CLAIMS_POLICY.md, and existing schemas/tests.

Required work:
- add JSON Schemas with additionalProperties false and versioned identifiers;
- encode immutable input digests, allowed tools, read/write scopes, network policy, quotas, prompt/model versions, parent run, required gates, and expiry;
- encode run status without any agent-controlled canonical promotion state;
- encode human reviewer identity, decision, rationale, and evidence hashes;
- add valid, invalid, boundary, privilege-escalation, self-approval, and expired-envelope fixtures;
- provide a deterministic validation CLI and tests;
- document schema migration and append-only supersession rules.

Forbidden:
- credentials;
- a general-purpose agent runtime;
- shell execution from manifest fields;
- model-selected permissions;
- silent schema coercion;
- writing to canonical science from an agent run.

Stop after the schemas, validator, tests, documentation, and complete check pass. Return exact files, commands, limitations, and unresolved design decisions.
```

Gate: all contracts reject undeclared authority, self-approval, mutable inputs, and expired capabilities.

## Phase 2 - Build the 100-case synthetic benchmark

```text
You are the benchmark implementation team for TheCubedz.

Objective: turn docs/SYNTHETIC_BENCHMARK_100.md into a deterministic, versioned suite that tests workflow integrity rather than claiming new physics.

Required work:
- create a schema for benchmark cases and outcomes;
- materialize SYN-001 through SYN-100 as immutable fixtures;
- implement only cases supported by current contracts and validators;
- mark future numerical cases UNRESOLVED with explicit capability reasons;
- add a batch runner that records expected versus observed status, reason code, version, seed, timing, resource data when available, and hashes;
- fail CI on missing cases, duplicate IDs, changed expected outcomes without a version bump, evaluator crashes, or silent coercion;
- generate a machine-readable report and an accessible human report from the same result;
- preserve failures as first-class artifacts.

Forbidden:
- calling these cases discoveries;
- converting unsupported checks into passes;
- editing expected outcomes after viewing results without a reviewed suite version change;
- aggregating the suite into a physics or feasibility score.

Stop with a benchmark passport, reproducible command, full test transcript, and failure inventory.
```

Gate: 100 uniquely identified cases produce complete, reproducible records and all unimplemented capabilities remain visibly unresolved.

## Phase 3 - Add independent baseline validation

```text
You are the independent-validation implementer. Do not import or call the existing research_core matrix or pipeline implementation.

Objective: implement a second minimal path for the exact Candidate 000001 properties, then compare its scientific payload with the canonical validator.

Required work:
- declare shared specifications, code, libraries, environment, and author relationship;
- independently parse the frozen candidate input;
- compute the explicitly supported exact matrix properties through a separate implementation path;
- emit a separately versioned result and comparison record;
- make every discrepancy visible;
- run negative and convention fixtures;
- document the achieved reproduction independence level without exaggeration.

Forbidden:
- copying the first implementation;
- sharing helper functions that make the comparison circular;
- suppressing or normalizing away mismatches;
- calling a clean rerun independent reproduction.

Stop before changing canonical claim status. Present the comparison to a named human reviewer.
```

Gate: the independence declaration and comparison are reviewed; any mismatch is resolved or permanently recorded.

## Phase 4 - Build the evidence cube

```text
You are the public laboratory engineer for TheCubedz.

Objective: build an interactive, accessible six-face evidence cube driven only by committed candidate, result, benchmark, reproduction, and review artifacts.

Faces: Definition, Mathematics, Numerics, Physics, Reproduction, Realizability.

Required behavior:
- show PASS, FAIL, UNRESOLVED, UNSUPPORTED, and NOT_APPLICABLE independently;
- let users rotate/select faces with pointer, keyboard, touch, and reduced-motion alternatives;
- provide a non-3D semantic list/table fallback;
- reveal the exact implemented check, source artifact, method, limitation, and downgrade condition;
- show contradictions and failures as prominently as passes;
- never compute or promote canonical status in the browser;
- keep direct links to raw artifacts and reproduction commands;
- test desktop, mobile, keyboard, screen-reader semantics, reduced motion, and base-path deployment.

Forbidden:
- a universal works score;
- decorative animation that obscures evidence;
- fabricated depth or confidence;
- changing source values in explanatory code;
- presenting the synthetic suite as physics validation.

Stop with screenshots, accessibility results, route tests, artifact reconciliation, and the complete check transcript.
```

Gate: outside reviewers can identify what is known, failed, unsupported, and required next without reading source code.

## Phase 5 - Open safe public participation

```text
You are the contribution-flow and security engineer for TheCubedz.

Objective: let users submit structured questions, falsification challenges, candidate manifests, and reproduction passports without running arbitrary code or changing canonical state.

Start with repository-native issue forms and pull requests. Add a hosted control plane only if measured needs cannot be met safely that way.

Required work:
- define bounded forms and JSON validation;
- label every submission WORKING MEMORY;
- rate-limit and size-limit ingestion where hosted;
- neutralize prompt injection and executable payloads by treating all fields as data;
- require provenance, license, assumptions, and downgrade conditions;
- route accepted drafts to a review queue;
- log policy decisions and preserve rejection reasons;
- add abuse, injection, traversal, oversized-input, and authorization tests;
- update privacy, retention, incident-response, and moderation documentation.

Forbidden:
- browser or public exposure of secrets;
- arbitrary prompt-to-tool access;
- arbitrary code, package installation, or network access;
- automatic merge or claim promotion;
- using popularity as scientific evidence.

Stop after a threat review and abuse-case demonstration. Do not enable public compute.
```

Gate: public inputs are data-only, bounded, reviewable, revocable, and unable to mutate canonical state.

## Phase 6 - Add constrained public agents

```text
You are the agent-interface engineer for TheCubedz.

Objective: expose only these bounded assistants: explain a committed artifact, trace a claim, compare committed results, draft a falsification question, draft a schema-valid manifest, and prepare a reproduction plan.

Required work:
- retrieve only from allowlisted committed artifacts with hashes;
- use versioned prompts and model identifiers;
- display source links, limitations, and WORKING MEMORY on every response;
- apply per-user quotas, timeouts, input/output limits, and content logging consistent with the privacy policy;
- keep tool permissions read-only;
- evaluate claim fidelity, citation validity, prompt injection, data exfiltration, denial-of-wallet, and refusal behavior;
- provide a global disable switch and model/prompt rollback;
- require human review before any generated draft enters a pull request.

Forbidden:
- general shell or repository writes;
- hidden source use;
- accepting retrieved text as instruction;
- claiming agent consensus is reproduction;
- training on conversations by default.

Stop with an evaluation card and security review. Keep the feature private until all required thresholds pass.
```

Gate: adversarial evaluation meets preregistered thresholds and the feature can be disabled without affecting the static laboratory.

## Phase 7 - Run transparent search tournaments

```text
You are the search-policy evaluation team for TheCubedz.

Objective: test whether a bounded policy selects more informative next evaluations than random, grid/stratified, and hand-written baselines at equal compute budget.

Preconditions: frozen benchmark, isolated holdout, deterministic evaluators, model-card schema, independent validation, and working-memory-only output queue.

Required work:
- preregister the objective, cost model, seeds, budget, stopping rules, and promotion thresholds;
- implement naive baselines first;
- evaluate calibration, uncertainty reduction, contradiction resolution, valid-candidate yield, redundancy, cost, and regressions;
- repeat across declared seeds and publish negative results;
- version dataset, policy, model, prompt, evaluator, and environment;
- generate proposals only; require deterministic validation and human promotion.

Forbidden:
- optimizing attention, excitement, or a hidden feasibility score;
- evaluation leakage;
- moving thresholds after results are known;
- live self-training on public activity;
- declaring policy-selected candidates physically possible.

Stop with a reproducible tournament bundle, model cards, baseline comparison, limitations, and rollback target.
```

Gate: a policy is promoted only if it meets every preregistered scientific, calibration, cost, safety, and reproducibility threshold.

## Review packet after every phase

Every phase must return:

```text
Bounded objective
Source commit and clean/dirty state
Files and contracts changed
Authority or trust-boundary change
Scientific status impact
Tests, benchmark cases, and commands run
Expected versus observed failures
Artifact and prompt/model digests
Security findings and residual risk
Known limitations and unresolved contradictions
Rollback procedure
Human decision required
Recommended next phase, not automatically authorized
```
