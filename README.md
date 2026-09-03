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

### 🚀 Two Visualization Types

1. 🌐 **Architecture Maps:** Codebase maps, system diagrams, microservice graphs.
2. 📈 **Progress Trackers:** Sprint boards, phased roadmaps, Kanban trackers.

### ⚡ Core Features

- 💎 **Intelligent Layout Engine:** Automatically organized group boxes, node chips, and fluid curved edges.
- ✨ **Animated Data-flow Particles:** Visual routing particles that flow smoothly along exact bezier curves.
- 📖 **Story Mode:** Sliding sidebar with a step-by-step walkthrough highlighting specific nodes of your architecture.
  <br/><img src="https://raw.githubusercontent.com/Kimanzi-Collins/vizcraft/main/assets/story.gif" width="600" style="border-radius: 8px; margin-top: 10px; margin-bottom: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);"/>
- 🎨 **10 Built-In Themes:** From `dark_neon` to `cyberpunk`, `dracula`, `nord`, and `minimal_light` - switchable dynamically at runtime.
- 💾 **State Persistence:** Checkable tasks for project trackers are saved directly to your browser's `localStorage`.
- 🧠 **Native SVG Logos:** Fully supports injecting official product SVG logos (via simpleicons) directly into architecture nodes.
- 📦 **100% Self-Contained HTML:** No server, no npm, no build step.

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

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 🏗️ Architecture JSON Schema

See `schemas/architecture.schema.json` for the full schema.

<details>
<summary><b>Click to expand Architecture Schema details</b></summary>
<br/>

- **Node kinds:** `entry`, `agent`, `service`, `store`, `external`, `model`, `cron`, `tool`
- **Node Logos:** Specify an SVG URL using the `logo` key to render exact product logos on your nodes.
- **Edge ports:** `top`, `bottom`, `left`, `right` *(auto-detected if omitted)*
- **Story steps:** Create step-by-step interactive walkthroughs by defining an array of steps highlighting specific nodes.

</details>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 📅 Progress JSON Schema

See `schemas/progress.schema.json` for the full schema.

<details>
<summary><b>Click to expand Progress Schema details</b></summary>
<br/>

- **Phases:** Group your work into logical sprints or modules.
- **AI Tips:** Inject context-aware advice into the sidebar for each phase.
- **Deep Notes:** Write multi-paragraph markdown notes for individual tasks, viewable in the sliding sidebar.

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

We have included a detailed real-world visualization in the `demos/` directory:
- **`demos/uber_architecture.html` / `demos/uber_architecture.json`**: A comprehensive interactive map of the Uber backend microservice architecture (featuring real logos for tools like Node, Go, HAProxy, Kafka, and Cassandra).

---

## 📜 License

MIT License - Built by Kimanzi Collins. Feel free to use, fork, and build upon this!
