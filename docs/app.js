/* New Software — client-side filter + sort + search.
   Data is embedded inline in <script id="news-data" type="application/json">.
   All DOM is built via createElement / textContent. */

(function () {
  "use strict";

  const data = JSON.parse(document.getElementById("news-data").textContent);
  const listEl = document.getElementById("news-list");
  const emptyEl = document.getElementById("empty");
  const countEl = document.getElementById("result-count");
  const qEl = document.getElementById("q");
  const sortEl = document.getElementById("sort");
  const clearBtn = document.getElementById("clear");

  const state = {
    q: "",
    filters: { category: "", channel: "" },
    sort: "date-desc",
  };

  const url = new URL(window.location.href);
  if (url.searchParams.get("q")) { state.q = url.searchParams.get("q"); qEl.value = state.q; }
  if (url.searchParams.get("category")) state.filters.category = url.searchParams.get("category");
  if (url.searchParams.get("channel"))  state.filters.channel  = url.searchParams.get("channel");
  if (url.searchParams.get("sort"))    { state.sort = url.searchParams.get("sort"); sortEl.value = state.sort; }

  function syncUrl() {
    const u = new URL(window.location.href);
    function set(k, v) { if (v) u.searchParams.set(k, v); else u.searchParams.delete(k); }
    set("q", state.q);
    set("category", state.filters.category);
    set("channel", state.filters.channel);
    set("sort", state.sort === "date-desc" ? "" : state.sort);
    window.history.replaceState(null, "", u.toString());
  }

  for (const d of data) {
    d._hay = [
      d.title, d.summary, d.category, d.channel,
      (d.tags || []).join(" "),
      d.repo_url, d.homepage, d.video_title
    ].join(" ").toLowerCase();
  }

  function matches(d) {
    if (state.filters.category && d.category !== state.filters.category) return false;
    if (state.filters.channel  && d.channel  !== state.filters.channel)  return false;
    if (state.q) {
      const q = state.q.toLowerCase().trim();
      if (!q) return true;
      for (const term of q.split(/\s+/)) if (!d._hay.includes(term)) return false;
    }
    return true;
  }

  function compare(a, b) {
    switch (state.sort) {
      case "date-asc":   return (a.created_at || "").localeCompare(b.created_at || "");
      case "title-asc":  return a.title.localeCompare(b.title);
      case "title-desc": return b.title.localeCompare(a.title);
      case "stars-desc": return (b.stars || 0) - (a.stars || 0);
      case "channel":    return a.channel.localeCompare(b.channel) || (b.created_at || "").localeCompare(a.created_at || "");
      case "date-desc":
      default:           return (b.created_at || "").localeCompare(a.created_at || "");
    }
  }

  // Append highlighted matches as text/<mark> nodes — never innerHTML.
  function appendHighlighted(parent, text, q) {
    if (!text) return;
    if (!q) { parent.appendChild(document.createTextNode(text)); return; }
    const safeQ = q.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
    const re = new RegExp(safeQ, "ig");
    const matchesIter = text.matchAll(re);
    let lastIndex = 0;
    for (const m of matchesIter) {
      if (m.index > lastIndex) parent.appendChild(document.createTextNode(text.slice(lastIndex, m.index)));
      const mk = document.createElement("mark");
      mk.textContent = m[0];
      parent.appendChild(mk);
      lastIndex = m.index + m[0].length;
    }
    if (lastIndex < text.length) parent.appendChild(document.createTextNode(text.slice(lastIndex)));
  }

  function el(tag, props, children) {
    const e = document.createElement(tag);
    if (props) for (const k in props) {
      if (k === "class") e.className = props[k];
      else if (k === "text") e.textContent = props[k];
      else e.setAttribute(k, props[k]);
    }
    if (children) for (const c of children) if (c) e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    return e;
  }

  function row(d) {
    const q = state.q.trim();
    const li = el("li", { class: "news-row" });
    li.appendChild(el("div", { class: "cat", text: (d.category || "news").toUpperCase() }));

    const mid = el("div");
    const titleWrap = el("div", { class: "title" });
    const a = el("a", { href: "news/" + d.uid + ".html" });
    appendHighlighted(a, d.title, q);
    titleWrap.appendChild(a);
    if (d.stars && d.stars > 0) {
      titleWrap.appendChild(document.createTextNode(" "));
      const stars = el("span", { class: "stars", title: "GitHub stars" });
      stars.textContent = "★ " + d.stars.toLocaleString();
      titleWrap.appendChild(stars);
    }
    mid.appendChild(titleWrap);

    const sum = el("div", { class: "summary" });
    appendHighlighted(sum, d.summary, q);
    mid.appendChild(sum);

    const via = el("div", { class: "via" });
    via.textContent = "via @" + d.channel + (d.tags && d.tags.length ? " · " + d.tags.slice(0, 4).join(" · ") : "");
    mid.appendChild(via);

    li.appendChild(mid);
    li.appendChild(el("div", { class: "date", text: d.date }));
    return li;
  }

  function render() {
    const filtered = data.filter(matches);
    filtered.sort(compare);
    countEl.textContent = filtered.length;
    while (listEl.firstChild) listEl.removeChild(listEl.firstChild);
    if (filtered.length === 0) {
      emptyEl.hidden = false;
    } else {
      emptyEl.hidden = true;
      const frag = document.createDocumentFragment();
      for (const d of filtered) frag.appendChild(row(d));
      listEl.appendChild(frag);
    }
    syncUrl();
  }

  function syncChips() {
    document.querySelectorAll(".chip").forEach((btn) => {
      const f = btn.dataset.filter;
      const v = btn.dataset.value;
      btn.classList.toggle("active", state.filters[f] === v);
    });
  }

  document.querySelectorAll(".chip").forEach((btn) => {
    btn.addEventListener("click", () => {
      const f = btn.dataset.filter;
      const v = btn.dataset.value;
      state.filters[f] = state.filters[f] === v ? "" : v;
      syncChips();
      render();
    });
  });

  let debounce = 0;
  qEl.addEventListener("input", () => {
    clearTimeout(debounce);
    debounce = setTimeout(() => { state.q = qEl.value; render(); }, 80);
  });
  sortEl.addEventListener("change", () => { state.sort = sortEl.value; render(); });
  clearBtn.addEventListener("click", () => {
    state.q = ""; state.filters = { category: "", channel: "" }; state.sort = "date-desc";
    qEl.value = ""; sortEl.value = "date-desc";
    syncChips(); render();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== qEl) {
      e.preventDefault();
      qEl.focus();
    } else if (e.key === "Escape" && document.activeElement === qEl) {
      qEl.value = ""; state.q = ""; qEl.blur(); render();
    }
  });

  syncChips();
  render();
})();
