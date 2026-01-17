<div align="center">

English | **[简体中文](README.md)**

# Agent Skills Hub

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.1-orange.svg)](https://github.com/youzaiAGI/agent-skills-hub)

**A unified CLI tool for managing AI Agent skill packages**


</div>

---

## Overview

Agent Skills Hub is a unified skill package management system that allows you to easily install, manage, and sync skill packages across different AI Agents (such as Claude, Cursor, Windsurf, etc.).

### Key Features

- **Unified Management**: Manage skill packages for multiple AI Agents with one tool
- **Interactive Search**: Interactive search interface for discovering new skills
- **Flexible Sync**: Support for both project-level and global skill synchronization
- **Broad Support**: Supports 13+ AI Agents including Claude, Cursor, Windsurf, Gemini, and more

---

## Supported Agents

Agent Skills Hub supports the following AI Agents:

| Agent | Project Path | Global Path |
|-------|--------------|-------------|
| ClaudeCode | `.claude/skills` | `~/.claude/skills` |
| Cursor | `.cursor/skills` | `~/.cursor/skills` |
| Windsurf | `.windsurf/skills` | `~/.codeium/windsurf/skills` |
| Gemini | `.gemini/skills` | `~/.gemini/skills` |
| Antigravity | `.agent/skills` | `~/.gemini/antigravity/skills` |
| Codex | `.codex/skills` | `~/.codex/skills` |
| OpenCode | `.opencode/skill` | `~/.config/opencode/skill` |
| Amp | `.agents/skills` | `~/.config/agents/skills` |
| Qwen | `.qwen/skills` | `~/.qwen/skills` |
| Qoder | `.qoder/skills` | `~/.qoder/skills` |
| KiloCode | `.kilocode/skills` | `~/.kilocode/skills` |
| RooCode | `.roo/skills` | `~/.roo/skills` |
| Goose | `.goose/skills` | `~/.config/goose/skills` |

---

## Installation

### Install via pip

```bash
pip install agent-skills-hub
```

### Install from source

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
pip install -e .
```

### Verify installation

```bash
skill --version
# Output: Skill Hub v1.0.2
```

---

## Core Features

### Interactive Search

`skill search` provides an intuitive TUI (Terminal User Interface) search function for easily discovering and installing skills.

```bash
skill search
```

#### Key Bindings

| Shortcut | Function |
|----------|----------|
| `←` `→` | Switch between Skill/Repo tabs |
| Letters | Real-time search filtering |
| `↑` `↓` | Move cursor selection |
| `Page Up` / `Page Down` | Navigate pages |
| `Enter` | View details and install/sync |
| `ESC` | Exit |

#### Installation Options

After entering skill details, you can choose from the following actions:

| Option | Description |
|--------|-------------|
| View SKILL.md | Browse skill documentation online |
| Install only to ~/.skill-hub | Download skills to local cache only |
| Install and sync to project | Install and select Agent to sync to project |
| Install and sync to global | Install and select Agent to sync to global |

---

### Interactive Management

`skill manage` provides a graphical skill management interface for unified management of installed skills and Agents.

```bash
skill manage
```

#### Key Bindings

| Shortcut | Function |
|----------|----------|
| `←` `→` | Switch tabs (Skill-Hub / Agent) |
| Letters | Real-time search filtering |
| `↑` `↓` | Move cursor selection |
| `Enter` | Enter skill details |
| `ESC` | Exit |

#### Tab Structure

| Tab | Function | Data Source |
|-----|----------|-------------|
| **Skill-Hub** | All skills in ~/.skill-hub | `~/.skill-hub` |
| **ClaudeCode** | Skills synced to ClaudeCode | `.claude/skills` `~/.claude/skills` |
| **Cursor** | Skills synced to Cursor | `.cursor/skills` `~/.cursor/skills` |
| ... | Other installed Agents | - |

#### Skill-Hub Tab Actions

After entering a skill, you can perform the following actions:

| Option | Description |
|--------|-------------|
| View SKILL.md | Preview local skill documentation file |
| Update skill | Call update command to update the skill |
| Delete skill | Call uninstall command to delete (requires confirmation) |
| Sync to project | Select Agents to sync to project level (current project Agents selected by default) |
| Sync to global | Select Agents to sync to global (global Agents selected by default) |

#### Agent Tab Actions

After entering a skill, you can perform the following actions:

| Option | Description |
|--------|-------------|
| View SKILL.md | Preview skill documentation in Agent directory |
| Delete skill | Remove symlink or directory (requires confirmation) |

#### Agent Tab List Format

Each skill displays its sync level:

```
(project)  python-tools
(project)  python-tools -> python-tools@anthropic/python-tools
(global)   git-workflow
(global)   git-workflow -> git-workflow@anthropic/git-workflow
```

---

## Command Line Tools

In addition to the interactive interface, Agent Skills Hub provides a complete set of command line tools.

### install - Install skill

```bash
skill install [options] <target>

Parameters:
  target        Target to install (format: skill@repo or repo)

Options:
  -u, --update  Force update installed skills

Examples:
  skill install web-debugger@anthropic/tools
  skill install -u web-debugger@anthropic/tools  # Force update
  skill install anthropic/python-tools            # Install entire repo
```

### update - Update skill

```bash
skill update <target>

Examples:
  skill update web-debugger@anthropic/tools
  skill update anthropic/python-tools
```

### uninstall - Uninstall skill

```bash
skill uninstall <target>

Examples:
  skill uninstall web-debugger@anthropic/tools
  skill uninstall anthropic/python-tools
```

### list - List installed skills

```bash
skill list
```

### sync - Sync skill to Agent

```bash
skill sync <agent_name> <target> [options]

Parameters:
  agent_name    Agent name (e.g., ClaudeCode, Cursor, etc.)
  target        Target to sync (format: skill@repo or repo)

Options:
  -p, --project          Sync to project level
  -g, --global           Sync to global level
  -f, --force            Force sync (overwrite existing skills)

Examples:
  skill sync ClaudeCode web-debugger@anthropic/tools -p
  skill sync Cursor python-tools@anthropic/python-tools -g -f
```

---

## Skill Format

The standard format for a skill repository:

```
owner/
└── repo-name/
    ├── skill-a/
    │   └── SKILL.md          # Skill description file (required)
    ├── skill-b/
    │   └── SKILL.md
    └── skill-c/
        └── SKILL.md
```

**Note**: Each skill directory must contain a `SKILL.md` file to be recognized as a valid skill.

---

## Development Guide

### Environment Setup

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### Adding New Agent Support

Edit `skill_hub/utils/agent_cmd.py` and add new Agent configuration in `config_data`:

```python
config_data = {
    # ... other configs
    "NewAgent": [
        ".newagent/skills",
        "~/.newagent/skills"
    ],
}
```

---

## License

This project is open source under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=youzaiAGI/agent-skills-hub&type=Date)](https://star-history.com/#youzaiAGI/agent-skills-hub&Date)

---

## Contact

- Author: youzaiAGI
- Email: youzaiagi@gmail.com
- Project homepage: https://github.com/youzaiAGI/agent-skills-hub


<div align="center">

**If this project helps you, please give it a Star ⭐**

</div>
