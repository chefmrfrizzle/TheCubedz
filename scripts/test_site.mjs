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
    'index.html', 'lab/index.html', 'graph/index.html', 'agents/index.html', 'method/index.html', 'learn/index.html', 'roadmap/index.html', 'contribute/index.html',
    '404.html', 'assets/styles.css', 'assets/site.js', 'assets/favicon.svg', 'assets/og-card.png',
    'data/candidate.json', 'data/result.json', 'data/candidate-000002.json', 'data/result-000002.json', 'data/benchmark-000002-passport.json',
    'data/synthetic-suite.json', 'data/synthetic-suite-result.json', 'data/crosscheck.json', 'data/crosscheck-000002.json', 'data/knowledge-graph.json', 'data/agents.json', 'data/roadmap.json', 'data/research-program.json', 'data/project-status.json', 'data/site-config.json',
    'site.webmanifest', 'robots.txt', 'llms.txt', 'build-manifest.json', 'README.md', 'CONTRIBUTING.md', 'SECURITY.md', 'LICENSE',
  ];
  for (const relative of required) if (!(await exists(path.join(dist, relative)))) fail(`Missing required build output: ${relative}`);
  note(`${required.length} required release files checked`);
}

async function verifyHtml(basePath = '') {
  const htmlFiles = ['index.html', 'lab/index.html', 'graph/index.html', 'agents/index.html', 'method/index.html', 'learn/index.html', 'roadmap/index.html', 'contribute/index.html', '404.html'];
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
    if (!html.includes('no transportation claim')) fail(`${relative}: missing explicit launch boundary`);
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
  const [candidate, result, coordinateCandidate, coordinateResult, passport, benchmark, crosscheck, coordinateCrosscheck, status, graph, agents, roadmap, program] = await Promise.all([
    json('data/candidate.json'), json('data/result.json'), json('data/candidate-000002.json'), json('data/result-000002.json'), json('data/benchmark-000002-passport.json'),
    json('data/synthetic-suite-result.json'), json('data/crosscheck.json'), json('data/crosscheck-000002.json'), json('data/project-status.json'), json('data/knowledge-graph.json'), json('data/agents.json'), json('data/roadmap.json'), json('data/research-program.json'),
  ]);
  const passed = result.checks.filter((check) => check.status === 'PASS').length;
  const failed = result.checks.filter((check) => check.status === 'FAIL').length;
  const coordinatePassed = coordinateResult.checks.filter((check) => check.status === 'PASS').length;
  const coordinateFailed = coordinateResult.checks.filter((check) => check.status === 'FAIL').length;
  if (candidate.candidate_id !== status.candidateId) fail('Project status candidate ID does not match candidate artifact');
  if (result.scientific_payload_digest !== status.scientificPayloadDigest) fail('Project status digest does not match result artifact');
  if (status.candidateCount !== 2 || status.coordinateBenchmarkId !== coordinateCandidate.candidate_id) fail('Project status does not expose both benchmark candidates');
  if (status.checkCount !== passed + coordinatePassed) fail(`Project status passed-check count ${status.checkCount} does not match benchmark total ${passed + coordinatePassed}`);
  if (status.failedCheckCount !== failed + coordinateFailed) fail(`Project status failed-check count ${status.failedCheckCount} does not match benchmark total ${failed + coordinateFailed}`);
  if (status.coordinateBenchmarkDigest !== coordinateResult.scientific_payload_digest || status.coordinateBenchmarkStatus !== 'BENCHMARK_VERIFIED') fail('Coordinate benchmark public status differs from its result');
  if (status.graphNodeCount !== graph.nodes.length || status.graphEdgeCount !== graph.edges.length) fail('Project status graph counts do not match graph snapshot');
  if (status.agentCount !== agents.agents.length) fail('Project status agent count does not match agent contracts');
  if (status.roadmapPhaseCount !== roadmap.phases.length) fail('Project status roadmap count does not match roadmap artifact');
  if (status.novelClaimCount !== 0) fail('Public V0 must report zero novel physics claims');
  if (status.transportationStatus !== 'NOT_A_TRANSPORTATION_PROPOSAL') fail('Transportation status boundary changed unexpectedly');
  if (benchmark.case_count !== 100 || benchmark.failed !== 0) fail('Synthetic workflow benchmark is incomplete or failing');
  if (crosscheck.comparison !== 'MATCH') fail('Separate implementation cross-check does not match the canonical result');
  if (coordinateCrosscheck.comparison !== 'MATCH') fail('Coordinate benchmark separate implementation does not match');
  if (crosscheck.independence.counts_as_external_reproduction !== false) fail('Implementation cross-check is overstated as external reproduction');
  if (program.research_question !== 'Can we shorten the distance to Mars—without changing the traveler?') fail('Public research question differs from the canonical program contract');
  if (passport.scientific_review !== 'CHANGES_REQUIRED' || passport.review_history.at(-1)?.response_status !== 'ADDRESSED_AWAITING_REREVIEW') fail('Coordinate benchmark review state must preserve changes-required and await re-review');
  if (program.current_evidence.implemented_checks !== passed + coordinatePassed || program.current_evidence.known_answer_examples !== 2 || program.current_evidence.workflow_cases !== benchmark.case_count) fail('Program evidence counts do not match public artifacts');
  if (program.current_evidence.novel_transportation_candidates !== 0 || program.current_evidence.traveler_safety_evaluations !== 0 || program.current_evidence.outside_reproductions !== 0) fail('Program contract overstates current evidence');
  const labHtml = await text('lab/index.html');
  if (!labHtml.includes('data-evidence-cube') || !labHtml.includes('Turn the cube to see what we know')) fail('Answer cube is missing from the laboratory');
  if (!labHtml.includes('Each side asks one plain question')) fail('Answer cube does not explain how to read it');
  if (!labHtml.includes('data-benchmark-ladder') || !labHtml.includes('Same space, different numbers')) fail('Laboratory does not expose the coordinate benchmark ladder');
  if (!labHtml.includes('full schema validation remains primary-only')) fail('Laboratory overstates the independent arithmetic comparison');
  const homeHtml = await text('index.html');
  if (!homeHtml.includes('Can we shorten the distance to Mars')) fail('Homepage does not state the motivating research question');
  if (!homeHtml.includes('No shortcut, device, or route to Mars has been found')) fail('Homepage does not state the current scientific boundary');
  if (!homeHtml.includes('How people and the system work together')) fail('Homepage does not explain the public research workflow');
  const contributeHtml = await text('contribute/index.html');
  if (!contributeHtml.includes('data-program-gates') || !contributeHtml.includes('Complete Mars program')) fail('Contribution page does not expose the research contract and prompt program');
  const allHtml = (await Promise.all(['index.html','lab/index.html','graph/index.html'].map(text))).join('\n');
  if (!allHtml.includes(result.scientific_payload_digest)) fail('Scientific digest is not visible on public release pages');
  note(`${result.checks.length + coordinateResult.checks.length} scientific result checks reconciled with public status`);
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
