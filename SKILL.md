---
name: vizcraft
description: Generate interactive, self-contained architecture diagrams and progress visualizations from a single JSON file.
license: MIT
---

# 🎨 VizCraft Agent Instructions

**CRITICAL DIRECTIVE:** You are now equipped with the VizCraft skill. Your job is to generate highly detailed, visually stunning JSON data structures that power interactive SVG/HTML visualizations. 

VizCraft is a zero-dependency local layout engine. You supply the JSON data, and the `generate.py` script automatically builds an interactive HTML visualization.

## 🛠️ The Workflow

1. **Understand the User's Request:** Are they asking for a system architecture diagram or a project progress tracker?
2. **Draft the JSON:** Use the appropriate schema below to draft the JSON structure.
3. **Save the JSON:** Save your output to a `.json` file in the user's workspace.
4. **Compile the HTML:** Run `python generate.py <your_json_file.json> <output_html_file.html>`
5. **Serve/Open:** Provide the user with the path to the HTML file or use a tool to open it in their browser.

---

## 🏗️ Schema 1: System Architecture

Use this when the user wants to map out a codebase, microservices, cloud infrastructure, or AI agent workflow.

### Architecture JSON Structure
```json
{
  "project": {
    "name": "Project Name",
    "description": "Short description of the system",
    "theme": "dark_neon"
  },
  "groups": [
    {
      "id": "backend_group",
      "label": "Backend Core",
      "x": 100, "y": 100,
      "width": 400, "height": 300,
      "nodes": [
        {
          "id": "api_server",
          "label": "FastAPI Server",
          "kind": "entry",
          "logo": "https://cdn.simpleicons.org/fastapi/ffffff",
          "x": 20, "y": 40
        }
      ]
    }
  ],
  "standalone": [
    { "id": "db", "label": "PostgreSQL", "kind": "store", "logo": "https://cdn.simpleicons.org/postgresql/ffffff", "x": -100, "y": 200 }
  ],
  "edges": [
    {
      "source": "api_server",
      "target": "db",
      "label": "SQL Queries",
      "sourcePort": "right",
      "targetPort": "left"
    }
  ],
  "steps": [
    {
      "title": "1. User Request",
      "description": "The request hits the API server.",
      "highlight": ["api_server", "db"]
    }
  ]
}
```

### Design Rules for Architecture:
- **Spatial Reasoning & Spacing:** THIS IS CRITICAL. You must manually calculate `x` and `y` coordinates for groups and nodes to prevent overlapping. Visualize a grid: use multiples of 100 or 150 for `x` and `y` to keep nodes perfectly aligned. Make sure the parent `group`'s `width` and `height` fully encapsulates its inner nodes. 
- **Grouping:** Group related nodes together into logical clusters (e.g., "Edge", "Core", "Database"). This makes the graph visually striking and easy to read.
- **Node Kinds:** `entry`, `agent`, `service`, `store`, `external`, `model`, `cron`, `tool`.
- **Logos (New):** You can now specify an exact SVG logo URL for nodes using the `logo` key. Use `https://cdn.simpleicons.org/<icon_name>/ffffff` for standard tech logos!
- **Story Mode:** Always include at least 3 `steps` to explain the flow. This powers the interactive "Story" tab.

---

## 📅 Schema 2: Project Progress (Tracker)

Use this when the user wants a Kanban board, a sprint tracker, a roadmap, or a task list. 
*Note: Progress trackers feature a sleek, modern layout with GSAP animations.*

### Progress JSON Structure
```json
{
  "project": {
    "name": "Uber Clone Tracker",
    "description": "MVP Sprint Roadmap",
    "theme": "dark_neon"
  },
  "phases": [
    {
      "id": "phase1",
      "title": "Phase 1: Foundation",
      "description": "Core setup and infrastructure.",
      "tip": "Ensure the database schema is locked before proceeding.",
      "tasks": [
        {
          "id": "t1",
          "title": "Setup PostgreSQL",
          "note": "Use Docker compose for local dev.\n\nRun migrations."
        }
      ]
    }
  ]
}
```

### Design Rules for Progress Tracker:
- **Phases:** Keep phases logical. 3 to 6 phases is ideal.
- **Tasks:** 3 to 5 tasks per phase. 
- **Notes:** Use the `note` field to provide extreme detail. This powers the interactive sidebar.
- **Tips:** Always provide a highly intelligent `tip` for each phase.

---

## 🎨 Theme Selection
Always choose a theme that fits the vibe of the project.
Available themes:
1. `dark_neon` (Default) - Sleek, futuristic, high-contrast, glassmorphic.
2. `cyberpunk` - Bright yellow/cyan/red, high aggression.
3. `dracula` - Dark purple/pink classic Dracula palette.
4. `synthwave` - Retro 80s magenta/purple outrun aesthetic.
5. `nord` - Arctic, cold blue/gray tones.
6. `gruvbox` - Warm retro groove box colors.
7. `solarized_dark` - Classic teal/yellow.
8. `monokai` - High contrast dark.
9. `rdr2_gritty` - Warm, sepia.
10. `minimal_light` - Clean, glassmorphic professional light mode.
