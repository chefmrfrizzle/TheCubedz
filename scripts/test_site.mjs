#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { access, readFile, readdir, stat } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');
const failures = [];
const notes = [];

function fail(message) { failures.push(message); }
function note(message) { notes.push(message); }
async function exists(filePath) { try { await access(filePath); return true; } catch { return false; } }
async function json(relative) { return JSON.parse(await readFile(path.join(dist, relative), 'utf8')); }
async function text(relative) { return readFile(path.join(dist, relative), 'utf8'); }

function extractAttributes(html, attribute) {
  const pattern = new RegExp(`\\b${attribute}="([^"]+)"`, 'g');
  return [...html.matchAll(pattern)].map((match) => match[1]);
}

function stripFragmentAndQuery(value) {
  return value.split('#')[0].split('?')[0];
}

function internalTarget(value, basePath = '') {
  if (!value || /^(?:https?:|mailto:|tel:|data:|javascript:|#)/i.test(value)) return null;
  let target = stripFragmentAndQuery(value);
  if (basePath && target.startsWith(`${basePath}/`)) target = target.slice(basePath.length);
  if (target === basePath) target = '/';
  if (!target.startsWith('/')) return null;
  const decoded = decodeURIComponent(target);
  if (decoded.endsWith('/')) return path.join(dist, decoded, 'index.html');
  const direct = path.join(dist, decoded);
  return direct;
}

async function verifyRequiredFiles() {
  const required = [
    'index.html', 'challenge/index.html', 'lab/index.html', 'calibrations/index.html', 'graph/index.html', 'agents/index.html', 'method/index.html', 'learn/index.html', 'roadmap/index.html', 'contribute/index.html',
    '404.html', 'assets/styles.css', 'assets/site.js', 'assets/favicon.svg', 'assets/og-card.png', 'assets/og-card-quiet-compute.png', 'assets/og-card-quiet-compute-v2.png',
    'data/candidate.json', 'data/result.json', 'data/candidate-000002.json', 'data/result-000002.json', 'data/benchmark-000002-passport.json', 'data/review-000002.json',
    'data/candidate-000003.json', 'data/result-000003.json', 'data/benchmark-000003-passport.json', 'data/crosscheck-000003.json',
    'data/synthetic-suite.json', 'data/synthetic-suite-result.json', 'data/crosscheck.json', 'data/crosscheck-000002.json', 'data/internal-clean-clone-reproduction.json', 'data/knowledge-graph.json', 'data/agents.json', 'data/roadmap.json', 'data/research-program.json', 'data/quiet-compute-program.json', 'data/project-status.json', 'data/site-config.json',
    'site.webmanifest', 'robots.txt', 'llms.txt', 'build-manifest.json', 'README.md', 'CONTRIBUTING.md', 'SECURITY.md', 'LICENSE', 'docs/QUIET_COMPUTE_NETWORK_LOGIC.md', 'docs/QUIET_COMPUTE_BACKEND.md', 'docs/QUIET_COMPUTE_CONTRIBUTION_TERMS_DRAFT.md', 'templates/quiet-compute/README.md', 'templates/quiet-compute/MEASUREMENT.template.json', 'templates/quiet-compute/PASSPORT-ROUND-0.template.json',
  ];
  for (const relative of required) if (!(await exists(path.join(dist, relative)))) fail(`Missing required build output: ${relative}`);
  note(`${required.length} required release files checked`);
}

async function verifyHtml(basePath = '') {
  const htmlFiles = ['index.html', 'challenge/index.html', 'lab/index.html', 'calibrations/index.html', 'graph/index.html', 'agents/index.html', 'method/index.html', 'learn/index.html', 'roadmap/index.html', 'contribute/index.html', '404.html'];
  const prohibited = [
    /we (?:have )?solved (?:the )?wormhole/i,
    /proves? (?:that )?wormholes? exist/i,
    /working warp (?:drive|device)/i,
    /instant(?:ly)? (?:travel|transport) to mars/i,
    /scientifically proven shortcut/i,
    /lorem ipsum/i,
  ];
  let linkCount = 0;
  for (const relative of htmlFiles) {
    const html = await text(relative);
    if (!/^<!doctype html>/i.test(html)) fail(`${relative}: missing HTML5 doctype`);
    if (!html.includes('<html lang="en"')) fail(`${relative}: missing document language`);
    if (!html.includes('id="main-content"')) fail(`${relative}: missing main-content landmark`);
    if (!html.includes('class="site-header"')) fail(`${relative}: missing shared header`);
    if (!html.includes('class="site-footer"')) fail(`${relative}: missing shared footer`);
    if (!html.includes('name="viewport"')) fail(`${relative}: missing responsive viewport`);
    if (!html.includes('name="description"')) fail(`${relative}: missing description metadata`);
    if (!html.includes('no verified quieter-system claim')) fail(`${relative}: missing explicit launch boundary`);
    for (const pattern of prohibited) if (pattern.test(html)) fail(`${relative}: prohibited claim pattern ${pattern}`);

    const urls = [...extractAttributes(html, 'href'), ...extractAttributes(html, 'src')];
    for (const url of urls) {
      const target = internalTarget(url, basePath);
      if (!target) continue;
      linkCount += 1;
      if (!(await exists(target))) {
        const indexVariant = path.join(target, 'index.html');
        if (!(await exists(indexVariant))) fail(`${relative}: unresolved internal URL ${url}`);
      }
    }
  }
  note(`${htmlFiles.length} HTML documents and ${linkCount} internal URLs checked`);
}

async function verifyArtifacts() {
  const [candidate, result, coordinateCandidate, coordinateResult, passport, review, curvedCandidate, curvedResult, curvedPassport, curvedCrosscheck, cleanCloneReproduction, benchmark, crosscheck, coordinateCrosscheck, status, graph, agents, roadmap, program, quietProgram] = await Promise.all([
    json('data/candidate.json'), json('data/result.json'), json('data/candidate-000002.json'), json('data/result-000002.json'), json('data/benchmark-000002-passport.json'), json('data/review-000002.json'),
    json('data/candidate-000003.json'), json('data/result-000003.json'), json('data/benchmark-000003-passport.json'), json('data/crosscheck-000003.json'),
    json('data/internal-clean-clone-reproduction.json'), json('data/synthetic-suite-result.json'), json('data/crosscheck.json'), json('data/crosscheck-000002.json'), json('data/project-status.json'), json('data/knowledge-graph.json'), json('data/agents.json'), json('data/roadmap.json'), json('data/research-program.json'), json('data/quiet-compute-program.json'),
  ]);
  const passed = result.checks.filter((check) => check.status === 'PASS').length;
  const failed = result.checks.filter((check) => check.status === 'FAIL').length;
  const coordinatePassed = coordinateResult.checks.filter((check) => check.status === 'PASS').length;
  const coordinateFailed = coordinateResult.checks.filter((check) => check.status === 'FAIL').length;
  const curvedPassed = curvedResult.checks.filter((check) => check.status === 'PASS').length;
  const curvedFailed = curvedResult.checks.filter((check) => check.status === 'FAIL').length;
  if (candidate.candidate_id !== status.candidateId) fail('Project status candidate ID does not match candidate artifact');
  if (result.scientific_payload_digest !== status.scientificPayloadDigest) fail('Project status digest does not match result artifact');
  if (status.candidateCount !== 3 || status.coordinateBenchmarkId !== coordinateCandidate.candidate_id || status.curvedBenchmarkId !== curvedCandidate.candidate_id) fail('Project status does not expose all three benchmark candidates');
  if (status.checkCount !== passed + coordinatePassed + curvedPassed) fail(`Project status passed-check count ${status.checkCount} does not match all benchmark results`);
  if (status.failedCheckCount !== failed + coordinateFailed + curvedFailed) fail(`Project status failed-check count ${status.failedCheckCount} does not match all benchmark results`);
  if (status.coordinateBenchmarkDigest !== coordinateResult.scientific_payload_digest || status.coordinateBenchmarkStatus !== 'BENCHMARK_VERIFIED') fail('Coordinate benchmark public status differs from its result');
  if (status.curvedBenchmarkDigest !== curvedResult.scientific_payload_digest || status.curvedBenchmarkStatus !== 'BENCHMARK_VERIFIED' || status.curvedBenchmarkScientificReview !== 'REQUESTED') fail('Curved benchmark public status or review boundary differs from its artifacts');
  if (status.graphNodeCount !== graph.nodes.length || status.graphEdgeCount !== graph.edges.length) fail('Project status graph counts do not match graph snapshot');
  if (status.agentCount !== agents.agents.length) fail('Project status agent count does not match agent contracts');
  if (status.roadmapPhaseCount !== roadmap.phases.length) fail('Project status roadmap count does not match roadmap artifact');
  if (status.novelClaimCount !== 0) fail('Public V0 must report zero novel physics claims');
  if (status.transportationStatus !== 'NOT_A_TRANSPORTATION_PROPOSAL') fail('Transportation status boundary changed unexpectedly');
  if (benchmark.case_count !== 100 || benchmark.failed !== 0) fail('Synthetic workflow benchmark is incomplete or failing');
  if (crosscheck.comparison !== 'MATCH') fail('Separate implementation cross-check does not match the canonical result');
  if (coordinateCrosscheck.comparison !== 'MATCH') fail('Coordinate benchmark separate implementation does not match');
  if (curvedCrosscheck.overall_status !== 'MATCH' || curvedCrosscheck.independence.external_reproduction !== false || curvedCrosscheck.signature.status !== 'UNSIGNED_NO_KEY') fail('Curved benchmark comparison is missing, mismatched, or overstated');
  if (crosscheck.independence.counts_as_external_reproduction !== false) fail('Implementation cross-check is overstated as external reproduction');
  if (program.research_question !== 'Can we shorten the distance to Mars—without changing the traveler?') fail('Public research question differs from the canonical program contract');
  if (passport.scientific_review !== 'CHANGES_REQUIRED' || passport.review_history.at(-1)?.response_status !== 'ADDRESSED_AWAITING_REREVIEW') fail('Published passport no longer matches its frozen approved source');
  if (review.outcome !== 'APPROVED' || review.approval_scope !== 'REPOSITORY_IMPLEMENTATION_AND_ARTIFACTS' || review.boundaries.external_scientific_reproduction !== false || review.remaining_objections.length !== 0) fail('Published implementation approval is missing, unresolved, or overstated');
  if (cleanCloneReproduction.comparison !== 'MATCH' || cleanCloneReproduction.independence.counts_as_external_reproduction !== false || cleanCloneReproduction.signature.status !== 'UNSIGNED_NO_KEY') fail('Published clean-clone reproduction is missing or overstated');
  if (status.coordinateBenchmarkReview !== review.outcome || status.coordinateBenchmarkReviewScope !== review.approval_scope) fail('Project status does not expose the current implementation review record');
  if (program.current_evidence.implemented_checks !== passed + coordinatePassed + curvedPassed || program.current_evidence.known_answer_examples !== 3 || program.current_evidence.workflow_cases !== benchmark.case_count) fail('Program evidence counts do not match public artifacts');
  if (program.current_evidence.novel_transportation_candidates !== 0 || program.current_evidence.traveler_safety_evaluations !== 0 || program.current_evidence.outside_reproductions !== 0) fail('Program contract overstates current evidence');
  if (quietProgram.campaign_line !== 'Data centers are too freaking loud.' || quietProgram.response_line !== "Let's make them quiet." || quietProgram.status !== 'VALIDATION_CORE_IMPLEMENTED' || quietProgram.authority !== 'DRAFT_NOT_PREREGISTERED') fail('Quiet Compute public status or campaign contract changed unexpectedly');
  if (quietProgram.current_evidence.published_acoustic_baselines !== 0 || quietProgram.current_evidence.verified_quieter_systems !== 0 || quietProgram.current_evidence.verified_superconductors !== 0 || quietProgram.current_evidence.public_volunteer_worker_enabled !== false) fail('Quiet Compute program overstates current evidence or worker availability');
  if (quietProgram.security.public_code_execution !== 'DISABLED' || quietProgram.security.worker_status !== 'ADMISSION_AND_PLANNING_IMPLEMENTED_EXECUTION_DISABLED') fail('Quiet Compute public-compute security boundary changed unexpectedly');
  if (quietProgram.implementation.measurement_sealing !== 'IMPLEMENTED' || quietProgram.implementation.signed_result_verification !== 'IMPLEMENTED' || quietProgram.implementation.tolerance_consensus !== 'IMPLEMENTED_NO_MAJORITY_OVERRIDE' || quietProgram.implementation.public_job_execution !== 'DISABLED') fail('Quiet Compute implementation inventory is incomplete or enables public execution');
  const labHtml = await text('lab/index.html');
  if (!labHtml.includes('Measure one machine. Change one thing. Prove what got quieter.') || !labHtml.includes('VALIDATION CORE IMPLEMENTED')) fail('Quiet Compute lab does not lead with the current operational challenge');
  if (!labHtml.includes('Every claimed improvement needs the complete chain') || !labHtml.includes('Tolerance consensus')) fail('Quiet Compute lab does not explain the evidence chain and consensus boundary');
  if (!labHtml.includes('No arbitrary public jobs run on contributor hardware') || !labHtml.includes('public execution opens until an independent sandbox review passes')) fail('Quiet Compute lab does not preserve the worker-security boundary');
  if (!labHtml.includes('/calibrations/')) fail('Quiet Compute lab does not preserve a clearly separated archive path');
  const archiveHtml = await text('calibrations/index.html');
  if (!archiveHtml.includes('Historical protocol archive') || !archiveHtml.includes('data-evidence-cube') || !archiveHtml.includes('Turn the cube to see what we know')) fail('Historical calibration archive is missing or not clearly labeled');
  if (!archiveHtml.includes('data-benchmark-ladder') || !archiveHtml.includes('Same space, different numbers')) fail('Historical archive does not expose the coordinate benchmark ladder');
  if (!archiveHtml.includes('full schema validation remains primary-only')) fail('Historical archive overstates the independent arithmetic comparison');
  if (!archiveHtml.includes('Implementation approval is not an outside scientific reproduction') || !archiveHtml.includes('/data/review-000002.json')) fail('Historical archive does not state or link the approval boundary');
  if (!archiveHtml.includes('data-curved-benchmark') || !archiveHtml.includes('Known curvature, strict boundaries')) fail('Historical archive does not expose the curved benchmark');
  if (!archiveHtml.includes('This does not solve Quiet Compute—or the Mars thesis') || !archiveHtml.includes('Outside signed reproduction</dt><dd>0')) fail('Historical archive overstates the curved benchmark');
  const homeHtml = await text('index.html');
  if (!homeHtml.includes('Data centers are too freaking loud.')) fail('Homepage does not state the first public challenge');
  if (!homeHtml.includes("Let's make them quiet.") || !homeHtml.includes('Join with your server')) fail('Homepage does not state the response or server-participation path');
  if (!homeHtml.includes('/assets/og-card-quiet-compute-v2.png')) fail('Homepage does not publish the current Quiet Compute social card');
  if (!homeHtml.includes('No public acoustic baseline, quieter design, or new superconductor has been verified')) fail('Homepage does not state the current Quiet Compute boundary');
  if (!homeHtml.includes('How people and computers work together')) fail('Homepage does not explain the public research workflow');
  if (!homeHtml.includes('>Quiet Lab</a>') || homeHtml.includes('>Lab</a>') || homeHtml.includes('>First challenge</a>')) fail('Primary navigation does not clearly name the Quiet Compute journey');
  const challengeHtml = await text('challenge/index.html');
  if (!challengeHtml.includes('Data centers are too freaking loud.') || !challengeHtml.includes("Let's make them quiet.") || !challengeHtml.includes('First we listen. Then we test everything.') || !challengeHtml.includes('Superconductors are one branch—not the assumed answer')) fail('Quiet Compute challenge does not distinguish its campaign, participation path, exact test, and long-horizon hypothesis');
  if (!challengeHtml.includes('id="install-linux-command"') || !challengeHtml.includes('data-copy-target="#install-linux-command"') || !challengeHtml.includes('python3.12 scripts/bootstrap.py')) fail('Quiet Compute challenge does not expose a copyable local installer');
  if (!challengeHtml.includes('This installs local tools only. It does not enroll a worker or upload data.')) fail('Quiet Compute installer does not state its safety boundary');
  if (!challengeHtml.includes('/docs/QUIET_COMPUTE_NETWORK_LOGIC.md')) fail('Quiet Compute challenge does not explain the installation and network logic');
  if (!challengeHtml.includes('Evidence gates—not public deadlines.') || !challengeHtml.includes('Measure the whole system—not just the loudest fan.')) fail('Quiet Compute challenge does not expose the evidence-gate and system-boundary context');
  if (challengeHtml.includes('NVIDIA Inception')) fail('Quiet Compute participant journey contains an unrelated startup-program promotion');
  const contributeHtml = await text('contribute/index.html');
  if (!contributeHtml.includes('Quiet Compute readiness') || !contributeHtml.includes('Quiet Compute build program') || !contributeHtml.includes('id="server-participant"') || !contributeHtml.includes('NO REMOTE ACCESS') || !contributeHtml.includes('/docs/QUIET_COMPUTE_NETWORK_LOGIC.md') || !contributeHtml.includes('/docs/QUIET_COMPUTE_BACKEND.md') || !contributeHtml.includes('/docs/QUIET_COMPUTE_CONTRIBUTION_TERMS_DRAFT.md') || !contributeHtml.includes('ADMISSION + PLANNING IMPLEMENTED · EXECUTION DISABLED')) fail('Contribution page does not expose server participation, contributor terms, security boundaries, backend state, network logic, readiness gates, and Quiet Compute prompt program');
  const primaryJourney = (await Promise.all(['index.html','challenge/index.html','lab/index.html','method/index.html','learn/index.html','roadmap/index.html','contribute/index.html'].map(text))).join('\n');
  if (/spacetime|mars thesis|wormhole|transportation device/i.test(primaryJourney)) fail('Primary Quiet Compute journey still exposes the historical spacetime program');
  note(`${result.checks.length + coordinateResult.checks.length + curvedResult.checks.length} scientific result checks reconciled with public status`);
}

async function verifyManifest() {
  const manifest = await json('build-manifest.json');
  for (const record of manifest.files) {
    const filePath = path.join(dist, record.path);
    if (!(await exists(filePath))) { fail(`Build manifest references missing file: ${record.path}`); continue; }
    const body = await readFile(filePath);
    const digest = createHash('sha256').update(body).digest('hex');
    const details = await stat(filePath);
    if (digest !== record.sha256) fail(`Build manifest digest mismatch: ${record.path}`);
    if (details.size !== record.bytes) fail(`Build manifest byte count mismatch: ${record.path}`);
  }
  note(`${manifest.files.length} build-manifest file fingerprints verified`);
}

async function verifyJavaScriptAndCss() {
  const jsCheck = spawnSync(process.execPath, ['--check', path.join(root, 'web/assets/site.js')], { encoding: 'utf8' });
  if (jsCheck.status !== 0) fail(`Browser JavaScript syntax error: ${jsCheck.stderr}`);
  const buildCheck = spawnSync(process.execPath, ['--check', path.join(root, 'scripts/build_site.mjs')], { encoding: 'utf8' });
  if (buildCheck.status !== 0) fail(`Build script syntax error: ${buildCheck.stderr}`);
  const css = await text('assets/styles.css');
  if (!css.includes('@media (max-width: 780px)')) fail('Responsive mobile breakpoint is missing');
  if (!css.includes(':focus-visible')) fail('Visible keyboard focus style is missing');
  if (!css.includes('prefers-reduced-motion')) fail('Reduced-motion preference is not handled');
  note('JavaScript syntax and core accessibility CSS checked');
}

async function verifyBasePathBuild() {
  const env = { ...process.env, PUBLIC_BASE_PATH: '/repository-preview' };
  const build = spawnSync(process.execPath, ['scripts/build_site.mjs'], { cwd: root, env, encoding: 'utf8' });
  if (build.status !== 0) { fail(`Base-path build failed: ${build.stderr}`); return; }
  try {
    const html = await text('index.html');
    if (!html.includes('href="/repository-preview/assets/styles.css?v=')) fail('Base-path build did not prefix or version stylesheet URL');
    if (!html.includes('href="/repository-preview/lab/"')) fail('Base-path build did not prefix internal navigation URL');
    await verifyHtml('/repository-preview');
    note('GitHub Pages-style base-path build checked');
  } finally {
    const restore = spawnSync(process.execPath, ['scripts/build_site.mjs'], { cwd: root, env: { ...process.env, PUBLIC_BASE_PATH: '' }, encoding: 'utf8' });
    if (restore.status !== 0) fail(`Unable to restore default build after base-path test: ${restore.stderr}`);
  }
}

async function main() {
  await verifyRequiredFiles();
  await verifyHtml();
  await verifyArtifacts();
  await verifyManifest();
  await verifyJavaScriptAndCss();
  await verifyBasePathBuild();

  console.log('\nWebsite release validation');
  notes.forEach((message) => console.log(`  PASS  ${message}`));
  failures.forEach((message) => console.error(`  FAIL  ${message}`));
  console.log(`\n${failures.length ? 'FAILED' : 'PASSED'}: ${notes.length} validation groups, ${failures.length} failure(s)`);
  if (failures.length) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
