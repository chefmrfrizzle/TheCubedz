export const navigation = [
  { href: '/', key: 'home', label: 'Overview' },
  { href: '/lab/', key: 'lab', label: 'Lab' },
  { href: '/graph/', key: 'graph', label: 'Graph' },
  { href: '/agents/', key: 'agents', label: 'Agents' },
  { href: '/method/', key: 'method', label: 'Method' },
  { href: '/learn/', key: 'learn', label: 'Learn' },
  { href: '/roadmap/', key: 'roadmap', label: 'Roadmap' },
  { href: '/contribute/', key: 'contribute', label: 'Contribute' },
];

const sourceCards = `
  <div class="source-grid">
    <a class="source-card" href="https://www.einsteintoolkit.org/" rel="noreferrer">
      <span class="eyebrow">Existing ecosystem</span><strong>Einstein Toolkit</strong>
      <span>Open community infrastructure for computational relativistic astrophysics and gravitational physics.</span>
    </a>
    <a class="source-card" href="https://www.grchombo.org/" rel="noreferrer">
      <span class="eyebrow">Existing ecosystem</span><strong>GRChombo / GRTL</strong>
      <span>Open numerical-relativity software for dynamical strong-gravity research.</span>
    </a>
    <a class="source-card" href="https://arxiv.org/abs/2404.03095" rel="noreferrer">
      <span class="eyebrow">Related research</span><strong>Warp Factory</strong>
      <span>A numerical framework for evaluating proposed warp-drive spacetime geometries.</span>
    </a>
    <a class="source-card" href="https://www.nasa.gov/humans-in-space/humans-to-mars/" rel="noreferrer">
      <span class="eyebrow">Benchmark context</span><strong>NASA: Humans to Mars</strong>
      <span>Public context for why Earth-to-Mars transportation remains a demanding engineering benchmark.</span>
    </a>
  </div>`;

export const pages = [
  {
    slug: '',
    key: 'home',
    title: 'TheCubedz',
    description: 'An open, reproducible experiment for representing, checking, challenging, and eventually searching mathematically defined spacetime candidates.',
    content: `
      <main id="main-content">
        <section class="hero shell section-pad">
          <div class="hero-copy">
            <div class="status-line"><span class="status-dot"></span> Public pre-alpha · open source · no transportation claim</div>
            <p class="eyebrow">A computational science experiment</p>
            <h1>Can we search spacetime systematically—and record exactly why ideas fail?</h1>
            <p class="hero-lede">This project turns speculative geometry into a reproducible workflow: define a candidate, run scoped validators, preserve the result, invite challenge, and learn where to search next.</p>
            <div class="hero-actions">
              <a class="button primary" href="/lab/">Inspect Candidate 000001</a>
              <a class="button secondary" href="/graph/">Open the evidence graph</a>
            </div>
            <p class="microcopy">The first milestone is deliberately ordinary: verify flat Minkowski spacetime before attempting anything exotic.</p>
          </div>
          <div class="hero-visual" aria-label="Conceptual Earth to Mars research diagram">
            <div class="coordinate-grid"></div>
            <div class="route-label route-label-earth">Earth</div>
            <div class="route-line"><span></span></div>
            <div class="route-label route-label-mars">Mars</div>
            <div class="state-cube" aria-hidden="true"><span class="cube-face cube-front"></span><span class="cube-face cube-back"></span><span class="cube-edge cube-edge-a"></span><span class="cube-edge cube-edge-b"></span><span class="cube-edge cube-edge-c"></span><span class="cube-edge cube-edge-d"></span></div>
            <div class="visual-caption"><span>Conventional question</span><strong>How do we cross the distance?</strong><span>Research question</span><strong>What configurations do the equations permit?</strong></div>
          </div>
        </section>

        <section class="status-band" aria-label="Current project status">
          <div class="shell metric-grid">
            <div class="metric"><span data-status="candidateCount">1</span><small>candidate defined</small></div>
            <div class="metric"><span data-status="checkCount">12</span><small>implemented checks passed</small></div>
            <div class="metric"><span data-status="novelClaimCount">0</span><small>novel physics claims</small></div>
            <div class="metric"><span data-status="reproductionCount">0</span><small>independent reproductions</small></div>
          </div>
        </section>

        <section class="shell section-pad split-section">
          <div>
            <p class="eyebrow">One idea, three levels</p>
            <h2>Understand the experiment without pretending the hard parts are simple.</h2>
            <p class="section-lede">Every verified object should be explainable to a curious beginner and inspectable by a technical contributor from the same underlying artifact.</p>
          </div>
          <div class="explanation-card" data-explanation-group>
            <div class="segmented" role="tablist" aria-label="Explanation level">
              <button class="segment active" type="button" data-level="simple" role="tab" aria-selected="true">Simple</button>
              <button class="segment" type="button" data-level="technical" role="tab" aria-selected="false">Technical</button>
              <button class="segment" type="button" data-level="researcher" role="tab" aria-selected="false">Researcher</button>
            </div>
            <div data-explanation="simple"><h3>Physics is the rulebook.</h3><p>We describe one possible arrangement, let deterministic mathematics inspect it, and save both the successes and failures. The computer may suggest the next puzzle piece. It does not get to declare itself correct.</p></div>
            <div data-explanation="technical" hidden><h3>Candidates are parameterized scientific objects.</h3><p>A candidate contains a metric, coordinates, conventions, assumptions, source model, and provenance. Versioned validators emit immutable results with explicit scope, methods, errors, limitations, and a content digest.</p></div>
            <div data-explanation="researcher" hidden><h3>The methodological hypothesis is measurable.</h3><p>Compare a versioned search policy against a frozen naive baseline on information gain, valid-candidate yield, calibration, computational cost, and reproducibility. Novelty is irrelevant until benchmark recovery and cross-validation succeed.</p></div>
          </div>
        </section>

        <section class="section-surface">
          <div class="shell section-pad">
            <p class="eyebrow">The operating loop</p>
            <h2>AI explores. Physics referees. Reproduction decides what survives.</h2>
            <div class="process-grid">
              <article><span>01</span><h3>Define</h3><p>Represent the candidate, assumptions, conventions, and falsification criteria.</p></article>
              <article><span>02</span><h3>Validate</h3><p>Run deterministic checks whose methods and boundaries are versioned.</p></article>
              <article><span>03</span><h3>Record</h3><p>Write an immutable result with provenance, warnings, and a scientific digest.</p></article>
              <article><span>04</span><h3>Challenge</h3><p>Invite reproductions, objections, cross-solver comparisons, and falsification attempts.</p></article>
              <article><span>05</span><h3>Map</h3><p>Connect sources, claims, candidates, results, failures, and corrections in a graph.</p></article>
              <article><span>06</span><h3>Learn</h3><p>Train only on named snapshots, evaluate offline, and promote a search policy through review.</p></article>
            </div>
          </div>
        </section>

        <section class="shell section-pad boundary-grid">
          <article class="boundary-card positive"><p class="eyebrow">What exists today</p><h2>A reproducible baseline pipeline.</h2><ul class="clean-list"><li>A typed Candidate 000001 record.</li><li>Twelve implemented deterministic checks.</li><li>Beginner and technical reports derived from one result.</li><li>An evidence ledger, knowledge graph, and controlled-learning design.</li><li>A public, mobile-responsive exploration surface.</li></ul></article>
          <article class="boundary-card caution"><p class="eyebrow">What does not exist today</p><h2>No wormhole. No warp device. No shortcut.</h2><ul class="clean-list"><li>No general numerical-relativity solver.</li><li>No exotic candidate has passed energy, stability, or causality review.</li><li>No physical realization or experiment has been proposed.</li><li>No independent reproduction has been recorded.</li><li>No AI model has been promoted as a scientific search policy.</li></ul></article>
        </section>

        <section class="section-surface" id="mars-benchmark">
          <div class="shell section-pad benchmark-layout">
            <div><p class="eyebrow">The motivating benchmark</p><h2>Earth → Mars is a question, not a promise.</h2><p class="section-lede">Mars turns an abstract optimization problem into something people can understand. The first public challenge is to create a trustworthy framework capable of comparing known candidate families—not to claim the route has been solved.</p></div>
            <div class="benchmark-card"><div><span>Baseline question</span><strong>Can the pipeline recover established results?</strong></div><div><span>Search question</span><strong>Can a policy find informative candidates efficiently?</strong></div><div><span>Long-horizon question</span><strong>Do any survivors deserve physical investigation?</strong></div><div><span>Current answer</span><strong>Only the first baseline is implemented.</strong></div></div>
          </div>
        </section>

        <section class="shell section-pad">
          <div class="section-intro"><p class="eyebrow">Reusable research protocol</p><h2>The strongest invention may be the way the system separates imagination from evidence.</h2><p class="section-lede narrow">The same ledger-and-validator pattern can be forked for materials discovery, engineering design spaces, robotics policies, mathematical conjectures, and other domains where proposals, tests, uncertainty, and reproduction must remain separate.</p></div>
          <div class="innovation-grid"><article><h3>Failure atlas</h3><p>Search every rejected configuration by reason, method, scope, and nearby parameter region.</p></article><article><h3>Adversarial review</h3><p>Make objections, failed reproductions, superseded claims, and retractions visible rather than burying them.</p></article><article><h3>Federated compute</h3><p>Later contributors can return signed result bundles from isolated runners instead of trusted prose.</p></article><article><h3>Uncertainty map</h3><p>Distinguish tested, rejected, contradictory, unresolved, and untouched regions—never one misleading promise score.</p></article></div>
        </section>

        <section class="section-surface"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">Related open ecosystems</p><h2>Build above existing scientific tools; do not pretend to replace them.</h2></div>${sourceCards}</div></section>
      </main>`,
  },
  {
    slug: 'lab', key: 'lab', title: 'Test the first example',
    description: 'See whether TheCubedz can correctly check the simplest known spacetime example, what passed, and what has not been tested yet.',
    content: `
      <main id="main-content" data-page="lab">
        <section class="shell page-hero section-pad compact"><div><p class="eyebrow">Try the first example</p><h1>Can the system correctly recognize ordinary, empty space?</h1><p class="hero-lede">We start with a known answer: flat spacetime, the simplest model used in relativity. If our checker cannot handle this example, it is not ready for harder ideas.</p></div><div class="page-status"><span class="status-dot"></span><strong data-lab-status>Loading result…</strong><small>This result applies only to this one example.</small></div></section>
        <section class="shell evidence-cube-section" aria-labelledby="evidence-cube-title">
          <div class="cube-intro"><div><p class="eyebrow">The answer cube</p><h2 id="evidence-cube-title">Turn the cube to see what we know—and what we do not.</h2></div><p>Each side asks one plain question. A green answer means that check passed. It never means the whole idea has been proven.</p></div>
          <div class="evidence-cube-panel" data-evidence-cube>
            <div class="cube-stage" aria-hidden="true">
              <div class="evidence-cube" data-cube-visual data-active-face="definition">
                <div class="evidence-cube-face cube-face-front"><span>Clear setup</span></div>
                <div class="evidence-cube-face cube-face-right"><span>Basic math</span></div>
                <div class="evidence-cube-face cube-face-back"><span>Simulation</span></div>
                <div class="evidence-cube-face cube-face-left"><span>Physics meaning</span></div>
                <div class="evidence-cube-face cube-face-top"><span>Checked twice</span></div>
                <div class="evidence-cube-face cube-face-bottom"><span>Buildable</span></div>
              </div>
            </div>
            <div class="cube-inspector">
              <div class="cube-face-nav" role="tablist" aria-label="Questions answered by the cube">
                <button type="button" role="tab" aria-selected="true" data-cube-select="definition">Clear setup</button>
                <button type="button" role="tab" aria-selected="false" data-cube-select="mathematics">Basic math</button>
                <button type="button" role="tab" aria-selected="false" data-cube-select="numerics">Simulation</button>
                <button type="button" role="tab" aria-selected="false" data-cube-select="physics">Physics meaning</button>
                <button type="button" role="tab" aria-selected="false" data-cube-select="reproduction">Checked twice</button>
                <button type="button" role="tab" aria-selected="false" data-cube-select="realizability">Buildable</button>
              </div>
              <article class="cube-detail" role="tabpanel" aria-live="polite" data-cube-detail><p>Loading answer…</p></article>
            </div>
          </div>
          <div class="cube-semantic-summary" data-cube-summary aria-label="Answers to all six cube questions"></div>
        </section>
        <section class="shell lab-layout section-pad-top" id="candidate">
          <aside class="lab-sidebar"><div class="sticky-panel"><p class="eyebrow">Example being tested</p><h2 data-candidate-title>Minkowski baseline</h2><dl class="metadata-list"><div><dt>Record name</dt><dd data-candidate-id>—</dd></div><div><dt>Version</dt><dd data-candidate-version>—</dd></div><div><dt>Why it exists</dt><dd data-candidate-use>—</dd></div><div><dt>Review stage</dt><dd data-candidate-status>—</dd></div><div><dt>Test recipe</dt><dd data-validation-profile>—</dd></div></dl><button class="button primary full" type="button" data-run-crosscheck>Check the basic math here</button><a class="button secondary full" href="/data/candidate.json">See the exact data file</a><p class="fine-print">This quick browser check is for learning. The saved Python result is the project's official record.</p></div></aside>
          <div class="lab-main">
            <section class="panel" id="metric"><div class="panel-heading"><div><p class="eyebrow">The numbers behind the example</p><h2>How flat spacetime is written</h2></div><span class="scope-tag">The exact numbers we tested</span></div><div class="metric-display" data-metric-matrix aria-label="Metric matrix">Loading…</div><p class="panel-note" data-metric-conventions>These numbers only have meaning when we also state the coordinates, units, and sign rules used to read them.</p></section>
            <section class="panel browser-run"><div class="panel-heading"><div><p class="eyebrow">Try it yourself</p><h2>Five quick checks in your browser</h2></div><strong data-browser-status>Ready</strong></div><div class="progress-track"><i data-browser-progress></i></div><ol class="run-log" data-browser-log><li>Press the button to check the matrix size, shape, symmetry, determinant, and expected values.</li></ol></section>
            <section class="panel" id="result"><div class="panel-heading"><div><p class="eyebrow">Official saved test</p><h2>All 12 checks</h2></div><div class="result-summary"><strong data-pass-count>—</strong><span>passed</span><strong data-fail-count>—</strong><span>failed</span></div></div><div class="check-list" data-check-list><p>Loading the saved result…</p></div></section>
            <section class="panel fingerprint-panel" id="validator"><div><p class="eyebrow">Result ID</p><h2>A fingerprint for this exact answer</h2><code data-fingerprint>Loading…</code><p>Change any important part of the example, checker, answer, warning, or limit and this long ID changes too. That makes silent changes easier to spot.</p></div><button class="button secondary" type="button" data-copy-target="[data-fingerprint]">Copy result ID</button></section>
            <section class="two-column-panels"><article class="panel positive"><p class="eyebrow">What this test shows</p><ul class="clean-list" data-established-list><li>Loading…</li></ul></article><article class="panel caution"><p class="eyebrow">What this test does not show</p><ul class="clean-list" data-limitations-list><li>Loading…</li></ul></article></section>
            <section class="panel reproduce-panel" id="reproduce"><div><p class="eyebrow">For developers: repeat the test</p><h2>A fresh copy should produce the same result ID.</h2></div><pre><code data-reproduction-command>python scripts/research.py verify candidates/CANDIDATE-000001.json --reproducible</code></pre><button class="button secondary" type="button" data-copy-target="[data-reproduction-command]">Copy command</button><p class="panel-note">Running our code again is a repeat, not independent proof. Independent confirmation needs another person, a separate setup, and their own saved comparison.</p></section>
          </div>
        </section>
      </main>`,
  },
  {
    slug: 'graph', key: 'graph', title: 'Evidence graph and second brain',
    description: 'Explore how questions, candidates, validators, runs, claims, reproductions, and search policies connect without allowing AI output to become truth.',
    content: `
      <main id="main-content" data-page="graph">
        <section class="shell page-hero section-pad compact"><div><p class="eyebrow">Durable research memory</p><h1>The model is replaceable. The evidence graph is the brain.</h1><p class="hero-lede">Every relationship should answer: what is connected, why, by which source or computation, and with what review state?</p></div><div class="page-status"><span class="status-dot"></span><strong>Graph snapshot 000001</strong><small>Canonical and working-memory objects are visually separated.</small></div></section>
        <section class="shell graph-workspace section-pad-top"><div class="graph-controls"><label>Search nodes<input type="search" data-graph-search placeholder="Candidate, claim, validator…"></label><label>Filter type<select data-graph-filter><option value="all">All types</option></select></label><label class="check-control"><input type="checkbox" data-graph-canonical> Canonical only</label><span class="graph-count" data-graph-count>Loading…</span></div><div class="graph-layout"><div class="graph-canvas-wrap"><svg class="graph-canvas" data-graph-canvas viewBox="0 0 980 600" role="img" aria-label="Interactive evidence graph"></svg><noscript><p class="noscript">JavaScript is required for the interactive graph. The raw snapshot remains available at <a href="/data/knowledge-graph.json">/data/knowledge-graph.json</a>.</p></noscript></div><aside class="graph-detail" data-graph-detail><p class="eyebrow">Selected object</p><h2>Choose a node</h2><p>Inspect its type, status, authority, summary, and direct relationships.</p></aside></div><div class="graph-list" data-graph-list aria-label="Accessible graph node list"></div></section>
        <section class="section-surface" id="learning-loop"><div class="shell section-pad"><p class="eyebrow">Controlled learning loop</p><h2>Observation becomes training data only through explicit gates.</h2><div class="loop-track"><div><span>1</span><strong>Ingest</strong><small>Evidence, candidates, runs, reproductions, telemetry</small></div><div><span>2</span><strong>Validate</strong><small>Schema, provenance, license, duplication, integrity</small></div><div><span>3</span><strong>Snapshot</strong><small>Immutable named dataset with exclusions</small></div><div><span>4</span><strong>Train offline</strong><small>Retriever, ranker, surrogate, explainer, search policy</small></div><div><span>5</span><strong>Benchmark</strong><small>Frozen holdouts, calibration, regressions, safety gates</small></div><div><span>6</span><strong>Review</strong><small>Promote, reject, or roll back with a model card</small></div></div></div></section>
        <section class="shell section-pad"><p class="eyebrow">Three memory tiers</p><div class="memory-grid"><article><span class="tier tier-a">A</span><h2>Canonical science</h2><p>Versioned candidates, deterministic results, reviewed evidence, reproductions, corrections, and retractions.</p><strong>May change scientific status.</strong></article><article><span class="tier tier-b">B</span><h2>Working research</h2><p>Hypotheses, agent proposals, unresolved extractions, candidate drafts, and challenge queues.</p><strong>May propose work—not truth.</strong></article><article><span class="tier tier-c">C</span><h2>Product telemetry</h2><p>Explanation choices, failed searches, voluntary clarity ratings, and interface friction.</p><strong>May improve UX—not physics.</strong></article></div></section>
        <section class="section-surface"><div class="shell section-pad boundary-grid"><article class="boundary-card positive"><p class="eyebrow">The useful kind of learning</p><h2>Choose more informative experiments.</h2><p>A search policy can learn which candidate regions are underexplored, anomalous, expensive, redundant, or likely to produce information. Every proposal keeps the policy version and input snapshot that generated it.</p></article><article class="boundary-card caution"><p class="eyebrow">The forbidden shortcut</p><h2>Never train popularity into physical truth.</h2><p>Clicks, votes, repeated agent statements, and exciting language cannot determine whether an equation is satisfied, a solver converged, or a result was independently reproduced.</p></article></div></section>
      </main>`,
  },
  {
    slug: 'agents', key: 'agents', title: 'Bounded research agents',
    description: 'Inspect the proposed agent system, its scientific responsibilities, permissions, prohibitions, and human approval gates.',
    content: `
      <main id="main-content" data-page="agents">
        <section class="shell page-hero section-pad compact"><div><p class="eyebrow">Bounded agent system</p><h1>Specialists can propose work. None can promote their own claims.</h1><p class="hero-lede">The goal is not a single omniscient agent. It is a reviewable team whose permissions mirror the scientific method.</p></div><div class="page-status"><span class="status-dot"></span><strong>9 bounded roles</strong><small>Only the baseline math and explainer roles are partially implemented.</small></div></section>
        <section class="shell section-pad-top"><div class="agent-grid" data-agent-grid><p>Loading agent contracts…</p></div></section>
        <section class="section-surface"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">Orchestration contract</p><h2>Every agent handoff produces a typed artifact.</h2></div><div class="orchestration-flow"><div><span>1</span><strong>Question</strong><small>research brief + scope</small></div><i>→</i><div><span>2</span><strong>Evidence</strong><small>sources + claim extracts</small></div><i>→</i><div><span>3</span><strong>Candidate</strong><small>schema + assumptions</small></div><i>→</i><div><span>4</span><strong>Validation</strong><small>solver output + limits</small></div><i>→</i><div><span>5</span><strong>Challenge</strong><small>objections + failure tests</small></div><i>→</i><div><span>6</span><strong>Review</strong><small>human status decision</small></div></div></div></section>
        <section class="shell section-pad boundary-grid"><article class="boundary-card positive"><p class="eyebrow">Agents are useful for</p><h2>Search, translation, triage, and experiment design.</h2><ul class="clean-list"><li>Finding and structuring relevant literature.</li><li>Drafting schema-conforming candidates.</li><li>Preparing deterministic solver jobs.</li><li>Finding contradictions and missing assumptions.</li><li>Explaining one result at multiple levels.</li><li>Ranking where computation may be informative next.</li></ul></article><article class="boundary-card caution"><p class="eyebrow">Agents are not allowed to</p><h2>Become the scientific authority.</h2><ul class="clean-list"><li>Invent citations or hide provenance.</li><li>Call a proposal valid before deterministic checks.</li><li>Upgrade a claim from generated prose.</li><li>Rewrite or delete canonical history.</li><li>Train on live clicks as a physics signal.</li><li>Approve their own model promotion.</li></ul></article></section>
        <section class="section-surface"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">Copy-pasteable operating system</p><h2>The repository contains prompts, schemas, and authority rules for coding and research agents.</h2><p class="section-lede">Agents should receive one bounded role, explicit inputs, required outputs, forbidden actions, validation commands, and a definition of done. The orchestrator records every handoff.</p></div><a class="button primary" href="/contribute/#agent-prompts">Open the agent build prompts</a></div></section>
      </main>`,
  },
  {
    slug: 'method', key: 'method', title: 'Scientific method and claims policy',
    description: 'The methodological hypothesis, objective functions, physics gates, falsification rules, and escalating definitions of success.',
    content: `
      <main id="main-content">
        <section class="shell page-hero section-pad compact"><div><p class="eyebrow">Methodology</p><h1>Search the possibility space. Refuse to grade our own imagination.</h1><p class="hero-lede">The project is a laboratory notebook, a map, and a student. The notebook and map are permanent. The student can be replaced.</p></div></section>
        <section class="shell section-pad-top split-section" id="hypothesis"><div><p class="eyebrow">The hypothesis</p><h2>Systematic search may reveal useful structure in a space too large for isolated manual proposals.</h2></div><blockquote class="hypothesis-card">There may exist mathematically admissible configurations of geometry, matter, fields, and boundary conditions with transportation-relevant properties, and a reproducible computational search process may map that space more effectively than proposing one geometry at a time.</blockquote></section>
        <section class="section-surface"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">The search problem</p><h2>Optimize for information—not a predetermined wormhole.</h2></div><div class="equation-card"><code>x* = arg min<sub>x</sub> [w<sub>t</sub>T + w<sub>e</sub>E + w<sub>v</sub>V + w<sub>s</sub>S + w<sub>c</sub>C + w<sub>r</sub>R]</code><p>Travel cost, energy, physical-law violations, instability, causality problems, and engineering unrealizability remain separate terms. The weights and constraints are versioned experiment inputs—not hidden product magic.</p></div></div></section>
        <section class="shell section-pad"><div class="section-intro"><p class="eyebrow">Physics referee</p><h2>A candidate moves through independent gates.</h2></div><div class="gate-grid"><article><span>1</span><h3>Definition</h3><p>Coordinates, conventions, metric, parameters, assumptions, provenance.</p></article><article><span>2</span><h3>Mathematics</h3><p>Constraint satisfaction, convergence, residuals, coordinate consistency.</p></article><article><span>3</span><h3>Source requirements</h3><p>Stress-energy or matter model implied by the geometry.</p></article><article><span>4</span><h3>Physical constraints</h3><p>Energy conditions, quantum bounds, conservation laws.</p></article><article><span>5</span><h3>Dynamics</h3><p>Stability, perturbations, horizons, singularities, controllability.</p></article><article><span>6</span><h3>Causality</h3><p>Closed causal curves, chronology issues, global consistency.</p></article><article><span>7</span><h3>Realizability</h3><p>Known matter, fields, materials, fabrication, measurement.</p></article><article><span>8</span><h3>Experiment</h3><p>Testable prediction, uncertainty, independent observation.</p></article></div></section>
        <section class="section-surface"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">Escalating success</p><h2>The project can succeed long before a transportation device exists.</h2></div><ol class="success-ladder"><li><span>0</span><div><strong>Baseline reproduction</strong><p>Known simple spacetimes produce expected properties.</p></div></li><li><span>1</span><div><strong>Benchmark recovery</strong><p>The engine recovers established candidate families it was not explicitly hard-coded to imitate.</p></div></li><li><span>2</span><div><strong>Search efficiency</strong><p>A transparent policy outperforms a defined naive baseline.</p></div></li><li><span>3</span><div><strong>Useful optimization</strong><p>The system improves a known family under declared constraints.</p></div></li><li><span>4</span><div><strong>Novel mathematical result</strong><p>A new candidate survives internal and external theoretical scrutiny.</p></div></li><li><span>5</span><div><strong>Novel reproduced result</strong><p>Independent implementations recover it within tolerance.</p></div></li><li><span>6</span><div><strong>Experimental prediction</strong><p>The theory predicts a measurable effect.</p></div></li><li><span>7</span><div><strong>Experimental support</strong><p>Independent observations support the prediction.</p></div></li></ol></div></section>
        <section class="shell section-pad boundary-grid"><article class="boundary-card positive"><p class="eyebrow">Falsification first</p><h2>Every claim carries its downgrade condition.</h2><p>A contribution is stronger when it explains what evidence, derivation, resolution test, or independent reproduction would cause the claim to be rejected.</p></article><article class="boundary-card caution"><p class="eyebrow">No universal score</p><h2>“Works” is not a scientific status.</h2><p>Mathematical consistency, physical admissibility, stability, causality, and engineering realizability remain separate assessments with different evidence.</p></article></section>
        <section class="section-surface"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">Research context</p><h2>The project begins as an orchestration and evidence layer above established tools.</h2></div>${sourceCards}</div></section>
      </main>`,
  },
  {
    slug: 'learn', key: 'learn', title: 'Learn the experiment',
    description: 'Plain-language and technical explanations of spacetime metrics, stress-energy, validators, reproduction, evidence graphs, and controlled learning.',
    content: `
      <main id="main-content" data-page="learn">
        <section class="shell page-hero section-pad compact"><div><p class="eyebrow">Learn the experiment</p><h1>The same evidence, explained at the level you need.</h1><p class="hero-lede">Explanations may change vocabulary and analogy. They may not change raw fields, status, uncertainty, provenance, or limitations.</p></div></section>
        <section class="shell section-pad-top concept-stack">
          <article class="concept-card" data-explanation-group><div class="concept-heading"><div><p class="eyebrow">Concept 01</p><h2>The Rubik's Cube analogy</h2></div><div class="segmented small"><button class="segment active" data-level="simple" type="button">Simple</button><button class="segment" data-level="technical" type="button">Technical</button></div></div><div data-explanation="simple"><p>Physics supplies the legal moves. A candidate is one arrangement. A validator checks only the rules it knows. Every failure colors in another part of the map.</p></div><div data-explanation="technical" hidden><p>The state space contains parameterized geometries, source models, fields, and boundary conditions. The project records validator predicates, outputs, scope, and provenance for each sampled point.</p></div></article>
          <article class="concept-card" data-explanation-group><div class="concept-heading"><div><p class="eyebrow">Concept 02</p><h2>Metric tensor</h2></div><div class="segmented small"><button class="segment active" data-level="simple" type="button">Simple</button><button class="segment" data-level="technical" type="button">Technical</button></div></div><div data-explanation="simple"><p>A mathematical rule describing how distance and time intervals are measured in a region of spacetime.</p></div><div data-explanation="technical" hidden><p>A symmetric rank-(0,2) tensor g<sub>μν</sub> defining the line element and local causal structure under declared coordinates and signature conventions.</p></div></article>
          <article class="concept-card" data-explanation-group><div class="concept-heading"><div><p class="eyebrow">Concept 03</p><h2>Stress-energy tensor</h2></div><div class="segmented small"><button class="segment active" data-level="simple" type="button">Simple</button><button class="segment" data-level="technical" type="button">Technical</button></div></div><div data-explanation="simple"><p>A ledger of energy, momentum, pressure, and stress—the things that source curvature in general relativity.</p></div><div data-explanation="technical" hidden><p>T<sub>μν</sub> encodes energy density, momentum density and flux, pressure, and shear, and appears on the source side of Einstein's field equations.</p></div></article>
          <article class="concept-card" data-explanation-group><div class="concept-heading"><div><p class="eyebrow">Concept 04</p><h2>Independent reproduction</h2></div><div class="segmented small"><button class="segment active" data-level="simple" type="button">Simple</button><button class="segment" data-level="technical" type="button">Technical</button></div></div><div data-explanation="simple"><p>Someone outside the original run tries the same test and records whether they get the same meaningful result.</p></div><div data-explanation="technical" hidden><p>A reproduction records an independent contributor, environment, implementation or solver, numerical tolerances, artifact hashes, and comparison outcome. Cross-implementation agreement is stronger than repeated execution of one code path.</p></div></article>
          <article class="concept-card" data-explanation-group><div class="concept-heading"><div><p class="eyebrow">Concept 05</p><h2>Evidence graph</h2></div><div class="segmented small"><button class="segment active" data-level="simple" type="button">Simple</button><button class="segment" data-level="technical" type="button">Technical</button></div></div><div data-explanation="simple"><p>A map showing which source supports which claim, which run tested which candidate, and which reproduction agreed or disagreed.</p></div><div data-explanation="technical" hidden><p>A typed, versioned projection from the append-only event ledger whose nodes and edges retain authority, provenance, status, and supersession semantics.</p></div></article>
        </section>
        <section class="section-surface"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">Verified explanation</p><h2>Candidate 000001 report</h2><p>Switch between the committed beginner and technical reports. Both are derived from the same result digest.</p></div><div class="report-switch"><button class="button secondary active" type="button" data-report-mode="beginner">Beginner report</button><button class="button secondary" type="button" data-report-mode="technical">Technical report</button></div><article class="report-view" data-report-view><p>Loading report…</p></article></div></section>
        <section class="shell section-pad"><div class="section-intro"><p class="eyebrow">Status vocabulary</p><h2>Words should expose uncertainty rather than disguise it.</h2></div><div class="status-vocabulary"><div><span class="pill neutral">HYPOTHESIS</span><p>A testable proposition with stated assumptions.</p></div><div><span class="pill pass">COMPUTATION SUPPORTED</span><p>A versioned computation supports the statement within declared scope.</p></div><div><span class="pill neutral">REPRODUCED</span><p>An independent implementation or environment recovered the result.</p></div><div><span class="pill warning">CHALLENGED</span><p>An unresolved objection may affect interpretation or status.</p></div><div><span class="pill fail">FALSIFIED</span><p>A decisive declared test failed.</p></div><div><span class="pill fail">RETRACTED</span><p>The claim was withdrawn; its history remains visible.</p></div></div></section>
      </main>`,
  },
  {
    slug: 'roadmap', key: 'roadmap', title: 'Research roadmap',
    description: 'A benchmark-gated path from one reproducible baseline to transparent search, federated reproduction, and only then novel research.',
    content: `
      <main id="main-content" data-page="roadmap">
        <section class="shell page-hero section-pad compact"><div><p class="eyebrow">Roadmap</p><h1>Earn complexity one benchmark at a time.</h1><p class="hero-lede">The project advances only when the previous layer is reproducible. Novel candidate generation remains gated until known baselines and cross-validator comparisons are strong.</p></div></section>
        <section class="shell section-pad-top"><div class="roadmap" data-roadmap><p>Loading roadmap…</p></div></section>
        <section class="section-surface"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">The reusable invention</p><h2>The protocol can outgrow spacetime research.</h2><p>The most transferable idea is not a wormhole. It is a disciplined loop for exploring any enormous computational possibility space.</p></div><div class="reuse-flow"><span>Candidate</span><i>→</i><span>Validator</span><i>→</i><span>Artifact</span><i>→</i><span>Graph</span><i>→</i><span>Search policy</span><i>→</i><span>Next experiment</span></div><div class="reuse-grid"><article><h3>Materials discovery</h3><p>Represent compounds, test predicted properties, preserve failed formulations, and prioritize informative experiments.</p></article><article><h3>Engineering design spaces</h3><p>Compare structures, constraints, simulations, and reproductions without hiding tradeoffs inside one score.</p></article><article><h3>Robotics policies</h3><p>Version environments, safety constraints, trials, failures, and model promotions behind frozen benchmarks.</p></article><article><h3>Mathematical exploration</h3><p>Separate conjecture generation from proof checking and keep every counterexample permanently discoverable.</p></article></div></div></section>
        <section class="shell section-pad boundary-grid"><article class="boundary-card positive"><p class="eyebrow">Scale now</p><h2>Contracts, provenance, tests, and participation.</h2><p>Portable schemas, deterministic artifacts, accessible explanations, issue templates, and independent reproduction are useful immediately.</p></article><article class="boundary-card caution"><p class="eyebrow">Scale later</p><h2>Databases, distributed solvers, models, and compute markets.</h2><p>Infrastructure is earned by measured scientific workload. V0 intentionally avoids microservices, authentication, payments, and autonomous job execution.</p></article></section>
      </main>`,
  },
  {
    slug: 'contribute', key: 'contribute', title: 'Contribute to the experiment',
    description: 'Reproduce, challenge, build, explain, curate, or govern the open research system through narrow, testable contributions.',
    content: `
      <main id="main-content" data-page="contribute">
        <section class="shell page-hero section-pad compact"><div><p class="eyebrow">Contribute</p><h1>You do not need to solve the universe to improve the instrument.</h1><p class="hero-lede">The first useful contributions are small, reproducible, and easy to challenge. Expertise helps—but careful documentation, testing, visualization, and skepticism matter too.</p></div></section>
        <section class="shell section-pad-top"><div class="contribution-grid"><article><span>REPRODUCE</span><h2>Run Candidate 000001</h2><p>Use a clean environment, compare the scientific digest, and publish every difference.</p><a href="#reproduce">See exact commands</a></article><article><span>CHALLENGE</span><h2>Try to break a claim</h2><p>Identify a hidden assumption, scope error, convention mismatch, or missing failure test.</p><a data-repository-issue="challenge" href="/CONTRIBUTING.md">Open guidance</a></article><article><span>BUILD</span><h2>Improve the instrument</h2><p>Add tests, schemas, visualizations, accessibility, or one narrowly scoped validator.</p><a data-repository-issue="build" href="/CONTRIBUTING.md">Open guidance</a></article><article><span>EXPLAIN</span><h2>Make rigor understandable</h2><p>Improve explanations without changing result status, raw fields, limitations, or provenance.</p><a data-repository-issue="explain" href="/CONTRIBUTING.md">Open guidance</a></article></div></section>
        <section class="section-surface" id="reproduce"><div class="shell section-pad setup-layout"><div><p class="eyebrow">Best first contribution</p><h2>Independently reproduce Candidate 000001.</h2><p class="section-lede">Clone the repository in a clean environment, run the baseline, compare the scientific digest, and document anything that differs.</p></div><div class="terminal-card"><div class="terminal-head"><span>TERMINAL</span><button type="button" data-copy-target="[data-setup-command]">Copy all</button></div><pre><code data-setup-command>git clone YOUR_REPOSITORY_URL
cd YOUR_REPOSITORY
python -m pip install --no-build-isolation -e '.[dev]'
python scripts/research.py verify candidates/CANDIDATE-000001.json --reproducible
PYTHONPATH=src pytest
npm run check
npm run build</code></pre></div></div></section>
        <section class="shell section-pad"><div class="section-intro"><p class="eyebrow">Contribution contract</p><h2>A professional pull request explains what changed and what did not.</h2></div><div class="steps-grid"><div><span>1</span><h3>Choose one bounded problem</h3><p>Reference a candidate, claim, validator, page, schema, or issue.</p></div><div><span>2</span><h3>Declare authority</h3><p>State whether the work changes canonical evidence, working research, or product presentation.</p></div><div><span>3</span><h3>Add tests and provenance</h3><p>Include sources, methods, commands, limitations, and expected failure cases.</p></div><div><span>4</span><h3>Submit a reviewable PR</h3><p>Include reproduction commands, status implications, and generated artifacts.</p></div></div></section>
        <section class="section-surface" id="agent-prompts"><div class="shell section-pad"><div class="section-intro"><p class="eyebrow">Agent build prompts</p><h2>Give coding and research agents a bounded role, not a vague command to “solve it.”</h2><p class="section-lede">The repository contains an orchestrator, builder, scientist, researcher, skeptic, reproduction, data-curation, security, release, and explainer prompt set.</p></div><div class="prompt-links" data-prompt-links><a href="/prompts/ORCHESTRATOR_AGENT.md">Orchestrator</a><a href="/prompts/BUILD_AGENT.md">Build agent</a><a href="/prompts/SCIENCE_AGENT.md">Science agent</a><a href="/prompts/SKEPTIC_AGENT.md">Skeptic</a><a href="/prompts/PHASE_1_IMPLEMENTATION.md">Phase 1 build</a></div></div></section>
        <section class="shell section-pad boundary-grid"><article class="boundary-card positive"><p class="eyebrow">Automatic acceptance pattern</p><h2>Narrow claim, clear evidence, reproducible artifact.</h2><p>The strongest contribution is boring to verify: its inputs are declared, its output is deterministic, its limitations are explicit, and another person can reproduce it.</p></article><article class="boundary-card caution"><p class="eyebrow">Automatic rejection pattern</p><h2>Exciting output without provenance.</h2><p>Generated metrics, summaries, simulations, or “discoveries” that cannot identify their source, method, validator, and reproducible artifact remain working-memory proposals.</p></article></section>
      </main>`,
  },
];
