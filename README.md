<div align="center">
  <img src="https://raw.githubusercontent.com/Kimanzi-Collins/vizcraft/main/assets/banner.gif" alt="VizCraft Banner" width="100%" />
  
  <br/>
  <h1>🎨 VizCraft</h1>
  <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Plus+Jakarta+Sans&weight=600&size=22&pause=1500&color=3B82F6&center=true&vCenter=true&width=600&lines=Zero-dependency+layout+engine;Generate+architecture+diagrams+from+JSON;Build+interactive+progress+trackers;100%25+Self-Contained+HTML" alt="Typing SVG" /></a>
  <p><b>Highly interactive, self-contained architecture maps and progress trackers generated from a single JSON file.</b></p>
  
  <p>
    <a href="https://github.com/Kimanzi-Collins/vizcraft/stargazers"><img src="https://img.shields.io/github/stars/Kimanzi-Collins/vizcraft?style=for-the-badge&color=ffd700&logo=star&cacheSeconds=60" alt="Stars" /></a>
    <a href="https://github.com/Kimanzi-Collins/vizcraft/network/members"><img src="https://img.shields.io/github/forks/Kimanzi-Collins/vizcraft?style=for-the-badge&color=007ec6&logo=git&cacheSeconds=60" alt="Forks" /></a>
    <a href="https://github.com/Kimanzi-Collins/vizcraft/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Kimanzi-Collins/vizcraft?style=for-the-badge&color=success&cacheSeconds=60" alt="License" /></a>
  </p>
</div>

<br/>

## ✨ What is VizCraft?

VizCraft turns pure JSON data into stunning, interactive HTML visualizations with **no build tools, no framework, and no server**. Drop your JSON in, run one Python command, and open the HTML directly in any browser.

<div align="center">
  <img src="https://raw.githubusercontent.com/Kimanzi-Collins/vizcraft/main/assets/demo.gif" alt="VizCraft Demo Animation" width="800" style="border-radius: 12px; box-shadow: 0 4px 30px rgba(0,0,0,0.5);" />
</div>

<br/>

### 🚀 What you can build

1. 🌐 **Architecture Maps:** Codebase maps, system diagrams, microservice graphs.
2. 🔀 **Flowcharts:** Decision flows using `pill` / `diamond` / `hexagon` / `cylinder` shapes, from the same template.
3. 📈 **Progress Trackers:** Sprint boards, phased roadmaps, task lists with owners, priorities and due dates.

### ⚡ Core Features

- 🧭 **Auto-layout:** Leave out `x`/`y` and VizCraft arranges groups and nodes in layers that follow your edges (`LR` or `TB`). No coordinate maths.
- 🔌 **Collision-free edge routing:** Edges are routed around nodes on a grid, parallel edges get their own lanes and ports, and labels are placed clear of nodes and each other. Four styles: `orthogonal`, `curved`, `step`, `straight`.
- ✨ **Animated Data-flow Particles:** Visual routing particles that flow along the routed edges.
- 🔍 **Hover to trace, click to pin:** Hovering a node lights its connections and shows a tooltip with its description and tags.
- 📖 **Story Mode:** Step-by-step walkthrough that zooms to the highlighted nodes, with Prev / Play / Next and arrow-key control.
  <br/><img src="https://raw.githubusercontent.com/Kimanzi-Collins/vizcraft/main/assets/story.gif" width="600" style="border-radius: 8px; margin-top: 10px; margin-bottom: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);"/>
- 🎨 **20 Built-In Themes:** `dark_neon`, `tokyo_night`, `catppuccin_mocha`, `github_dark`, `rose_pine`, `everforest`, `dracula`, `synthwave`, `nord`, `gruvbox`, `solarized_dark`/`solarized_light`, `monokai`, `rdr2_gritty`, `blueprint`, `terminal`, `paper`, `high_contrast`, `minimal_light`, `cyberpunk`. Switch live in the sidebar. Plus three node styles (`card`, `tinted`, `outline`).
- ✅ **Built-in validation:** `generate.py` flags dangling edges, duplicate ids, overlapping boxes and unknown themes before you open the file.
- 💾 **State Persistence:** Checkable tasks for project trackers are saved directly to your browser's `localStorage`.
- 🧠 **Logos & 16 node kinds:** Inject product logos via simpleicons (auto-inverted on light themes, falls back to a kind icon if a URL is dead), or use built-in icons for `queue`, `gateway`, `cache`, `function`, `user`, `security`...
- 📦 **Single-file HTML:** No server, no npm, no build step. Fonts and GSAP load from CDNs; offline, pages still work with system fonts and without entry animations.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 📦 Install as an AI Agent Skill

Install VizCraft directly into your AI coding agent (Claude Code, Cursor, Antigravity, Copilot, Cline, Codex, etc.) with a single command:

```bash
# Install into your current workspace
npx skills add Kimanzi-Collins/vizcraft

# Or install globally across all your coding agents
npx skills add Kimanzi-Collins/vizcraft -g
```

Once installed, your agent automatically reads `SKILL.md` to design and generate architecture diagrams and progress trackers on demand.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## ⚡ Quick Start

### 1. Direct CLI Generation (No Git Clone Required)

Run directly using `npx`:

```bash
npx vizcraft <input.json> <output.html>
```

### 2. Python Setup

```bash
# 1. Clone the repo
git clone https://github.com/Kimanzi-Collins/vizcraft
cd vizcraft

# 2. Generate a visualization from JSON
python generate.py demos/demo_progress.json output/demo.html

# 3. Open output/demo.html in any browser!
```

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 🛠️ CLI Reference

The CLI auto-detects whether your JSON is an architecture map or a progress tracker based on its keys.

```bash
# Python
python generate.py <input.json> <output.html>

# Node / npx
npx vizcraft <input.json> <output.html>
```

| Flag | What it does |
|---|---|
| `--check` | Validate only; don't write HTML |
| `--strict` | Exit non-zero (and write nothing) if validation finds warnings |
| `--open`, `-o` | Open the result in your browser |
| `--template`, `-t` | Force `architecture` or `progress` |
| `--list-themes` | Print every theme id |
| `--quiet`, `-q` | Only print errors |

Tip: append `?theme=nord` to the HTML's URL to preview any theme without editing the JSON.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 🏗️ Architecture JSON Schema

See [`schemas/architecture.schema.json`](schemas/architecture.schema.json) for the full schema and [SKILL.md](SKILL.md) for guidance.

<details>
<summary><b>Click to expand Architecture Schema details</b></summary>
<br/>

- **Node kinds:** `entry`, `agent`, `service`, `store`, `external`, `model`, `cron`, `tool`, `queue`, `gateway`, `client`, `cache`, `function`, `user`, `monitor`, `security` (plus aliases like `database`, `lambda`, `llm`)
- **Node shapes:** `rect`, `pill`, `diamond`, `hexagon`, `cylinder`
- **Node extras:** `logo`, `description` and `tags` (hover tooltip)
- **Edges:** `label`, `style` (`solid`/`dashed`/`dotted`), `bidirectional`, `color`; ports (`top`/`bottom`/`left`/`right`) are optional hints, auto-picked if omitted
- **Layout:** omit `x`/`y` for auto-layout; `project.direction` is `LR` or `TB`
- **Project options:** `theme`, `edgeStyle`, `nodeStyle`, `direction`
- **Story steps:** `highlight` accepts node ids or group ids

</details>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 📅 Progress JSON Schema

See [`schemas/progress.schema.json`](schemas/progress.schema.json) for the full schema.

<details>
<summary><b>Click to expand Progress Schema details</b></summary>
<br/>

- **Phases:** Group your work into logical sprints or modules.
- **AI Tips:** Inject context-aware advice into the sidebar for each phase.
- **Deep Notes:** Notes support `**bold**`, `*italic*`, `` `code` `` and bullet lists, viewable in the sliding sidebar.
- **Task metadata:** optional `done`, `priority`, `owner`, `due` and `tags` render as chips. Task ids must be unique (they are the saved-progress keys).
- **Quality of life:** *Next up* shortcut, *Hide completed*, *Reset progress*.

</details>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 🤖 Using with AI Agents

VizCraft is natively packaged as an agent skill. You can install it into Claude Code, Cursor, Copilot, Antigravity, Cline, and other supported agents with:

```bash
npx skills add Kimanzi-Collins/vizcraft
```

Once added, the agent automatically ingests [SKILL.md](SKILL.md) to understand the layout schemas, theme options, SVG logo injection, and spatial reasoning rules needed to generate visualizations for your projects.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 🌟 Featured Demos

Open any of these from the `demos/` directory:
- **`uber_architecture`**: Uber's backend microservice map with hand-placed coordinates, real logos and a 5-step story.
- **`saas_platform`**: A grouped SaaS stack with **no coordinates**: auto-layout, new node kinds, curved edges, tinted nodes, Catppuccin theme.
- **`auth_flowchart`**: A login/MFA **flowchart** using diamonds, pills, a hexagon and a cylinder, top-to-bottom, Tokyo Night theme.
- **`demo_progress`** / **`uber_progress`**: Phased progress trackers.

---

## 📜 License

MIT License - Built by Kimanzi Collins. Feel free to use, fork, and build upon this!
