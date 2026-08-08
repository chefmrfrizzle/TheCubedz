const root = document.documentElement;
const basePath = normalizeBase(root.dataset.basePath || '');
const runtime = {
  candidate: null,
  result: null,
  coordinateCandidate: null,
  coordinateResult: null,
  coordinateCrosscheck: null,
  coordinatePassport: null,
  benchmark: null,
  crosscheck: null,
  graph: null,
  agents: null,
  roadmap: null,
  program: null,
  config: null,
};

function normalizeBase(value) {
  if (!value || value === '/') return '';
  return `/${String(value).replace(/^\/+|\/+$/g, '')}`;
}

function withBase(path = '/') {
  if (/^(?:https?:|mailto:|tel:|#)/i.test(path)) return path;
  const clean = path.startsWith('/') ? path : `/${path}`;
  return `${basePath}${clean}` || '/';
}

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function formatValue(value) {
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  return JSON.stringify(value);
}

async function getJson(path) {
  const response = await fetch(withBase(path), { headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error(`Unable to load ${path} (${response.status})`);
  return response.json();
}

async function getText(path) {
  const response = await fetch(withBase(path), { headers: { Accept: 'text/plain' } });
  if (!response.ok) throw new Error(`Unable to load ${path} (${response.status})`);
  return response.text();
}

function setText(selector, value, scope = document) {
  const node = scope.querySelector(selector);
  if (node) node.textContent = value;
}

function setAllText(selector, value, scope = document) {
  scope.querySelectorAll(selector).forEach((node) => { node.textContent = value; });
}

function statusClass(status = '') {
  const value = status.toUpperCase();
  if (value.includes('UNSUPPORTED') || value.includes('UNRESOLVED') || value.includes('NOT_APPLICABLE')) return 'neutral';
  if (value.includes('PASS') || value.includes('VERIFIED') || value.includes('COMPLETE') || value.includes('SUPPORTED') || value.includes('LIVE') || value.includes('MATCH')) return 'pass';
  if (value.includes('FAIL') || value.includes('RETRACT') || value.includes('FALS')) return 'fail';
  if (value.includes('WARN') || value.includes('REVIEW') || value.includes('PARTIAL') || value.includes('GATED') || value.includes('DRAFT')) return 'warning';
  return 'neutral';
}

function createPill(status) {
  return `<span class="pill ${statusClass(status)}">${escapeHtml(status.replaceAll('_', ' '))}</span>`;
}

function initializeNavigation() {
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-site-nav]');
  if (!toggle || !nav) return;

  const close = () => {
    nav.classList.remove('open');
    document.body.classList.remove('nav-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    document.body.classList.toggle('nav-open', isOpen);
    toggle.setAttribute('aria-expanded', String(isOpen));
  });
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) close();
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 1080) close();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') close();
  });
}

function initializeExplanationGroups() {
  document.querySelectorAll('[data-explanation-group]').forEach((group) => {
    const controls = [...group.querySelectorAll('[data-level]')];
    const panels = [...group.querySelectorAll('[data-explanation]')];
    controls.forEach((button) => {
      button.addEventListener('click', () => {
        const level = button.dataset.level;
        controls.forEach((control) => {
          const active = control === button;
          control.classList.toggle('active', active);
          control.setAttribute('aria-selected', String(active));
        });
        panels.forEach((panel) => { panel.hidden = panel.dataset.explanation !== level; });
      });
    });
  });
}

async function copyText(text, button) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.append(area);
    area.select();
    document.execCommand('copy');
    area.remove();
  }
  const original = button.textContent;
  button.textContent = 'Copied';
  window.setTimeout(() => { button.textContent = original; }, 1500);
}

function initializeCopyButtons() {
  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.querySelector(button.dataset.copyTarget);
      if (!target) return;
      await copyText(target.textContent.trim(), button);
    });
  });
}

async function initializeRuntimeConfig() {
  try {
    runtime.config = await getJson('/data/site-config.json');
  } catch {
    runtime.config = { repositoryUrl: '', contactUrl: '' };
  }

  const repo = runtime.config.repositoryUrl || '';
  const contact = runtime.config.contactUrl || (repo ? `${repo}/discussions` : '');
  document.querySelectorAll('[data-repository-link]').forEach((anchor) => {
    if (repo) anchor.href = repo;
    else anchor.hidden = true;
  });
  document.querySelectorAll('[data-contact-link]').forEach((anchor) => {
    if (contact) anchor.href = contact;
    else anchor.hidden = true;
  });
  document.querySelectorAll('[data-repository-issue]').forEach((anchor) => {
    const kind = anchor.dataset.repositoryIssue;
    if (!repo) return;
    const templates = {
      question: 'research-question.yml',
      candidate: 'candidate.yml',
      challenge: 'challenge.yml',
      reproduction: 'reproduction.yml',
    };
    const titles = {
      challenge: 'Scientific challenge: ',
      build: 'Build proposal: ',
      explain: 'Explanation improvement: ',
    };
    anchor.href = templates[kind]
      ? `${repo}/issues/new?template=${encodeURIComponent(templates[kind])}`
      : `${repo}/issues/new?title=${encodeURIComponent(titles[kind] || '')}`;
  });

  if (repo) {
    document.querySelectorAll('[data-setup-command]').forEach((node) => {
      node.textContent = node.textContent
        .replace('YOUR_REPOSITORY_URL', repo)
        .replace('YOUR_REPOSITORY', repo.split('/').filter(Boolean).at(-1) || 'repository');
    });
  }
}

async function hydrateProjectStatus() {
  const targets = document.querySelectorAll('[data-status]');
  if (!targets.length) return;
  try {
    const status = await getJson('/data/project-status.json');
    targets.forEach((node) => {
      const key = node.dataset.status;
      if (Object.hasOwn(status, key)) node.textContent = status[key];
    });
  } catch (error) {
    console.warn(error);
  }
}

function renderMatrix(matrix) {
  const columns = matrix[0]?.length || 0;
  const cells = matrix.flat().map((value) => `<span>${escapeHtml(value)}</span>`).join('');
  return `<span class="metric-bracket left" aria-hidden="true"></span><span class="metric-grid-values" style="grid-template-columns:repeat(${columns},minmax(1.4rem,1fr))">${cells}</span><span class="metric-bracket right" aria-hidden="true"></span>`;
}

const plainCheckSummaries = {
  'schema.candidate.v1': 'The example file includes all required information.',
  'metric.dimension': 'The number grid is the right size.',
  'metric.symmetry': 'The number grid matches across its diagonal.',
  'metric.determinant': 'The number grid is usable, not collapsed.',
  'metric.inverse': 'The checker can reverse the number grid.',
  'coordinate_map.coordinates': 'The two coordinate lists match the declared conversion.',
  'coordinate_map.jacobian': 'The conversion can be reversed without collapsing a direction.',
  'coordinate_map.pullback': 'The converted number grid exactly matches the submitted one.',
  'minkowski.components': 'Every number matches the known flat-space answer.',
  'minkowski.signature': 'The plus and minus signs match the chosen rule.',
  'minkowski.cosmological_constant': 'The background-curvature value is zero, as expected here.',
  'minkowski.constant_components': 'The numbers do not change from place to place in this example.',
  'minkowski.connection': 'The coordinate-correction terms are zero, as expected here.',
  'minkowski.curvature': 'Every curvature test is zero: this space is flat.',
  'minkowski.vacuum_source': 'The result is consistent with empty space under these rules.',
};

function renderCheck(check, index) {
  const observed = formatValue(check.observed);
  const expected = formatValue(check.expected);
  return `<details class="check-card" ${index === 0 ? 'open' : ''}>
    <summary>${createPill(check.status === 'PASS' ? 'PASSED' : check.status)}<h3>${escapeHtml(plainCheckSummaries[check.check_id] || check.summary)}</h3></summary>
    <div class="check-body"><dl>
      <dt>Technical name</dt><dd><code>${escapeHtml(check.check_id)}</code></dd>
      <dt>Group</dt><dd>${escapeHtml(check.category)}</dd>
      <dt>How it was checked</dt><dd>${escapeHtml(check.method)}</dd>
      <dt>What this check covers</dt><dd>${escapeHtml(check.scope)}</dd>
      <dt>What we got</dt><dd><code>${escapeHtml(observed)}</code></dd>
      <dt>Expected answer</dt><dd><code>${escapeHtml(expected)}</code></dd>
    </dl></div>
  </details>`;
}

async function initializeLab() {
  if (!document.querySelector('[data-page="lab"]')) return;
  try {
    [runtime.candidate, runtime.result, runtime.coordinateCandidate, runtime.coordinateResult, runtime.coordinateCrosscheck, runtime.coordinatePassport, runtime.benchmark, runtime.crosscheck] = await Promise.all([
      getJson('/data/candidate.json'),
      getJson('/data/result.json'),
      getJson('/data/candidate-000002.json'),
      getJson('/data/result-000002.json'),
      getJson('/data/crosscheck-000002.json'),
      getJson('/data/benchmark-000002-passport.json'),
      getJson('/data/synthetic-suite-result.json'),
      getJson('/data/crosscheck.json'),
    ]);
    const { candidate, result } = runtime;
    setText('[data-candidate-title]', candidate.title);
    setText('[data-candidate-id]', candidate.candidate_id);
    setText('[data-candidate-version]', candidate.version);
    setText('[data-candidate-use]', candidate.intended_use === 'BENCHMARK' ? 'Known-answer practice test' : candidate.intended_use.replaceAll('_', ' '));
    setText('[data-candidate-status]', candidate.status === 'DRAFT' ? 'Early draft' : candidate.status.replaceAll('_', ' '));
    setText('[data-validation-profile]', candidate.validation_profile === 'benchmark.minkowski_cartesian_v1' ? 'Flat-spacetime check (version 1)' : candidate.validation_profile);
    setText('[data-lab-status]', result.assessment.overall_status === 'BASELINE_VERIFIED' ? 'KNOWN ANSWER PASSED' : result.assessment.overall_status.replaceAll('_', ' '));
    setText('[data-fingerprint]', result.scientific_payload_digest);
    setText('[data-metric-conventions]', 'We use four coordinates—time, left/right, forward/back, and up/down—with the standard -+++ sign rule. The background-curvature value is set to zero.');

    const matrix = document.querySelector('[data-metric-matrix]');
    if (matrix) matrix.innerHTML = renderMatrix(candidate.metric.components);

    const passed = result.checks.filter((check) => check.status === 'PASS').length;
    const failed = result.checks.filter((check) => check.status === 'FAIL').length;
    setText('[data-pass-count]', passed);
    setText('[data-fail-count]', failed);
    const checks = document.querySelector('[data-check-list]');
    if (checks) checks.innerHTML = result.checks.map(renderCheck).join('');

    const established = document.querySelector('[data-established-list]');
    if (established) {
      established.innerHTML = [
        `This exact flat-space example passed all ${passed} checks built for it.`,
        'The checker found the expected answer: no curvature and no matter-energy in this empty-space example.',
        'The saved result ID will change if any important input or output changes.',
        'This confirms the starter test works. It does not confirm a new physics idea.',
      ].map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    }
    const limitations = document.querySelector('[data-limitations-list]');
    if (limitations) limitations.innerHTML = [
      'This first panel checks one simple, exact representation; the second benchmark below adds only one declared constant coordinate conversion.',
      "It cannot yet solve general versions of Einstein's equations.",
      'It has not tested stability, cause-and-effect problems, unusual matter, or whether anything can be built.',
      'Passing this test is a software milestone—not evidence for warp travel or a route to Mars.',
    ].map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    initializeBenchmarkLadder();
    initializeEvidenceCube();
  } catch (error) {
    const main = document.querySelector('.lab-main');
    if (main) main.insertAdjacentHTML('afterbegin', `<div class="error-panel">${escapeHtml(error.message)}</div>`);
    setText('[data-lab-status]', 'Artifact unavailable');
  }

  const runButton = document.querySelector('[data-run-crosscheck]');
  if (runButton) runButton.addEventListener('click', runBrowserCrosscheck);
}

function initializeBenchmarkLadder() {
  const section = document.querySelector('[data-benchmark-ladder]');
  if (!section) return;
  const { candidate, coordinateCandidate, coordinateResult, coordinateCrosscheck, coordinatePassport } = runtime;
  if (!candidate || !coordinateCandidate || !coordinateResult || !coordinateCrosscheck || !coordinatePassport) return;
  const referenceMatrix = section.querySelector('[data-reference-metric]');
  const coordinateMatrix = section.querySelector('[data-coordinate-metric]');
  if (referenceMatrix) referenceMatrix.innerHTML = renderMatrix(candidate.metric.components);
  if (coordinateMatrix) coordinateMatrix.innerHTML = renderMatrix(coordinateCandidate.metric.components);
  const passed = coordinateResult.checks.filter((check) => check.status === 'PASS').length;
  const failed = coordinateResult.checks.filter((check) => check.status === 'FAIL').length;
  setText('[data-coordinate-title]', coordinateCandidate.title, section);
  setText('[data-coordinate-statement]', coordinateResult.assessment.statement, section);
  setText('[data-coordinate-status]', coordinateResult.assessment.overall_status === 'BENCHMARK_VERIFIED' ? 'KNOWN ANSWER PASSED' : coordinateResult.assessment.overall_status.replaceAll('_', ' '), section);
  setText('[data-coordinate-pass-count]', passed, section);
  setText('[data-coordinate-fail-count]', failed, section);
  setText('[data-coordinate-crosscheck]', `${coordinateCrosscheck.comparison === 'MATCH' ? 'MATCHED' : coordinateCrosscheck.comparison} ${Object.keys(coordinateCrosscheck.observations.checks).length}/${coordinateResult.checks.length} (same project)`, section);
  setText('[data-coordinate-review]', coordinatePassport.scientific_review === 'REQUESTED' ? 'REVIEW REQUESTED' : coordinatePassport.scientific_review.replaceAll('_', ' '), section);
}

function evidenceCubeFaces() {
  const { candidate, result, benchmark, crosscheck } = runtime;
  if (!candidate || !result || !benchmark || !crosscheck) return [];
  const passed = result.checks.filter((check) => check.status === 'PASS');
  const mathChecks = passed.filter((check) => ['mathematics', 'benchmark', 'analytic implication'].includes(check.category));
  return [
    {
      id: 'definition', label: 'Clear setup', status: result.checks.find((check) => check.check_id === 'schema.candidate.v1')?.status || 'UNRESOLVED', statusLabel: 'YES — FOR THIS TEST',
      question: 'Did we describe the example clearly enough for a computer to read it?',
      answer: 'Yes. The file includes a name, version, four coordinates, units, rules, and the exact test recipe.',
      evidence: `The system read ${candidate.candidate_id}, version ${candidate.version}, without finding a missing or malformed required field.`,
      limitation: 'A well-written idea can still be wrong. This only shows that the instructions are complete enough to test.',
      source: '/data/candidate.json', sourceLabel: 'See the exact submitted data',
    },
    {
      id: 'mathematics', label: 'Basic math', status: mathChecks.length === 10 ? 'PASS' : 'UNRESOLVED', statusLabel: mathChecks.length === 10 ? 'YES — FOR THIS TEST' : 'NOT YET',
      question: 'Does the basic math match the known answer for flat spacetime?',
      answer: `${mathChecks.length === 10 ? 'Yes' : 'Not yet'}. ${mathChecks.length} math checks agree with the expected flat-spacetime example.`,
      evidence: 'The checker tested the matrix size, symmetry, determinant, inverse, signs, connection, and curvature.',
      limitation: 'The second benchmark recognizes one declared constant coordinate rescaling. The checker still cannot infer arbitrary transformations or solve general spacetime equations.',
      source: '/data/result.json', sourceLabel: 'See the official saved result',
    },
    {
      id: 'numerics', label: 'Simulation', status: 'UNSUPPORTED', statusLabel: 'NOT TESTED',
      question: 'Did we test this with a full computer simulation?',
      answer: 'No. This version uses exact arithmetic for one simple example. It does not run a large numerical-relativity simulation.',
      evidence: `The 100 practice cases include ${benchmark.outcomes.UNRESOLVED || 0} honest "not enough information" answers instead of turning unsupported work into passes.`,
      limitation: 'We have no evidence yet about numerical stability, resolution, convergence, or complicated changing geometries.',
      source: '/data/synthetic-suite-result.json', sourceLabel: 'See the 100 practice-case results',
    },
    {
      id: 'physics', label: 'Physics meaning', status: 'UNRESOLVED', statusLabel: 'LIMITED ANSWER',
      question: 'What does this result tell us about real physics?',
      answer: 'Only that this known flat-space example behaves as expected under the limited rules we implemented.',
      evidence: 'For this example, the calculated curvature and matter-energy values are zero. That is the expected answer for empty, flat spacetime.',
      limitation: 'We did not test wormholes, warp travel, energy conditions, stability, cause-and-effect problems, or unusual matter.',
      source: '/data/result.json', sourceLabel: 'See the physics result and limits',
    },
    {
      id: 'reproduction', label: 'Checked twice', status: 'UNRESOLVED', statusLabel: 'NOT INDEPENDENT',
      question: 'Did another person independently get the same result?',
      answer: `Not yet. A second code path inside this project ${crosscheck.comparison === 'MATCH' ? 'matched all 12 checks' : 'did not fully match'}, but that is not outside confirmation.`,
      evidence: `Two implementations in this repository compared ${Object.keys(crosscheck.observations.checks).length} named checks.`,
      limitation: 'A real independent reproduction needs another person, a separate setup, and their own recorded comparison.',
      source: '/data/crosscheck.json', sourceLabel: 'See how the second check was recorded',
    },
    {
      id: 'realizability', label: 'Buildable', status: 'NOT_APPLICABLE', statusLabel: 'NOT A DEVICE',
      question: 'Does this show that we can build a spacetime device?',
      answer: 'No. This example is a ruler for testing the software, not a machine design.',
      evidence: 'The project labels this example as a benchmark and makes no transportation claim.',
      limitation: 'There is no device design, material plan, energy budget, experiment, or route to Mars.',
      source: '/data/result.json', sourceLabel: 'See the official claim boundary',
    },
  ];
}

function initializeEvidenceCube() {
  const container = document.querySelector('[data-evidence-cube]');
  if (!container) return;
  const visual = container.querySelector('[data-cube-visual]');
  const detail = container.querySelector('[data-cube-detail]');
  const controls = [...container.querySelectorAll('[data-cube-select]')];
  const summary = document.querySelector('[data-cube-summary]');
  const faces = evidenceCubeFaces();
  const render = (id, moveFocus = false) => {
    const face = faces.find((item) => item.id === id) || faces[0];
    visual.dataset.activeFace = face.id;
    controls.forEach((button) => {
      const selected = button.dataset.cubeSelect === face.id;
      button.setAttribute('aria-selected', String(selected));
      button.classList.toggle('active', selected);
      if (moveFocus && selected) button.focus();
    });
    detail.innerHTML = `<div class="cube-detail-heading"><div><p class="eyebrow">${escapeHtml(face.label)}</p><h3>${escapeHtml(face.question)}</h3></div><span class="pill ${statusClass(face.status)}">${escapeHtml(face.statusLabel)}</span></div>
      <p class="cube-answer">${escapeHtml(face.answer)}</p>
      <dl><div><dt>What we checked</dt><dd>${escapeHtml(face.evidence)}</dd></div><div><dt>What we still cannot claim</dt><dd>${escapeHtml(face.limitation)}</dd></div></dl>
      <a class="button secondary" href="${withBase(face.source)}">${escapeHtml(face.sourceLabel)}</a>`;
  };
  controls.forEach((button, index) => {
    button.addEventListener('click', () => render(button.dataset.cubeSelect));
    button.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      let next = index;
      if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = controls.length - 1;
      else next = (index + (event.key === 'ArrowLeft' || event.key === 'ArrowUp' ? -1 : 1) + controls.length) % controls.length;
      render(controls[next].dataset.cubeSelect, true);
    });
  });
  if (summary) summary.innerHTML = faces.map((face) => `<article><div><strong>${escapeHtml(face.label)}</strong><span class="pill ${statusClass(face.status)}">${escapeHtml(face.statusLabel)}</span></div><p>${escapeHtml(face.question)}</p><small>${escapeHtml(face.answer)}</small></article>`).join('');
  render('definition');
}

function determinant(matrix) {
  const work = matrix.map((row) => row.map(Number));
  let det = 1;
  for (let column = 0; column < work.length; column += 1) {
    let pivot = column;
    for (let row = column + 1; row < work.length; row += 1) {
      if (Math.abs(work[row][column]) > Math.abs(work[pivot][column])) pivot = row;
    }
    if (Math.abs(work[pivot][column]) < Number.EPSILON) return 0;
    if (pivot !== column) {
      [work[pivot], work[column]] = [work[column], work[pivot]];
      det *= -1;
    }
    const pivotValue = work[column][column];
    det *= pivotValue;
    for (let row = column + 1; row < work.length; row += 1) {
      const factor = work[row][column] / pivotValue;
      for (let col = column + 1; col < work.length; col += 1) work[row][col] -= factor * work[column][col];
    }
  }
  return det;
}

function isSymmetric(matrix) {
  return matrix.every((row, i) => row.every((value, j) => value === matrix[j]?.[i]));
}

function matrixEquals(a, b) {
  return a.length === b.length && a.every((row, i) => row.length === b[i]?.length && row.every((value, j) => value === b[i][j]));
}

async function runBrowserCrosscheck() {
  const button = document.querySelector('[data-run-crosscheck]');
  const progress = document.querySelector('[data-browser-progress]');
  const log = document.querySelector('[data-browser-log]');
  const status = document.querySelector('[data-browser-status]');
  if (!runtime.candidate || !button || !progress || !log || !status) return;

  button.disabled = true;
  log.innerHTML = '';
  status.textContent = 'Checking five simple properties…';
  const matrix = runtime.candidate.metric.components;
  const expected = [[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]];
  const checks = [
    ['The number grid has four rows', matrix.length === 4],
    ['Each row contains four numbers', matrix.every((row) => row.length === 4)],
    ['The grid matches across its diagonal', isSymmetric(matrix)],
    ['The grid is usable, not collapsed', Math.abs(determinant(matrix)) > Number.EPSILON],
    ['Every number matches the known flat-space answer', matrixEquals(matrix, expected)],
  ];

  for (let index = 0; index < checks.length; index += 1) {
    const [label, passed] = checks[index];
    await new Promise((resolve) => window.setTimeout(resolve, 180));
    const item = document.createElement('li');
    item.textContent = `${passed ? 'PASS' : 'FAIL'} — ${label}`;
    log.append(item);
    progress.style.width = `${((index + 1) / checks.length) * 100}%`;
  }

  const failures = checks.filter(([, passed]) => !passed).length;
  status.textContent = failures === 0 ? '5 quick checks passed' : `${failures} quick checks failed`;
  button.textContent = 'Run again';
  button.disabled = false;
}

function graphColor(type) {
  const map = {
    ResearchQuestion: '#64e9e4',
    Hypothesis: '#8bb8ff',
    Challenge: '#ffcc74',
    CandidateFamily: '#b8f16d',
    Candidate: '#b8f16d',
    Validator: '#c0a8ff',
    Run: '#64e9e4',
    Claim: '#effcfc',
    ReproductionQueue: '#ff8f85',
    SearchPolicy: '#8bb8ff',
  };
  return map[type] || '#a7bdc0';
}

function graphPositions(nodes) {
  const positions = new Map();
  const columns = [
    ['Challenge', 'ResearchQuestion'],
    ['Hypothesis', 'CandidateFamily'],
    ['Candidate', 'SearchPolicy'],
    ['Run', 'Validator'],
    ['Claim', 'ReproductionQueue'],
  ];
  columns.forEach((types, columnIndex) => {
    const columnNodes = nodes.filter((node) => types.includes(node.type));
    columnNodes.forEach((node, rowIndex) => {
      const x = 90 + columnIndex * 195;
      const y = columnNodes.length === 1 ? 300 : 175 + rowIndex * 250;
      positions.set(node.id, { x, y });
    });
  });
  nodes.filter((node) => !positions.has(node.id)).forEach((node, index) => {
    positions.set(node.id, { x: 100 + (index % 5) * 190, y: 100 + Math.floor(index / 5) * 230 });
  });
  return positions;
}

function renderGraphDetail(node, graph) {
  const detail = document.querySelector('[data-graph-detail]');
  if (!detail) return;
  const relationships = graph.edges.filter((edge) => edge.source === node.id || edge.target === node.id);
  detail.innerHTML = `<p class="eyebrow">Selected object</p>
    <h2>${escapeHtml(node.label)}</h2>
    ${createPill(node.status)}
    <p>${escapeHtml(node.summary)}</p>
    <dl>
      <div><dt>ID</dt><dd><code>${escapeHtml(node.id)}</code></dd></div>
      <div><dt>Type</dt><dd>${escapeHtml(node.type)}</dd></div>
      <div><dt>Authority</dt><dd>${node.canonical ? 'Canonical snapshot object' : 'Working-memory object'}</dd></div>
      <div><dt>Direct relationships</dt><dd>${relationships.length}</dd></div>
    </dl>
    ${relationships.length ? `<h3>Connected evidence</h3><ul class="clean-list">${relationships.map((edge) => {
      const otherId = edge.source === node.id ? edge.target : edge.source;
      const other = graph.nodes.find((item) => item.id === otherId);
      return `<li><strong>${escapeHtml(edge.relationship.replaceAll('_', ' '))}</strong><br>${escapeHtml(other?.label || otherId)}</li>`;
    }).join('')}</ul>` : ''}
    ${node.href ? `<a class="button secondary full" href="${withBase(node.href)}">Open related artifact</a>` : ''}`;
}

function drawGraph(graph, nodes) {
  const svg = document.querySelector('[data-graph-canvas]');
  if (!svg) return;
  const nodeIds = new Set(nodes.map((node) => node.id));
  const edges = graph.edges.filter((edge) => nodeIds.has(edge.source) && nodeIds.has(edge.target));
  const positions = graphPositions(nodes);
  svg.replaceChildren();

  edges.forEach((edge) => {
    const source = positions.get(edge.source);
    const target = positions.get(edge.target);
    if (!source || !target) return;
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', source.x);
    line.setAttribute('y1', source.y);
    line.setAttribute('x2', target.x);
    line.setAttribute('y2', target.y);
    line.setAttribute('class', 'graph-edge');
    line.dataset.edgeId = edge.id;
    svg.append(line);
  });

  nodes.forEach((node) => {
    const point = positions.get(node.id);
    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    group.setAttribute('class', 'graph-node');
    group.setAttribute('tabindex', '0');
    group.setAttribute('role', 'button');
    group.setAttribute('aria-label', `${node.type}: ${node.label}, status ${node.status}`);
    group.dataset.nodeId = node.id;
    group.setAttribute('transform', `translate(${point.x} ${point.y})`);

    const halo = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    halo.setAttribute('r', '17');
    halo.setAttribute('fill', 'transparent');
    halo.setAttribute('stroke', node.canonical ? graphColor(node.type) : '#718b8f');
    halo.setAttribute('stroke-dasharray', node.canonical ? '0' : '4 4');
    halo.setAttribute('opacity', '0.35');
    group.append(halo);

    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('r', '9');
    circle.setAttribute('fill', graphColor(node.type));
    circle.setAttribute('stroke', graphColor(node.type));
    group.append(circle);

    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', '0');
    label.setAttribute('y', '34');
    label.setAttribute('text-anchor', 'middle');
    const words = node.label.split(' ');
    const lines = [];
    let current = '';
    words.forEach((word) => {
      if (`${current} ${word}`.trim().length > 22) {
        lines.push(current.trim());
        current = word;
      } else current = `${current} ${word}`;
    });
    if (current.trim()) lines.push(current.trim());
    lines.slice(0, 3).forEach((text, index) => {
      const tspan = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
      tspan.setAttribute('x', '0');
      tspan.setAttribute('dy', index === 0 ? '0' : '14');
      tspan.textContent = text;
      label.append(tspan);
    });
    group.append(label);

    const select = () => {
      svg.querySelectorAll('.graph-node').forEach((item) => item.classList.toggle('active', item === group));
      svg.querySelectorAll('.graph-edge').forEach((item) => {
        const edge = graph.edges.find((candidate) => candidate.id === item.dataset.edgeId);
        item.classList.toggle('active', edge?.source === node.id || edge?.target === node.id);
      });
      renderGraphDetail(node, graph);
    };
    group.addEventListener('click', select);
    group.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        select();
      }
    });
    svg.append(group);
  });
}

async function initializeGraph() {
  if (!document.querySelector('[data-page="graph"]')) return;
  try {
    runtime.graph = await getJson('/data/knowledge-graph.json');
    const graph = runtime.graph;
    const search = document.querySelector('[data-graph-search]');
    const filter = document.querySelector('[data-graph-filter]');
    const canonical = document.querySelector('[data-graph-canonical]');
    const count = document.querySelector('[data-graph-count]');
    const list = document.querySelector('[data-graph-list]');
    const types = [...new Set(graph.nodes.map((node) => node.type))].sort();
    types.forEach((type) => {
      const option = document.createElement('option');
      option.value = type;
      option.textContent = type.replace(/([a-z])([A-Z])/g, '$1 $2');
      filter.append(option);
    });

    const render = () => {
      const query = search.value.trim().toLowerCase();
      const selectedType = filter.value;
      const canonicalOnly = canonical.checked;
      const nodes = graph.nodes.filter((node) => {
        const matchesText = !query || [node.id, node.type, node.label, node.status, node.summary].join(' ').toLowerCase().includes(query);
        const matchesType = selectedType === 'all' || node.type === selectedType;
        return matchesText && matchesType && (!canonicalOnly || node.canonical);
      });
      count.textContent = `${nodes.length} of ${graph.nodes.length} nodes`;
      drawGraph(graph, nodes);
      list.innerHTML = nodes.map((node) => `<button type="button" data-node-list-id="${escapeHtml(node.id)}"><strong>${escapeHtml(node.label)}</strong><small>${escapeHtml(node.type)} · ${escapeHtml(node.status)}</small></button>`).join('') || '<p class="empty-state">No nodes match the current filters.</p>';
      list.querySelectorAll('[data-node-list-id]').forEach((button) => {
        button.addEventListener('click', () => {
          const node = graph.nodes.find((item) => item.id === button.dataset.nodeListId);
          if (node) renderGraphDetail(node, graph);
        });
      });
      if (nodes.length) renderGraphDetail(nodes[0], graph);
    };
    [search, filter, canonical].forEach((control) => control.addEventListener('input', render));
    render();
  } catch (error) {
    setText('[data-graph-count]', 'Graph unavailable');
    const detail = document.querySelector('[data-graph-detail]');
    if (detail) detail.innerHTML = `<div class="error-panel">${escapeHtml(error.message)}</div>`;
  }
}

async function initializeAgents() {
  const grid = document.querySelector('[data-agent-grid]');
  if (!grid) return;
  try {
    runtime.agents = await getJson('/data/agents.json');
    grid.insertAdjacentHTML('beforebegin', `<p class="agent-principle">${escapeHtml(runtime.agents.principle)}</p>`);
    grid.innerHTML = runtime.agents.agents.map((agent) => `<article class="agent-card">
      <header><div><span class="agent-stage">${escapeHtml(agent.stage)}</span><h2>${escapeHtml(agent.name)}</h2></div>${createPill(agent.status)}</header>
      <p>${escapeHtml(agent.purpose)}</p>
      <div class="agent-permissions"><div><h3>May</h3><ul>${agent.may.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></div><div><h3>May not</h3><ul>${agent.may_not.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></div></div>
    </article>`).join('');
  } catch (error) {
    grid.innerHTML = `<div class="error-panel">${escapeHtml(error.message)}</div>`;
  }
}

async function initializeRoadmap() {
  const container = document.querySelector('[data-roadmap]');
  if (!container) return;
  try {
    runtime.roadmap = await getJson('/data/roadmap.json');
    container.innerHTML = runtime.roadmap.phases.map((phase) => `<article class="roadmap-phase">
      <span>${escapeHtml(phase.id)}</span><div><h2>${escapeHtml(phase.title)}</h2><p>${escapeHtml(phase.outcome)}</p></div>${createPill(phase.status)}
    </article>`).join('');
  } catch (error) {
    container.innerHTML = `<div class="error-panel">${escapeHtml(error.message)}</div>`;
  }
}

function programStatusLabel(status) {
  const labels = {
    PASS: 'WORKING NOW',
    FAIL: 'FAILED',
    NOT_IMPLEMENTED: 'NOT BUILT',
    NOT_EVALUATED: 'NOT TESTED',
    UNRESOLVED: 'UNKNOWN',
  };
  return labels[status] || status.replaceAll('_', ' ');
}

async function initializeResearchProgram() {
  const question = document.querySelector('[data-program-question]');
  const summaries = [...document.querySelectorAll('[data-program-summary]')];
  const gates = document.querySelector('[data-program-gates]');
  if (!question && !summaries.length && !gates) return;
  try {
    runtime.program = await getJson('/data/research-program.json');
    if (question) question.textContent = runtime.program.research_question;
    summaries.forEach((node) => {
      const value = runtime.program.public_summary[node.dataset.programSummary];
      if (value) node.textContent = value;
    });
    if (gates) {
      gates.innerHTML = runtime.program.success_gates.map((gate) => `<article><span>${escapeHtml(gate.id)}</span><h3>${escapeHtml(gate.question)}</h3><div class="program-gate-status"><span class="pill ${statusClass(gate.status)}">${escapeHtml(programStatusLabel(gate.status))}</span></div><p>${escapeHtml(gate.evidence.length ? `Evidence: ${gate.evidence.join(', ')}` : gate.downgrade_condition)}</p></article>`).join('');
    }
  } catch (error) {
    if (gates) gates.innerHTML = `<div class="error-panel">${escapeHtml(error.message)}</div>`;
  }
}

function inlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => `<a href="${escapeHtml(href)}">${label}</a>`);
}

function markdownToHtml(markdown) {
  const lines = markdown.replaceAll('\r\n', '\n').split('\n');
  const output = [];
  let inCode = false;
  let code = [];
  let listType = null;
  let table = [];

  const closeList = () => {
    if (listType) output.push(`</${listType}>`);
    listType = null;
  };
  const flushTable = () => {
    if (!table.length) return;
    const [header, , ...rows] = table;
    const cells = (row) => row.split('|').slice(1, -1).map((cell) => cell.trim());
    output.push(`<div style="overflow-x:auto"><table><thead><tr>${cells(header).map((cell) => `<th>${inlineMarkdown(cell)}</th>`).join('')}</tr></thead><tbody>${rows.map((row) => `<tr>${cells(row).map((cell) => `<td>${inlineMarkdown(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`);
    table = [];
  };

  lines.forEach((line) => {
    if (line.trim().startsWith('```')) {
      flushTable(); closeList();
      if (inCode) {
        output.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`);
        code = [];
      }
      inCode = !inCode;
      return;
    }
    if (inCode) { code.push(line); return; }
    if (line.trim().startsWith('|')) {
      closeList(); table.push(line); return;
    }
    flushTable();
    if (!line.trim()) { closeList(); return; }
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      closeList();
      const level = heading[1].length;
      output.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      return;
    }
    const unordered = line.match(/^[-*]\s+(.+)$/);
    if (unordered) {
      if (listType !== 'ul') { closeList(); output.push('<ul>'); listType = 'ul'; }
      output.push(`<li>${inlineMarkdown(unordered[1])}</li>`);
      return;
    }
    const ordered = line.match(/^\d+\.\s+(.+)$/);
    if (ordered) {
      if (listType !== 'ol') { closeList(); output.push('<ol>'); listType = 'ol'; }
      output.push(`<li>${inlineMarkdown(ordered[1])}</li>`);
      return;
    }
    if (line.startsWith('> ')) {
      closeList(); output.push(`<blockquote>${inlineMarkdown(line.slice(2))}</blockquote>`); return;
    }
    closeList(); output.push(`<p>${inlineMarkdown(line)}</p>`);
  });
  flushTable(); closeList();
  return output.join('\n');
}

async function initializeReports() {
  const view = document.querySelector('[data-report-view]');
  if (!view) return;
  const buttons = [...document.querySelectorAll('[data-report-mode]')];
  const load = async (mode) => {
    buttons.forEach((button) => button.classList.toggle('active', button.dataset.reportMode === mode));
    view.innerHTML = '<p>Loading report…</p>';
    try {
      const markdown = await getText(`/data/report-${mode}.md`);
      view.innerHTML = markdownToHtml(markdown);
    } catch (error) {
      view.innerHTML = `<div class="error-panel">${escapeHtml(error.message)}</div>`;
    }
  };
  buttons.forEach((button) => button.addEventListener('click', () => load(button.dataset.reportMode)));
  load('beginner');
}

function initializeExternalLinks() {
  document.querySelectorAll('a[href^="http"]').forEach((anchor) => {
    if (!anchor.rel) anchor.rel = 'noreferrer';
    if (!anchor.target && !runtime.config?.repositoryUrl?.startsWith(anchor.origin)) anchor.target = '_blank';
  });
}

async function main() {
  initializeNavigation();
  initializeExplanationGroups();
  initializeCopyButtons();
  await initializeRuntimeConfig();
  initializeExternalLinks();
  await Promise.all([
    hydrateProjectStatus(),
    initializeLab(),
    initializeGraph(),
    initializeAgents(),
    initializeRoadmap(),
    initializeResearchProgram(),
    initializeReports(),
  ]);
}

main().catch((error) => console.error('Site initialization failed', error));
