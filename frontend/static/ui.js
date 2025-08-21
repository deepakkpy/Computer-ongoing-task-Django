document.addEventListener("DOMContentLoaded", () => {
  // ---------- State ----------
  const state = {
    host: null,
    auto: false,
    timer: null,
    processes: [],
    expanded: new Set(),
  };

  // ---------- El helpers ----------
  const $ = (sel) => document.querySelector(sel);
  const hostTitle = $("#hostTitle");
  const syscard = $("#syscard");
  const tree = $("#tree");
  const computers = $("#computers");

  // ---------- Controls ----------
  if ($("#refresh")) $("#refresh").onclick = () => loadHost(state.host);
  if ($("#refreshList")) $("#refreshList").onclick = loadComputers;
  if ($("#auto")) {
    $("#auto").onchange = (e) => {
      state.auto = e.target.checked;
      if (state.auto) startCycle();
      else clearInterval(state.timer);
    };
  }

  // Tabs
  $("#tab-processes").onclick = () => switchTab("processes");
  $("#tab-system").onclick = () => switchTab("system");

  function switchTab(tab) {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((c) => c.classList.remove("active"));

    if (tab === "processes") {
      $("#tab-processes").classList.add("active");
      $("#tab-content-processes").classList.add("active");
    } else {
      $("#tab-system").classList.add("active");
      $("#tab-content-system").classList.add("active");
    }
  }

  // ---------- Utils ----------
  const fmt = (n) => (n == null ? "" : (Math.round(n * 10) / 10).toString());
  const escapeHtml = (s) =>
    String(s).replace(/[&<>"']/g, (m) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[m]));

  function startCycle() {
    clearInterval(state.timer);
    state.timer = setInterval(() => {
      if (state.host) loadHost(state.host, { keepExpanded: true });
    }, 5000);
  }

  // ---------- API: computers ----------
  async function loadComputers() {
    const res = await fetch("/api/computers/");
    const data = await res.json();

    computers.innerHTML = "";
    data.forEach((c) => {
      const div = document.createElement("div");
      div.className = "computer-item" + (state.host === c.hostname ? " active" : "");
      div.dataset.host = c.hostname;
      div.innerHTML = `
        <div style="font-weight:600">${escapeHtml(c.hostname)}</div>
        <div style="font-size:12px;opacity:.7">
          Last seen: ${new Date(c.last_seen).toLocaleString()}
        </div>`;
      div.onclick = () => {
        // Update active highlight
        document.querySelectorAll(".computer-item").forEach((el) => el.classList.remove("active"));
        div.classList.add("active");

        // Set current host and reset process tree expansion
        state.host = c.hostname;
        state.expanded.clear();

        // Load host data
        loadHost(c.hostname);
      };
      computers.appendChild(div);
    });
  }

  // ---------- Build tree index ----------
  function buildRoots(items) {
    const byPid = new Map();
    items.forEach((p) => byPid.set(p.pid, { ...p, children: [] }));
    const roots = [];
    byPid.forEach((node) => {
      if (byPid.has(node.ppid)) byPid.get(node.ppid).children.push(node);
      else roots.push(node);
    });
    return roots;
  }

  // ---------- Render tree (four columns) ----------
  function renderTree() {
    const roots = buildRoots(state.processes);
    tree.innerHTML = "";
    roots.sort((a, b) => a.name.localeCompare(b.name)).forEach((n) => appendNode(n, 0));
  }

  function appendNode(node, depth) {
    const hasChildren = node.children && node.children.length > 0;
    const isOpen = state.expanded.has(node.pid);

    const row = document.createElement("div");
    row.className = "node row-grid";

    // Col 1: Name + caret + PID, with indent
    const c1 = document.createElement("div");
    c1.className = "cell namecell";
    c1.innerHTML = `
      <span class="indent" style="--d:${depth}"></span>
      <span class="chev">${hasChildren ? (isOpen ? "▾" : "▸") : "•"}</span>
      <span class="name">${escapeHtml(node.name)}</span>
      <span class="pid">(PID ${node.pid})</span>`;
    if (hasChildren) {
      c1.querySelector(".chev").onclick = (e) => {
        e.stopPropagation();
        if (isOpen) state.expanded.delete(node.pid);
        else state.expanded.add(node.pid);
        renderTree();
      };
    }

    // Col 2: Memory
    const c2 = document.createElement("div");
    c2.className = "cell";
    c2.textContent = fmt(node.mem_mb);

    // Col 3: CPU
    const c3 = document.createElement("div");
    c3.className = "cell";
    c3.textContent = fmt(node.cpu);

    // Col 4: PPID
    const c4 = document.createElement("div");
    c4.className = "cell";
    c4.textContent = node.ppid ?? "-";

    row.append(c1, c2, c3, c4);
    tree.appendChild(row);

    if (hasChildren && isOpen) {
      node.children
        .sort((a, b) => a.name.localeCompare(b.name))
        .forEach((child) => appendNode(child, depth + 1));
    }
  }

  // ---------- Load selected host ----------
  async function loadHost(host, opts = {}) {
    if (!host) return;

    hostTitle.textContent = host;

    const res = await fetch(`/api/computers/${encodeURIComponent(host)}/latest/`);
    if (res.status !== 200) {
      tree.innerHTML = '<div class="node">No data</div>';
      syscard.classList.add("hidden");
      return;
    }

    const data = await res.json();

    if (!opts.keepExpanded) state.expanded.clear();
    state.processes = Array.isArray(data.processes) ? data.processes : [];

    renderTree();

    syscard.classList.remove("hidden");
    syscard.innerHTML = [
      ["OS", data.os],
      ["CPU", data.cpu_model],
      ["Cores/Threads", `${data.cores}/${data.threads}`],
      ["RAM Total (GB)", fmt(data.ram_total_gb)],
      ["RAM Used (GB)", fmt(data.ram_used_gb)],
      ["RAM Free (GB)", fmt(data.ram_available_gb)],
      ["Disk Total (GB)", fmt(data.storage_total_gb)],
      ["Disk Used (GB)", fmt(data.storage_used_gb)],
      ["Disk Free (GB)", fmt(data.storage_free_gb)],
    ]
      .map(([k, v]) => `<div class="sysitem"><span class="k">${k}</span><span class="v">${v ?? ""}</span></div>`)
      .join("");
  }

  // ---------- Init ----------
  loadComputers();
});
