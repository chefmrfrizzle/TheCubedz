const root = document.documentElement;
const basePath = normalizeBase(root.dataset.basePath || '');
const runtime = {
  candidate: null,
  result: null,
  benchmark: null,
  crosscheck: null,
  graph: null,
  agents: null,
  roadmap: null,
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
    const titles = {
      challenge: 'Scientific challenge: ',
      build: 'Build proposal: ',
      explain: 'Explanation improvement: ',
    };
    anchor.href = `${repo}/issues/new?title=${encodeURIComponent(titles[kind] || '')}`;
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

function renderCheck(check, index) {
  const observed = formatValue(check.observed);
  const expected = formatValue(check.expected);
  return `<details class="check-card" ${index === 0 ? 'open' : ''}>
    <summary>${createPill(check.status)}<h3>${escapeHtml(check.summary)}</h3></summary>
    <div class="check-body"><dl>
      <dt>Check ID</dt><dd><code>${escapeHtml(check.check_id)}</code></dd>
      <dt>Category</dt><dd>${escapeHtml(check.category)}</dd>
      <dt>Method</dt><dd>${escapeHtml(check.method)}</dd>
      <dt>Scope</dt><dd>${escapeHtml(check.scope)}</dd>
      <dt>Observed</dt><dd><code>${escapeHtml(observed)}</code></dd>
      <dt>Expected</dt><dd><code>${escapeHtml(expected)}</code></dd>
    </dl></div>
  </details>`;
}

async function initializeLab() {
  if (!document.querySelector('[data-page="lab"]')) return;
  try {
    [runtime.candidate, runtime.result, runtime.benchmark, runtime.crosscheck] = await Promise.all([
      getJson('/data/candidate.json'),
      getJson('/data/result.json'),
      getJson('/data/synthetic-suite-result.json'),
      getJson('/data/crosscheck.json'),
    ]);
    const { candidate, result } = runtime;
    setText('[data-candidate-title]', candidate.title);
    setText('[data-candidate-id]', candidate.candidate_id);
    setText('[data-candidate-version]', candidate.version);
    setText('[data-candidate-use]', candidate.intended_use);
    setText('[data-candidate-status]', candidate.status);
    setText('[data-validation-profile]', candidate.validation_profile);
    setText('[data-lab-status]', result.assessment.overall_status.replaceAll('_', ' '));
    setText('[data-fingerprint]', result.scientific_payload_digest);
    setText('[data-metric-conventions]', `${candidate.coordinate_system.name}; signature ${candidate.conventions.metric_signature}; ${candidate.conventions.units}; Λ = ${candidate.conventions.cosmological_constant}.`);

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
        result.assessment.statement,
        `${passed} implemented checks passed for the exact selected profile.`,
        `Validator ${result.validator.name} ${result.validator.version} produced a stable scientific payload digest.`,
        `Candidate file digest: sha256:${result.candidate.sha256}.`,
      ].map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    }
    const limitations = document.querySelector('[data-limitations-list]');
    if (limitations) limitations.innerHTML = result.limitations.map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    initializeEvidenceCube();
  } catch (error) {
    const main = document.querySelector('.lab-main');
    if (main) main.insertAdjacentHTML('afterbegin', `<div class="error-panel">${escapeHtml(error.message)}</div>`);
    setText('[data-lab-status]', 'Artifact unavailable');
  }

  const runButton = document.querySelector('[data-run-crosscheck]');
  if (runButton) runButton.addEventListener('click', runBrowserCrosscheck);
}

function evidenceCubeFaces() {
  const { candidate, result, benchmark, crosscheck } = runtime;
  if (!candidate || !result || !benchmark || !crosscheck) return [];
  const passed = result.checks.filter((check) => check.status === 'PASS');
  const mathChecks = passed.filter((check) => ['mathematics', 'benchmark', 'analytic implication'].includes(check.category));
  return [
    {
      id: 'definition', label: 'Definition', status: result.checks.find((check) => check.check_id === 'schema.candidate.v1')?.status || 'UNRESOLVED',
      summary: 'The submitted candidate is machine-readable under the current schema.',
      evidence: `${candidate.candidate_id}@${candidate.version} declares four coordinates, the ${candidate.validation_profile} profile, and explicit conventions.`,
      limitation: 'Schema validity establishes document shape and declared metadata. It does not establish physical possibility.',
      source: '/data/candidate.json', sourceLabel: 'Candidate JSON',
    },
    {
      id: 'mathematics', label: 'Mathematics', status: mathChecks.length === 8 ? 'PASS' : 'UNRESOLVED',
      summary: `${mathChecks.length} implemented mathematical, benchmark, and analytic checks pass for this exact representation.`,
      evidence: `The committed validator reports determinant, inverse, symmetry, exact components, signature, connection, and curvature implications within its named profile.`,
      limitation: 'This is not a general tensor engine and does not prove equivalence under arbitrary coordinate transformations.',
      source: '/data/result.json', sourceLabel: 'Canonical result',
    },
    {
      id: 'numerics', label: 'Numerics', status: 'UNSUPPORTED',
      summary: 'No numerical-relativity solver or convergence study is implemented.',
      evidence: `${benchmark.outcomes.UNRESOLVED || 0} synthetic workflow cases remain explicitly unresolved across all categories; unsupported capabilities are never converted into passes.`,
      limitation: 'The exact baseline uses rational arithmetic. It supplies no numerical stability, resolution, conditioning, or convergence evidence for general metrics.',
      source: '/data/synthetic-suite-result.json', sourceLabel: '100-case workflow benchmark',
    },
    {
      id: 'physics', label: 'Physics', status: 'UNRESOLVED',
      summary: 'The exact baseline is consistent with vacuum under the declared classical assumptions.',
      evidence: result.assessment.physical_status.replaceAll('_', ' '),
      limitation: 'Energy conditions, perturbative stability, causal structure, material models, and exotic candidates have not been evaluated.',
      source: '/data/result.json', sourceLabel: 'Scoped physical interpretation',
    },
    {
      id: 'reproduction', label: 'Reproduction', status: 'UNRESOLVED',
      summary: `A separate implementation path reports ${crosscheck.comparison}; no outside reproduction is recorded.`,
      evidence: `${crosscheck.implementation.method}. The comparison covers ${Object.keys(crosscheck.observations.checks).length} named checks.`,
      limitation: crosscheck.limitations.join(' '),
      source: '/data/crosscheck.json', sourceLabel: 'Implementation cross-check passport',
    },
    {
      id: 'realizability', label: 'Realizability', status: 'NOT_APPLICABLE',
      summary: 'Candidate 000001 is a benchmark, not a device or transportation proposal.',
      evidence: result.assessment.transportation_status.replaceAll('_', ' '),
      limitation: 'No engineering design, material requirement, energy budget, experiment, or route to Mars is claimed.',
      source: '/data/result.json', sourceLabel: 'Assessment boundary',
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
    detail.innerHTML = `<div class="cube-detail-heading"><div><p class="eyebrow">${escapeHtml(face.label)} face</p><h3>${escapeHtml(face.summary)}</h3></div>${createPill(face.status)}</div>
      <dl><div><dt>Evidence</dt><dd>${escapeHtml(face.evidence)}</dd></div><div><dt>Boundary</dt><dd>${escapeHtml(face.limitation)}</dd></div></dl>
      <a class="button secondary" href="${withBase(face.source)}">Open ${escapeHtml(face.sourceLabel)}</a>`;
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
  if (summary) summary.innerHTML = faces.map((face) => `<article><div><strong>${escapeHtml(face.label)}</strong>${createPill(face.status)}</div><p>${escapeHtml(face.summary)}</p></article>`).join('');
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
  status.textContent = 'Running scoped checks…';
  const matrix = runtime.candidate.metric.components;
  const expected = [[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]];
  const checks = [
    ['Matrix has four rows', matrix.length === 4],
    ['Every row has four components', matrix.every((row) => row.length === 4)],
    ['Matrix is symmetric', isSymmetric(matrix)],
    ['Determinant is non-zero', Math.abs(determinant(matrix)) > Number.EPSILON],
    ['Components match the declared exact baseline', matrixEquals(matrix, expected)],
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
  status.textContent = failures === 0 ? '5 convenience checks passed' : `${failures} convenience checks failed`;
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
    initializeReports(),
  ]);
}

main().catch((error) => console.error('Site initialization failed', error));
