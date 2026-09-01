#!/usr/bin/env python3
"""
VizCraft Generator
==================
Generates self-contained, Awwwards-level HTML visualizations from JSON data.

Usage:
  python generate.py demos/demo_progress.json output/progress.html

Template auto-detected from JSON:
  - "groups" / "standalone" / "edges" -> architecture
  - "phases"                           -> progress

Author: Collins (github.com/Kimanzi-Collins)
License: MIT
"""
import json, os, sys, argparse, tempfile, webbrowser
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

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

def generate(input_path, output_path, force_template=None):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    with open(input_path, encoding='utf-8-sig') as f:
        data = json.load(f)
    template_type = force_template or detect_template(data)
    print(f"[VizCraft] Template: {template_type}")
    html = load_template(template_type)
    proj = data.get("project", {})
    html = html.replace("__PROJECT_NAME__", proj.get("name", "Architecture"))
    html = html.replace("__PROJECT_DESC__", proj.get("description", ""))
    html = html.replace("__THEME__", proj.get("theme", "dark_neon"))
    html = html.replace("__VIZCRAFT_DATA__", json.dumps(data, ensure_ascii=False))
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
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
    p = argparse.ArgumentParser(description="VizCraft — Architecture & Progress Visualizations")
    p.add_argument("input", help="Input JSON file")
    p.add_argument("output", help="Output HTML file")
    p.add_argument("--template", "-t", choices=["architecture", "progress"])
    p.add_argument("--open", "-o", action="store_true", help="Open in browser after generation")
    args = p.parse_args()
    try:
        out = generate(args.input, args.output, args.template)
        if args.open:
            webbrowser.open(f"file://{out}")
    except (FileNotFoundError, ValueError) as e:
        print(f"[VizCraft] Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
