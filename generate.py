#!/usr/bin/env python3
"""
VizCraft Generator
==================
Generates self-contained, Awwwards-level HTML visualizations from JSON data.

Usage:
  python generate.py demos/demo_progress.json output/progress.html
  python generate.py my_system.json --check          # validate only
  python generate.py --list-themes

Template auto-detected from JSON:
  - "groups" / "standalone" / "edges" -> architecture
  - "phases"                           -> progress

Before writing the HTML the input is validated. Problems (dangling edges,
overlapping boxes, duplicate ids, unknown themes...) are printed as warnings;
pass --strict to turn them into a non-zero exit code.

Author: Collins (github.com/Kimanzi-Collins)
License: MIT
"""
import argparse
import html as htmllib
import json
import os
import re
import sys
import tempfile
import webbrowser
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

THEMES_FILE = "_themes.css"
SHARED_JS_FILE = "_shared.js"
THEME_MARKER = re.compile(r"/\*\s*@theme\s+([A-Za-z0-9_]+)\s*\|\s*(.+?)\s*\*/")
DEFAULT_THEME = "dark_neon"

# --- Vocabulary (keep in sync with templates/architecture.html) -------------
NODE_KINDS = [
    "entry", "agent", "service", "store", "external", "model", "cron", "tool",
    "queue", "gateway", "client", "cache", "function", "user", "monitor", "security",
]
KIND_ALIASES = {
    "database", "db", "storage", "datastore", "bucket", "api", "backend", "server",
    "microservice", "app", "process", "frontend", "ui", "web", "mobile", "browser",
    "lb", "loadbalancer", "load_balancer", "proxy", "cdn", "router", "actor", "person",
    "broker", "stream", "topic", "bus", "lambda", "serverless", "worker",
    "observability", "monitoring", "metrics", "logging", "auth", "iam", "firewall",
    "vault", "llm", "ai", "ml", "job", "scheduler", "timer", "third_party",
    "thirdparty", "saas", "start", "end", "decision",
}
SHAPES = ["rect", "pill", "diamond", "hexagon", "cylinder"]
EDGE_STYLES = ["orthogonal", "curved", "step", "straight"]
NODE_STYLES = ["card", "tinted", "outline"]
LINE_STYLES = ["solid", "dashed", "dotted"]
PORTS = ["top", "bottom", "left", "right", "auto"]
DIRECTIONS = ["LR", "TB"]

# Group geometry (keep in sync with the layout constants in architecture.html)
GROUP_PAD_X, GROUP_PAD_BOTTOM = 20, 30
GROUP_MIN_W, GROUP_MIN_H = 160, 100


def node_size(shape, label):
    """Node (width, height) in px. Mirrors sizeOf() in architecture.html."""
    text_w = len(label) * 7
    if shape == "diamond":
        return max(150, text_w + 80), 64
    if shape == "hexagon":
        return max(140, text_w + 70), 44
    if shape == "cylinder":
        return max(120, text_w + 40), 44
    if shape == "pill":
        return max(120, text_w + 44), 34
    return max(120, text_w + 40), 34


# ---------------------------------------------------------------------------
# Themes & template assembly
# ---------------------------------------------------------------------------
def discover_themes():
    """Return [{'id': ..., 'label': ...}] parsed from `@theme` markers in _themes.css."""
    css = (TEMPLATES_DIR / THEMES_FILE).read_text(encoding="utf-8")
    return [{"id": m.group(1), "label": m.group(2)} for m in THEME_MARKER.finditer(css)]


def detect_template(data):
    if "phases" in data:
        return "progress"
    if "groups" in data or "standalone" in data or "edges" in data:
        return "architecture"
    raise ValueError("Cannot detect template type. See README for JSON schema.")


def load_template(template_type):
    p = TEMPLATES_DIR / f"{template_type}.html"
    if not p.exists():
        raise FileNotFoundError(f"Template not found: {p}")
    return p.read_text(encoding="utf-8")


def js_safe_json(data):
    """JSON for embedding inside a <script> block without letting the data end it."""
    text = json.dumps(data, ensure_ascii=False)
    return (text.replace("</", "<\\/").replace("<!--", "<\\!--")
                .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def render(data, template_type, themes=None):
    """Assemble the final HTML string for `data`."""
    themes = themes if themes is not None else discover_themes()
    theme_ids = [t["id"] for t in themes]
    proj = data.get("project") or {}
    theme = proj.get("theme", DEFAULT_THEME)
    if theme not in theme_ids:
        theme = DEFAULT_THEME

    out = load_template(template_type)
    css = (TEMPLATES_DIR / THEMES_FILE).read_text(encoding="utf-8")
    shared = (TEMPLATES_DIR / SHARED_JS_FILE).read_text(encoding="utf-8")
    shared = shared.replace("/*__VIZCRAFT_THEME_LIST__*/[]", js_safe_json(themes))

    out = out.replace("/*__VIZCRAFT_THEMES__*/", css)
    out = out.replace("/*__VIZCRAFT_SHARED__*/", shared)
    out = out.replace("__PROJECT_NAME__", htmllib.escape(str(proj.get("name", "Architecture"))))
    out = out.replace("__PROJECT_DESC__", htmllib.escape(str(proj.get("description", ""))))
    out = out.replace("__THEME__", theme)
    out = out.replace("/*__VIZCRAFT_DATA__*/ null", js_safe_json(data))
    return out


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
class Report:
    """Collects validation messages. `warnings` count towards --strict."""

    def __init__(self):
        self.items = []

    def warn(self, msg):
        self.items.append(("WARN", msg))

    def note(self, msg):
        self.items.append(("NOTE", msg))

    @property
    def warnings(self):
        return [m for lvl, m in self.items if lvl == "WARN"]

    def print(self, stream=None):
        stream = stream or sys.stderr
        for lvl, msg in self.items:
            print(f"[VizCraft] {lvl}: {msg}", file=stream)


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _rects_overlap(a, b):
    return a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and a[1] < b[1] + b[3] and a[1] + a[3] > b[1]


def _check_project(proj, report, template_type):
    themes = [t["id"] for t in discover_themes()]
    theme = proj.get("theme")
    if theme is not None and theme not in themes:
        report.warn(f'project.theme "{theme}" is not a known theme; using {DEFAULT_THEME}. '
                    f'Run --list-themes to see the options.')
    if template_type == "architecture":
        if "edgeStyle" in proj and proj["edgeStyle"] not in EDGE_STYLES:
            report.warn(f'project.edgeStyle "{proj["edgeStyle"]}" is invalid (use one of {", ".join(EDGE_STYLES)}).')
        if "nodeStyle" in proj and proj["nodeStyle"] not in NODE_STYLES:
            report.warn(f'project.nodeStyle "{proj["nodeStyle"]}" is invalid (use one of {", ".join(NODE_STYLES)}).')
        if "direction" in proj and str(proj["direction"]).upper() not in DIRECTIONS:
            report.warn(f'project.direction "{proj["direction"]}" is invalid (use LR or TB).')
    if not proj.get("name"):
        report.note("project.name is missing.")


def validate_architecture(data):
    report = Report()
    _check_project(data.get("project") or {}, report, "architecture")

    groups = data.get("groups") or []
    standalone = data.get("standalone") or []
    edges = data.get("edges") or []
    steps = data.get("steps") or []

    nodes = {}           # id -> dict with resolved geometry info
    group_ids = set()
    seen_ids = {}

    def claim(ident, what):
        if ident in seen_ids:
            report.warn(f'Duplicate id "{ident}" ({what}; already used by {seen_ids[ident]}). '
                        f'Ids must be unique across groups and nodes.')
        seen_ids[ident] = what

    def register(n, where, group=None):
        nid = n.get("id")
        if not isinstance(nid, str) or not nid:
            report.warn(f"A node in {where} has no string 'id'.")
            return None
        claim(nid, f"node in {where}")
        label = str(n.get("label", nid))
        kind = str(n.get("kind", "")).lower().replace(" ", "_").replace("-", "_")
        if n.get("kind") is not None and kind not in NODE_KINDS and kind not in KIND_ALIASES:
            report.warn(f'Node "{nid}" has unknown kind "{n.get("kind")}" (rendered grey). '
                        f'Known kinds: {", ".join(NODE_KINDS)}.')
        shape = n.get("shape", "rect")
        if shape not in SHAPES:
            report.warn(f'Node "{nid}" has unknown shape "{shape}" (use one of {", ".join(SHAPES)}).')
            shape = "rect"
        w, h = node_size(shape, label)
        info = {"id": nid, "w": w, "h": h, "x": n.get("x"), "y": n.get("y"), "group": group}
        nodes[nid] = info
        return info

    group_nodes = {}
    for gi, g in enumerate(groups):
        gid = g.get("id", f"group-{gi}")
        group_ids.add(gid)
        claim(gid, "group")
        group_nodes[gid] = [i for i in (register(n, f'group "{gid}"', gid) for n in g.get("nodes") or []) if i]
    standalone_nodes = [i for i in (register(n, "standalone", None) for n in standalone) if i]

    # Edges
    for i, e in enumerate(edges):
        src, tgt = e.get("source"), e.get("target")
        for end, ref in (("source", src), ("target", tgt)):
            if ref not in nodes:
                report.warn(f'Edge #{i + 1} ({src} -> {tgt}) {end} "{ref}" does not match any node id; the edge will not be drawn.')
        for key in ("sourcePort", "targetPort"):
            if key in e and e[key] not in PORTS:
                report.warn(f'Edge #{i + 1} {key} "{e[key]}" is invalid (use top, bottom, left, right or auto).')
        if "style" in e and e["style"] not in LINE_STYLES:
            report.warn(f'Edge #{i + 1} style "{e["style"]}" is invalid (use solid, dashed or dotted).')

    connected = set()
    for e in edges:
        connected.add(e.get("source"))
        connected.add(e.get("target"))
    for nid in nodes:
        if nid not in connected:
            report.note(f'Node "{nid}" has no edges.')

    # Story steps
    for i, s in enumerate(steps):
        if not s.get("title"):
            report.warn(f"Step #{i + 1} has no title.")
        for ref in s.get("highlight") or []:
            if ref not in nodes and ref not in group_ids:
                report.warn(f'Step #{i + 1} highlights unknown id "{ref}".')
    if len(steps) < 3:
        report.note("Fewer than 3 story steps; Story mode works best with 3-6.")

    # Layout / overlap checks only make sense when everything is positioned manually
    def positioned(item):
        return _num(item.get("x")) and _num(item.get("y"))

    top_level = list(groups) + list(standalone)
    if top_level and not all(positioned(t) for t in top_level):
        report.note("Some groups/standalone nodes have no x/y: VizCraft will auto-layout the diagram.")
        return report

    rects = []   # (label, (x, y, w, h))
    for gi, g in enumerate(groups):
        gid = g.get("id", f"group-{gi}")
        members = group_nodes.get(gid, [])
        w = g.get("width") if _num(g.get("width")) else GROUP_MIN_W
        h = g.get("height") if _num(g.get("height")) else GROUP_MIN_H
        if members and all(_num(m["x"]) and _num(m["y"]) for m in members):
            w = max(w, max(m["x"] + m["w"] + GROUP_PAD_X + 10 for m in members))
            h = max(h, max(m["y"] + m["h"] + GROUP_PAD_BOTTOM for m in members))
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    ma, mb = members[a], members[b]
                    ra = (ma["x"], ma["y"], ma["w"], ma["h"])
                    rb = (mb["x"], mb["y"], mb["w"], mb["h"])
                    if _rects_overlap(ra, rb):
                        report.warn(f'Nodes "{ma["id"]}" and "{mb["id"]}" overlap inside group "{gid}". '
                                    f'Move one (nodes are at least {ma["w"]}x{ma["h"]} px).')
        rects.append((f'group "{gid}"', (g["x"], g["y"], w, h)))
    for n in standalone_nodes:
        rects.append((f'node "{n["id"]}"', (n["x"], n["y"], n["w"], n["h"])))
    for a in range(len(rects)):
        for b in range(a + 1, len(rects)):
            if _rects_overlap(rects[a][1], rects[b][1]):
                report.warn(f"{rects[a][0]} overlaps {rects[b][0]}. Increase the spacing between them "
                            f"or remove x/y to use auto-layout.")
    return report


def validate_progress(data):
    report = Report()
    _check_project(data.get("project") or {}, report, "progress")
    phases = data.get("phases") or []
    if not phases:
        report.warn("No phases defined.")
    phase_ids, task_ids = set(), {}
    for pi, p in enumerate(phases):
        pid = p.get("id")
        if not pid:
            report.warn(f"Phase #{pi + 1} has no id.")
        elif pid in phase_ids:
            report.warn(f'Duplicate phase id "{pid}".')
        phase_ids.add(pid)
        if not p.get("title"):
            report.warn(f"Phase #{pi + 1} has no title.")
        if not p.get("tip"):
            report.note(f'Phase "{pid or pi + 1}" has no tip.')
        tasks = p.get("tasks") or []
        if not tasks:
            report.warn(f'Phase "{pid or pi + 1}" has no tasks.')
        for ti, t in enumerate(tasks):
            tid = t.get("id")
            if not tid:
                report.warn(f'Task #{ti + 1} in phase "{pid or pi + 1}" has no id (progress is saved by task id).')
            elif tid in task_ids:
                report.warn(f'Duplicate task id "{tid}" (also in phase "{task_ids[tid]}"); '
                            f'ticking one would tick both.')
            else:
                task_ids[tid] = pid
            if not t.get("title"):
                report.warn(f'Task "{tid or ti + 1}" has no title.')
            if not t.get("note"):
                report.note(f'Task "{tid or ti + 1}" has no note.')
    return report


def validate(data, template_type):
    return validate_architecture(data) if template_type == "architecture" else validate_progress(data)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def load_json(input_path):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    try:
        with open(input_path, encoding="utf-8-sig") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"{input_path} is not valid JSON: {e.msg} (line {e.lineno}, column {e.colno})")
    if not isinstance(data, dict):
        raise ValueError("The top level of the JSON must be an object.")
    return data


def generate(input_path, output_path, force_template=None, strict=False, quiet=False):
    data = load_json(input_path)
    template_type = force_template or detect_template(data)
    if not quiet:
        print(f"[VizCraft] Template: {template_type}")

    report = validate(data, template_type)
    if not quiet:
        report.print()
    if strict and report.warnings:
        raise ValueError(f"{len(report.warnings)} validation warning(s) with --strict; nothing written.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render(data, template_type), encoding="utf-8")
    if not quiet:
        print(f"[VizCraft] Generated: {output_path.resolve()}")
    return str(output_path.resolve())


def generate_from_dict(json_data, filename):
    """Generates the HTML file to a temporary location and returns the path."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(json_data, tmp)
        tmp_path = tmp.name
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    try:
        return generate(tmp_path, str(out_dir / filename))
    finally:
        os.unlink(tmp_path)


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    p = argparse.ArgumentParser(description="VizCraft: architecture diagrams & progress trackers from JSON")
    p.add_argument("input", nargs="?", help="Input JSON file")
    p.add_argument("output", nargs="?", help="Output HTML file")
    p.add_argument("--template", "-t", choices=["architecture", "progress"])
    p.add_argument("--open", "-o", action="store_true", help="Open in browser after generation")
    p.add_argument("--strict", action="store_true", help="Fail (exit 2) if validation finds any warnings")
    p.add_argument("--check", action="store_true", help="Validate the JSON only; do not write HTML")
    p.add_argument("--quiet", "-q", action="store_true", help="Only print errors")
    p.add_argument("--list-themes", action="store_true", help="List available themes and exit")
    args = p.parse_args()

    if args.list_themes:
        for t in discover_themes():
            print(f'{t["id"]:<18} {t["label"]}')
        return

    if not args.input:
        p.error("input JSON is required")
    if not args.check and not args.output:
        p.error("output HTML is required (or use --check)")

    try:
        if args.check:
            data = load_json(args.input)
            template_type = args.template or detect_template(data)
            report = validate(data, template_type)
            report.print()
            n = len(report.warnings)
            print(f"[VizCraft] {template_type}: {n} warning(s)." if n else f"[VizCraft] {template_type}: OK.")
            sys.exit(2 if (n and args.strict) else 0)
        out = generate(args.input, args.output, args.template, strict=args.strict, quiet=args.quiet)
        if args.open:
            webbrowser.open(Path(out).as_uri())
    except (FileNotFoundError, ValueError) as e:
        print(f"[VizCraft] Error: {e}", file=sys.stderr)
        sys.exit(2 if "--strict" in str(e) else 1)


if __name__ == "__main__":
    main()
