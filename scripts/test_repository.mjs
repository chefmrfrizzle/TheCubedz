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
    'candidates/CANDIDATE-000001.json', 'artifacts/results/CANDIDATE-000001.result.json', 'data/ledger/events.jsonl', 'data/knowledge-graph.json',
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
  const graph = JSON.parse(await readFile(path.join(root, 'data/knowledge-graph.json'), 'utf8'));
  const readme = await readFile(path.join(root, 'README.md'), 'utf8');
  if (candidate.candidate_id !== result.candidate.candidate_id) fail('Candidate and result IDs differ');
  if (!readme.includes(result.scientific_payload_digest)) fail('README does not publish the exact scientific payload digest');
  if (!readme.includes('Novel physics claims | 0')) fail('README does not explicitly report zero novel physics claims');
  if (result.assessment.transportation_status !== 'NOT_A_TRANSPORTATION_PROPOSAL') fail('Transportation boundary changed');
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
