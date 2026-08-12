#!/usr/bin/env node
import { access, readFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = new Set(process.argv.slice(2));
const stageIndex = process.argv.indexOf('--stage');
const stage = stageIndex >= 0 ? process.argv[stageIndex + 1] : 'site';
const jsonOutput = args.has('--json');

if (args.has('--help')) {
  console.log('Usage: node scripts/production_preflight.mjs [--stage site|intake|compute] [--json]');
  console.log('Checks production readiness without printing secret values or changing external state.');
  process.exit(0);
}

if (!['site', 'intake', 'compute'].includes(stage)) {
  console.error(`Unknown production stage: ${stage}`);
  process.exit(2);
}

const results = [];
function record(id, status, message) { results.push({ id, status, message }); }
async function exists(relativePath) {
  try { await access(path.join(root, relativePath)); return true; } catch { return false; }
}
function run(command, commandArgs) {
  return spawnSync(command, commandArgs, { cwd: root, encoding: 'utf8', shell: false });
}
function output(process) { return `${process.stdout || ''}${process.stderr || ''}`.trim(); }

const requiredFiles = [
  'vercel.json',
  'site.config.json',
  '.github/workflows/ci.yml',
  '.github/workflows/codeql.yml',
  'docs/PRODUCTION_INTEGRATION_PLAN.md',
  'prompts/PRODUCTION_INTEGRATION_PROGRAM.md',
];

for (const file of requiredFiles) {
  record(`file:${file}`, await exists(file) ? 'PASS' : 'BLOCKER', await exists(file) ? 'present' : 'missing');
}

const [nodeMajor, nodeMinor] = process.versions.node.split('.').map(Number);
record('runtime:node', nodeMajor > 20 || (nodeMajor === 20 && nodeMinor >= 9) ? 'PASS' : 'BLOCKER', `Node ${process.versions.node}; requires 20.9+`);

const gitRoot = run('git', ['rev-parse', '--show-toplevel']);
if (gitRoot.status !== 0) {
  record('git:repository', 'BLOCKER', 'not a Git repository');
} else {
  record('git:repository', 'PASS', output(gitRoot));
  const origin = run('git', ['remote', 'get-url', 'origin']);
  const originValue = output(origin);
  record('git:origin', origin.status === 0 && /github\.com[/:]chefmrfrizzle\/TheCubedz(?:\.git)?$/i.test(originValue) ? 'PASS' : 'BLOCKER', originValue || 'origin missing');

  const branch = run('git', ['branch', '--show-current']);
  record('git:branch', branch.status === 0 ? 'PASS' : 'BLOCKER', output(branch) || 'detached HEAD');

  const status = run('git', ['status', '--porcelain']);
  const changedCount = output(status) ? output(status).split(/\r?\n/).length : 0;
  record('git:clean', status.status === 0 && changedCount === 0 ? 'PASS' : 'BLOCKER', changedCount === 0 ? 'working tree clean' : `${changedCount} changed or untracked path(s)`);

  const upstream = run('git', ['rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}']);
  if (upstream.status !== 0) {
    record('git:upstream', 'BLOCKER', 'current branch has no upstream');
  } else {
    const unpublished = run('git', ['rev-list', '--count', '@{u}..HEAD']);
    const unpublishedCount = Number.parseInt(output(unpublished), 10);
    record('git:published', unpublished.status === 0 && unpublishedCount === 0 ? 'PASS' : 'BLOCKER', Number.isFinite(unpublishedCount) ? `${unpublishedCount} local commit(s) not on ${output(upstream)}` : 'unable to compare upstream');
  }
}

const siteConfig = JSON.parse(await readFile(path.join(root, 'site.config.json'), 'utf8'));
record('site:url', /^https:\/\/[^/]+/.test(siteConfig.siteUrl || '') ? 'PASS' : 'BLOCKER', siteConfig.siteUrl || 'siteUrl missing');
record('site:repository', siteConfig.repositoryUrl === 'https://github.com/chefmrfrizzle/TheCubedz' ? 'PASS' : 'BLOCKER', siteConfig.repositoryUrl || 'repositoryUrl missing');

const vercelConfig = JSON.parse(await readFile(path.join(root, 'vercel.json'), 'utf8'));
const headers = new Map((vercelConfig.headers || []).flatMap((entry) => entry.headers || []).map((entry) => [entry.key.toLowerCase(), entry.value]));
for (const header of ['content-security-policy', 'strict-transport-security', 'x-content-type-options', 'referrer-policy', 'permissions-policy']) {
  record(`header:${header}`, headers.has(header) ? 'PASS' : 'BLOCKER', headers.has(header) ? 'configured' : 'missing');
}

const linked = await exists('.vercel/project.json');
record('vercel:link', linked ? 'PASS' : 'BLOCKER', linked ? 'local project link present' : 'run Vercel link from the intended production account');

const vercelCli = run(process.platform === 'win32' ? 'where.exe' : 'which', ['vercel']);
record('vercel:cli', vercelCli.status === 0 ? 'PASS' : 'WARN', vercelCli.status === 0 ? output(vercelCli).split(/\r?\n/)[0] : 'global CLI not found; use a pinned npx invocation or install the CLI');

const ghAuth = run('gh', ['auth', 'status']);
record('github:auth', ghAuth.status === 0 ? 'PASS' : 'BLOCKER', ghAuth.status === 0 ? 'authenticated; token value not displayed' : 'GitHub CLI is not authenticated');

if (ghAuth.status === 0) {
  const protection = run('gh', ['api', 'repos/chefmrfrizzle/TheCubedz/branches/main/protection']);
  if (protection.status !== 0) {
    record('github:protection', 'BLOCKER', 'unable to read main branch protection');
  } else {
    const body = JSON.parse(protection.stdout);
    const contexts = new Set(body.required_status_checks?.contexts || []);
    const expected = ['Public release contract', 'Science / Python 3.12', 'Science / Python 3.13', 'Analyze javascript-typescript', 'Analyze python'];
    const missing = expected.filter((item) => !contexts.has(item));
    record('github:required-checks', missing.length === 0 ? 'PASS' : 'BLOCKER', missing.length === 0 ? 'all release and analysis checks required' : `not required: ${missing.join(', ')}`);
    record('github:reviews', body.required_pull_request_reviews?.required_approving_review_count >= 1 && body.required_pull_request_reviews?.require_code_owner_reviews === true ? 'PASS' : 'BLOCKER', 'requires one approval and code-owner review');
    record('github:history', body.required_linear_history?.enabled === true && body.allow_force_pushes?.enabled === false && body.allow_deletions?.enabled === false ? 'PASS' : 'BLOCKER', 'linear history; no force push or deletion');
    record('github:signed-commits', body.required_signatures?.enabled === true ? 'PASS' : 'WARN', body.required_signatures?.enabled === true ? 'required' : 'not required; configure future commit signing before enabling');
  }
}

const stageVariables = {
  intake: ['DATABASE_URL', 'BLOB_READ_WRITE_TOKEN', 'CLERK_SECRET_KEY', 'NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY', 'RESEND_API_KEY'],
  compute: ['DATABASE_URL', 'BLOB_READ_WRITE_TOKEN', 'CLERK_SECRET_KEY', 'NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY', 'RESEND_API_KEY', 'VERCEL_PROJECT_ID'],
};

for (const variable of stage === 'site' ? [] : stageVariables[stage]) {
  record(`env:${variable}`, process.env[variable] ? 'PASS' : 'BLOCKER', process.env[variable] ? 'set; value not displayed' : 'not set in this environment');
}

if (stage === 'compute') {
  record('compute:public-enrollment', 'BLOCKER', 'public execution requires an independent sandbox assessment and must remain disabled');
}

const counts = { PASS: 0, WARN: 0, BLOCKER: 0 };
for (const result of results) counts[result.status] += 1;
const report = { schema_version: '1.0.0', stage, generated_at: new Date().toISOString(), counts, results };

if (jsonOutput) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`\nTheCubedz production preflight — ${stage}\n`);
  for (const result of results) console.log(`  ${result.status.padEnd(7)} ${result.id} — ${result.message}`);
  console.log(`\n${counts.PASS} passed, ${counts.WARN} warning(s), ${counts.BLOCKER} blocker(s)`);
  console.log('No secret values were printed and no external state was changed.');
}

process.exit(counts.BLOCKER === 0 ? 0 : 1);
