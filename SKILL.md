---
name: vizcraft
description: Generate interactive, self-contained architecture diagrams, flowcharts and progress trackers from a single JSON file. Auto-layout, collision-free edge routing, 20 themes.
license: MIT
---

# 🎨 VizCraft Agent Instructions

You can turn a JSON description into an interactive HTML visualization with **no dependencies**. You write the JSON; `generate.py` validates it and builds the page. Layout and edge routing are done by VizCraft, so **you do not need to calculate coordinates**.

## 🛠️ The Workflow

1. **Pick the type:** system/infra/agent map or flowchart → *architecture* (Schema 1). Roadmap, sprint board, task list → *progress* (Schema 2).
2. **Write the JSON** to a `.json` file in the user's workspace.
3. **Validate and build:** `python generate.py <file.json> <out.html>`
   - Read the `WARN` lines it prints and **fix every one**, then re-run. They catch dangling edges, duplicate ids, unknown kinds/themes, overlapping boxes and bad story ids.
   - Validate only: `python generate.py <file.json> --check`. Fail on warnings: add `--strict`.
4. **Open it:** give the user the HTML path (or `--open` to launch the browser).

Useful: `python generate.py --list-themes`. Full JSON Schemas are in `schemas/`.

---

## 🏗️ Schema 1: Architecture (also flowcharts)

```json
{
  "project": {
    "name": "Checkout System",
    "description": "Order flow from cart to fulfilment",
    "theme": "tokyo_night",
    "edgeStyle": "orthogonal",
    "nodeStyle": "card",
    "direction": "LR"
  },
  "groups": [
    {
      "id": "backend", "label": "Backend",
      "nodes": [
        { "id": "api", "label": "Orders API", "kind": "service",
          "logo": "https://cdn.simpleicons.org/fastapi/ffffff",
          "description": "Validates carts and creates orders.", "tags": ["Python"] },
        { "id": "db", "label": "Postgres", "kind": "store", "shape": "cylinder" }
      ]
    }
  ],
  "standalone": [
    { "id": "shopper", "label": "Shopper", "kind": "user" }
  ],
  "edges": [
    { "source": "shopper", "target": "api", "label": "HTTPS" },
    { "source": "api", "target": "db", "label": "SQL" },
    { "source": "api", "target": "db", "label": "read replica", "style": "dashed" }
  ],
  "steps": [
    { "title": "Shopper checks out", "description": "The request reaches the API.", "highlight": ["shopper", "api"] }
  ]
}
```

### Layout: let VizCraft do it (default)
- **Omit `x`/`y` everywhere** and VizCraft lays groups and nodes out in layers following the edge direction (`direction`: `LR` left→right, or `TB` top→bottom). This is the recommended path and cannot produce overlaps.
- Only set coordinates if the user wants an exact arrangement. Then it is all-or-nothing: give **every** group and standalone node `x`/`y` (node `x`/`y` are relative to their group), keep ≥ 40 px between boxes, and make `width`/`height` enclose the nodes. The validator reports overlaps.
- Nodes are at least 120×34 px (wider for long labels). Keep labels short (≤ 24 chars).

### Nodes
- `kind` (colour + icon): `entry` `agent` `service` `store` `external` `model` `cron` `tool` `queue` `gateway` `client` `cache` `function` `user` `monitor` `security`.
  Aliases also work: `database`→store, `api`→service, `lambda`→function, `llm`→model, `broker`→queue, `lb`/`cdn`→gateway, `auth`→security, `start`→entry, `end`→external, `decision`→agent.
- `shape`: `rect` (default), `pill` (start/end, entry points), `diamond` (decisions), `hexagon` (processing/prepare), `cylinder` (databases).
- `logo`: `https://cdn.simpleicons.org/<slug>/ffffff` (white logos are auto-inverted on light themes). Check the slug exists; if it fails the kind icon is used.
- `description` and `tags` appear in the hover tooltip. Use them, they make diagrams self-explaining.

### Edges
- `label` (keep short), `style`: `solid` | `dashed` (async/optional) | `dotted` (telemetry/weak), `bidirectional: true`, `color`.
- **Do not set `sourcePort`/`targetPort`** unless you must; the router picks sides, spreads parallel edges onto separate lanes and avoids nodes. A hint pointing away from the target is ignored.
- Edges are routed without overlapping nodes or each other where space allows; labels are placed clear of nodes and other labels.

### Flowcharts
Use `standalone` nodes only, `"direction": "TB"`, shapes `pill` (start/end), `rect` (step), `diamond` (decision) and label branch edges `yes`/`no`. The first outgoing edge of a diamond keeps the straight-through port; later branches fan out sideways. See `demos/auth_flowchart.json`.

### Story mode
Add 3–6 `steps`. `highlight` takes node ids **or group ids**. The viewer zooms to the highlighted nodes, lights their edges and offers Prev / Play / Next (and ← → keys).

### Project options
| key | values | default |
|---|---|---|
| `theme` | see Themes | `dark_neon` |
| `edgeStyle` | `orthogonal` (rounded), `curved`, `step` (sharp), `straight` | `orthogonal` |
| `nodeStyle` | `card`, `tinted`, `outline` (neon glow) | `card` |
| `direction` | `LR`, `TB` | `LR` |

Users can change theme, edge style and node style live in the sidebar.

---

## 📅 Schema 2: Progress tracker

```json
{
  "project": { "name": "Launch Plan", "description": "MVP roadmap", "theme": "catppuccin_mocha" },
  "phases": [
    {
      "id": "phase1", "title": "Phase 1: Foundation", "description": "Core setup.",
      "tip": "Lock the schema before building features.",
      "tasks": [
        { "id": "t1", "title": "Set up Postgres", "note": "Use Docker Compose.\n- run migrations\n- seed **test data**",
          "done": true, "priority": "high", "owner": "Sam", "due": "Fri", "tags": ["db"] }
      ]
    }
  ]
}
```
- 3–6 phases, 3–5 tasks each. **Task `id`s must be unique across the whole file** (they are the saved-progress keys).
- `note` supports `**bold**`, `*italic*`, `` `code` `` and `- ` bullets. Be detailed; it fills the Notes panel.
- Optional per task: `done` (initial state), `priority` (`p0`/`high`, `p1`/`medium`, `p2`/`low`), `owner`, `due`, `tags`.
- Always give each phase a useful `tip`. Progress is saved in the browser's localStorage; the sidebar has *Hide completed*, *Reset progress* and a *Next up* shortcut.

---

## 🎨 Themes (20)
Choose one that fits the project's mood, and prefer a light theme for documents that will be printed or screenshotted into slides.

**Dark:** `dark_neon` (default, clean), `tokyo_night`, `catppuccin_mocha`, `github_dark`, `rose_pine`, `everforest`, `dracula`, `synthwave`, `nord`, `gruvbox`, `solarized_dark`, `monokai`, `rdr2_gritty` (sepia/serif), `blueprint` (engineering blue), `terminal` (green CRT), `high_contrast` (accessibility).
**Light:** `minimal_light`, `solarized_light`, `paper` (serif, print-friendly), `cyberpunk` (loud yellow).

`python generate.py --list-themes` prints the current list. All themes meet WCAG AA contrast for text.

## ✅ Checklist before you hand over
- `generate.py` ran with **no WARN lines**.
- Every edge `source`/`target` and every `highlight` id exists.
- Labels are short; nodes have `description`s; ≥ 3 story steps.
- You told the user the output path and that they can switch themes/edge style in the sidebar.
