import json
from pathlib import Path

rows = json.loads(Path(r"D:\Tools\Solar\Scotland Solar Project Plan\_solar_kw_data.json").read_text(encoding="utf-8"))
payload = json.dumps(rows, ensure_ascii=False)

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Scotland Solar — Keyword Explorer</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<style>
  :root {
    --bg: #0f1419;
    --panel: #1a222c;
    --panel2: #243040;
    --border: #2f3d4d;
    --text: #e8eef4;
    --muted: #8b9aab;
    --accent: #3d9cf0;
    --good: #3ecf8e;
    --warn: #f0b429;
    --bad: #f07178;
    --s: #5eead4;
    --a: #3d9cf0;
    --b: #a78bfa;
    --c: #f0b429;
    --d: #94a3b8;
    --skip: #64748b;
    --emd: #34d399;
    --brand: #fbbf24;
    --area: #60a5fa;
    --mention: #94a3b8;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: "Segoe UI", system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.45;
  }
  header {
    padding: 28px 24px 18px;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(180deg, #16202a, var(--bg));
  }
  h1 { margin: 0 0 6px; font-size: 1.55rem; font-weight: 650; letter-spacing: -0.02em; }
  .sub { color: var(--muted); font-size: 0.92rem; max-width: 820px; }
  .wrap { padding: 18px 24px 40px; max-width: 1480px; margin: 0 auto; }
  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
    margin-bottom: 16px;
  }
  .stat {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 14px;
  }
  .stat .n { font-size: 1.35rem; font-weight: 700; }
  .stat .l { color: var(--muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; }
  .panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 14px;
  }
  .panel h2 { margin: 0 0 10px; font-size: 0.95rem; font-weight: 650; }
  .controls, .radius-controls {
    display: grid;
    gap: 10px;
    align-items: end;
  }
  .controls { grid-template-columns: 1.4fr repeat(4, 1fr) auto; margin-bottom: 12px; }
  .radius-controls { grid-template-columns: 1.3fr 0.7fr 1.5fr 1fr 0.9fr auto auto; }
  @media (max-width: 980px) {
    .controls, .radius-controls { grid-template-columns: 1fr 1fr; }
  }
  label { display: block; font-size: 0.75rem; color: var(--muted); margin-bottom: 4px; }
  input, select, button {
    width: 100%;
    background: var(--panel2);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 9px 11px;
    font: inherit;
  }
  .panel input, .panel select { background: var(--bg); }
  input:focus, select:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
  button {
    background: var(--accent);
    border-color: transparent;
    color: #041018;
    font-weight: 650;
    cursor: pointer;
  }
  button.secondary { background: var(--panel2); color: var(--text); border-color: var(--border); }
  button:disabled { opacity: 0.45; cursor: not-allowed; }
  .chips { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
  .chip {
    border: 1px solid var(--border);
    background: var(--panel);
    color: var(--muted);
    border-radius: 999px;
    padding: 5px 11px;
    font-size: 0.8rem;
    cursor: pointer;
  }
  .chip.on { background: #1e3a55; color: #cfe8ff; border-color: #2f6ea8; }
  .rec {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
  }
  @media (max-width: 900px) { .rec { grid-template-columns: 1fr; } }
  .rec-box {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    min-height: 80px;
  }
  .rec-box h3 { margin: 0 0 8px; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.04em; }
  .rec-box.emd h3 { color: var(--emd); }
  .rec-box.area h3 { color: var(--area); }
  .rec-box.mention h3 { color: var(--mention); }
  .rec-box ul { margin: 0; padding-left: 18px; font-size: 0.88rem; }
  .rec-box li { margin-bottom: 4px; }
  .note { color: var(--muted); font-size: 0.82rem; margin-top: 10px; }
  .table-wrap {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: auto;
    max-height: calc(100vh - 420px);
    background: var(--panel);
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
  th, td { padding: 9px 12px; text-align: left; border-bottom: 1px solid var(--border); white-space: nowrap; }
  th {
    position: sticky; top: 0; z-index: 2;
    background: #1f2a36;
    cursor: pointer;
    user-select: none;
    color: #c5d2df;
    font-weight: 600;
  }
  th:hover { color: #fff; }
  th .arrow { opacity: 0.45; font-size: 0.75em; }
  tr:hover td { background: rgba(61,156,240,0.07); }
  tr.hub td { background: rgba(52,211,153,0.08); }
  .tier, .role {
    display: inline-block;
    min-width: 42px;
    text-align: center;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 0.75rem;
    font-weight: 700;
  }
  .tier-S { background: rgba(94,234,212,0.18); color: var(--s); }
  .tier-A { background: rgba(61,156,240,0.18); color: var(--a); }
  .tier-B { background: rgba(167,139,250,0.18); color: var(--b); }
  .tier-C { background: rgba(240,180,41,0.18); color: var(--c); }
  .tier-D { background: rgba(148,163,184,0.15); color: var(--d); }
  .tier-Skip { background: rgba(100,116,139,0.2); color: var(--skip); }
  .role-EMD { background: rgba(52,211,153,0.18); color: var(--emd); }
  .role-Brand { background: rgba(251,191,36,0.18); color: var(--brand); }
  .role-Area { background: rgba(96,165,250,0.18); color: var(--area); }
  .role-Mention { background: rgba(148,163,184,0.15); color: var(--mention); }
  .role-Skip { background: rgba(100,116,139,0.2); color: var(--skip); }
  .rec-box.brand h3 { color: var(--brand); }
  .bar {
    height: 7px; border-radius: 99px; background: #2a3644; overflow: hidden; width: 80px; display: inline-block; vertical-align: middle; margin-right: 8px;
  }
  .bar > i { display: block; height: 100%; background: var(--accent); }
  .bar.comp > i { background: var(--warn); }
  .bar.comp.high > i { background: var(--bad); }
  .bar.comp.low > i { background: var(--good); }
  .meta { color: var(--muted); font-size: 0.85rem; margin: 10px 0 0; }
  .legend { color: var(--muted); font-size: 0.82rem; margin-top: 14px; line-height: 1.6; }
  .legend strong { color: var(--text); font-weight: 600; }
  .mode-tabs { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
  .mode-tabs button { width: auto; padding: 8px 14px; }
  .mode-tabs button.active { box-shadow: 0 0 0 2px rgba(61,156,240,0.35); }
  .hidden { display: none !important; }
  .plan-summary { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
  .plan-pill {
    background: var(--panel2); border: 1px solid var(--border); border-radius: 10px;
    padding: 10px 14px; min-width: 120px;
  }
  .plan-pill .n { font-size: 1.35rem; font-weight: 700; }
  .plan-pill .l { color: var(--muted); font-size: 0.78rem; margin-top: 2px; }
  .plan-pill.emd .n { color: var(--emd); }
  .plan-pill.brand .n { color: var(--brand); }
  .plan-pill.area .n { color: var(--area); }
  .plan-grid { display: grid; grid-template-columns: 1fr 1.15fr; gap: 16px; align-items: start; }
  @media (max-width: 980px) { .plan-grid { grid-template-columns: 1fr; } }
  .plan-col {
    background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 14px;
    max-height: calc(100vh - 220px); overflow: auto;
  }
  .plan-col h2 { margin: 0 0 4px; font-size: 1.05rem; }
  .plan-col .subh { color: var(--muted); font-size: 0.8rem; margin-bottom: 12px; }
  .emd-row, .cluster-card {
    border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; margin-bottom: 8px;
    background: #151c24;
  }
  .emd-row {
    display: grid; grid-template-columns: minmax(110px, 1.1fr) 1fr auto; gap: 10px; align-items: center;
  }
  .emd-row .town { font-weight: 650; }
  .emd-row .vol { font-variant-numeric: tabular-nums; font-weight: 700; color: var(--emd); white-space: nowrap; }
  .volbar {
    height: 8px; border-radius: 99px; background: #2a3644; overflow: hidden;
  }
  .volbar > i { display: block; height: 100%; border-radius: 99px; }
  .volbar.emd > i { background: var(--emd); }
  .volbar.brand > i { background: var(--brand); }
  .volbar.area > i { background: var(--area); }
  .cluster-card h3 {
    margin: 0 0 6px; font-size: 0.98rem; display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap;
  }
  .cluster-card h3 .brand-name { color: var(--brand); }
  .cluster-card h3 .combined { color: var(--muted); font-weight: 600; font-size: 0.85rem; }
  .cluster-meta { color: var(--muted); font-size: 0.75rem; margin-bottom: 8px; }
  .area-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .area-list li {
    display: grid; grid-template-columns: minmax(90px, 1fr) 1fr auto; gap: 8px; align-items: center;
    font-size: 0.88rem;
  }
  .area-list .tag {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.03em;
    padding: 1px 6px; border-radius: 999px; margin-left: 6px; vertical-align: middle;
  }
  .area-list .tag.Brand { background: rgba(251,191,36,0.18); color: var(--brand); }
  .area-list .tag.Area { background: rgba(96,165,250,0.18); color: var(--area); }
  .area-list .tag.Mention, .area-list .tag.Skip { background: rgba(148,163,184,0.15); color: var(--mention); }
  .plan-empty { color: var(--muted); font-size: 0.9rem; padding: 12px 0; }
  .plan-tools { margin-bottom: 12px; }
  .plan-tools label.chk { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--muted); margin-top: 18px; }
  .plan-tools input[type=checkbox] { width: auto; }
  .site-layout { display: grid; grid-template-columns: 320px 1fr; gap: 14px; min-height: 70vh; }
  @media (max-width: 980px) { .site-layout { grid-template-columns: 1fr; } }
  .site-index {
    background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 12px;
    max-height: calc(100vh - 200px); overflow: auto; position: sticky; top: 12px;
  }
  .site-index h3 { margin: 12px 0 8px; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
  .site-index h3:first-child { margin-top: 4px; }
  .site-item {
    display: block; width: 100%; text-align: left; background: #151c24; border: 1px solid var(--border);
    border-radius: 10px; padding: 10px 12px; margin-bottom: 6px; cursor: pointer; color: var(--text);
  }
  .site-item:hover { border-color: #4b6280; }
  .site-item.active { border-color: var(--accent); box-shadow: 0 0 0 1px rgba(61,156,240,0.35); }
  .site-item .t { font-weight: 650; }
  .site-item .m { color: var(--muted); font-size: 0.75rem; margin-top: 2px; }
  .site-item.emd .t { color: var(--emd); }
  .site-item.brand .t { color: var(--brand); }
  .site-detail {
    background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 16px 18px;
    max-height: calc(100vh - 200px); overflow: auto;
  }
  .site-detail .empty-detail { color: var(--muted); padding: 40px 12px; text-align: center; }
  .site-hero { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
  .site-hero h2 { margin: 0 0 4px; font-size: 1.35rem; }
  .site-hero .domain { color: var(--good); font-weight: 600; }
  .badge-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
  .badge {
    font-size: 0.72rem; padding: 3px 8px; border-radius: 999px; border: 1px solid var(--border);
    background: var(--panel2); color: var(--muted);
  }
  .badge.emd { color: var(--emd); border-color: rgba(52,211,153,0.35); }
  .badge.brand { color: var(--brand); border-color: rgba(251,191,36,0.35); }
  .site-tabs { display: flex; gap: 6px; flex-wrap: wrap; margin: 12px 0 14px; }
  .site-tabs button {
    width: auto; padding: 7px 12px; background: var(--panel2); color: var(--muted); border: 1px solid var(--border);
  }
  .site-tabs button.on { color: var(--text); border-color: var(--accent); background: #1c2a3a; }
  .site-section { display: none; }
  .site-section.on { display: block; }
  .sitemap-tree { list-style: none; margin: 0; padding: 0; }
  .sitemap-tree li {
    border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; margin-bottom: 7px; background: #151c24;
  }
  .sitemap-tree .path { font-family: ui-monospace, Consolas, monospace; color: var(--accent); font-size: 0.85rem; }
  .sitemap-tree .ptitle { font-weight: 650; margin-top: 2px; }
  .sitemap-tree .pmeta { color: var(--muted); font-size: 0.78rem; margin-top: 3px; }
  .sitemap-tree li.clickable { cursor: pointer; }
  .sitemap-tree li.clickable:hover, .sitemap-tree li.hl {
    border-color: rgba(96,165,250,0.55); background: #172231;
  }
  .kw-table, .content-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  .kw-table th, .content-table th, .kw-table td, .content-table td {
    text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: top;
  }
  .kw-table th, .content-table th { color: var(--muted); font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.03em; }
  .kw-pri { color: var(--emd); font-weight: 650; }
  .kw-sec { color: var(--area); }
  .kw-sup { color: var(--muted); }
  .lock-note {
    display: inline-flex; gap: 8px; align-items: center; flex-wrap: wrap;
    background: #1a2736; border: 1px solid #314860; color: #b7c8da;
    border-radius: 10px; padding: 8px 12px; font-size: 0.82rem; margin-bottom: 12px;
  }
  .lock-note strong { color: var(--text); }
  .area-chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0 4px; }
  .area-chip {
    width: auto; padding: 5px 10px; font-size: 0.78rem; background: #15202b; border: 1px solid var(--border); color: var(--text);
  }
  .area-chip:hover { border-color: var(--area); }
  .area-chip.on { border-color: var(--area); color: var(--area); }
  .badge.high { color: var(--emd); border-color: rgba(52,211,153,0.45); }
  .badge.low { color: #94a3b8; border-color: rgba(148,163,184,0.4); }
  .badge.moderate { color: #f0b429; border-color: rgba(240,180,41,0.45); }
  .badge.good { color: #60a5fa; border-color: rgba(96,165,250,0.45); }
  .site-item.low .t { color: #94a3b8; }
  .site-item.moderate .t { color: #f0b429; }
  .site-item.good .t { color: #60a5fa; }
  .sitemap-group {
    margin: 14px 0 8px; padding: 6px 10px; border-radius: 8px;
    background: #1a2736; color: var(--muted); font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700;
  }
  .sitemap-group.areas { color: var(--area); background: rgba(96,165,250,0.08); }
  .area-url-block {
    border: 1px solid rgba(96,165,250,0.25); border-radius: 12px; padding: 8px;
    margin-bottom: 10px; background: rgba(96,165,250,0.04);
  }
  .map-layout { display: grid; grid-template-columns: 300px 1fr; gap: 14px; min-height: 70vh; }
  @media (max-width: 980px) { .map-layout { grid-template-columns: 1fr; } }
  .map-side {
    background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 12px;
    max-height: calc(100vh - 200px); overflow: auto;
  }
  #coverageMap {
    height: calc(100vh - 200px); min-height: 520px; border-radius: 14px;
    border: 1px solid var(--border); background: #0b1220;
  }
  .map-legend { display: grid; gap: 6px; margin: 10px 0; font-size: 0.82rem; }
  .map-legend span { display: inline-flex; align-items: center; gap: 8px; }
  .dot {
    width: 10px; height: 10px; border-radius: 50%; display: inline-block;
    box-shadow: 0 0 0 2px rgba(0,0,0,0.25);
  }
  .dot.high { background: #34d399; }
  .dot.low { background: #94a3b8; }
  .dot.moderate { background: #f0b429; }
  .dot.good { background: #60a5fa; }
  .dot.pick { background: #f472b6; }
  .map-cover-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .map-cover-list li {
    border: 1px solid var(--border); border-radius: 8px; padding: 8px 10px; background: #151c24; font-size: 0.85rem;
  }
  .map-cover-list .t { font-weight: 650; }
  .map-cover-list .m { color: var(--muted); font-size: 0.75rem; margin-top: 2px; }
  .map-chk { display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: var(--muted); margin: 4px 0; }
  .map-chk input { width: auto; }
  .leaflet-container { font: inherit; background: #0b1220; }
  .leaflet-popup-content-wrapper { background: #1a222c; color: #e8eef4; border-radius: 10px; }
  .leaflet-popup-tip { background: #1a222c; }
  .leaflet-popup-content { margin: 10px 12px; font-size: 0.85rem; }
</style>
</head>
<body>
<header>
  <h1>Scotland Solar Panel Keyword Explorer</h1>
  <p class="sub">Scottish places only. Primary term is “solar panels {place}” from DataForSEO Labs, Google UK, checked November 2026. Places with no Labs volume are left out. Suggested domains are name ideas, not availability checks. CPC is the Labs figure in USD.</p>
</header>
<div class="wrap">
  <div class="mode-tabs">
    <button type="button" id="modeAll" class="active">All towns</button>
    <button type="button" id="modeRadius" class="secondary">Radius cluster</button>
    <button type="button" id="modePlan" class="secondary">Plan board</button>
    <button type="button" id="modeSites" class="secondary">Site plans</button>
    <button type="button" id="modeMap" class="secondary">Scotland map</button>
  </div>

  <div class="stats" id="stats"></div>

  <div class="panel" id="radiusPanel" class="hidden">
    <h2>Radius cluster planner</h2>
    <div class="radius-controls">
      <div>
        <label for="hub">Hub town (required for catchment)</label>
        <select id="hub"></select>
      </div>
      <div>
        <label for="radius">Miles from hub</label>
        <select id="radius">
          <option value="5">5 miles</option>
          <option value="10">10 miles</option>
          <option value="15">15 miles</option>
          <option value="20" selected>20 miles</option>
          <option value="25">25 miles</option>
          <option value="30">30 miles</option>
          <option value="40">40 miles</option>
        </select>
      </div>
      <div>
        <label for="emdFloor">EMD volume floor</label>
        <input id="emdFloor" type="number" min="10" step="10" value="70" />
      </div>
      <div>
        <label for="radiusRegion">Limit to region</label>
        <select id="radiusRegion"><option value="">All regions</option></select>
      </div>
      <div>
        <label>&nbsp;</label>
        <button id="applyRadius" type="button">Build clusters</button>
      </div>
      <div>
        <label>&nbsp;</label>
        <button id="exportRadiusBtn" type="button" class="secondary">Export CSV</button>
      </div>
    </div>
    <div class="rec" id="recBoxes">
      <div class="rec-box emd"><h3>Solo EMDs (vol ≥ floor)</h3><ul id="recEmd"><li class="note">Click Build clusters</li></ul></div>
      <div class="rec-box brand"><h3>Low-vol cluster brands</h3><ul id="recBrand"><li class="note">—</li></ul></div>
      <div class="rec-box area"><h3>Area pages on cluster brands</h3><ul id="recArea"><li class="note">—</li></ul></div>
    </div>
    <p class="note" id="radiusNote">
      Pick a hub (e.g. Glasgow) + miles. The table lists every place in this Scotland list within that distance. Volume at or above the floor stays a solo site. Places below the floor become one brand around the hub.
    </p>
  </div>

  <div class="panel hidden" id="planPanel">
    <h2>Full plan board</h2>
    <p class="note" style="margin-top:0">Scotland view: every solo site, then every smaller brand cluster with its area pages. Neighbour radius links places that sit near each other. Solo sites are never folded into a cluster.</p>
    <div class="radius-controls plan-tools">
      <div>
        <label for="planRadius">Cluster link radius</label>
        <select id="planRadius">
          <option value="5">5 miles</option>
          <option value="10">10 miles</option>
          <option value="15">15 miles</option>
          <option value="20" selected>20 miles</option>
          <option value="25">25 miles</option>
          <option value="30">30 miles</option>
        </select>
      </div>
      <div>
        <label for="planFloor">EMD volume floor</label>
        <input id="planFloor" type="number" min="10" step="10" value="70" />
      </div>
      <div>
        <label for="planRegion">Region</label>
        <select id="planRegion"><option value="">All regions</option></select>
      </div>
      <div>
        <label for="planSearch">Find town</label>
        <input id="planSearch" type="search" placeholder="Filter board…" />
      </div>
      <div>
        <label class="chk"><input type="checkbox" id="planMultiOnly" /> Multi-town brands only</label>
      </div>
      <div>
        <label>&nbsp;</label>
        <button id="planRefresh" type="button">Refresh board</button>
      </div>
    </div>
    <div class="plan-summary" id="planSummary"></div>
    <div class="plan-grid">
      <div class="plan-col">
        <h2 style="color:var(--emd)">Solo EMDs</h2>
        <div class="subh" id="planEmdSub">Towns at/above the volume floor — each gets its own domain</div>
        <div id="planEmdList"></div>
      </div>
      <div class="plan-col">
        <h2 style="color:var(--brand)">Brand clusters</h2>
        <div class="subh" id="planBrandSub">Low-vol towns only — brand name + area pages (never under an EMD)</div>
        <div id="planBrandList"></div>
      </div>
    </div>
  </div>

  <div class="panel hidden" id="sitesPanel">
    <h2>Site plans</h2>
    <div class="lock-note">
      Locked: <strong>20 mi</strong> · <strong>vol ≥ 70 = high EMD</strong> ·
      1-town clusters → <strong>low EMD</strong> ·
      2–4 town clusters → <strong>moderate</strong> (separate) ·
      5+ town clusters → <strong>good</strong> brand ·
      every cluster town gets its own <code>/areas/…/</code> URL.
    </div>
    <div class="radius-controls plan-tools" style="margin-bottom:12px">
      <div>
        <label for="sitesSearch">Find site / town</label>
        <input id="sitesSearch" type="search" placeholder="e.g. glasgow, fife, galashiels…" />
      </div>
      <div>
        <label for="sitesFilter">Show</label>
        <select id="sitesFilter">
          <option value="all">All sites</option>
          <option value="high">High EMDs (vol ≥ 70)</option>
          <option value="low">Low EMDs (1 town)</option>
          <option value="moderate">Moderate clusters (2–4)</option>
          <option value="good">Good clusters (5+)</option>
        </select>
      </div>
      <div>
        <label>&nbsp;</label>
        <button id="sitesExport" type="button" class="secondary">Export open plan</button>
      </div>
    </div>
    <div class="site-layout">
      <div class="site-index" id="sitesIndex"></div>
      <div class="site-detail" id="sitesDetail">
        <div class="empty-detail">Select an EMD or brand on the left to open its sitemap, content plan, and keyword targets.</div>
      </div>
    </div>
  </div>

  <div class="panel hidden" id="mapPanel">
    <h2>Scotland coverage map</h2>
    <p class="note" style="margin-top:0">Same locked plan as Site plans (20 mi clusters · vol ≥ 70). Pick a location to see what sits inside a coverage radius, or click markers on the map.</p>
    <div class="map-layout">
      <div class="map-side">
        <div>
          <label for="mapTown">Select location</label>
          <select id="mapTown"></select>
        </div>
        <div style="margin-top:10px">
          <label for="mapCoverMiles">Coverage radius (miles)</label>
          <select id="mapCoverMiles">
            <option value="5">5 miles</option>
            <option value="10">10 miles</option>
            <option value="15">15 miles</option>
            <option value="20" selected>20 miles</option>
            <option value="25">25 miles</option>
            <option value="30">30 miles</option>
            <option value="40">40 miles</option>
          </select>
        </div>
        <div style="margin-top:10px">
          <label>Show layers</label>
          <label class="map-chk"><input type="checkbox" id="mapShowHigh" checked /> High EMDs</label>
          <label class="map-chk"><input type="checkbox" id="mapShowLow" checked /> Low EMDs</label>
          <label class="map-chk"><input type="checkbox" id="mapShowModerate" checked /> Moderate clusters</label>
          <label class="map-chk"><input type="checkbox" id="mapShowGood" checked /> Good clusters</label>
          <label class="map-chk"><input type="checkbox" id="mapShowCircles" /> Site 15 mi rings (hubs)</label>
        </div>
        <div class="map-legend">
          <span><i class="dot high"></i> High EMD (vol ≥ 70)</span>
          <span><i class="dot low"></i> Low EMD (1 town)</span>
          <span><i class="dot moderate"></i> Moderate (2–4)</span>
          <span><i class="dot good"></i> Good (5+)</span>
          <span><i class="dot pick"></i> Selected location</span>
        </div>
        <button type="button" id="mapFitUk" class="secondary" style="width:100%;margin-bottom:10px">Reset Scotland view</button>
        <button type="button" id="mapOpenSite" style="width:100%;margin-bottom:10px">Open site plan for selection</button>
        <h3 style="margin:8px 0;font-size:0.9rem">Inside coverage</h3>
        <div id="mapCoverSummary" class="note">Select a town to inspect coverage.</div>
        <ul class="map-cover-list" id="mapCoverList"></ul>
      </div>
      <div id="coverageMap"></div>
    </div>
  </div>

  <div id="filterPanel">
    <div class="controls">
      <div>
        <label for="q">Search town / keyword</label>
        <input id="q" type="search" placeholder="e.g. glasgow, edinburgh, fife" />
      </div>
      <div>
        <label for="tier">Tier</label>
        <select id="tier">
          <option value="">All tiers</option>
          <option value="S">S — 200+ searches</option>
          <option value="A">A — 70–199</option>
          <option value="B">B — 30–69</option>
          <option value="C">C — 20–29</option>
          <option value="D">D — about 10</option>
          <option value="Skip">Skip</option>
        </select>
      </div>
      <div>
        <label for="region">Region</label>
        <select id="region"><option value="">All regions</option></select>
      </div>
      <div>
        <label for="minVol">Min volume</label>
        <input id="minVol" type="number" min="0" step="10" value="0" />
      </div>
      <div>
        <label for="maxComp">Max competition %</label>
        <input id="maxComp" type="number" min="0" max="100" step="1" value="100" />
      </div>
      <div>
        <label>&nbsp;</label>
        <button id="exportBtn" type="button">Export CSV</button>
      </div>
    </div>
    <div class="chips" id="chips">
      <button type="button" class="chip" data-preset="priority">Priority (S+A)</button>
      <button type="button" class="chip" data-preset="clyde">Glasgow & Clyde</button>
      <button type="button" class="chip" data-preset="lothian">Edinburgh & Lothians</button>
      <button type="button" class="chip" data-preset="floor">Volume ≥ 70</button>
      <button type="button" class="chip" data-preset="value">High CPC (≥$10)</button>
      <button type="button" class="chip" data-preset="small">Small towns (D)</button>
      <button type="button" class="chip" data-preset="reset">Reset</button>
    </div>
  </div>

  <div class="table-wrap" id="tableWrap">
    <table>
      <thead>
        <tr>
          <th data-key="cluster_name">Cluster <span class="arrow"></span></th>
          <th data-key="role">Page role <span class="arrow"></span></th>
          <th data-key="brand_hub">Brand <span class="arrow"></span></th>
          <th data-key="miles">Mi to brand <span class="arrow"></span></th>
          <th data-key="tier">Tier <span class="arrow"></span></th>
          <th data-key="town">Town <span class="arrow"></span></th>
          <th data-key="volume">Volume <span class="arrow"></span></th>
          <th data-key="cpc">CPC $ <span class="arrow"></span></th>
          <th data-key="competition">Ads competition <span class="arrow"></span></th>
          <th data-key="opportunity_score">Opportunity <span class="arrow"></span></th>
          <th data-key="region">Region <span class="arrow"></span></th>
          <th data-key="emd_best_available">Suggested EMD <span class="arrow"></span></th>
          <th data-key="emd_primary">Domain pattern <span class="arrow"></span></th>
        </tr>
      </thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
  <p class="meta" id="meta"></p>
  <p class="legend" id="legend">
    <strong>Catchment mode:</strong>
    Choose a hub and a distance to see every Scottish place in this list inside that circle.
    Places at or above the volume floor stay solo sites. Places below it share one brand, and that brand never includes the solo sites.
    Leave the hub empty to auto-cluster the smaller places by neighbour distance.
  </p>
</div>
<script>
const DATA = __DATA__;
let mode = "all"; // all | radius | plan | sites | map
let sortKey = "volume";
let sortDir = "desc";
let filtered = [...DATA];
let radiusActive = false;
let siteCatalog = []; // built for Site plans tab
let activeSiteId = null;
let activeSiteTab = "overview";
let activeAreaFocus = null;
const SITE_PLAN_RADIUS = 20;
const SITE_PLAN_FLOOR = 70;
let coverageMap = null;
let mapMarkersLayer = null;
let mapCirclesLayer = null;
let mapPickCircle = null;
let mapPickMarker = null;
let mapTownIndex = new Map(); // town lower -> {row, site, value}

const q = document.getElementById("q");
const tier = document.getElementById("tier");
const region = document.getElementById("region");
const minVol = document.getElementById("minVol");
const maxComp = document.getElementById("maxComp");
const tbody = document.getElementById("tbody");
const stats = document.getElementById("stats");
const meta = document.getElementById("meta");
const hub = document.getElementById("hub");
const radius = document.getElementById("radius");
const emdFloor = document.getElementById("emdFloor");
const radiusPanel = document.getElementById("radiusPanel");
const filterPanel = document.getElementById("filterPanel");
const planPanel = document.getElementById("planPanel");
const sitesPanel = document.getElementById("sitesPanel");
const mapPanel = document.getElementById("mapPanel");
const tableWrap = document.getElementById("tableWrap");
const legend = document.getElementById("legend");

radiusPanel.classList.add("hidden");

const regions = [...new Set(DATA.map(d => d.region))].sort();
regions.forEach(r => {
  const o = document.createElement("option");
  o.value = r; o.textContent = r; region.appendChild(o);
});

const radiusRegion = document.getElementById("radiusRegion");
regions.forEach(r => {
  const o = document.createElement("option");
  o.value = r; o.textContent = r; radiusRegion.appendChild(o);
});

const planRegion = document.getElementById("planRegion");
regions.forEach(r => {
  const o = document.createElement("option");
  o.value = r; o.textContent = r; planRegion.appendChild(o);
});

const noneOpt = document.createElement("option");
noneOpt.value = "";
noneOpt.textContent = "— None (auto-cluster) —";
hub.appendChild(noneOpt);
const hubs = DATA.filter(d => d.lat != null).slice().sort((a,b) => a.town.localeCompare(b.town));
hubs.forEach(d => {
  const o = document.createElement("option");
  o.value = d.town;
  o.textContent = `${d.town} (${d.volume}/mo)`;
  hub.appendChild(o);
});
hub.value = ""; // default: no forced centre

function money(n){ return "$" + (Number(n) || 0).toFixed(2); }
function maxVol(){ return Math.max(...DATA.map(d => d.volume), 1); }
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function haversineMiles(lat1, lng1, lat2, lng2) {
  const R = 3958.8;
  const toRad = d => d * Math.PI / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a = Math.sin(dLat/2)**2 + Math.cos(toRad(lat1))*Math.cos(toRad(lat2))*Math.sin(dLng/2)**2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

function strongestTown(rows) {
  return [...rows].sort((a,b) => b.volume - a.volume || b.opportunity_score - a.opportunity_score)[0];
}

/** Connected components: towns linked if within linkMiles of each other. */
function buildAutoClusters(towns, linkMiles) {
  const n = towns.length;
  const parent = Array.from({length: n}, (_, i) => i);
  function find(i){ return parent[i] === i ? i : (parent[i] = find(parent[i])); }
  function unite(i,j){ const a=find(i), b=find(j); if (a!==b) parent[a]=b; }
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const d = haversineMiles(towns[i].lat, towns[i].lng, towns[j].lat, towns[j].lng);
      if (d <= linkMiles) unite(i, j);
    }
  }
  const groups = new Map();
  for (let i = 0; i < n; i++) {
    const root = find(i);
    if (!groups.has(root)) groups.set(root, []);
    groups.get(root).push(towns[i]);
  }
  return [...groups.values()];
}

/** Solo EMD for one high-volume town — never joins a low-vol brand. */
function assignSoloEmd(r, floor) {
  const copy = {...r};
  copy.cluster_id = "";
  copy.cluster_name = `EMD · ${r.town}`;
  copy.brand_hub = r.town;
  copy.miles = 0;
  copy.cluster_volume = r.volume;
  copy.role = "EMD";
  copy.role_reason = `Volume ≥ ${floor} → own EMD (not shared with low-vol clusters)`;
  return copy;
}

/** Low-volume towns only: one Brand + Area/Mention pages. Never includes ≥floor EMDs.
 *  preferredHub: when set (catchment mode), that town is the brand if it is in the low-vol set.
 *  milesFrom: optional centre for Miles column (hub lat/lng object {lat,lng,town}).
 */
function assignLowVolCluster(rows, clusterId, floor, preferredHub, milesFrom) {
  if (!rows.length) return [];
  let brand = preferredHub && rows.some(r => r.town === preferredHub)
    ? rows.find(r => r.town === preferredHub)
    : strongestTown(rows);
  const clusterVol = rows.reduce((s, t) => s + (t.volume || 0), 0);
  const clusterName = `Brand · ${brand.town}`;
  const mileCentre = milesFrom || brand;
  return rows.map(r => {
    const copy = {...r};
    copy.cluster_id = clusterId;
    copy.cluster_name = clusterName;
    copy.brand_hub = brand.town;
    copy.cluster_volume = clusterVol;
    if (mileCentre.lat != null && r.lat != null) {
      copy.miles = Math.round(haversineMiles(r.lat, r.lng, mileCentre.lat, mileCentre.lng) * 10) / 10;
    } else {
      copy.miles = "";
    }
    if (r.volume <= 0) {
      copy.role = "Skip";
      copy.role_reason = "No measurable volume";
      return copy;
    }
    if (r.town === brand.town) {
      copy.role = "Brand";
      copy.role_reason = `Low-vol cluster brand (combined ${clusterVol}/mo, all towns < ${floor})`;
    } else if (r.volume >= 20) {
      copy.role = "Area";
      copy.role_reason = `Area page on ${brand.town} brand (not on any ≥${floor} EMD)`;
    } else {
      copy.role = "Mention";
      copy.role_reason = `Mention on ${brand.town} brand`;
    }
    return copy;
  });
}

function setMode(next) {
  mode = next;
  document.getElementById("modeAll").classList.toggle("active", mode === "all");
  document.getElementById("modeRadius").classList.toggle("active", mode === "radius");
  document.getElementById("modePlan").classList.toggle("active", mode === "plan");
  document.getElementById("modeSites").classList.toggle("active", mode === "sites");
  document.getElementById("modeMap").classList.toggle("active", mode === "map");
  document.getElementById("modeAll").classList.toggle("secondary", mode !== "all");
  document.getElementById("modeRadius").classList.toggle("secondary", mode !== "radius");
  document.getElementById("modePlan").classList.toggle("secondary", mode !== "plan");
  document.getElementById("modeSites").classList.toggle("secondary", mode !== "sites");
  document.getElementById("modeMap").classList.toggle("secondary", mode !== "map");

  radiusPanel.classList.toggle("hidden", mode !== "radius");
  filterPanel.classList.toggle("hidden", mode !== "all");
  planPanel.classList.toggle("hidden", mode !== "plan");
  sitesPanel.classList.toggle("hidden", mode !== "sites");
  mapPanel.classList.toggle("hidden", mode !== "map");
  const hideTable = mode === "plan" || mode === "sites" || mode === "map";
  tableWrap.classList.toggle("hidden", hideTable);
  legend.classList.toggle("hidden", hideTable);
  meta.classList.toggle("hidden", hideTable);
  if (mode === "all") {
    radiusActive = false;
    DATA.forEach(d => { delete d.miles; delete d.role; delete d.role_reason; });
    applyFilter();
  } else if (mode === "radius") {
    applyRadius();
  } else if (mode === "plan") {
    renderPlanBoard();
  } else if (mode === "sites") {
    renderSitesTab();
  } else {
    renderMapTab();
  }
}

/** Nationwide plan: solo EMDs + low-vol brand clusters (same rules as radius, no hub). */
function computeNationwidePlan(linkMiles, floor, regionFilter) {
  let pool = DATA.filter(d => d.lat != null);
  if (regionFilter) pool = pool.filter(d => d.region === regionFilter);
  const high = pool.filter(d => d.volume >= floor).sort((a,b) => b.volume - a.volume);
  const low = pool.filter(d => d.volume < floor);
  const emds = high.map(r => assignSoloEmd(r, floor));
  let lowClusters = buildAutoClusters(low, linkMiles)
    .map(c => c.filter(Boolean))
    .filter(c => c.length)
    .sort((a, b) => {
      const va = a.reduce((s, t) => s + t.volume, 0);
      const vb = b.reduce((s, t) => s + t.volume, 0);
      return vb - va;
    });
  const brands = lowClusters.map((clusterTowns, idx) => {
    const rows = assignLowVolCluster(clusterTowns, idx + 1, floor, null, null);
    const brand = rows.find(r => r.role === "Brand") || rows[0];
    return {
      id: idx + 1,
      name: brand ? brand.town : rows[0].town,
      cluster_volume: rows.reduce((s, t) => s + (t.volume || 0), 0),
      towns: rows.sort((a, b) => {
        const rank = r => (r.role === "Brand" ? 0 : r.role === "Area" ? 1 : 2);
        return rank(a) - rank(b) || b.volume - a.volume;
      }),
    };
  });
  return { emds, brands, poolSize: pool.length };
}

function renderPlanBoard() {
  const linkMiles = Number(document.getElementById("planRadius").value);
  const floor = Number(document.getElementById("planFloor").value || 70);
  const reg = planRegion.value;
  const qPlan = (document.getElementById("planSearch").value || "").trim().toLowerCase();
  const multiOnly = document.getElementById("planMultiOnly").checked;
  const { emds, brands, poolSize } = computeNationwidePlan(linkMiles, floor, reg);

  let emdList = emds;
  let brandList = brands;
  if (qPlan) {
    emdList = emds.filter(r => r.town.toLowerCase().includes(qPlan) || (r.region || "").toLowerCase().includes(qPlan));
    brandList = brands.filter(b =>
      b.name.toLowerCase().includes(qPlan) ||
      b.towns.some(t => t.town.toLowerCase().includes(qPlan))
    );
  }
  if (multiOnly) brandList = brandList.filter(b => b.towns.filter(t => t.volume > 0).length > 1);

  const areaCount = brandList.reduce((s, b) => s + b.towns.filter(t => t.role === "Area").length, 0);
  const brandVol = brandList.reduce((s, b) => s + b.cluster_volume, 0);
  const emdVol = emdList.reduce((s, r) => s + r.volume, 0);
  const maxE = Math.max(...emdList.map(r => r.volume), 1);
  const maxB = Math.max(...brandList.map(b => b.cluster_volume), 1);

  document.getElementById("planSummary").innerHTML = `
    <div class="plan-pill emd"><div class="n">${emdList.length}</div><div class="l">Solo EMDs · ${emdVol.toLocaleString()}/mo</div></div>
    <div class="plan-pill brand"><div class="n">${brandList.length}</div><div class="l">Brand clusters · ${brandVol.toLocaleString()}/mo</div></div>
    <div class="plan-pill area"><div class="n">${areaCount}</div><div class="l">Area pages on brands</div></div>
    <div class="plan-pill"><div class="n">${linkMiles} mi</div><div class="l">Link radius · floor ${floor} · ${poolSize} towns</div></div>
  `;
  document.getElementById("planEmdSub").textContent =
    `${emdList.length} towns ≥ ${floor} vol — each is its own EMD domain`;
  document.getElementById("planBrandSub").textContent =
    `${brandList.length} brands from towns under ${floor} (linked within ${linkMiles} mi) — area pages stay on these brands only`;

  document.getElementById("planEmdList").innerHTML = emdList.length
    ? emdList.map(r => `
      <div class="emd-row">
        <div>
          <div class="town">${escapeHtml(r.town)}</div>
          <div style="color:var(--muted);font-size:0.75rem">${escapeHtml(r.region || "")}${r.emd_best_available ? " · " + escapeHtml(r.emd_best_available) : ""}</div>
        </div>
        <div class="volbar emd" title="${r.volume}/mo"><i style="width:${Math.round(r.volume / maxE * 100)}%"></i></div>
        <div class="vol">${r.volume.toLocaleString()}/mo</div>
      </div>`).join("")
    : `<div class="plan-empty">No EMDs match.</div>`;

  document.getElementById("planBrandList").innerHTML = brandList.length
    ? brandList.map(b => {
        const members = b.towns.filter(t => !qPlan || t.town.toLowerCase().includes(qPlan) || b.name.toLowerCase().includes(qPlan));
        const show = members.length ? members : b.towns;
        return `
        <div class="cluster-card">
          <h3>
            <span class="brand-name">Brand · ${escapeHtml(b.name)}</span>
            <span class="combined">combined ${b.cluster_volume.toLocaleString()}/mo · ${b.towns.length} towns</span>
          </h3>
          <div class="volbar brand" style="margin-bottom:8px"><i style="width:${Math.round(b.cluster_volume / maxB * 100)}%"></i></div>
          <div class="cluster-meta">Low-vol cluster only — not shared with any ≥${floor} EMD</div>
          <ul class="area-list">
            ${show.map(t => `
              <li>
                <div>${escapeHtml(t.town)}<span class="tag ${t.role}">${t.role}</span></div>
                <div class="volbar area"><i style="width:${Math.max(2, Math.round((t.volume || 0) / Math.max(b.cluster_volume, 1) * 100))}%"></i></div>
                <div style="font-variant-numeric:tabular-nums;color:${t.role === "Brand" ? "var(--brand)" : "var(--text)"}">${(t.volume || 0).toLocaleString()}/mo</div>
              </li>`).join("")}
          </ul>
        </div>`;
      }).join("")
    : `<div class="plan-empty">No brand clusters match.</div>`;

  stats.innerHTML = `
    <div class="stat"><div class="n">${emdList.length}</div><div class="l">Solo EMDs</div></div>
    <div class="stat"><div class="n">${brandList.length}</div><div class="l">Brand clusters</div></div>
    <div class="stat"><div class="n">${areaCount}</div><div class="l">Area pages</div></div>
    <div class="stat"><div class="n">${(emdVol + brandVol).toLocaleString()}</div><div class="l">Plan volume / mo</div></div>
  `;
}

function prettyTown(t) {
  return String(t || "").replace(/\b\w/g, c => c.toUpperCase());
}
function slugTown(t) {
  return String(t || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}
function domainFor(row) {
  return row.emd_primary || (`solarpanels${slugTown(row.town).replace(/-/g,"")}.co.uk`);
}
function brandDomain(brandName) {
  const s = slugTown(brandName).replace(/-/g, "");
  return `${s}solar.co.uk`;
}

function servicePages(townLabel) {
  const T = prettyTown(townLabel);
  const scot = String(townLabel).toLowerCase() === "scotland";
  return [
    { slug: "solar-panel-installation", title: `Solar Panel Installation ${T}`, h1: `Solar Panel Installation in ${T}`, primary: `solar panel installation ${townLabel}`, words: 1100, brief: `Domestic install page for ${T}. System sizes, MCS, roof types, process, and a quote form.` },
    { slug: "solar-battery-storage", title: `Solar Battery Storage ${T}`, h1: `Solar Battery Storage in ${T}`, primary: `solar battery storage ${townLabel}`, words: 1000, brief: `Solar plus battery for ${T}: export, backup, and when a battery is worth adding.` },
    { slug: "solar-panel-cost", title: `Solar Panel Cost ${T}`, h1: `Solar Panel Cost in ${T}`, primary: scot ? "cost of solar panels scotland" : `solar panels cost ${townLabel}`, words: 1000, brief: `Price ranges for ${T}. 4kW and 6kW, battery add-on, scaffolding, and what moves the quote.` },
    { slug: "commercial-solar-panels", title: `Commercial Solar Panels ${T}`, h1: `Commercial Solar Panels in ${T}`, primary: `commercial solar panels ${townLabel}`, words: 900, brief: `Business roofs, farms, and warehouses in ${T}.` },
    { slug: "solar-panel-grants", title: `Solar Panel Grants ${T}`, h1: `Solar Panel Grants in ${T}`, primary: scot ? "solar panel grants scotland" : `solar panel grants ${townLabel}`, words: 1100, brief: scot ? `Home Energy Scotland grant and interest-free loan. Who qualifies, and why the install has to be MCS.` : `How the Scotland grant and loan applies to homeowners in ${T}.` },
    { slug: "solar-panel-repairs", title: `Solar Panel Repairs ${T}`, h1: `Solar Panel Repairs in ${T}`, primary: `solar panel repairs ${townLabel}`, words: 700, brief: `Inverters, monitoring, bird proofing, and maintenance for systems already on roofs in ${T}.` },
  ];
}

function keywordsForTown(town, volume, role) {
  const t = town.toLowerCase();
  const page = role === "area" ? `/areas/${slugTown(t)}/` : "/";
  const primary = t === "scotland" ? "solar panels scotland" : `solar panels ${t}`;
  const row = DATA.find(d => d.town.toLowerCase() === t) || {};
  const rows = [
    { kw: primary, type: "Primary", page, vol: volume, note: "Core money term — measured UK volume" },
    { kw: t === "scotland" ? "solar panels in scotland" : `${t} solar panels`, type: "Primary alt", page, vol: "—", note: "Word-order variant. Do not build a second URL." },
    { kw: `solar panel installation ${t}`, type: "Secondary", page: "/solar-panel-installation/", vol: "—", note: "Service page" },
    { kw: `solar panel installers ${t}`, type: "Secondary", page, vol: "—", note: "Installer-intent variant of the same page" },
    { kw: `solar battery storage ${t}`, type: "Secondary", page: "/solar-battery-storage/", vol: "—", note: "Battery service page" },
    { kw: `solar panels cost ${t}`, type: "Secondary", page: "/solar-panel-cost/", vol: "—", note: "Pricing page" },
    { kw: `commercial solar panels ${t}`, type: "Supporting", page: "/commercial-solar-panels/", vol: "—", note: "Business roofs" },
    { kw: `solar panel grants ${t}`, type: "Content", page: "/solar-panel-grants/", vol: "—", note: "Grant and Home Energy Scotland loan" },
    { kw: "solar panels near me", type: "Supporting", page: "/", vol: "—", note: "Homepage plus Google Business Profile" },
  ];
  (row.extras || []).forEach(ex => {
    rows.push({ kw: ex.kw, type: ex.type || "Secondary", page: ex.page || page, vol: ex.vol, note: ex.note || "Measured" });
  });
  return rows;
}

function valueLabel(v) {
  return ({ high: "High value", low: "Low value", moderate: "Moderate value", good: "Good value" })[v] || v;
}

function buildEmdSitePlan(row, value = "high") {
  const town = row.town;
  const T = prettyTown(town);
  const domain = domainFor(row);
  const services = servicePages(town);
  const lean = value === "low";
  const sitemap = [
    { section: "core", path: "/", title: `Home — Solar Panels ${T}`, type: "Money", primary: town.toLowerCase() === "scotland" ? "solar panels scotland" : `solar panels ${town}`, words: lean ? 900 : 1200, brief: `${valueLabel(value)} EMD homepage. Rank for solar panels ${town}. Quote form, MCS, recent local installs, FAQs.`, vol: row.volume, focusTown: town },
    { section: "areas", path: `/areas/${slugTown(town)}/`, title: `Solar Panels ${T}`, type: "Area", primary: town.toLowerCase() === "scotland" ? "solar panels scotland" : `solar panels ${town}`, words: lean ? 700 : 900, brief: `Area URL for ${T}. Keep a unique intro, or 301 it to the homepage if this site only covers one place.`, vol: row.volume, focusTown: town },
    ...services.map(s => ({ section: "services", path: `/${s.slug}/`, title: s.title, type: "Service", primary: s.primary, words: lean ? Math.round(s.words * 0.75) : s.words, brief: s.brief, vol: "—", focusTown: town })),
    { section: "core", path: "/about/", title: `About Us`, type: "Trust", primary: null, words: lean ? 350 : 500, brief: `MCS installer story, coverage, and proof for ${T}.`, vol: "—", focusTown: town },
    { section: "core", path: "/contact/", title: `Contact & Free Quote`, type: "Conversion", primary: `solar panel quote ${town}`, words: 400, brief: `Phone, form, and a map centred on ${T}.`, vol: "—", focusTown: town },
  ];
  if (!lean) {
    sitemap.push(
      { section: "content", path: "/blog/are-solar-panels-worth-it/", title: `Are Solar Panels Worth It in ${T}?`, type: "Content", primary: `are solar panels worth it ${town}`, words: 1200, brief: `Payback, Scottish weather, export, and the grant or loan. Links to the cost and grants pages.`, vol: "—", focusTown: town },
      { section: "content", path: "/blog/do-solar-panels-work-in-scotland/", title: `Do Solar Panels Work in Scotland?`, type: "Content", primary: "do solar panels work in scotland", words: 1000, brief: `Generation in Scottish light, orientation, and what a typical home actually produces.`, vol: "—", focusTown: town },
    );
  }
  const keywords = keywordsForTown(town, row.volume, "emd");
  keywords.forEach(k => { if (k.page === "/") { /* keep */ } });
  return {
    id: `emd:${value}:${slugTown(town)}`,
    kind: "emd",
    value,
    name: town,
    title: `${value === "high" ? "High" : "Low"} EMD · ${T}`,
    domain,
    volume: row.volume,
    region: row.region,
    cpc: row.cpc,
    competition: row.competition,
    townCount: 1,
    areas: [{ town, volume: row.volume, role: "EMD", path: `/areas/${slugTown(town)}/` }],
    sitemap,
    keywords,
    summary: value === "high"
      ? `Solo site for ${T} (${row.volume}/mo, at or above ${SITE_PLAN_FLOOR}). This place is not shared with a low-volume cluster.`
      : `Small solo site for ${T} (${row.volume}/mo). No other under-${SITE_PLAN_FLOOR} place sits within ${SITE_PLAN_RADIUS} miles, so it stays its own site.`,
  };
}

function buildBrandSitePlan(brand, value) {
  const name = brand.name;
  const T = prettyTown(name);
  const domain = brandDomain(name);
  const townsSorted = [...brand.towns].sort((a, b) => b.volume - a.volume || a.town.localeCompare(b.town));
  const services = servicePages(name);

  // Every town in the cluster gets a real area URL (grouped together in the sitemap)
  const areaEntries = townsSorted.map(t => ({
    section: "areas",
    path: `/areas/${slugTown(t.town)}/`,
    title: `Solar Panels ${prettyTown(t.town)}`,
    type: "Area",
    primary: `solar panels ${t.town}`,
    words: t.volume >= 40 ? 1000 : (t.volume > 0 ? 800 : 600),
    brief: t.town === name
      ? `Brand-hub area page for ${prettyTown(t.town)} (${t.volume}/mo). Can match homepage angle but keep a crawlable /areas/ URL for the cluster map.`
      : `Area page for ${prettyTown(t.town)} (${t.volume}/mo). Unique local intro, landmarks, distance from ${T}, links to services + quote.`,
    vol: t.volume,
    focusTown: t.town,
    role: t.town === name ? "Brand" : (t.volume >= 20 ? "Area" : "Area"),
  }));

  const sitemap = [
    { section: "core", path: "/", title: `Home — Solar Panels ${T}`, type: "Money", primary: `solar panels ${name}`, words: value === "good" ? 1200 : 1000, brief: `${valueLabel(value)} cluster homepage. List all ${townsSorted.length} places with links to /areas/. Quote form above the fold.`, vol: brand.towns.find(t => t.town === name)?.volume || 0, focusTown: name },
    { section: "areas", path: "/areas/", title: `Areas We Cover (${townsSorted.length} towns)`, type: "Hub", primary: null, words: 500 + townsSorted.length * 40, brief: `Cluster index listing every area URL below in volume order. This is the map of the brand.`, vol: brand.cluster_volume, focusTown: name },
    ...areaEntries,
    ...services.map(s => ({ section: "services", path: `/${s.slug}/`, title: s.title, type: "Service", primary: s.primary, words: s.words, brief: s.brief + ` Soft-mention the full town list; deep-link top area pages.`, vol: "—", focusTown: name })),
    { section: "core", path: "/about/", title: `About`, type: "Trust", primary: null, words: 500, brief: `MCS credentials and coverage for the ${townsSorted.length} places on this site.`, vol: "—", focusTown: name },
    { section: "core", path: "/contact/", title: `Contact & Free Quote`, type: "Conversion", primary: null, words: 400, brief: `One quote flow for all ${townsSorted.length} towns.`, vol: "—", focusTown: name },
  ];

  let keywords = [];
  townsSorted.forEach(t => {
    keywords = keywords.concat(keywordsForTown(t.town, t.volume, "area"));
  });
  // Homepage also targets brand-town primary
  keywords = [
    { kw: `solar panels ${name}`, type: "Primary", page: "/", vol: brand.towns.find(t => t.town === name)?.volume || 0, note: "Brand homepage money term" },
    ...keywords,
  ];
  const seen = new Set();
  keywords = keywords.filter(k => (seen.has(k.kw + k.page) ? false : (seen.add(k.kw + k.page), true)));

  return {
    id: `brand:${value}:${slugTown(name)}:${brand.id}`,
    kind: "brand",
    value,
    name,
    title: `${value === "good" ? "Good" : "Moderate"} cluster · ${T}`,
    domain,
    volume: brand.cluster_volume,
    region: brand.towns[0]?.region || "",
    cpc: null,
    competition: null,
    townCount: townsSorted.length,
    areas: townsSorted.map(t => ({
      town: t.town,
      volume: t.volume,
      role: t.town === name ? "Brand" : "Area",
      path: `/areas/${slugTown(t.town)}/`,
    })),
    sitemap,
    keywords,
    summary: value === "good"
      ? `Good-value cluster (${townsSorted.length} towns, ${brand.cluster_volume}/mo combined). Multi-area brand — every town has /areas/{town}/. Not shared with ≥${SITE_PLAN_FLOOR} EMDs.`
      : `Moderate-value cluster (${townsSorted.length} towns, ${brand.cluster_volume}/mo). Kept as its own separate site (under 5 towns). Every town has /areas/{town}/.`,
  };
}

function buildSiteCatalog() {
  const { emds, brands } = computeNationwidePlan(SITE_PLAN_RADIUS, SITE_PLAN_FLOOR, "");
  const highEmds = emds.map(r => buildEmdSitePlan(r, "high"));
  const lowEmds = [];
  const moderate = [];
  const good = [];

  brands.forEach(b => {
    const n = b.towns.length;
    if (n <= 1) {
      const row = b.towns[0];
      if (!row) return;
      lowEmds.push(buildEmdSitePlan(row, "low"));
    } else if (n < 5) {
      moderate.push(buildBrandSitePlan(b, "moderate"));
    } else {
      good.push(buildBrandSitePlan(b, "good"));
    }
  });

  siteCatalog = [...highEmds, ...lowEmds, ...moderate, ...good];
  return siteCatalog;
}

function findSiteForTown(townName) {
  const t = (townName || "").toLowerCase();
  // Prefer exact EMD ownership first (high then low)
  const emd = siteCatalog.find(s => s.kind === "emd" && s.name.toLowerCase() === t);
  if (emd) return { site: emd, area: t };
  const brand = siteCatalog.find(s => s.kind === "brand" && s.areas.some(a => a.town.toLowerCase() === t));
  if (brand) return { site: brand, area: t };
  return null;
}

function siteItemHtml(s) {
  const cls = s.kind === "emd" ? (s.value === "low" ? "low" : "emd") : s.value;
  const meta = s.kind === "emd"
    ? `${s.volume.toLocaleString()}/mo · ${escapeHtml(s.domain)}`
    : `${s.volume.toLocaleString()}/mo · ${s.townCount} towns · ${escapeHtml(s.domain)}`;
  return `
    <button type="button" class="site-item ${cls} ${activeSiteId === s.id ? "active" : ""}" data-site-id="${escapeHtml(s.id)}">
      <div class="t">${escapeHtml(prettyTown(s.name))}</div>
      <div class="m">${valueLabel(s.value)} · ${meta}</div>
    </button>`;
}

function renderSitesTab() {
  buildSiteCatalog();
  const q = (document.getElementById("sitesSearch").value || "").trim().toLowerCase();
  const filt = document.getElementById("sitesFilter").value;
  let list = siteCatalog.slice();
  if (filt === "high") list = list.filter(s => s.value === "high");
  if (filt === "low") list = list.filter(s => s.value === "low");
  if (filt === "moderate") list = list.filter(s => s.value === "moderate");
  if (filt === "good") list = list.filter(s => s.value === "good");
  if (q) {
    list = list.filter(s =>
      s.name.toLowerCase().includes(q) ||
      s.domain.toLowerCase().includes(q) ||
      s.areas.some(a => a.town.toLowerCase().includes(q)) ||
      (s.region || "").toLowerCase().includes(q)
    );
  }
  const high = list.filter(s => s.value === "high");
  const low = list.filter(s => s.value === "low");
  const moderate = list.filter(s => s.value === "moderate");
  const good = list.filter(s => s.value === "good");
  const idx = document.getElementById("sitesIndex");
  idx.innerHTML = `
    <div style="color:var(--muted);font-size:0.78rem;margin-bottom:8px">
      ${high.length} high · ${low.length} low · ${moderate.length} moderate · ${good.length} good · ${SITE_PLAN_RADIUS} mi / floor ${SITE_PLAN_FLOOR}
    </div>
    <h3>High EMDs (vol ≥ ${SITE_PLAN_FLOOR})</h3>
    ${high.map(siteItemHtml).join("") || `<div class="plan-empty">None</div>`}
    <h3>Low EMDs (1 town only)</h3>
    ${low.map(siteItemHtml).join("") || `<div class="plan-empty">None</div>`}
    <h3>Moderate clusters (2–4 towns)</h3>
    ${moderate.map(siteItemHtml).join("") || `<div class="plan-empty">None</div>`}
    <h3>Good clusters (5+ towns)</h3>
    ${good.map(siteItemHtml).join("") || `<div class="plan-empty">None</div>`}
  `;
  idx.querySelectorAll("[data-site-id]").forEach(btn => {
    btn.addEventListener("click", () => openSitePlan(btn.getAttribute("data-site-id"), null));
  });

  const all = siteCatalog;
  stats.innerHTML = `
    <div class="stat"><div class="n">${all.filter(s=>s.value==="high").length}</div><div class="l">High EMDs</div></div>
    <div class="stat"><div class="n">${all.filter(s=>s.value==="low").length}</div><div class="l">Low EMDs</div></div>
    <div class="stat"><div class="n">${all.filter(s=>s.value==="moderate").length}</div><div class="l">Moderate (2–4)</div></div>
    <div class="stat"><div class="n">${all.filter(s=>s.value==="good").length}</div><div class="l">Good (5+)</div></div>
  `;

  if (activeSiteId && siteCatalog.some(s => s.id === activeSiteId)) {
    openSitePlan(activeSiteId, activeAreaFocus);
  } else if (!activeSiteId && list[0]) {
    openSitePlan(list[0].id, null);
  } else if (!list.length) {
    document.getElementById("sitesDetail").innerHTML = `<div class="empty-detail">No sites match this filter.</div>`;
  }
}

function openSitePlan(siteId, areaFocus) {
  const site = siteCatalog.find(s => s.id === siteId);
  if (!site) return;
  activeSiteId = siteId;
  activeAreaFocus = areaFocus;
  document.querySelectorAll(".site-item").forEach(el => {
    el.classList.toggle("active", el.getAttribute("data-site-id") === siteId);
  });
  renderSiteDetail(site, areaFocus);
}

function renderSiteDetail(site, areaFocus) {
  const detail = document.getElementById("sitesDetail");
  const focus = (areaFocus || "").toLowerCase();
  const sitemap = focus
    ? site.sitemap.map(p => ({...p, hl: (p.focusTown || "").toLowerCase() === focus}))
    : site.sitemap;
  const keywords = focus
    ? site.keywords.filter(k => k.kw.includes(focus) || k.page.includes(slugTown(focus)))
    : site.keywords;
  const contentRows = focus
    ? sitemap.filter(p => p.hl || p.type === "Service" || p.path === "/" || p.type === "Hub" || p.section === "areas")
    : sitemap;

  const sectionOrder = ["core", "areas", "services", "content"];
  const sectionTitles = {
    core: "Core pages",
    areas: `Area pages (${site.areas.length}) — all towns in this site`,
    services: "Service pages",
    content: "Content / blog",
  };
  function renderSitemapGrouped(pages) {
    return sectionOrder.map(sec => {
      const items = pages.filter(p => (p.section || "core") === sec);
      if (!items.length) return "";
      const wrapOpen = sec === "areas" ? `<div class="area-url-block">` : "";
      const wrapClose = sec === "areas" ? `</div>` : "";
      return `${wrapOpen}<div class="sitemap-group ${sec}">${sectionTitles[sec]}</div>
        <ul class="sitemap-tree">
          ${items.map((p,i) => `
            <li class="${p.focusTown ? "clickable" : ""} ${p.hl ? "hl" : ""}" data-focus-town="${escapeHtml(p.focusTown || "")}">
              <div class="path">${escapeHtml(p.path)}</div>
              <div class="ptitle">${escapeHtml(p.title)}</div>
              <div class="pmeta">${escapeHtml(p.type)}${p.primary ? " · KW: " + escapeHtml(p.primary) : ""}${p.vol !== "—" && p.vol != null ? " · " + p.vol + "/mo" : ""} · ~${p.words || 0} words</div>
            </li>`).join("")}
        </ul>${wrapClose}`;
    }).join("");
  }

  detail.innerHTML = `
    <div class="site-hero">
      <div>
        <h2>${escapeHtml(site.title)}</h2>
        <div class="domain">${escapeHtml(site.domain)}</div>
        <div class="badge-row">
          <span class="badge ${site.value}">${escapeHtml(valueLabel(site.value))}</span>
          <span class="badge ${site.kind}">${site.kind === "emd" ? "Solo EMD" : "Cluster brand"}</span>
          <span class="badge">${Number(site.volume).toLocaleString()}/mo</span>
          <span class="badge">${site.townCount || site.areas.length} town${(site.townCount || site.areas.length) === 1 ? "" : "s"}</span>
          ${site.region ? `<span class="badge">${escapeHtml(site.region)}</span>` : ""}
          <span class="badge">${site.sitemap.filter(p => p.section === "areas").length} area URLs</span>
        </div>
      </div>
      <div style="text-align:right">
        <button type="button" class="secondary" id="siteCopyBtn" style="width:auto">Copy plan as Markdown</button>
      </div>
    </div>
    <p style="color:var(--muted);margin:0 0 8px">${escapeHtml(site.summary)}</p>
    <div class="area-chip-row">
      ${site.areas.map(a => `
        <button type="button" class="area-chip ${(focus && a.town.toLowerCase()===focus) ? "on" : ""}" data-area="${escapeHtml(a.town)}">
          ${escapeHtml(prettyTown(a.town))} · ${a.volume}/mo · <code style="font-size:0.7rem">${escapeHtml(a.path || "/areas/" + slugTown(a.town) + "/")}</code>
        </button>`).join("")}
    </div>
    <div class="site-tabs">
      <button type="button" data-stab="overview" class="${activeSiteTab==="overview"?"on":""}">Overview</button>
      <button type="button" data-stab="sitemap" class="${activeSiteTab==="sitemap"?"on":""}">Sitemap</button>
      <button type="button" data-stab="content" class="${activeSiteTab==="content"?"on":""}">Content plan</button>
      <button type="button" data-stab="keywords" class="${activeSiteTab==="keywords"?"on":""}">Keywords</button>
    </div>

    <div class="site-section ${activeSiteTab==="overview"?"on":""}" id="sec-overview">
      <table class="content-table">
        <tr><th>Field</th><th>Value</th></tr>
        <tr><td>Value tier</td><td><strong>${escapeHtml(valueLabel(site.value))}</strong> — ${site.value === "high" ? "vol ≥ 70, own site" : site.value === "low" ? "one small place, own site" : site.value === "moderate" ? "2–4 place cluster" : "5+ place cluster"}</td></tr>
        <tr><td>Site type</td><td>${site.kind === "emd" ? "Solo EMD domain" : "Multi-area cluster brand (low-vol towns only)"}</td></tr>
        <tr><td>Suggested domain</td><td><strong>${escapeHtml(site.domain)}</strong></td></tr>
        <tr><td>Primary market</td><td>${escapeHtml(prettyTown(site.name))} (${site.kind === "emd" ? site.volume : site.areas.find(a=>a.town===site.name)?.volume || "—"}/mo known)</td></tr>
        <tr><td>Area URLs</td><td>${site.areas.map(a => `<code>${escapeHtml(a.path || "/areas/"+slugTown(a.town)+"/")}</code> ${prettyTown(a.town)} (${a.volume}/mo)`).join("<br>")}</td></tr>
        <tr><td>Build order</td><td>1) Home + Contact · 2) All /areas/ pages · 3) Core services · 4) Pricing/About${site.value === "high" ? " · 5) Blog posts" : ""}</td></tr>
        <tr><td>Internal links</td><td>Home → every area URL. Each area → Home, /areas/, services, Contact.</td></tr>
        <tr><td>Off-page</td><td>GBP in ${escapeHtml(prettyTown(site.name))}, citations matching Contact NAP.</td></tr>
      </table>
    </div>

    <div class="site-section ${activeSiteTab==="sitemap"?"on":""}" id="sec-sitemap">
      ${renderSitemapGrouped(sitemap)}
    </div>

    <div class="site-section ${activeSiteTab==="content"?"on":""}" id="sec-content">
      <table class="content-table">
        <thead><tr><th>Section</th><th>URL</th><th>H1 / angle</th><th>Primary KW</th><th>Words</th><th>Brief</th></tr></thead>
        <tbody>
          ${contentRows.map(p => `
            <tr class="${p.hl ? "hl" : ""}">
              <td style="color:var(--muted);font-size:0.75rem;text-transform:uppercase">${escapeHtml(p.section || "core")}</td>
              <td><code>${escapeHtml(p.path)}</code></td>
              <td>${escapeHtml(p.title)}</td>
              <td>${p.primary ? escapeHtml(p.primary) : "—"}</td>
              <td>${p.words || "—"}</td>
              <td style="color:var(--muted)">${escapeHtml(p.brief || "")}</td>
            </tr>`).join("")}
        </tbody>
      </table>
    </div>

    <div class="site-section ${activeSiteTab==="keywords"?"on":""}" id="sec-keywords">
      <table class="kw-table">
        <thead><tr><th>Keyword</th><th>Type</th><th>Maps to</th><th>Vol</th><th>Notes</th></tr></thead>
        <tbody>
          ${keywords.map(k => `
            <tr>
              <td class="${k.type.startsWith("Primary") ? "kw-pri" : k.type==="Secondary" ? "kw-sec" : "kw-sup"}">${escapeHtml(k.kw)}</td>
              <td>${escapeHtml(k.type)}</td>
              <td><code>${escapeHtml(k.page)}</code></td>
              <td>${k.vol === "—" || k.vol == null ? "—" : Number(k.vol).toLocaleString()}</td>
              <td style="color:var(--muted)">${escapeHtml(k.note)}</td>
            </tr>`).join("")}
        </tbody>
      </table>
      <p class="note" style="margin-top:10px">Measured volumes are marked in the Vol column. A dash means the term is a page target, not a figure from this pull. Suggested domains have not been checked for availability.</p>
    </div>
  `;

  detail.querySelectorAll("[data-stab]").forEach(btn => {
    btn.addEventListener("click", () => {
      activeSiteTab = btn.getAttribute("data-stab");
      renderSiteDetail(site, activeAreaFocus);
    });
  });
  detail.querySelectorAll("[data-area]").forEach(btn => {
    btn.addEventListener("click", () => {
      const town = btn.getAttribute("data-area");
      const hit = findSiteForTown(town);
      activeSiteTab = "content";
      if (hit) openSitePlan(hit.site.id, town);
      else openSitePlan(site.id, town);
    });
  });
  detail.querySelectorAll(".sitemap-tree li.clickable").forEach(li => {
    li.addEventListener("click", () => {
      const t = li.getAttribute("data-focus-town");
      if (!t) return;
      activeAreaFocus = t;
      activeSiteTab = "content";
      renderSiteDetail(site, t);
    });
  });
  const copyBtn = document.getElementById("siteCopyBtn");
  if (copyBtn) copyBtn.addEventListener("click", () => copySitePlanMarkdown(site));
}

function copySitePlanMarkdown(site) {
  const lines = [];
  lines.push(`# ${site.title}`);
  lines.push(`Domain: ${site.domain}`);
  lines.push(`Volume: ${site.volume}/mo · Type: ${site.kind} · Value: ${site.value}`);
  lines.push("");
  lines.push(site.summary);
  lines.push("");
  lines.push("## Area URLs (grouped)");
  site.areas.forEach(a => lines.push(`- ${a.path || "/areas/"+slugTown(a.town)+"/"} — ${a.town} — ${a.volume}/mo — ${a.role}`));
  lines.push("");
  lines.push("## Sitemap & content plan");
  let lastSec = null;
  site.sitemap.forEach(p => {
    if (p.section && p.section !== lastSec) {
      lines.push(`### Section: ${p.section}`);
      lastSec = p.section;
    }
    lines.push(`#### ${p.path}`);
    lines.push(`- Title: ${p.title}`);
    lines.push(`- Type: ${p.type}`);
    if (p.primary) lines.push(`- Primary KW: ${p.primary}`);
    lines.push(`- Words: ${p.words || 0}`);
    lines.push(`- Brief: ${p.brief}`);
    lines.push("");
  });
  lines.push("## Keywords");
  site.keywords.forEach(k => lines.push(`- [${k.type}] ${k.kw} → ${k.page} (${k.vol}/mo) — ${k.note}`));
  const text = lines.join("\n");
  navigator.clipboard.writeText(text).then(() => {
    alert("Site plan copied as Markdown.");
  }).catch(() => {
    const w = window.open("", "_blank");
    w.document.write(`<pre>${escapeHtml(text)}</pre>`);
  });
}

function exportOpenSitePlan() {
  const site = siteCatalog.find(s => s.id === activeSiteId);
  if (!site) { alert("Open a site plan first."); return; }
  copySitePlanMarkdown(site);
}

const MAP_COLORS = { high: "#34d399", low: "#94a3b8", moderate: "#f0b429", good: "#60a5fa", pick: "#f472b6" };

function rebuildMapTownIndex() {
  buildSiteCatalog();
  mapTownIndex = new Map();
  siteCatalog.forEach(site => {
    site.areas.forEach(a => {
      const row = DATA.find(d => d.town.toLowerCase() === a.town.toLowerCase());
      if (!row || row.lat == null) return;
      mapTownIndex.set(a.town.toLowerCase(), {
        town: a.town,
        volume: a.volume,
        role: a.role,
        path: a.path,
        lat: row.lat,
        lng: row.lng,
        region: row.region,
        site,
        value: site.value,
      });
    });
  });
  // Also index high-vol / any DATA towns not in catalog areas (shouldn't happen often)
  DATA.forEach(d => {
    if (d.lat == null) return;
    const key = d.town.toLowerCase();
    if (mapTownIndex.has(key)) return;
    const hit = findSiteForTown(d.town);
    mapTownIndex.set(key, {
      town: d.town, volume: d.volume, role: hit ? (hit.site.kind === "emd" ? "EMD" : "Area") : "—",
      path: "", lat: d.lat, lng: d.lng, region: d.region,
      site: hit ? hit.site : null, value: hit ? hit.site.value : "low",
    });
  });
}

function initCoverageMap() {
  if (coverageMap) {
    setTimeout(() => coverageMap.invalidateSize(), 50);
    return;
  }
  coverageMap = L.map("coverageMap", { zoomControl: true }).setView([56.8, -4.2], 6);
  // Esri Canvas Dark Gray — no API key; OSM public tiles block file:// / non-policy clients
  L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
    attribution: "Tiles &copy; Esri",
    maxZoom: 16,
  }).addTo(coverageMap);
  L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}", {
    attribution: "",
    maxZoom: 16,
    opacity: 0.9,
  }).addTo(coverageMap);
  mapMarkersLayer = L.layerGroup().addTo(coverageMap);
  mapCirclesLayer = L.layerGroup().addTo(coverageMap);
  setTimeout(() => coverageMap.invalidateSize(), 80);
}

function circleMarkerFor(value, isHub) {
  const color = MAP_COLORS[value] || MAP_COLORS.low;
  return {
    radius: isHub ? 8 : 6,
    color: "#0b1220",
    weight: 1,
    fillColor: color,
    fillOpacity: isHub ? 0.95 : 0.75,
  };
}

function refreshMapLayers() {
  if (!coverageMap) return;
  rebuildMapTownIndex();
  mapMarkersLayer.clearLayers();
  mapCirclesLayer.clearLayers();

  const show = {
    high: document.getElementById("mapShowHigh").checked,
    low: document.getElementById("mapShowLow").checked,
    moderate: document.getElementById("mapShowModerate").checked,
    good: document.getElementById("mapShowGood").checked,
  };
  const showRings = document.getElementById("mapShowCircles").checked;

  // One marker per town in index; hubs get rings
  const drawnHubs = new Set();
  mapTownIndex.forEach(info => {
    if (!show[info.value]) return;
    const isHub = info.site && info.site.name.toLowerCase() === info.town.toLowerCase();
    const m = L.circleMarker([info.lat, info.lng], circleMarkerFor(info.value, isHub));
    const siteLabel = info.site
      ? `${info.site.title} · ${info.site.domain}`
      : "Unassigned";
    m.bindPopup(`
      <strong>${escapeHtml(prettyTown(info.town))}</strong><br>
      ${info.volume}/mo · ${escapeHtml(valueLabel(info.value))}<br>
      Role: ${escapeHtml(info.role)}<br>
      Site: ${escapeHtml(siteLabel)}
      ${info.path ? `<br><code>${escapeHtml(info.path)}</code>` : ""}
      <br><button type="button" class="map-pop-site" data-site-id="${info.site ? escapeHtml(info.site.id) : ""}" data-town="${escapeHtml(info.town)}" style="margin-top:6px">Open site plan</button>
    `);
    m.on("popupopen", e => {
      const btn = e.popup.getElement().querySelector(".map-pop-site");
      if (!btn) return;
      btn.addEventListener("click", () => {
        const sid = btn.getAttribute("data-site-id");
        const town = btn.getAttribute("data-town");
        if (!sid) return;
        activeSiteId = sid;
        activeAreaFocus = town;
        setMode("sites");
      });
    });
    m.on("click", () => {
      document.getElementById("mapTown").value = info.town;
      updateMapSelection(info.town, false);
    });
    mapMarkersLayer.addLayer(m);

    if (showRings && isHub && info.site && !drawnHubs.has(info.site.id)) {
      drawnHubs.add(info.site.id);
      const ring = L.circle([info.lat, info.lng], {
        radius: SITE_PLAN_RADIUS * 1609.34,
        color: MAP_COLORS[info.value],
        weight: 1,
        fillColor: MAP_COLORS[info.value],
        fillOpacity: 0.06,
      });
      mapCirclesLayer.addLayer(ring);
    }
  });
}

function populateMapTownSelect() {
  const sel = document.getElementById("mapTown");
  const current = sel.value;
  const towns = DATA.filter(d => d.lat != null).slice().sort((a,b) => a.town.localeCompare(b.town));
  sel.innerHTML = `<option value="">— Pick a town —</option>` + towns.map(d => {
    const info = mapTownIndex.get(d.town.toLowerCase());
    const tier = info ? valueLabel(info.value) : "";
    return `<option value="${escapeHtml(d.town)}">${escapeHtml(d.town)} (${d.volume}/mo${tier ? " · " + tier : ""})</option>`;
  }).join("");
  if (current && [...sel.options].some(o => o.value === current)) sel.value = current;
}

function updateMapSelection(townName, pan = true) {
  if (!coverageMap) return;
  if (mapPickCircle) { coverageMap.removeLayer(mapPickCircle); mapPickCircle = null; }
  if (mapPickMarker) { coverageMap.removeLayer(mapPickMarker); mapPickMarker = null; }

  if (!townName) {
    document.getElementById("mapCoverSummary").textContent = "Select a town to inspect coverage.";
    document.getElementById("mapCoverList").innerHTML = "";
    return;
  }
  const centre = DATA.find(d => d.town === townName);
  if (!centre || centre.lat == null) return;
  const miles = Number(document.getElementById("mapCoverMiles").value || 15);
  const info = mapTownIndex.get(townName.toLowerCase());

  mapPickCircle = L.circle([centre.lat, centre.lng], {
    radius: miles * 1609.34,
    color: MAP_COLORS.pick,
    weight: 2,
    fillColor: MAP_COLORS.pick,
    fillOpacity: 0.08,
  }).addTo(coverageMap);
  mapPickMarker = L.circleMarker([centre.lat, centre.lng], {
    radius: 10, color: "#fff", weight: 2, fillColor: MAP_COLORS.pick, fillOpacity: 1,
  }).addTo(coverageMap).bindPopup(`Selected: <strong>${escapeHtml(prettyTown(townName))}</strong>`);

  if (pan) {
    coverageMap.fitBounds(mapPickCircle.getBounds(), { padding: [40, 40], maxZoom: 11 });
  }

  const nearby = [];
  mapTownIndex.forEach(t => {
    const dist = haversineMiles(centre.lat, centre.lng, t.lat, t.lng);
    if (dist <= miles) nearby.push({ ...t, miles: Math.round(dist * 10) / 10 });
  });
  nearby.sort((a, b) => a.miles - b.miles || b.volume - a.volume);

  const byValue = { high: 0, low: 0, moderate: 0, good: 0 };
  const sites = new Map();
  nearby.forEach(n => {
    byValue[n.value] = (byValue[n.value] || 0) + 1;
    if (n.site) sites.set(n.site.id, n.site);
  });

  document.getElementById("mapCoverSummary").innerHTML =
    `<strong>${escapeHtml(prettyTown(townName))}</strong> · ${centre.volume}/mo` +
    `${info ? ` · ${escapeHtml(valueLabel(info.value))}` : ""}` +
    `<br>${nearby.length} towns within ${miles} mi · ${sites.size} site(s)` +
    `<br>High ${byValue.high || 0} · Low ${byValue.low || 0} · Mod ${byValue.moderate || 0} · Good ${byValue.good || 0}`;

  document.getElementById("mapCoverList").innerHTML = nearby.map(n => `
    <li>
      <div class="t"><i class="dot ${n.value}"></i> ${escapeHtml(prettyTown(n.town))} — ${n.miles} mi</div>
      <div class="m">${n.volume}/mo · ${escapeHtml(valueLabel(n.value))} · ${escapeHtml(n.role)}
        ${n.site ? ` · ${escapeHtml(n.site.title)}` : ""}
        ${n.path ? ` · <code>${escapeHtml(n.path)}</code>` : ""}
      </div>
    </li>`).join("") || `<li class="note">No towns in range.</li>`;
}

function renderMapTab() {
  rebuildMapTownIndex();
  populateMapTownSelect();
  initCoverageMap();
  refreshMapLayers();
  const selected = document.getElementById("mapTown").value;
  if (selected) updateMapSelection(selected, true);
  else {
    coverageMap.setView([56.8, -4.2], 6);
    document.getElementById("mapCoverSummary").textContent = "Select a town to inspect coverage.";
    document.getElementById("mapCoverList").innerHTML = "";
  }
  stats.innerHTML = `
    <div class="stat"><div class="n">${[...mapTownIndex.values()].filter(t=>t.value==="high").length}</div><div class="l">High on map</div></div>
    <div class="stat"><div class="n">${[...mapTownIndex.values()].filter(t=>t.value==="low").length}</div><div class="l">Low on map</div></div>
    <div class="stat"><div class="n">${[...mapTownIndex.values()].filter(t=>t.value==="moderate").length}</div><div class="l">Moderate towns</div></div>
    <div class="stat"><div class="n">${[...mapTownIndex.values()].filter(t=>t.value==="good").length}</div><div class="l">Good-cluster towns</div></div>
  `;
}

function applyFilter() {
  if (mode === "radius" && radiusActive) {
    // keep radius set; only re-render/sort
    sortRows();
    render();
    return;
  }
  const query = q.value.trim().toLowerCase();
  const t = tier.value;
  const reg = region.value;
  const mv = Number(minVol.value || 0);
  const mc = Number(maxComp.value || 100);
  filtered = DATA.filter(d => {
    if (t && d.tier !== t) return false;
    if (reg && d.region !== reg) return false;
    if (d.volume < mv) return false;
    if (d.competition > mc) return false;
    if (query && !(d.town.toLowerCase().includes(query) || d.keyword.toLowerCase().includes(query) || d.region.toLowerCase().includes(query))) return false;
    return true;
  }).map(d => ({...d, role: d.role || "—", miles: d.miles ?? ""}));
  sortRows();
  render();
  renderRecEmpty();
}

function applyRadius() {
  const focusTown = hub.value; // hub for catchment
  const linkMiles = Number(radius.value);
  const floor = Number(emdFloor.value || 70);
  const reg = radiusRegion.value;

  let pool = DATA.filter(d => d.lat != null);
  if (reg) pool = pool.filter(d => d.region === reg);

  let centre = null;
  if (focusTown) {
    centre = DATA.find(d => d.town === focusTown);
    if (!centre || centre.lat == null) {
      alert("That hub town has no coordinates.");
      return;
    }
    // Catchment disk: every town in the keyword list within X miles of the hub
    pool = pool
      .map(d => {
        const dist = haversineMiles(centre.lat, centre.lng, d.lat, d.lng);
        return {...d, focus_miles: Math.round(dist * 10) / 10};
      })
      .filter(d => d.focus_miles <= linkMiles);
  }

  // Split: high-vol = solo EMDs; low-vol = brand cluster(s) that never share with EMDs
  const high = pool.filter(d => d.volume >= floor);
  const low = pool.filter(d => d.volume < floor);

  let assigned = high
    .sort((a, b) => b.volume - a.volume)
    .map(r => {
      const copy = assignSoloEmd(r, floor);
      // In catchment mode, Miles = distance from hub so you can see who sits in the circle
      if (centre && r.lat != null) {
        copy.miles = Math.round(haversineMiles(centre.lat, centre.lng, r.lat, r.lng) * 10) / 10;
      }
      return copy;
    });

  let lowClusters;
  if (focusTown && centre) {
    // One brand for the whole low-vol set inside the hub circle
    lowClusters = low.length ? [low] : [];
  } else {
    // Nationwide: low-vol towns cluster with each other by neighbour distance
    lowClusters = buildAutoClusters(low, linkMiles)
      .map(c => c.filter(Boolean))
      .filter(c => c.length)
      .sort((a, b) => {
        const va = a.reduce((s, t) => s + t.volume, 0);
        const vb = b.reduce((s, t) => s + t.volume, 0);
        return vb - va;
      });
  }

  lowClusters.forEach((clusterTowns, idx) => {
    assigned = assigned.concat(
      assignLowVolCluster(
        clusterTowns,
        idx + 1,
        floor,
        focusTown || null,
        centre || null
      )
    );
  });

  filtered = assigned;
  radiusActive = true;
  // Catchment: sort by miles from hub so area names are obvious
  sortKey = focusTown ? "miles" : "cluster_name";
  sortDir = "asc";
  sortRows();
  render();
  renderRec(assigned, focusTown, linkMiles, floor, high.length, lowClusters.length);
}

function renderRecEmpty() {
  if (mode !== "radius") return;
  document.getElementById("recEmd").innerHTML = "<li class='note'>Click Build clusters</li>";
  document.getElementById("recBrand").innerHTML = "<li class='note'>—</li>";
  document.getElementById("recArea").innerHTML = "<li class='note'>—</li>";
}

function renderRec(rows, focusTown, linkMiles, floor, emdCount, brandClusterCount) {
  const emd = rows.filter(r => r.role === "EMD").sort((a,b) => b.volume - a.volume);
  const brands = rows.filter(r => r.role === "Brand").sort((a,b) => (b.cluster_volume||0) - (a.cluster_volume||0));
  const area = rows.filter(r => r.role === "Area" || r.role === "Mention").sort((a,b) => b.volume - a.volume);
  const fmt = (r, showReason) => `<li><strong>${escapeHtml(r.town)}</strong> — ${r.volume}/mo` +
    `${r.role === "Brand" && r.cluster_volume ? ` · cluster ${r.cluster_volume}/mo` : ""}` +
    `${r.cluster_name ? ` · ${escapeHtml(r.cluster_name)}` : ""}` +
    `${showReason ? ` <span style="color:var(--muted)">(${escapeHtml(r.role_reason)})</span>` : ""}` +
    `${r.brand_hub && r.role !== "EMD" && r.role !== "Brand" ? ` <span style="color:var(--muted)">→ ${escapeHtml(r.brand_hub)}</span>` : ""}</li>`;
  document.getElementById("recEmd").innerHTML = emd.length ? emd.map(r => fmt(r, true)).join("") : "<li class='note'>None</li>";
  document.getElementById("recBrand").innerHTML = brands.length ? brands.map(r => fmt(r, true)).join("") : "<li class='note'>None</li>";
  document.getElementById("recArea").innerHTML = area.length ? area.map(r => fmt(r, true)).join("") : "<li class='note'>None</li>";
  const focusTxt = focusTown
    ? `Catchment of ${focusTown}: every town in your list within ${linkMiles} mi (see Miles column).`
    : `No hub — nationwide low-vol auto-clusters by ${linkMiles} mi neighbour links.`;
  document.getElementById("radiusNote").textContent =
    `${focusTxt} Floor ${floor}: ${emdCount} solo EMD(s) in this view. ${brandClusterCount} low-vol brand(s) covering only towns under ${floor}. ${rows.length} towns listed.`;
}

function sortRows() {
  filtered.sort((a, b) => {
    let av = a[sortKey], bv = b[sortKey];
    if (sortKey === "miles") {
      av = av === "" || av == null ? 9999 : av;
      bv = bv === "" || bv == null ? 9999 : bv;
    }
    let cmp;
    if (typeof av === "string" || typeof bv === "string") {
      cmp = String(av ?? "").localeCompare(String(bv ?? ""));
    } else {
      cmp = (av ?? 0) - (bv ?? 0);
    }
    if (cmp === 0 && mode === "radius") {
      // Keep clusters readable: Brand/EMD first, then volume
      if (a.cluster_name === b.cluster_name) {
        const rank = r => (r.role === "EMD" || r.role === "Brand") ? 0 : (r.role === "Area" ? 1 : 2);
        const rd = rank(a) - rank(b);
        if (rd !== 0) return rd;
        return b.volume - a.volume;
      }
    }
    return sortDir === "asc" ? cmp : -cmp;
  });
}

function renderStats(rows) {
  const totalVol = rows.reduce((s, r) => s + r.volume, 0);
  const avgCpc = rows.length ? rows.reduce((s, r) => s + r.cpc, 0) / rows.length : 0;
  const emd = rows.filter(r => r.role === "EMD").length;
  const brands = rows.filter(r => r.role === "Brand").length;
  const area = rows.filter(r => r.role === "Area").length;
  const sCount = rows.filter(r => r.tier === "S" || r.tier === "A").length;
  stats.innerHTML = `
    <div class="stat"><div class="n">${rows.length}</div><div class="l">Towns shown</div></div>
    <div class="stat"><div class="n">${totalVol.toLocaleString()}</div><div class="l">Combined volume</div></div>
    <div class="stat"><div class="n">${money(avgCpc)}</div><div class="l">Avg CPC</div></div>
    <div class="stat"><div class="n">${mode === "radius" ? emd : sCount}</div><div class="l">${mode === "radius" ? "Solo EMDs" : "S + A priorities"}</div></div>
    <div class="stat"><div class="n">${mode === "radius" ? brands : rows.filter(r => r.tier === "Skip").length}</div><div class="l">${mode === "radius" ? "Cluster brands" : "Skip / dead"}</div></div>
    ${mode === "radius" ? `<div class="stat"><div class="n">${area}</div><div class="l">Area pages</div></div>` : ""}
  `;
}

function bar(val, max, cls) {
  const pct = Math.min(100, Math.round((val / max) * 100));
  return `<span class="bar ${cls || ""}"><i style="width:${pct}%"></i></span>`;
}

function render() {
  renderStats(filtered);
  const mv = maxVol();
  tbody.innerHTML = filtered.map(d => {
    const compCls = d.competition <= 40 ? "comp low" : d.competition >= 70 ? "comp high" : "comp";
    const role = d.role || "—";
    const miles = (d.miles === 0 || d.miles) ? d.miles : "—";
    const isBrand = mode === "radius" && (d.role === "Brand" || d.role === "EMD");
    return `<tr class="${isBrand ? "hub" : ""}">
      <td>${d.cluster_name ? escapeHtml(d.cluster_name) : "—"}</td>
      <td>${role !== "—" ? `<span class="role role-${role}">${role}</span>` : "—"}</td>
      <td>${d.brand_hub ? escapeHtml(d.brand_hub) : "—"}</td>
      <td>${miles}</td>
      <td><span class="tier tier-${d.tier}">${d.tier}</span></td>
      <td><strong>${escapeHtml(d.town)}</strong></td>
      <td>${bar(d.volume, mv)}${d.volume.toLocaleString()}</td>
      <td>${money(d.cpc)}</td>
      <td>${bar(d.competition, 100, compCls)}${d.competition}%</td>
      <td>${d.opportunity_score}</td>
      <td>${escapeHtml(d.region)}</td>
      <td>${d.emd_best_available ? `<span>${escapeHtml(d.emd_best_available)}</span>` : "—"}</td>
      <td style="color:var(--muted)">${escapeHtml(d.emd_primary || "")}</td>
    </tr>`;
  }).join("");
  meta.textContent = `Showing ${filtered.length} of ${DATA.length} towns · sorted by ${sortKey} (${sortDir})` + (mode === "radius" && radiusActive ? ` · cluster mode` : "");
  document.querySelectorAll("th").forEach(th => {
    const arrow = th.querySelector(".arrow");
    if (!arrow) return;
    arrow.textContent = th.dataset.key === sortKey ? (sortDir === "asc" ? "▲" : "▼") : "";
  });
}

document.querySelectorAll("th[data-key]").forEach(th => {
  th.addEventListener("click", () => {
    const key = th.dataset.key;
    if (sortKey === key) sortDir = sortDir === "asc" ? "desc" : "asc";
    else {
      sortKey = key;
      sortDir = ["town","region","keyword","tier","role","cluster_name","brand_hub","emd_best_available","emd_primary"].includes(key) ? "asc" : (key === "miles" ? "asc" : "desc");
    }
    sortRows();
    render();
  });
});

[q, tier, region, minVol, maxComp].forEach(el => el.addEventListener("input", applyFilter));
document.getElementById("applyRadius").addEventListener("click", applyRadius);
document.getElementById("modeAll").addEventListener("click", () => setMode("all"));
document.getElementById("modeRadius").addEventListener("click", () => setMode("radius"));
document.getElementById("modePlan").addEventListener("click", () => setMode("plan"));
document.getElementById("modeSites").addEventListener("click", () => setMode("sites"));
document.getElementById("modeMap").addEventListener("click", () => setMode("map"));
hub.addEventListener("change", () => { if (mode === "radius") applyRadius(); });
radius.addEventListener("change", () => { if (mode === "radius") applyRadius(); });
emdFloor.addEventListener("change", () => { if (mode === "radius") applyRadius(); });
radiusRegion.addEventListener("change", () => { if (mode === "radius") applyRadius(); });

["planRadius", "planFloor", "planRegion", "planMultiOnly"].forEach(id => {
  document.getElementById(id).addEventListener("change", () => { if (mode === "plan") renderPlanBoard(); });
});
document.getElementById("planSearch").addEventListener("input", () => { if (mode === "plan") renderPlanBoard(); });
document.getElementById("planRefresh").addEventListener("click", renderPlanBoard);

document.getElementById("sitesSearch").addEventListener("input", () => { if (mode === "sites") renderSitesTab(); });
document.getElementById("sitesFilter").addEventListener("change", () => { if (mode === "sites") renderSitesTab(); });
document.getElementById("sitesExport").addEventListener("click", exportOpenSitePlan);

document.getElementById("mapTown").addEventListener("change", () => {
  if (mode === "map") updateMapSelection(document.getElementById("mapTown").value, true);
});
document.getElementById("mapCoverMiles").addEventListener("change", () => {
  if (mode === "map") updateMapSelection(document.getElementById("mapTown").value, true);
});
["mapShowHigh","mapShowLow","mapShowModerate","mapShowGood","mapShowCircles"].forEach(id => {
  document.getElementById(id).addEventListener("change", () => {
    if (mode !== "map") return;
    refreshMapLayers();
    const t = document.getElementById("mapTown").value;
    if (t) updateMapSelection(t, false);
  });
});
document.getElementById("mapFitUk").addEventListener("click", () => {
  if (!coverageMap) return;
  coverageMap.setView([56.8, -4.2], 6);
});
document.getElementById("mapOpenSite").addEventListener("click", () => {
  const t = document.getElementById("mapTown").value;
  if (!t) { alert("Select a location first."); return; }
  const hit = findSiteForTown(t);
  if (!hit) { alert("No site plan for that town."); return; }
  activeSiteId = hit.site.id;
  activeAreaFocus = t;
  setMode("sites");
});

function exportCsv() {
  const cols = ["cluster_name","cluster_id","cluster_volume","town","keyword","volume","cpc","competition","opportunity_score","tier","volume_bucket","region","miles","role","role_reason","brand_hub","emd_primary","emd_best_available","emd_available_count","lat","lng"];
  const lines = [cols.join(",")].concat(filtered.map(r => cols.map(c => {
    const v = r[c];
    const s = String(v ?? "");
    return /[",\n]/.test(s) ? `"${s.replace(/"/g,'""')}"` : s;
  }).join(",")));
  const blob = new Blob([lines.join("\n")], {type:"text/csv;charset=utf-8"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = mode === "radius" ? "scotland-solar-radius-cluster.csv" : "scotland-solar-filtered.csv";
  a.click();
  URL.revokeObjectURL(a.href);
}

document.getElementById("chips").addEventListener("click", e => {
  const btn = e.target.closest("[data-preset]");
  if (!btn) return;
  document.querySelectorAll(".chip").forEach(c => c.classList.remove("on"));
  const p = btn.dataset.preset;
  if (p !== "reset") btn.classList.add("on");
  q.value = ""; tier.value = ""; region.value = ""; minVol.value = 0; maxComp.value = 100;
  if (p === "clyde") region.value = "Glasgow & Clyde";
  if (p === "lothian") region.value = "Edinburgh & Lothians";
  if (p === "small") tier.value = "D";
  applyFilter();
  if (p === "priority") {
    filtered = DATA.filter(d => d.tier === "S" || d.tier === "A").map(d => ({...d, role:"—", miles:""}));
    sortRows(); render();
  }
  if (p === "value") {
    filtered = DATA.filter(d => d.cpc >= 10).map(d => ({...d, role:"—", miles:""}));
    sortRows(); render();
  }
  if (p === "floor") {
    filtered = DATA.filter(d => d.volume >= 70).map(d => ({...d, role:"—", miles:""}));
    sortKey = "volume"; sortDir = "desc";
    sortRows(); render();
  }
});

document.getElementById("exportBtn").addEventListener("click", exportCsv);
document.getElementById("exportRadiusBtn").addEventListener("click", exportCsv);

applyFilter();

</script>
</body>
</html>
"""

html = html.replace("__DATA__", payload)
# fix duplicate class attribute on radius panel in template
html = html.replace(
    '<div class="panel" id="radiusPanel" class="hidden">',
    '<div class="panel hidden" id="radiusPanel">',
)

out_paths = [
    Path(r"D:\Tools\Solar\Scotland Solar Project Plan\scotland-solar-keyword-explorer.html"),
    Path(r"D:\Tools\Solar\Scotland Solar Project Plan\public\index.html"),
]
for out in out_paths:
    out.write_text(html, encoding="utf-8")
    print("wrote", out)
