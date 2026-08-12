#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { access, cp, mkdir, readFile, readdir, rm, stat, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { navigation, pages } from '../web/pages.mjs';

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const distDir = path.join(projectRoot, 'dist');
const webDir = path.join(projectRoot, 'web');

function normalizeBase(value) {
  if (!value || value === '/') return '';
  return `/${String(value).replace(/^\/+|\/+$/g, '')}`;
}

function joinUrl(base, route = '/') {
  if (/^(?:https?:|mailto:|tel:|#)/i.test(route)) return route;
  const normalizedRoute = route.startsWith('/') ? route : `/${route}`;
  return `${base}${normalizedRoute}` || '/';
}

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function base64Url(value) {
  return Buffer.from(value).toString('base64url');
}

function rewriteRootUrls(html, basePath) {
  if (!basePath) return html;
  return html
    .replace(/\b(href|src|action)="\/(?!\/)/g, `$1="${basePath}/`)
    .replace(/\bcontent="\/(?!\/)/g, `content="${basePath}/`);
}

function pageRoute(page) {
  return page.slug ? `/${page.slug}/` : '/';
}

function siteHeader(page, basePath) {
  const nav = navigation.map((item) => {
    const current = item.key === page.key ? ' aria-current="page"' : '';
    return `<a href="${joinUrl(basePath, item.href)}"${current}>${escapeHtml(item.label)}</a>`;
  }).join('');
  return `<header class="site-header">
    <div class="shell header-inner">
      <a class="site-identity" href="${joinUrl(basePath, '/')}">
        <span class="identity-mark" aria-hidden="true"></span>
        <span class="identity-copy"><strong>TheCubedz</strong><small>open evidence engine</small></span>
      </a>
      <nav class="site-nav" id="primary-navigation" data-site-nav aria-label="Primary navigation">${nav}</nav>
      <div class="header-actions">
        <a class="button secondary" data-repository-link href="${joinUrl(basePath, '/contribute/')}">View source</a>
        <a class="button primary" href="${joinUrl(basePath, '/contribute/#server-participant')}">Join the challenge</a>
        <button class="nav-toggle" type="button" data-nav-toggle aria-controls="primary-navigation" aria-expanded="false" aria-label="Open navigation"><span></span></button>
      </div>
    </div>
  </header>`;
}

function siteFooter(config, basePath, result) {
  return `<footer class="site-footer">
    <div class="shell footer-grid">
      <div><p class="eyebrow">Quiet Compute · public pre-alpha</p><h2>Data centers are too freaking loud. Let's make them quiet.</h2><p>Bring one server, one measurement, or one reproducible idea. Quiet Compute has no published baseline or verified quieter design yet.</p></div>
      <div class="footer-links"><strong>Quiet Compute</strong><a href="${joinUrl(basePath, '/challenge/')}">The challenge</a><a href="${joinUrl(basePath, '/lab/')}">Quiet Compute lab</a><a href="${joinUrl(basePath, '/method/')}">How it works</a><a href="${joinUrl(basePath, '/learn/')}">Learn</a><a href="${joinUrl(basePath, '/roadmap/')}">Roadmap</a><a href="${joinUrl(basePath, '/contribute/')}">Join</a></div>
      <div class="footer-links"><strong>Project</strong><a href="${joinUrl(basePath, '/CONTRIBUTING.md')}">Contributing</a><a href="${joinUrl(basePath, '/docs/QUIET_COMPUTE_BACKEND.md')}">Algorithms</a><a href="${joinUrl(basePath, '/SECURITY.md')}">Security</a><a href="${joinUrl(basePath, '/calibrations/')}">Historical protocol archive</a><a data-contact-link href="${joinUrl(basePath, '/contribute/')}">Contact</a></div>
    </div>
    <div class="shell footer-meta">Version ${escapeHtml(config.version)} · measurement passport draft · public worker execution disabled · no verified quieter-system claim</div>
  </footer>`;
}

function documentHtml({ page, config, result, basePath, assetVersion }) {
  const route = pageRoute(page);
  const title = page.title === config.title ? config.title : `${page.title} | ${config.title}`;
  const canonical = config.siteUrl ? new URL(joinUrl(basePath, route), `${config.siteUrl.replace(/\/$/, '')}/`).href : '';
  const socialImagePath = config.socialImage || '/assets/og-card.png';
  const socialImage = config.siteUrl ? new URL(joinUrl(basePath, socialImagePath), `${config.siteUrl.replace(/\/$/, '')}/`).href : joinUrl(basePath, socialImagePath);
  const body = rewriteRootUrls(page.content, basePath);
  return `<!doctype html>
<html lang="en" data-base-path="${escapeHtml(basePath)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#071013">
  <meta name="color-scheme" content="dark">
  <meta name="description" content="${escapeHtml(page.description)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="generator" content="repository-static-builder/1.0">
  <title>${escapeHtml(title)}</title>
  ${canonical ? `<link rel="canonical" href="${escapeHtml(canonical)}">` : ''}
  <link rel="icon" href="${joinUrl(basePath, '/assets/favicon.svg')}" type="image/svg+xml">
  <link rel="manifest" href="${joinUrl(basePath, '/site.webmanifest')}">
  <link rel="stylesheet" href="${joinUrl(basePath, '/assets/styles.css')}?v=${encodeURIComponent(assetVersion)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${escapeHtml(title)}">
  <meta property="og:description" content="${escapeHtml(page.description)}">
  <meta property="og:image" content="${escapeHtml(socialImage)}">
  ${canonical ? `<meta property="og:url" content="${escapeHtml(canonical)}">` : ''}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${escapeHtml(title)}">
  <meta name="twitter:description" content="${escapeHtml(page.description)}">
  <meta name="twitter:image" content="${escapeHtml(socialImage)}">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  ${siteHeader(page, basePath)}
  ${body}
  ${siteFooter(config, basePath, result)}
  <script type="module" src="${joinUrl(basePath, '/assets/site.js')}?v=${encodeURIComponent(assetVersion)}"></script>
</body>
</html>`;
}

async function readJson(relativePath) {
  return JSON.parse(await readFile(path.join(projectRoot, relativePath), 'utf8'));
}

async function fileExists(filePath) {
  try { await access(filePath); return true; } catch { return false; }
}

async function copyIfExists(relativePath, destination = relativePath) {
  const source = path.join(projectRoot, relativePath);
  if (!(await fileExists(source))) return;
  const target = path.join(distDir, destination);
  await mkdir(path.dirname(target), { recursive: true });
  await cp(source, target, { recursive: true });
}

async function listFiles(directory, prefix = '') {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const absolute = path.join(directory, entry.name);
    const relative = path.posix.join(prefix, entry.name);
    if (entry.isDirectory()) files.push(...await listFiles(absolute, relative));
    else files.push(relative);
  }
  return files;
}

async function sha256File(filePath) {
  const hash = createHash('sha256');
  hash.update(await readFile(filePath));
  return hash.digest('hex');
}

function gitValue(args, fallback = 'UNAVAILABLE') {
  const process = spawnSync('git', args, { cwd: projectRoot, encoding: 'utf8' });
  return process.status === 0 ? process.stdout.trim() || fallback : fallback;
}

async function build() {
  const rawConfig = await readJson('site.config.json');
  const config = {
    ...rawConfig,
    repositoryUrl: process.env.PUBLIC_REPOSITORY_URL || rawConfig.repositoryUrl || '',
    siteUrl: process.env.PUBLIC_SITE_URL || rawConfig.siteUrl || '',
    contactUrl: process.env.PUBLIC_CONTACT_URL || rawConfig.contactUrl || '',
  };
  const basePath = normalizeBase(process.env.PUBLIC_BASE_PATH || '');
  const assetHash = createHash('sha256');
  assetHash.update(await readFile(path.join(webDir, 'assets', 'styles.css')));
  assetHash.update(await readFile(path.join(webDir, 'assets', 'site.js')));
  const assetVersion = assetHash.digest('hex').slice(0, 16);
  const [candidate, result, coordinateCandidate, coordinateResult, curvedCandidate, curvedResult, curvedPassport, curvedCrosscheck, benchmark, crosscheck, coordinateCrosscheck, passport, review, graph, agents, roadmap, program] = await Promise.all([
    readJson('candidates/CANDIDATE-000001.json'),
    readJson('artifacts/results/CANDIDATE-000001.result.json'),
    readJson('candidates/CANDIDATE-000002.json'),
    readJson('artifacts/results/CANDIDATE-000002.result.json'),
    readJson('candidates/CANDIDATE-000003.json'),
    readJson('artifacts/results/CANDIDATE-000003.result.json'),
    readJson('benchmarks/BENCHMARK-000003.passport.json'),
    readJson('artifacts/reproductions/CANDIDATE-000003.einsteinpy-crosscheck.json'),
    readJson('artifacts/benchmarks/synthetic-suite-v1.result.json'),
    readJson('artifacts/reproductions/CANDIDATE-000001.crosscheck.json'),
    readJson('artifacts/reproductions/CANDIDATE-000002.crosscheck.json'),
    readJson('benchmarks/BENCHMARK-000002.passport.json'),
    readJson('artifacts/reviews/REVIEW-000002.json'),
    readJson('data/knowledge-graph.json'),
    readJson('data/agents.json'),
    readJson('data/roadmap.json'),
    readJson('data/research-program.json'),
  ]);

  await rm(distDir, { recursive: true, force: true });
  await mkdir(path.join(distDir, 'assets'), { recursive: true });
  await mkdir(path.join(distDir, 'data'), { recursive: true });

  for (const page of pages) {
    const outputDir = page.slug ? path.join(distDir, page.slug) : distDir;
    await mkdir(outputDir, { recursive: true });
    await writeFile(path.join(outputDir, 'index.html'), documentHtml({ page, config, result, basePath, assetVersion }), 'utf8');
  }

  await copyIfExists('web/assets', 'assets');
  await copyIfExists('candidates/CANDIDATE-000001.json', 'data/candidate.json');
  await copyIfExists('artifacts/results/CANDIDATE-000001.result.json', 'data/result.json');
  await copyIfExists('candidates/CANDIDATE-000002.json', 'data/candidate-000002.json');
  await copyIfExists('artifacts/results/CANDIDATE-000002.result.json', 'data/result-000002.json');
  await copyIfExists('candidates/CANDIDATE-000003.json', 'data/candidate-000003.json');
  await copyIfExists('artifacts/results/CANDIDATE-000003.result.json', 'data/result-000003.json');
  await copyIfExists('benchmarks/BENCHMARK-000003.passport.json', 'data/benchmark-000003-passport.json');
  await copyIfExists('artifacts/reproductions/CANDIDATE-000003.einsteinpy-crosscheck.json', 'data/crosscheck-000003.json');
  await copyIfExists('artifacts/benchmarks/synthetic-suite-v1.result.json', 'data/synthetic-suite-result.json');
  await copyIfExists('benchmarks/synthetic-suite-v1.json', 'data/synthetic-suite.json');
  await copyIfExists('artifacts/reproductions/CANDIDATE-000001.crosscheck.json', 'data/crosscheck.json');
  await copyIfExists('artifacts/reproductions/CANDIDATE-000002.crosscheck.json', 'data/crosscheck-000002.json');
  await copyIfExists('artifacts/reproductions/INTERNAL-CLEAN-CLONE-000001.json', 'data/internal-clean-clone-reproduction.json');
  await copyIfExists('benchmarks/BENCHMARK-000002.passport.json', 'data/benchmark-000002-passport.json');
  await copyIfExists('artifacts/reviews/REVIEW-000002.json', 'data/review-000002.json');
  await copyIfExists('artifacts/reports/CANDIDATE-000001.beginner.md', 'data/report-beginner.md');
  await copyIfExists('artifacts/reports/CANDIDATE-000001.technical.md', 'data/report-technical.md');
  await copyIfExists('artifacts/reports/CANDIDATE-000002.beginner.md', 'data/report-000002-beginner.md');
  await copyIfExists('artifacts/reports/CANDIDATE-000002.technical.md', 'data/report-000002-technical.md');
  await copyIfExists('artifacts/reports/CANDIDATE-000003.beginner.md', 'data/report-000003-beginner.md');
  await copyIfExists('artifacts/reports/CANDIDATE-000003.technical.md', 'data/report-000003-technical.md');
  await copyIfExists('data/knowledge-graph.json', 'data/knowledge-graph.json');
  await copyIfExists('data/agents.json', 'data/agents.json');
  await copyIfExists('data/roadmap.json', 'data/roadmap.json');
  await copyIfExists('data/research-program.json', 'data/research-program.json');
  await copyIfExists('data/quiet-compute-program.json', 'data/quiet-compute-program.json');
  await copyIfExists('data/ledger/events.jsonl', 'data/events.jsonl');
  await copyIfExists('src/core', 'schemas');
  await copyIfExists('prompts', 'prompts');
  await copyIfExists('docs', 'docs');
  await copyIfExists('templates', 'templates');

  const publicFiles = ['README.md', 'CONTRIBUTING.md', 'GOVERNANCE.md', 'SECURITY.md', 'CODE_OF_CONDUCT.md', 'LICENSE', 'NOTICE', 'CHANGELOG.md', 'SUPPORT.md', 'CITATION.cff'];
  for (const file of publicFiles) await copyIfExists(file);

  const status = {
    schemaVersion: '1.0.0',
    releaseStatus: config.status,
    version: config.version,
    candidateCount: 3,
    checkCount: [result, coordinateResult, curvedResult].flatMap((item) => item.checks).filter((check) => check.status === 'PASS').length,
    failedCheckCount: [result, coordinateResult, curvedResult].flatMap((item) => item.checks).filter((check) => check.status === 'FAIL').length,
    novelClaimCount: 0,
    reproductionCount: graph.nodes.filter((node) => node.type === 'Reproduction' && node.status === 'REPRODUCED').length,
    implementationCrosscheckCount: [crosscheck.comparison, coordinateCrosscheck.comparison, curvedCrosscheck.overall_status].filter((status) => status === 'MATCH').length,
    syntheticCaseCount: benchmark.case_count,
    syntheticCaseFailureCount: benchmark.failed,
    graphNodeCount: graph.nodes.length,
    graphEdgeCount: graph.edges.length,
    agentCount: agents.agents.length,
    roadmapPhaseCount: roadmap.phases.length,
    candidateId: candidate.candidate_id,
    candidateStatus: candidate.status,
    resultStatus: result.assessment.overall_status,
    transportationStatus: result.assessment.transportation_status,
    scientificPayloadDigest: result.scientific_payload_digest,
    coordinateBenchmarkId: coordinateCandidate.candidate_id,
    coordinateBenchmarkStatus: coordinateResult.assessment.overall_status,
    coordinateBenchmarkDigest: coordinateResult.scientific_payload_digest,
    coordinateBenchmarkReview: review.outcome,
    coordinateBenchmarkReviewScope: review.approval_scope,
    curvedBenchmarkId: curvedCandidate.candidate_id,
    curvedBenchmarkStatus: curvedResult.assessment.overall_status,
    curvedBenchmarkDigest: curvedResult.scientific_payload_digest,
    curvedBenchmarkPassport: `${curvedPassport.passport_id}@${curvedPassport.passport_version}`,
    curvedBenchmarkCrosscheck: curvedCrosscheck.overall_status,
    curvedBenchmarkScientificReview: curvedPassport.scientific_review,
    generatedAt: result.run.recorded_at,
  };
  await writeFile(path.join(distDir, 'data', 'project-status.json'), `${JSON.stringify(status, null, 2)}\n`, 'utf8');
  await writeFile(path.join(distDir, 'data', 'site-config.json'), `${JSON.stringify({ ...config, basePath }, null, 2)}\n`, 'utf8');

  const manifest = {
    name: config.title,
    short_name: config.shortTitle,
    description: config.description,
    start_url: joinUrl(basePath, '/'),
    scope: joinUrl(basePath, '/'),
    display: 'standalone',
    background_color: '#071013',
    theme_color: '#071013',
    icons: [{ src: joinUrl(basePath, '/assets/favicon.svg'), sizes: 'any', type: 'image/svg+xml', purpose: 'any' }],
  };
  await writeFile(path.join(distDir, 'site.webmanifest'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  await writeFile(path.join(distDir, 'robots.txt'), `User-agent: *\nAllow: /\n${config.siteUrl ? `Sitemap: ${config.siteUrl.replace(/\/$/, '')}${basePath}/sitemap.xml\n` : ''}`, 'utf8');

  const llms = `# ${config.title}\n\n> ${config.description}\n\n## First public challenge\n\n- Campaign line: Data centers are too freaking loud.\n- Response: Let's make them quiet.\n- Participation: contribute one locally measured server or data-center baseline; do not provide remote access or credentials.\n- Exact question: can a declared compute system reduce acoustic output under the same useful workload while satisfying thermal, energy, water, reliability, cost, uncertainty, and reproduction constraints?\n- Status: validation core implemented; measurement passport remains a draft.\n- Public worker execution: disabled.\n- Published Quiet Compute acoustic baselines: 0.\n- Verified quieter systems: 0.\n- Verified new superconductors: 0.\n\n## Historical protocol archive\n\n- The earlier mathematical candidates remain archived software-calibration records; they are not the current public challenge.\n- ${result.checks.length + coordinateResult.checks.length + curvedResult.checks.length} scoped checks are implemented and currently pass.\n- Candidate 000002 implementation re-review: ${review.outcome}.\n- Candidate 000003 scientific review: ${curvedPassport.scientific_review}.\n- External scientific reproductions: 0.\n- Primary baseline digest: ${result.scientific_payload_digest}\n- Coordinate benchmark digest: ${coordinateResult.scientific_payload_digest}\n- Curved benchmark digest: ${curvedResult.scientific_payload_digest}\n- No Quiet Compute baseline, verified quieter design, or new superconductor has been demonstrated.\n\n## Core documents\n\n- ${joinUrl(basePath, '/README.md')}\n- ${joinUrl(basePath, '/CONTRIBUTING.md')}\n- ${joinUrl(basePath, '/docs/QUIET_COMPUTE_NETWORK_LOGIC.md')}\n- ${joinUrl(basePath, '/docs/QUIET_COMPUTE_BACKEND.md')}\n- ${joinUrl(basePath, '/challenge/')}\n- ${joinUrl(basePath, '/lab/')}\n- ${joinUrl(basePath, '/method/')}\n- ${joinUrl(basePath, '/calibrations/')}\n\n## Machine-readable artifacts\n\n- ${joinUrl(basePath, '/data/quiet-compute-program.json')}\n- ${joinUrl(basePath, '/data/candidate.json')}\n- ${joinUrl(basePath, '/data/result.json')}\n- ${joinUrl(basePath, '/data/candidate-000002.json')}\n- ${joinUrl(basePath, '/data/result-000002.json')}\n- ${joinUrl(basePath, '/data/candidate-000003.json')}\n- ${joinUrl(basePath, '/data/result-000003.json')}\n- ${joinUrl(basePath, '/data/benchmark-000003-passport.json')}\n- ${joinUrl(basePath, '/data/crosscheck-000003.json')}\n- ${joinUrl(basePath, '/data/review-000002.json')}\n- ${joinUrl(basePath, '/data/knowledge-graph.json')}\n- ${joinUrl(basePath, '/data/agents.json')}\n`;
  await writeFile(path.join(distDir, 'llms.txt'), llms, 'utf8');

  const notFoundPage = {
    slug: '404', key: '404', title: 'Page not found', description: 'The requested research page does not exist.',
    content: `<main id="main-content"><section class="shell page-hero section-pad compact"><div><p class="eyebrow">404</p><h1>This page does not exist.</h1><p class="hero-lede">Return to Quiet Compute or open the working lab.</p><div class="hero-actions"><a class="button primary" href="/">Return to overview</a><a class="button secondary" href="/lab/">Open the Quiet Compute lab</a></div></div></section></main>`,
  };
  await writeFile(path.join(distDir, '404.html'), documentHtml({ page: notFoundPage, config, result, basePath, assetVersion }), 'utf8');

  if (config.siteUrl) {
    const siteRoot = config.siteUrl.replace(/\/$/, '');
    const urls = pages.map((page) => `${siteRoot}${joinUrl(basePath, pageRoute(page))}`);
    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((url) => `  <url><loc>${escapeHtml(url)}</loc></url>`).join('\n')}\n</urlset>\n`;
    await writeFile(path.join(distDir, 'sitemap.xml'), sitemap, 'utf8');
  }

  const files = (await listFiles(distDir)).filter((file) => file !== 'build-manifest.json').sort();
  const fileRecords = [];
  for (const relative of files) {
    const absolute = path.join(distDir, relative);
    const details = await stat(absolute);
    fileRecords.push({ path: relative, bytes: details.size, sha256: await sha256File(absolute) });
  }
  const buildManifest = {
    schemaVersion: '1.0.0',
    releaseVersion: config.version,
    sourceCommit: gitValue(['rev-parse', 'HEAD']),
    sourceTreeState: gitValue(['status', '--porcelain']) ? 'DIRTY' : 'CLEAN',
    basePath,
    generatedAt: result.run.recorded_at,
    scientificPayloadDigest: result.scientific_payload_digest,
    files: fileRecords,
  };
  const payload = `${JSON.stringify(buildManifest, null, 2)}\n`;
  await writeFile(path.join(distDir, 'build-manifest.json'), payload, 'utf8');

  const output = {
    pages: pages.length,
    files: fileRecords.length + 1,
    basePath: basePath || '/',
    repositoryConfigured: Boolean(config.repositoryUrl),
    siteUrlConfigured: Boolean(config.siteUrl),
    manifestDigest: `sha256:${createHash('sha256').update(payload).digest('hex')}`,
  };
  console.log(JSON.stringify(output, null, 2));
}

build().catch((error) => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
