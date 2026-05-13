/* ===================================================
   app.js — OpenContext Demo Interactive Logic
=================================================== */

// ── Navbar scroll effect ──────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

// ── Hero typewriter ───────────────────────────────
(function heroTypewriter() {
  const commands = ['opencontext setup', 'opencontext init', 'opencontext initbranch', 'opencontext sync'];
  const outputEl = document.getElementById('terminal-output-hero');
  const tw = document.getElementById('typewriter');
  let cmdIdx = 0;

  const outputs = {
    'opencontext setup': [
      { cls: 't-white', text: 'hello' },
      { cls: 't-muted', text: 'Jira Email: alice@corp.com' },
      { cls: 't-muted', text: 'Jira API Token: ••••••••••••••' },
      { cls: 't-success', text: '✓ Global Config Set' },
      { cls: 't-success', text: '✓ Git hook generated at .git/hooks/pre-commit' },
    ],
    'opencontext init': [
      { cls: 't-muted', text: 'Jira Domain: corp.atlassian.net' },
      { cls: 't-info', text: '→ Fetching OpenSpec design documents...' },
      { cls: 't-success', text: '✓ Local Config Set' },
      { cls: 't-success', text: '✓ Spec context saved to sdlc/' },
      { cls: 't-white', text: 'Next: run extract_architecture in chatbot' },
    ],
    'opencontext initbranch': [
      { cls: 't-info', text: '→ Reading architectural_facts.json...' },
      { cls: 't-info', text: '→ Vectorizing with all-MiniLM-L6-v2...' },
      { cls: 't-success', text: 'V  E  C  T  O  R   E  D' },
      { cls: 't-info', text: '→ Fetching Jira ticket PROJ-42...' },
      { cls: 't-success', text: '✓ agent.md written to .agent/tasks/' },
    ],
    'opencontext sync': [
      { cls: 't-info', text: '→ Reading sdlc/diff_analysis.json...' },
      { cls: 't-info', text: '→ Re-vectorizing diff insights...' },
      { cls: 't-success', text: 'V  E  C  T  O  R   E  D' },
      { cls: 't-info', text: '→ Re-fetching Jira ticket...' },
      { cls: 't-success', text: '✓ agent.md regenerated — context is fresh' },
    ],
  };

  function runHeroCycle() {
    const cmd = commands[cmdIdx % commands.length];
    // type command
    tw.classList.remove('done');
    tw.textContent = '';
    let i = 0;
    const typeInt = setInterval(() => {
      tw.textContent += cmd[i];
      i++;
      if (i >= cmd.length) {
        clearInterval(typeInt);
        tw.classList.add('done');
        showOutput(cmd);
      }
    }, 55);
  }

  function showOutput(cmd) {
    outputEl.innerHTML = '';
    const lines = outputs[cmd] || [];
    lines.forEach((line, idx) => {
      setTimeout(() => {
        const div = document.createElement('div');
        div.className = `terminal-line-out ${line.cls}`;
        div.textContent = line.text;
        outputEl.appendChild(div);
        if (idx === lines.length - 1) {
          setTimeout(() => {
            cmdIdx++;
            outputEl.innerHTML = '';
            runHeroCycle();
          }, 2800);
        }
      }, idx * 340);
    });
  }

  runHeroCycle();
})();


// ── Intersection observer for section animations ──
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'none';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.workflow-step, .problem-card, .arch-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(el);
});


// ── DEMO SECTION ──────────────────────────────────
const DEMO_DATA = {
  setup: {
    title: '🔑 opencontext setup',
    explanation: {
      title: 'What happens behind the scenes',
      body: 'Your Jira email and API token are saved to ~/.opencontext/global.config.json. ' +
            'A pre-commit Git hook is installed at .git/hooks/pre-commit that automatically ' +
            'runs the diff capturer on every git commit, keeping architectural context always current.',
    },
    artifacts: [
      { label: '~/.opencontext/global.config.json', cls: 'artifact-item--green' },
      { label: '.git/hooks/pre-commit', cls: 'artifact-item--blue' },
    ],
    lines: [
      { delay: 0,    text: '$ opencontext setup', cls: 't-accent terminal-line' },
      { delay: 400,  text: 'hello', cls: 't-white terminal-line-out' },
      { delay: 800,  text: 'Jira Email: alice@corp.com', cls: 't-muted terminal-line-out' },
      { delay: 1100, text: 'Jira API Token: ••••••••••••••••', cls: 't-muted terminal-line-out' },
      { delay: 1500, text: '✓ Global Config Set', cls: 't-success terminal-line-out' },
      { delay: 1800, text: '✓ Git hook written to .git/hooks/pre-commit', cls: 't-success terminal-line-out' },
      { delay: 2200, text: '✓ Hook marked executable (chmod +x)', cls: 't-success terminal-line-out' },
    ],
  },
  init: {
    title: '📐 opencontext init',
    explanation: {
      title: 'What happens behind the scenes',
      body: 'Your Jira domain is saved to opencontext.config.json in the project root. ' +
            'OpenSpec design docs are fetched from the .agent/ directory and stored in sdlc/. ' +
            'An Antigravity task is created so the AI agent can extract architectural facts on your behalf.',
    },
    artifacts: [
      { label: 'opencontext.config.json', cls: 'artifact-item--green' },
      { label: 'sdlc/spec_context.md', cls: 'artifact-item--blue' },
      { label: '.agent/tasks/extract_architecture.md', cls: 'artifact-item--purple' },
    ],
    lines: [
      { delay: 0,    text: '$ opencontext init', cls: 't-accent terminal-line' },
      { delay: 400,  text: 'Jira Domain: corp.atlassian.net', cls: 't-muted terminal-line-out' },
      { delay: 800,  text: '→ Fetching OpenSpec design documents...', cls: 't-info terminal-line-out' },
      { delay: 1200, text: '  Found: proposal.md, design.md, tasks/', cls: 't-dim terminal-line-out' },
      { delay: 1600, text: '→ Creating Antigravity extraction task...', cls: 't-info terminal-line-out' },
      { delay: 2000, text: '✓ Local Config Set', cls: 't-success terminal-line-out' },
      { delay: 2400, text: '✓ Spec context saved', cls: 't-success terminal-line-out' },
      { delay: 2800, text: 'Execute the following command in chatbot:', cls: 't-warn terminal-line-out' },
      { delay: 3000, text: '  run extract_architecture', cls: 't-white terminal-line-out' },
    ],
  },
  initbranch: {
    title: '🧠 opencontext initbranch',
    explanation: {
      title: 'What happens behind the scenes',
      body: 'Architectural facts from sdlc/architectural_facts.json are embedded using all-MiniLM-L6-v2 ' +
            '(sentence-transformers) and stored in a local LanceDB vector database. Your Jira ticket is ' +
            'fetched, and a RAG search retrieves the top-3 most relevant architectural context chunks. ' +
            'Finally, a grounded agent.md task is generated with Zero Drift guardrails.',
    },
    artifacts: [
      { label: 'sdlc/dataVektor/ (LanceDB)', cls: 'artifact-item--green' },
      { label: '.agent/tasks/generate_agent.md', cls: 'artifact-item--purple' },
    ],
    lines: [
      { delay: 0,    text: '$ opencontext initbranch', cls: 't-accent terminal-line' },
      { delay: 400,  text: '→ Reading sdlc/architectural_facts.json...', cls: 't-info terminal-line-out' },
      { delay: 800,  text: '  Loaded 12 architectural fact strings', cls: 't-dim terminal-line-out' },
      { delay: 1200, text: '→ Embedding with all-MiniLM-L6-v2...', cls: 't-info terminal-line-out' },
      { delay: 1600, text: '  Connecting to LanceDB at sdlc/dataVektor', cls: 't-dim terminal-line-out' },
      { delay: 2000, text: 'V  E  C  T  O  R   E  D', cls: 't-success terminal-line-out' },
      { delay: 2400, text: '→ Fetching Jira ticket PROJ-42...', cls: 't-info terminal-line-out' },
      { delay: 2800, text: '  "Add payment gateway integration"', cls: 't-dim terminal-line-out' },
      { delay: 3200, text: '→ RAG: retrieving top-3 context chunks...', cls: 't-info terminal-line-out' },
      { delay: 3600, text: '✓ agent.md written to .agent/tasks/', cls: 't-success terminal-line-out' },
      { delay: 4000, text: 'Execute the following command in chatbot:', cls: 't-warn terminal-line-out' },
      { delay: 4200, text: '  run generate_agent', cls: 't-white terminal-line-out' },
    ],
  },
  sync: {
    title: '🔄 opencontext sync',
    explanation: {
      title: 'What happens behind the scenes',
      body: 'The pre-commit Git hook captured a diff_analysis.json during your last commit. ' +
            'sync re-embeds those diff insights into LanceDB, then fetches the latest Jira ticket state ' +
            'and regenerates the agent.md task. Your AI agent now has the freshest possible context ' +
            'reflecting every code change you\'ve made since initbranch.',
    },
    artifacts: [
      { label: 'sdlc/diff_analysis.json (read)', cls: 'artifact-item--green' },
      { label: 'sdlc/dataVektor/ (updated)', cls: 'artifact-item--blue' },
      { label: '.agent/tasks/generate_agent.md', cls: 'artifact-item--purple' },
    ],
    lines: [
      { delay: 0,    text: '$ opencontext sync', cls: 't-accent terminal-line' },
      { delay: 400,  text: '→ Reading sdlc/diff_analysis.json...', cls: 't-info terminal-line-out' },
      { delay: 800,  text: '  Loaded 7 diff insight strings from last commit', cls: 't-dim terminal-line-out' },
      { delay: 1200, text: '→ Re-vectorizing diff insights...', cls: 't-info terminal-line-out' },
      { delay: 1600, text: '  Appending to LanceDB table string_vectors', cls: 't-dim terminal-line-out' },
      { delay: 2000, text: 'V  E  C  T  O  R   E  D', cls: 't-success terminal-line-out' },
      { delay: 2400, text: '→ Re-fetching Jira ticket PROJ-42...', cls: 't-info terminal-line-out' },
      { delay: 2800, text: '→ RAG: context is now diff-aware...', cls: 't-info terminal-line-out' },
      { delay: 3200, text: '✓ agent.md regenerated — context is fresh', cls: 't-success terminal-line-out' },
      { delay: 3600, text: 'Execute the following command in chatbot:', cls: 't-warn terminal-line-out' },
      { delay: 3800, text: '  run generate_agent', cls: 't-white terminal-line-out' },
    ],
  },
};

const demoTerminalBody = document.getElementById('demo-terminal-body');
const demoTerminalTitle = document.getElementById('demo-terminal-title');
const explanationTitle = document.getElementById('explanation-title');
const explanationBody = document.getElementById('explanation-body');
const artifactList = document.getElementById('artifact-list');

let demoAnimTimeout = [];

function clearDemoTimeouts() {
  demoAnimTimeout.forEach(clearTimeout);
  demoAnimTimeout = [];
}

function runDemo(cmd) {
  clearDemoTimeouts();
  demoTerminalBody.innerHTML = '';
  artifactList.innerHTML = '';

  const data = DEMO_DATA[cmd];
  demoTerminalTitle.textContent = data.title;
  explanationTitle.textContent = data.explanation.title;
  explanationBody.textContent = data.explanation.body;

  // Render terminal lines with delays
  data.lines.forEach(({ delay, text, cls }) => {
    const t = setTimeout(() => {
      const el = document.createElement('div');
      el.className = cls;
      el.textContent = text;
      demoTerminalBody.appendChild(el);
    }, delay);
    demoAnimTimeout.push(t);
  });

  // Render artifacts after last line
  const lastDelay = data.lines[data.lines.length - 1].delay + 400;
  const t = setTimeout(() => {
    data.artifacts.forEach(({ label, cls }) => {
      const div = document.createElement('div');
      div.className = `artifact-item ${cls}`;
      div.textContent = label;
      artifactList.appendChild(div);
    });
  }, lastDelay);
  demoAnimTimeout.push(t);

  // Update active button
  document.querySelectorAll('.demo-cmd-btn').forEach(btn => {
    btn.classList.toggle('demo-cmd-btn--active', btn.dataset.cmd === cmd);
  });
}

// Wire buttons
document.querySelectorAll('.demo-cmd-btn').forEach(btn => {
  btn.addEventListener('click', () => runDemo(btn.dataset.cmd));
});

// Init with setup
runDemo('setup');


// ── Copy install command ──────────────────────────
const copyBtn = document.getElementById('copy-install-btn');
if (copyBtn) {
  copyBtn.addEventListener('click', () => {
    const text = document.getElementById('install-code').textContent;
    navigator.clipboard.writeText(text).then(() => {
      copyBtn.classList.add('copied');
      copyBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
      setTimeout(() => {
        copyBtn.classList.remove('copied');
        copyBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;
      }, 2000);
    });
  });
}


// ── Smooth active nav link tracking ──────────────
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navLinks.forEach(link => {
        link.style.color = link.getAttribute('href') === `#${entry.target.id}`
          ? 'var(--clr-primary-light)'
          : '';
      });
    }
  });
}, { threshold: 0.5 });

sections.forEach(s => sectionObserver.observe(s));
