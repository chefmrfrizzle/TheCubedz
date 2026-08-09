#!/usr/bin/env node
import { readFile, readdir, stat, access } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const failures = [];
const notes = [];

function fail(message) { failures.push(message); }
function note(message) { notes.push(message); }
async function exists(filePath) { try { await access(filePath); return true; } catch { return false; } }

async function walk(directory) {
  const output = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (['.git', 'node_modules', 'dist', '.venv', '.pytest_cache'].includes(entry.name)) continue;
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) output.push(...await walk(absolute));
    else output.push(absolute);
  }
  return output;
}

function relative(filePath) { return path.relative(root, filePath).replaceAll(path.sep, '/'); }

async function checkRequiredFiles() {
  const required = [
    'README.md', 'CONTRIBUTING.md', 'GOVERNANCE.md', 'SECURITY.md', 'CODE_OF_CONDUCT.md', 'LICENSE', 'NOTICE', 'CHANGELOG.md', 'SUPPORT.md', 'CITATION.cff',
    'docs/SCIENTIFIC_CLAIMS_POLICY.md', 'docs/THREAT_MODEL.md', 'docs/LAUNCH.md', 'docs/SECOND_BRAIN.md', 'docs/AGENT_OPERATING_SYSTEM.md', 'docs/SCALE_ARCHITECTURE.md',
    'candidates/CANDIDATE-000001.json', 'artifacts/results/CANDIDATE-000001.result.json', 'candidates/CANDIDATE-000002.json', 'artifacts/results/CANDIDATE-000002.result.json',
    'benchmarks/BENCHMARK-000002.passport.json', 'artifacts/reproductions/CANDIDATE-000002.crosscheck.json', 'artifacts/reproductions/INTERNAL-CLEAN-CLONE-000001.json', 'artifacts/reviews/REVIEW-000002.json', 'src/core/benchmark-passport.schema.json', 'src/core/reproduction-record.schema.json', 'src/core/review-record.schema.json', 'data/ledger/events.jsonl', 'data/knowledge-graph.json',
    'data/research-program.json', 'src/core/research-program.schema.json', 'prompts/MARS_RESEARCH_PROGRAM.md', '.github/ISSUE_TEMPLATE/research-question.yml',
    '.github/workflows/ci.yml', '.github/workflows/pages.yml', '.github/workflows/codeql.yml', '.github/dependabot.yml',
  ];
  for (const item of required) if (!(await exists(path.join(root, item)))) fail(`Missing repository contract file: ${item}`);
  note(`${required.length} repository contract files checked`);
}

async function checkJsonAndJsonl(files) {
  let count = 0;
  for (const file of files.filter((item) => item.endsWith('.json'))) {
    try { JSON.parse(await readFile(file, 'utf8')); count += 1; }
    catch (error) { fail(`${relative(file)} is not valid JSON: ${error.message}`); }
  }
  for (const file of files.filter((item) => item.endsWith('.jsonl'))) {
    const lines = (await readFile(file, 'utf8')).split(/\r?\n/).filter(Boolean);
    lines.forEach((line, index) => {
      try { JSON.parse(line); count += 1; }
      catch (error) { fail(`${relative(file)} line ${index + 1} is not valid JSON: ${error.message}`); }
    });
  }
  note(`${count} JSON documents/events parsed`);
}

async function checkMarkdownLinks(files) {
  let checked = 0;
  for (const file of files.filter((item) => item.endsWith('.md'))) {
    const body = await readFile(file, 'utf8');
    const links = [...body.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)].map((match) => match[1].trim().replace(/^<|>$/g, ''));
    for (const raw of links) {
      if (!raw || /^(?:https?:|mailto:|tel:|#)/i.test(raw)) continue;
      const targetValue = raw.split('#')[0].split('?')[0];
      if (!targetValue) continue;
      const target = path.resolve(path.dirname(file), decodeURIComponent(targetValue));
      checked += 1;
      if (!(await exists(target))) fail(`${relative(file)} links to missing path: ${raw}`);
    }
  }
  note(`${checked} relative Markdown links checked`);
}

async function checkScientificConsistency() {
  const candidate = JSON.parse(await readFile(path.join(root, 'candidates/CANDIDATE-000001.json'), 'utf8'));
  const result = JSON.parse(await readFile(path.join(root, 'artifacts/results/CANDIDATE-000001.result.json'), 'utf8'));
  const coordinateCandidate = JSON.parse(await readFile(path.join(root, 'candidates/CANDIDATE-000002.json'), 'utf8'));
  const coordinateResult = JSON.parse(await readFile(path.join(root, 'artifacts/results/CANDIDATE-000002.result.json'), 'utf8'));
  const coordinateCrosscheck = JSON.parse(await readFile(path.join(root, 'artifacts/reproductions/CANDIDATE-000002.crosscheck.json'), 'utf8'));
  const baselineCrosscheck = JSON.parse(await readFile(path.join(root, 'artifacts/reproductions/CANDIDATE-000001.crosscheck.json'), 'utf8'));
  const cleanCloneReproduction = JSON.parse(await readFile(path.join(root, 'artifacts/reproductions/INTERNAL-CLEAN-CLONE-000001.json'), 'utf8'));
  const passport = JSON.parse(await readFile(path.join(root, 'benchmarks/BENCHMARK-000002.passport.json'), 'utf8'));
  const review = JSON.parse(await readFile(path.join(root, 'artifacts/reviews/REVIEW-000002.json'), 'utf8'));
  const graph = JSON.parse(await readFile(path.join(root, 'data/knowledge-graph.json'), 'utf8'));
  const benchmark = JSON.parse(await readFile(path.join(root, 'artifacts/benchmarks/synthetic-suite-v1.result.json'), 'utf8'));
  const program = JSON.parse(await readFile(path.join(root, 'data/research-program.json'), 'utf8'));
  const readme = await readFile(path.join(root, 'README.md'), 'utf8');
  if (candidate.candidate_id !== result.candidate.candidate_id) fail('Candidate and result IDs differ');
  if (coordinateCandidate.candidate_id !== coordinateResult.candidate.candidate_id || passport.candidate_id !== coordinateCandidate.candidate_id) fail('Coordinate benchmark candidate, result, and passport IDs differ');
  if (!readme.includes(result.scientific_payload_digest)) fail('README does not publish the exact scientific payload digest');
  if (!readme.includes('Novel physics claims | 0')) fail('README does not explicitly report zero novel physics claims');
  if (result.assessment.transportation_status !== 'NOT_A_TRANSPORTATION_PROPOSAL') fail('Transportation boundary changed');
  if (program.status !== 'OPEN_RESEARCH_QUESTION') fail('Research program is no longer an open question');
  const implementedChecks = result.checks.length + coordinateResult.checks.length;
  if (program.current_evidence.known_answer_examples !== 2 || program.current_evidence.implemented_checks !== implementedChecks) fail('Research program benchmark counts do not match canonical artifacts');
  if (coordinateResult.assessment.overall_status !== 'BENCHMARK_VERIFIED' || coordinateResult.assessment.transportation_status !== 'NOT_A_TRANSPORTATION_PROPOSAL') fail('Coordinate benchmark status or transportation boundary changed');
  if (coordinateCrosscheck.comparison !== 'MATCH' || coordinateCrosscheck.independence.counts_as_external_reproduction !== false) fail('Coordinate cross-check mismatch or independence overclaim');
  if (passport.scientific_review !== 'CHANGES_REQUIRED' || passport.review_history.at(-1)?.response_status !== 'ADDRESSED_AWAITING_REREVIEW' || passport.preregistered_checks.join('|') !== coordinateResult.checks.map((item) => item.check_id).join('|')) fail('Frozen benchmark passport provenance or preregistered check order changed');
  if (review.outcome !== 'APPROVED' || review.approval_scope !== 'REPOSITORY_IMPLEMENTATION_AND_ARTIFACTS' || review.subject.passport_id !== passport.passport_id || review.subject.passport_version !== passport.passport_version || review.subject.result_digest !== coordinateResult.scientific_payload_digest || review.remaining_objections.length !== 0) fail('Coordinate implementation approval record is missing, mismatched, or unresolved');
  if (review.boundaries.external_scientific_reproduction !== false || review.boundaries.novel_physics_claim !== false || review.boundaries.transportation_claim !== false) fail('Coordinate implementation approval overstates its scientific scope');
  if (cleanCloneReproduction.comparison !== 'MATCH' || cleanCloneReproduction.independence.clean_remote_clone !== true || cleanCloneReproduction.independence.separate_library !== true || cleanCloneReproduction.independence.counts_as_external_reproduction !== false) fail('Internal clean-clone reproduction is missing, mismatched, or overstated');
  if (cleanCloneReproduction.signature.status !== 'UNSIGNED_NO_KEY' || cleanCloneReproduction.signature.content_digest_is_not_a_signature !== true || cleanCloneReproduction.conflict_of_interest.disclosed !== true) fail('Internal reproduction signature or conflict disclosure is inaccurate');
  if (coordinateCrosscheck.comparison_scope.schema_conformance_crosschecked !== false || coordinateCrosscheck.comparison_scope.excluded_reference_checks.join('|') !== 'schema.candidate.v1') fail('Coordinate cross-check overstates schema validation coverage');
  if (baselineCrosscheck.comparison_scope.schema_conformance_crosschecked !== false || baselineCrosscheck.comparison_scope.excluded_reference_checks.join('|') !== 'schema.candidate.v1') fail('Baseline cross-check overstates schema validation coverage');
  const sourceCommit = coordinateResult.run.source_commit;
  const reviewedHead = spawnSync('git', ['cat-file', '-e', `${review.subject.head_commit}^{commit}`], { cwd: root });
  if (reviewedHead.status !== 0) fail('Implementation approval does not reference an available Git commit');
  const sourcePredatesReview = spawnSync('git', ['merge-base', '--is-ancestor', sourceCommit, review.subject.head_commit], { cwd: root });
  if (sourcePredatesReview.status !== 0) fail('Coordinate result source commit is not an ancestor of the approved PR head');
  const sourcePaths = [
    'candidates/CANDIDATE-000002.json',
    'benchmarks/BENCHMARK-000002.passport.json',
    'src/core/candidate.schema.json',
    'src/core/benchmark-passport.schema.json',
    'src/research_core/pipeline.py',
    'src/research_core/matrix.py',
    'src/research_core/schema_validation.py',
  ];
  if (!/^[0-9a-f]{40}$/.test(sourceCommit)) fail('Coordinate result does not record a concrete source commit');
  for (const sourcePath of sourcePaths) {
    const existsAtCommit = spawnSync('git', ['cat-file', '-e', `${sourceCommit}:${sourcePath}`], { cwd: root });
    if (existsAtCommit.status !== 0) fail(`Coordinate result source commit does not contain ${sourcePath}`);
    const unchangedSinceCommit = spawnSync('git', ['diff', '--quiet', sourceCommit, '--', sourcePath], { cwd: root });
    if (unchangedSinceCommit.status !== 0) fail(`Coordinate result source commit does not contain the exact current ${sourcePath}`);
  }
  note(`${sourcePaths.length} coordinate-result source paths verified at ${sourceCommit.slice(0, 12)}`);
  if (program.current_evidence.workflow_cases !== benchmark.case_count) fail('Research program workflow count does not match the frozen benchmark');
  if (program.current_evidence.novel_transportation_candidates !== 0 || program.current_evidence.traveler_safety_evaluations !== 0 || program.current_evidence.outside_reproductions !== 0) fail('Research program overstates current evidence');
  if (program.security.public_code_execution !== 'DISABLED' || program.security.agent_authority !== 'PROPOSE_ONLY' || program.security.canonical_promotion !== 'NAMED_HUMAN_ONLY') fail('Research program weakens the public security boundary');
  const nodeIds = new Set(graph.nodes.map((node) => node.id));
  for (const edge of graph.edges) {
    if (!nodeIds.has(edge.source)) fail(`Graph edge ${edge.id} has missing source ${edge.source}`);
    if (!nodeIds.has(edge.target)) fail(`Graph edge ${edge.id} has missing target ${edge.target}`);
  }
  note(`${graph.nodes.length} graph nodes and ${graph.edges.length} graph edges reconciled`);
}

async function checkTrackedFiles() {
  const process = spawnSync('git', ['ls-files', '-z'], { cwd: root, encoding: 'buffer' });
  if (process.status !== 0) { fail('Unable to inspect tracked Git files'); return; }
  const tracked = process.stdout.toString('utf8').split('\0').filter(Boolean);
  const forbidden = tracked.filter((file) => file === '.env' || file.startsWith('.venv/') || file.startsWith('dist/') || file.startsWith('node_modules/') || file.startsWith('build/') || file.includes('/__pycache__/') || file.endsWith('.pyc') || file.endsWith('.pyo'));
  if (forbidden.length) fail(`Forbidden generated/private paths are tracked: ${forbidden.join(', ')}`);
  note(`${tracked.length} tracked paths checked for private/generated files`);
}

async function checkPlaceholdersAndSecrets(files) {
  const allowedPlaceholderFiles = new Set(['.env.example', '.github/CODEOWNERS.example', 'scripts/test_repository.mjs']);
  const privateKeyPattern = /-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----/;
  let scanned = 0;
  for (const file of files) {
    const details = await stat(file);
    if (details.size > 2_000_000) continue;
    const name = relative(file);
    if (/\.(?:png|jpg|jpeg|gif|webp|ico)$/i.test(name)) continue;
    const body = await readFile(file, 'utf8');
    scanned += 1;
    if (privateKeyPattern.test(body)) fail(`${name} appears to contain a private key`);
    if (!allowedPlaceholderFiles.has(name) && /REPLACE_WITH_ACCOUNT|REPLACE_WITH_REPOSITORY/.test(body)) fail(`${name} contains an unresolved repository placeholder`);
  }
  note(`${scanned} text files scanned for secrets and unresolved active placeholders`);
}

async function checkWorkflowSafety() {
  const workflowDir = path.join(root, '.github/workflows');
  const files = (await readdir(workflowDir)).filter((name) => /\.ya?ml$/.test(name));
  for (const name of files) {
    const body = await readFile(path.join(workflowDir, name), 'utf8');
    if (body.includes('pull_request_target:')) fail(`${name} uses pull_request_target and needs a dedicated threat review`);
    if (!body.includes('permissions:')) fail(`${name} does not declare permissions explicitly`);
    if (/permissions:\s*write-all/.test(body)) fail(`${name} grants write-all permissions`);
    const mutableActions = [...body.matchAll(/uses:\s*([^\s#]+)@([^\s#]+)/g)]
      .filter(([, action, reference]) => !action.startsWith('./') && !/^[0-9a-f]{40}$/.test(reference));
    if (mutableActions.length) fail(`${name} uses mutable action references: ${mutableActions.map(([, action, reference]) => `${action}@${reference}`).join(', ')}`);
  }
  note(`${files.length} workflow files checked for high-risk trigger/permission patterns`);
}

async function checkLicenseAndLockfile() {
  const license = await readFile(path.join(root, 'LICENSE'), 'utf8');
  if (!license.includes('Apache License') || !license.includes('Version 2.0')) fail('LICENSE is not the full Apache 2.0 text');
  const lock = JSON.parse(await readFile(path.join(root, 'package-lock.json'), 'utf8'));
  if (lock.lockfileVersion < 3) fail('package-lock.json uses an outdated lockfile format');
  note('License and package lockfile checked');
}

async function main() {
  const files = await walk(root);
  await checkRequiredFiles();
  await checkJsonAndJsonl(files);
  await checkMarkdownLinks(files);
  await checkScientificConsistency();
  await checkTrackedFiles();
  await checkPlaceholdersAndSecrets(files);
  await checkWorkflowSafety();
  await checkLicenseAndLockfile();

  console.log('\nRepository integrity validation');
  notes.forEach((message) => console.log(`  PASS  ${message}`));
  failures.forEach((message) => console.error(`  FAIL  ${message}`));
  console.log(`\n${failures.length ? 'FAILED' : 'PASSED'}: ${notes.length} validation groups, ${failures.length} failure(s)`);
  if (failures.length) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
