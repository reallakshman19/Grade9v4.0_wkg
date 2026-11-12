#!/usr/bin/env python3
"""
build_79_browser.py — Generates the Grade9 v4 Private 79-Question Inventory & Candidate Audit Browser.
Merges source-index-private.json, registry.json, and lot rosters into a standalone offline browser.
"""

import json
import os
import re

LOTS_DIR = r"D:\CodeD\grade9v4\workspace\output\G9V4_LOTS"
LOT00_JSON = os.path.join(LOTS_DIR, "LOT-00", "source-index-private.json")
REGISTRY_JSON = r"D:\CodeD\grade9v4\workspace\legacy\g9v3.5\chatgpt\output\WPE_Core2_Candidate_2026-10-30\data\registry.json"
OUTPUT_HTML = os.path.join(LOTS_DIR, "G9V4_PRIVATE_79_QUESTION_BROWSER.html")

def load_data():
    with open(LOT00_JSON, "r", encoding="utf-8") as f:
        lot00 = json.load(f)

    with open(REGISTRY_JSON, "r", encoding="utf-8") as f:
        registry = json.load(f)

    reg_map = {r["id"]: r for r in registry.get("records", []) if "id" in r}

    # Load lot mappings from LOT-02 to LOT-14
    lot_map = {}
    for i in range(2, 15):
        lot_id = f"LOT-{i:02d}"
        roster_path = os.path.join(LOTS_DIR, lot_id, "ROSTER_PRIVATE.json")
        if os.path.exists(roster_path):
            try:
                with open(roster_path, "r", encoding="utf-8") as rf:
                    roster = json.load(rf)
                    for item in roster.get("roster", []):
                        sid = item.get("source_id")
                        if sid:
                            lot_map[sid] = item.get("lot", lot_id)
            except Exception as e:
                print(f"Error reading {roster_path}: {e}")

    records = []
    for rec in lot00.get("records", []):
        rid = rec["id"]
        reg_item = reg_map.get(rid, {})

        # Extract stem and clean options
        stem = reg_item.get("stem", "")
        options = reg_item.get("options", [])
        
        # Figure note
        fig_note = reg_item.get("prior", {}).get("figure_note", "") if isinstance(reg_item.get("prior"), dict) else ""
        if not fig_note and reg_item.get("question_figure_refs"):
            fig_note = f"Figure referenced: {len(reg_item['question_figure_refs'])} asset(s) unverified"

        # Solution / answer note
        ans_obj = reg_item.get("answer", {}) if isinstance(reg_item.get("answer"), dict) else {}
        solution = ans_obj.get("solution", "")

        lot_assigned = lot_map.get(rid, "UNASSIGNED" if rec["scope"] != "IN_SCOPE" else "LOT-14 (PENDING)")

        record_entry = {
            "index": rec.get("index"),
            "ref": rec.get("anonymous_ref"),
            "id": rid,
            "task_id": rec.get("exact_task_identity"),
            "primary": rec.get("is_primary_identity"),
            "duplicate_status": rec.get("duplicate_status"),
            "alias_of": rec.get("alias_of"),
            "paper": rec.get("paper"),
            "origin": rec.get("origin"),
            "scope": rec.get("scope"),
            "scope_note": rec.get("scope_note"),
            "lot": lot_assigned,
            "stem": stem,
            "options": options,
            "figure_status": rec.get("figure_status"),
            "figure_note": fig_note,
            "key_status": rec.get("official_key_status"),
            "key_note": rec.get("official_key_note"),
            "solution": solution,
            "holds": rec.get("holds", []),
            "stem_sha256": rec.get("stem_sha256"),
        }
        records.append(record_entry)

    return records

def generate_html(records):
    records_json = json.dumps(records, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Grade9 v4.0 — Private 79-Question Inventory & Candidate Audit Browser</title>
<style>
:root {{
    --bg: #0b1320;
    --surface: #152238;
    --surface-hover: #1c2d4a;
    --border: #283a58;
    --border-subtle: #1e2e48;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --accent-hover: #0284c7;
    --warn-bg: #291e0a;
    --warn-border: #855307;
    --warn-text: #fde047;
    --danger-bg: #301014;
    --danger-border: #7f1d1d;
    --danger-text: #fca5a5;
    --success-bg: #0b2e1e;
    --success-border: #166534;
    --success-text: #86efac;
    --tag-bg: #1e293b;
    --tag-text: #cbd5e1;
    --font-math: "Cambria Math", "STIX Two Math", "Noto Sans Math", "Latin Modern Math", serif;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.5;
    padding-bottom: 60px;
}}

header {{
    background: #080d15;
    border-bottom: 2px solid var(--accent);
    padding: 24px 20px;
    position: sticky;
    top: 0;
    z-index: 100;
}}

.header-container {{
    max-width: 1380px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}}

.title-group h1 {{
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.badge-private {{
    background: #991b1b;
    color: #fee2e2;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.title-group p {{
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 4px;
}}

/* Disclosure Banner */
.disclaimer-banner {{
    max-width: 1380px;
    margin: 20px auto;
    padding: 14px 18px;
    background: var(--warn-bg);
    border: 1px solid var(--warn-border);
    border-left: 6px solid var(--warn-text);
    border-radius: 8px;
    color: var(--warn-text);
    font-size: 13px;
    line-height: 1.6;
}}

/* KPI Metric Cards */
.kpi-grid {{
    max-width: 1380px;
    margin: 0 auto 24px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px;
}}

.kpi-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
}}

.kpi-label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    display: block;
    margin-bottom: 6px;
}}

.kpi-value {{
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
}}

.kpi-subtext {{
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 4px;
}}

/* Filter Bar */
.filter-bar {{
    max-width: 1380px;
    margin: 0 auto 20px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
}}

.search-input {{
    flex: 1 1 280px;
    min-height: 40px;
    background: #080d15;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 14px;
    color: #ffffff;
    font-size: 14px;
}}

.search-input:focus {{
    outline: 2px solid var(--accent);
    border-color: var(--accent);
}}

select.filter-select {{
    min-height: 40px;
    background: #080d15;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 13px;
    cursor: pointer;
}}

.view-toggle {{
    display: flex;
    gap: 4px;
    background: #080d15;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 3px;
}}

.view-btn {{
    padding: 6px 12px;
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-size: 12px;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
}}

.view-btn.active {{
    background: var(--accent);
    color: #080d15;
}}

.results-count {{
    font-size: 13px;
    color: var(--text-muted);
    margin-left: auto;
    font-weight: 500;
}}

/* Cards Container */
.cards-container {{
    max-width: 1380px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.question-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    transition: border-color 0.15s ease;
}}

.question-card:hover {{
    border-color: var(--accent);
}}

.card-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-subtle);
}}

.card-identifiers {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}}

.ref-pill {{
    background: #1e3a8a;
    color: #93c5fd;
    font-weight: 700;
    font-size: 12px;
    padding: 2px 8px;
    border-radius: 4px;
}}

.id-badge {{
    background: #1e293b;
    border: 1px solid var(--border);
    color: #ffffff;
    font-family: ui-monospace, Menlo, Consolas, monospace;
    font-weight: 600;
    font-size: 13px;
    padding: 2px 8px;
    border-radius: 4px;
}}

.task-id {{
    color: var(--text-muted);
    font-size: 12px;
}}

.card-badges {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}}

.pill {{
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 999px;
    text-transform: uppercase;
}}

.pill-lot {{ background: #0c4a6e; color: #7dd3fc; border: 1px solid #0284c7; }}
.pill-in-scope {{ background: var(--success-bg); color: var(--success-text); border: 1px solid var(--success-border); }}
.pill-prereq {{ background: #312e81; color: #c7d2fe; border: 1px solid #4f46e5; }}
.pill-collision {{ background: #3b0764; color: #f0abfc; border: 1px solid #9333ea; }}
.pill-hold {{ background: var(--danger-bg); color: var(--danger-text); border: 1px solid var(--danger-border); }}
.pill-figure {{ background: #291e0a; color: #fde047; border: 1px solid #78350f; }}
.pill-textonly {{ background: #1e293b; color: #94a3b8; border: 1px solid #334155; }}

.card-paper {{
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 12px;
}}

.card-stem {{
    font-size: 15px;
    line-height: 1.6;
    color: #f8fafc;
    margin-bottom: 14px;
    background: #0c1422;
    padding: 14px 16px;
    border-radius: 6px;
    border-left: 3px solid var(--accent);
    font-family: inherit;
}}

.options-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 8px;
    margin-bottom: 14px;
}}

.option-box {{
    background: #0f1828;
    border: 1px solid var(--border-subtle);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
}}

.card-accordion {{
    margin-top: 10px;
    border-top: 1px solid var(--border-subtle);
    padding-top: 10px;
}}

.accordion-toggle {{
    background: transparent;
    border: none;
    color: var(--accent);
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}}

.accordion-toggle:hover {{
    color: #ffffff;
}}

.accordion-body {{
    display: none;
    margin-top: 10px;
    padding: 12px;
    background: #080d15;
    border-radius: 6px;
    font-size: 12px;
}}

.accordion-body.open {{
    display: block;
}}

.hold-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}}

.hold-tag {{
    font-family: ui-monospace, Menlo, Consolas, monospace;
    font-size: 10px;
    background: #3b1116;
    border: 1px solid #7f1d1d;
    color: #fca5a5;
    padding: 2px 6px;
    border-radius: 4px;
}}

/* Table View */
.table-container {{
    max-width: 1380px;
    margin: 0 auto;
    overflow-x: auto;
    display: none;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    text-align: left;
}}

th, td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-subtle);
}}

th {{
    background: #080d15;
    color: var(--text-muted);
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    position: sticky;
    top: 80px;
}}

tr:hover {{
    background: var(--surface-hover);
}}

footer {{
    max-width: 1380px;
    margin: 40px auto 0;
    text-align: center;
    font-size: 12px;
    color: var(--text-muted);
    border-top: 1px solid var(--border-subtle);
    padding-top: 20px;
}}
</style>
</head>
<body>

<header>
    <div class="header-container">
        <div class="title-group">
            <h1>Grade9 v4.0 — WPE 79-Question Inventory Browser <span class="badge-private">Private Workspace</span></h1>
            <p>Custody: D:\\CodeD\\grade9v4\\workspace\\output\\G9V4_LOTS\\ · Authenticated Local Repository Archive</p>
        </div>
        <div style="font-size: 12px; color: var(--text-muted); text-align: right;">
            Academic Admission: <strong style="color: #fca5a5;">0 / 3 (100% HOLD)</strong><br>
            Student Release: <strong style="color: #fca5a5;">NOT AUTHORIZED</strong>
        </div>
    </div>
</header>

<main style="padding: 0 16px;">
    <div class="disclaimer-banner" role="region" aria-label="Governance Disclaimer">
        <strong>PRIVATE AUDIT INTERFACE · NOT AN APPROVED QUESTION BANK · 0 ADMITTED FOR RELEASE</strong><br>
        This internal dashboard browses all 79 raw question records collected for the Work, Power &amp; Energy (WPE) pilot curriculum.
        All authentic stems, option lists, and figure descriptions are held under strict local source custody. Source rights, official answers, diagram redrafts, and independent academic QRT reviews remain in active HOLD status.
    </div>

    <section class="kpi-grid" aria-label="Inventory Metrics">
        <div class="kpi-card">
            <span class="kpi-label">Raw Records Collected</span>
            <div class="kpi-value">79</div>
            <div class="kpi-subtext">All candidate entries in registry.json</div>
        </div>
        <div class="kpi-card">
            <span class="kpi-label">Provisional Distinct</span>
            <div class="kpi-value">78</div>
            <div class="kpi-subtext">1 candidate alias pair identified</div>
        </div>
        <div class="kpi-card">
            <span class="kpi-label">In-Scope WPE Questions</span>
            <div class="kpi-value">65</div>
            <div class="kpi-subtext">Core mechanical work &amp; energy physics</div>
        </div>
        <div class="kpi-card">
            <span class="kpi-label">Processed in Lots 02–13</span>
            <div class="kpi-value">60</div>
            <div class="kpi-subtext">Batches A, B, C, D (12 lots &times; 5)</div>
        </div>
        <div class="kpi-card">
            <span class="kpi-label">Pending Lot 14 Candidates</span>
            <div class="kpi-value">5</div>
            <div class="kpi-subtext">Remaining in-scope candidates to process</div>
        </div>
        <div class="kpi-card" style="border-left: 4px solid var(--danger-border);">
            <span class="kpi-label">Admitted for Student Release</span>
            <div class="kpi-value" style="color: #fca5a5;">0</div>
            <div class="kpi-subtext">100% HOLD:ACADEMIC_ADMISSION</div>
        </div>
    </section>

    <section class="filter-bar" aria-label="Controls and Filters">
        <input type="text" id="searchInput" class="search-input" placeholder="Search by ID (e.g. EX-M2, Q01), sitting, stem keywords, or hold code...">
        
        <select id="scopeFilter" class="filter-select" aria-label="Filter by Scope">
            <option value="ALL">All Scopes (79)</option>
            <option value="IN_SCOPE">In-Scope WPE (65)</option>
            <option value="PREREQUISITE_BRIDGE">Prerequisite Bridges (8)</option>
            <option value="COLLISION_OUT_OF_SCOPE">Collisions / Out-of-Scope (5)</option>
        </select>

        <select id="lotFilter" class="filter-select" aria-label="Filter by Lot">
            <option value="ALL">All Lots</option>
            <option value="LOT-02">Lot 02 (Batch A)</option>
            <option value="LOT-03">Lot 03 (Batch A)</option>
            <option value="LOT-04">Lot 04 (Batch A)</option>
            <option value="LOT-05">Lot 05 (Batch B)</option>
            <option value="LOT-06">Lot 06 (Batch B)</option>
            <option value="LOT-07">Lot 07 (Batch B)</option>
            <option value="LOT-08">Lot 08 (Batch C)</option>
            <option value="LOT-09">Lot 09 (Batch C)</option>
            <option value="LOT-10">Lot 10 (Batch C)</option>
            <option value="LOT-11">Lot 11 (Batch D)</option>
            <option value="LOT-12">Lot 12 (Batch D)</option>
            <option value="LOT-13">Lot 13 (Batch D)</option>
            <option value="LOT-14">Lot 14 (Pending)</option>
            <option value="UNASSIGNED">Unassigned (Prereq/Collision)</option>
        </select>

        <select id="figureFilter" class="filter-select" aria-label="Filter by Figure Status">
            <option value="ALL">All Figures (79)</option>
            <option value="TEXT_ONLY_NO_FIGURE">Text-Only (43)</option>
            <option value="REQUIRED">Requires Figure Diagram (36)</option>
        </select>

        <div class="view-toggle" role="group" aria-label="View toggle">
            <button type="button" id="btnCardView" class="view-btn active">Cards</button>
            <button type="button" id="btnTableView" class="view-btn">Table</button>
        </div>

        <span id="resultsCount" class="results-count">Showing 79 of 79 records</span>
    </section>

    <!-- Cards View -->
    <div id="cardsView" class="cards-container"></div>

    <!-- Table View -->
    <div id="tableView" class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Ref</th>
                    <th>ID / Task</th>
                    <th>Lot</th>
                    <th>Scope</th>
                    <th>Paper / Sitting</th>
                    <th>Figure</th>
                    <th>Key Status</th>
                    <th>Stem Preview</th>
                    <th>Active Holds</th>
                </tr>
            </thead>
            <tbody id="tableBody"></tbody>
        </table>
    </div>

    <footer>
        Grade9 v4.0 · Private Source Custody Browser · Strictly Internal Research &amp; Reconciliation · No Academic Approval Inferred
    </footer>
</main>

<script id="recordsData" type="application/json">
{records_json}
</script>

<script>
const records = JSON.parse(document.getElementById('recordsData').textContent);

const cardsView = document.getElementById('cardsView');
const tableView = document.getElementById('tableView');
const tableBody = document.getElementById('tableBody');
const searchInput = document.getElementById('searchInput');
const scopeFilter = document.getElementById('scopeFilter');
const lotFilter = document.getElementById('lotFilter');
const figureFilter = document.getElementById('figureFilter');
const resultsCount = document.getElementById('resultsCount');
const btnCardView = document.getElementById('btnCardView');
const btnTableView = document.getElementById('btnTableView');

let activeView = 'cards';

function getScopeBadge(scope) {{
    if (scope === 'IN_SCOPE') return '<span class="pill pill-in-scope">In-Scope WPE</span>';
    if (scope === 'PREREQUISITE_BRIDGE') return '<span class="pill pill-prereq">Prereq Bridge</span>';
    return '<span class="pill pill-collision">Collision / Out-of-Scope</span>';
}}

function getFigureBadge(figStatus) {{
    if (figStatus === 'TEXT_ONLY_NO_FIGURE') return '<span class="pill pill-textonly">Text Only</span>';
    return '<span class="pill pill-figure">Requires Figure</span>';
}}

function renderCards(filtered) {{
    cardsView.innerHTML = '';
    filtered.forEach(r => {{
        const card = document.createElement('article');
        card.className = 'question-card';

        let optionsHtml = '';
        if (r.options && r.options.length > 0) {{
            optionsHtml = '<div class="options-grid">' + 
                r.options.map(opt => `<div class="option-box">${{escapeHtml(opt)}}</div>`).join('') +
                '</div>';
        }}

        let figureHtml = '';
        if (r.figure_note) {{
            figureHtml = `<div style="font-size: 12px; color: var(--warn-text); background: var(--warn-bg); padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; border: 1px solid var(--warn-border);">
                <strong>Figure Description Note:</strong> ${{escapeHtml(r.figure_note)}}
            </div>`;
        }}

        let duplicateNotice = '';
        if (r.duplicate_status === 'CANDIDATE_ALIAS') {{
            duplicateNotice = `<span style="font-size: 11px; background: #4c1d95; color: #e9d5ff; padding: 2px 6px; border-radius: 4px;">Candidate Alias of ${{r.alias_of}}</span>`;
        }}

        let holdsHtml = '';
        if (r.holds && r.holds.length > 0) {{
            holdsHtml = `<div class="hold-tags">` + 
                r.holds.map(h => `<span class="hold-tag">${{h}}</span>`).join('') +
                `</div>`;
        }}

        let solutionHtml = '';
        if (r.solution) {{
            solutionHtml = `<div style="margin-top: 8px; padding-top: 8px; border-top: 1px dashed var(--border-subtle); color: var(--text-muted);">
                <strong style="color: var(--text);">Solution / Derivation Excerpt:</strong><br>${{escapeHtml(r.solution)}}
            </div>`;
        }}

        card.innerHTML = `
            <div class="card-top">
                <div class="card-identifiers">
                    <span class="ref-pill">${{r.ref}}</span>
                    <span class="id-badge">${{r.id}}</span>
                    <span class="task-id">${{r.task_id || ''}}</span>
                    ${{duplicateNotice}}
                </div>
                <div class="card-badges">
                    <span class="pill pill-lot">${{r.lot}}</span>
                    ${{getScopeBadge(r.scope)}}
                    ${{getFigureBadge(r.figure_status)}}
                    <span class="pill pill-hold">Hold: Admission</span>
                </div>
            </div>
            <div class="card-paper">
                <strong>Paper / Sitting:</strong> ${{escapeHtml(r.paper)}} &bull; <strong>Origin:</strong> ${{r.origin}}
            </div>
            <div class="card-stem">
                ${{escapeHtml(r.stem) || '<em style="color: var(--text-muted);">Stem text not bound in registry.</em>'}}
            </div>
            ${{figureHtml}}
            ${{optionsHtml}}
            <div class="card-accordion">
                <button type="button" class="accordion-toggle" onclick="toggleDetails(this)">
                    <span>Show Technical Holds &amp; Audit Metadata</span> &darr;
                </button>
                <div class="accordion-body">
                    <div><strong>Official Key Status:</strong> ${{r.key_status}} &bull; ${{escapeHtml(r.key_note || 'Unmapped')}}</div>
                    <div style="margin-top: 4px;"><strong>Stem SHA-256:</strong> <code style="font-size: 11px;">${{r.stem_sha256 || 'None'}}</code></div>
                    ${{solutionHtml}}
                    <div style="margin-top: 8px;"><strong>Active Blocker Holds (${{r.holds ? r.holds.length : 0}}):</strong></div>
                    ${{holdsHtml}}
                </div>
            </div>
        `;
        cardsView.appendChild(card);
    }});
}}

function renderTable(filtered) {{
    tableBody.innerHTML = '';
    filtered.forEach(r => {{
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${{r.ref}}</strong></td>
            <td><code>${{r.id}}</code><br><small style="color: var(--text-muted);">${{r.task_id || ''}}</small></td>
            <td><span class="pill pill-lot">${{r.lot}}</span></td>
            <td>${{getScopeBadge(r.scope)}}</td>
            <td><small>${{escapeHtml(r.paper)}}</small></td>
            <td>${{getFigureBadge(r.figure_status)}}</td>
            <td><small>${{r.key_status}}</small></td>
            <td style="max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                <span title="${{escapeHtml(r.stem || '')}}">${{escapeHtml((r.stem || '').substring(0, 80))}}...</span>
            </td>
            <td><small style="color: #fca5a5;">${{r.holds ? r.holds.length : 0}} holds</small></td>
        `;
        tableBody.appendChild(row);
    }});
}}

function toggleDetails(btn) {{
    const body = btn.nextElementSibling;
    const isOpen = body.classList.toggle('open');
    btn.innerHTML = isOpen ? '<span>Hide Technical Holds &amp; Audit Metadata</span> &uarr;' : '<span>Show Technical Holds &amp; Audit Metadata</span> &darr;';
}}

function escapeHtml(text) {{
    if (!text) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}}

function applyFilters() {{
    const query = searchInput.value.toLowerCase().trim();
    const scopeVal = scopeFilter.value;
    const lotVal = lotFilter.value;
    const figureVal = figureFilter.value;

    const filtered = records.filter(r => {{
        // Scope
        if (scopeVal !== 'ALL' && r.scope !== scopeVal) return false;

        // Lot
        if (lotVal !== 'ALL') {{
            if (lotVal === 'UNASSIGNED') {{
                if (r.lot !== 'UNASSIGNED') return false;
            }} else {{
                if (!r.lot.startsWith(lotVal)) return false;
            }}
        }}

        // Figure
        if (figureVal === 'TEXT_ONLY_NO_FIGURE' && r.figure_status !== 'TEXT_ONLY_NO_FIGURE') return false;
        if (figureVal === 'REQUIRED' && r.figure_status === 'TEXT_ONLY_NO_FIGURE') return false;

        // Search query
        if (query) {{
            const matchId = (r.id || '').toLowerCase().includes(query);
            const matchRef = (r.ref || '').toLowerCase().includes(query);
            const matchTask = (r.task_id || '').toLowerCase().includes(query);
            const matchPaper = (r.paper || '').toLowerCase().includes(query);
            const matchStem = (r.stem || '').toLowerCase().includes(query);
            const matchHolds = (r.holds || []).some(h => h.toLowerCase().includes(query));
            if (!matchId && !matchRef && !matchTask && !matchPaper && !matchStem && !matchHolds) return false;
        }}

        return true;
    }});

    resultsCount.textContent = `Showing ${{filtered.length}} of ${{records.length}} records`;

    if (activeView === 'cards') {{
        renderCards(filtered);
    }} else {{
        renderTable(filtered);
    }}
}}

searchInput.addEventListener('input', applyFilters);
scopeFilter.addEventListener('change', applyFilters);
lotFilter.addEventListener('change', applyFilters);
figureFilter.addEventListener('change', applyFilters);

btnCardView.addEventListener('click', () => {{
    activeView = 'cards';
    btnCardView.classList.add('active');
    btnTableView.classList.remove('active');
    cardsView.style.display = 'flex';
    tableView.style.display = 'none';
    applyFilters();
}});

btnTableView.addEventListener('click', () => {{
    activeView = 'table';
    btnTableView.classList.add('active');
    btnCardView.classList.remove('active');
    cardsView.style.display = 'none';
    tableView.style.display = 'block';
    applyFilters();
}});

// Initial render
applyFilters();
</script>
</body>
</html>
"""
    with open(OUTPUT_HTML, "w", encoding="utf-8") as out:
        out.write(html_content)

    print(f"Generated Private 79-Question Browser: {OUTPUT_HTML}")
    print(f"File size: {os.path.getsize(OUTPUT_HTML)} bytes")

def main():
    records = load_data()
    print(f"Loaded {len(records)} records from private custody files.")
    generate_html(records)

if __name__ == "__main__":
    main()
