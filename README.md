<div align="center">

**[English](README_EN.md)** | 简体中文

# Agent Skills Hub

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.1-orange.svg)](https://github.com/youzaiAGI/agent-skills-hub)

**一个用于管理 AI Agent 技能包的统一命令行工具**


</div>

---

## 简介

Agent Skills Hub 是一个统一的技能包管理系统，让你能够轻松地在不同的 AI Agent（如 Claude、Cursor、Windsurf 等）之间安装、管理和同步技能包。

### 主要特性

- **统一管理**：一个工具管理多个 AI Agent 的技能包
- **在线搜索**：交互式搜索界面，轻松发现新技能
- **灵活同步**：支持项目级和全局级技能同步
- **广泛支持**：支持 Claude、Cursor、Windsurf、Gemini 等 13+ 种 AI Agent

---

## 支持的 Agent

Agent Skills Hub 支持以下 AI Agent：

| Agent | 项目路径 | 全局路径 |
|-------|----------|----------|
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

## 安装

### 使用 pip 安装

```bash
pip install agent-skills-hub
```

### 从源码安装

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
pip install -e .
```

### 验证安装

```bash
skill --version
# 输出: Skill Hub v1.0.2
```

---

## 核心功能

### 交互式搜索

`skill search` 提供了一个直观的 TUI（终端用户界面）搜索功能，让你轻松发现和安装技能。

```bash
skill search
```

#### 功能说明

| 快捷键 | 功能 |
|--------|------|
| `←` `→` | 切换 Skill/Repo 标签页 |
| 字母 | 实时搜索过滤 |
| `↑` `↓` | 移动光标选择 |
| `Page Up` / `Page Down` | 翻页 |
| `Enter` | 查看详情并选择安装/同步 |
| `ESC` | 退出 |

#### 安装选项

进入技能详情后，可选择以下操作：

| 选项 | 说明 |
|------|------|
| 查看 SKILL.md | 在线浏览技能文档 |
| 仅安装到 ~/.skill-hub | 仅下载技能到本地缓存 |
| 安装并同步到项目 | 安装并选择 Agent 同步到项目 |
| 安装并同步到全局 | 安装并选择 Agent 同步到全局 |

#### 自定义技能支持

Agent Skills Hub 支持自定义技能列表扩展，允许用户添加自己的技能源。

##### 自定义技能文件

在 `~/.skill-hub/` 目录下创建 `skill_custom.list` 文件，每行添加一个自定义技能：

```
skill-name@owner/repo
another-skill@owner/repo
```
并手动删除 `~/.skill-hub/skill.list` 文件

当使用 `skill search` 或其他命令时，系统会自动将自定义技能追加到主技能列表中，与官方技能一起搜索和管理。

---

### 交互式管理

`skill manage` 提供图形化的技能管理界面，统一管理已安装的技能和 Agent。

```bash
skill manage
```

#### 功能说明

| 快捷键 | 功能 |
|--------|------|
| `←` `→` | 切换标签页（Skill-Hub / Agent） |
| 字母 | 实时搜索过滤 |
| `↑` `↓` | 移动光标选择 |
| `Enter` | 进入技能详情 |
| `ESC` | 退出 |

#### 标签页结构

| Tab | 功能 | 数据来源 |
|-----|------|----------|
| **Skill-Hub** | ~/.skill-hub 中的所有技能 | `~/.skill-hub` |
| **ClaudeCode** | ClaudeCode 已同步的技能 | `.claude/skills` `~/.claude/skills` |
| **Cursor** | Cursor 已同步的技能 | `.cursor/skills` `~/.cursor/skills` |
| ... | 其他已安装的 Agent | - |

#### Skill-Hub Tab 详情操作

进入某个技能后，可进行以下操作：

| 选项 | 说明 |
|------|------|
| 查看 SKILL.md | 预览本地的技能文档文件 |
| 更新 skill | 调用 update 命令更新技能 |
| 删除 skill | 调用 uninstall 命令删除（需二次确认） |
| 同步到项目 | 选择 Agent 同步到项目级（默认选中当前项目 Agent） |
| 同步到全局 | 选择 Agent 同步到全局（默认选中全局 Agent） |

#### Agent Tab 详情操作

进入某个技能后，可进行以下操作：

| 选项 | 说明 |
|------|------|
| 查看 SKILL.md | 预览 Agent 目录下的技能文档 |
| 删除 skill | 删除软链接或目录（需二次确认） |

#### Agent Tab 列表格式

每个技能会显示同步级别：

```
(project)  python-tools
(project)  python-tools -> python-tools@anthropic/python-tools
(global)   git-workflow
(global)   git-workflow -> git-workflow@anthropic/git-workflow
```

---

## 命令行工具

除了交互式界面，Agent Skills Hub 也提供了完整的命令行工具集。

### install - 安装技能

```bash
skill install [options] <target>

参数:
  target        要安装的目标 (格式: skill@repo 或 repo)

选项:
  -u, --update  强制更新已安装的技能

示例:
  skill install web-debugger@anthropic/tools
  skill install -u web-debugger@anthropic/tools  # 强制更新
  skill install anthropic/python-tools            # 安装整个仓库
```

### update - 更新技能

```bash
skill update <target>

示例:
  skill update web-debugger@anthropic/tools
  skill update anthropic/python-tools
```

### uninstall - 卸载技能

```bash
skill uninstall <target>

示例:
  skill uninstall web-debugger@anthropic/tools
  skill uninstall anthropic/python-tools
```

### list - 列出已安装技能

```bash
skill list
```

### sync - 同步技能到 Agent

```bash
skill sync <agent_name> <target> [options]

参数:
  agent_name    Agent 名称（如 ClaudeCode、Cursor 等）
  target        要同步的目标 (格式: skill@repo 或 repo)

选项:
  -p, --project          同步到项目级别
  -g, --global           同步到全局级别
  -f, --force            强制同步（覆盖已存在的技能）

示例:
  skill sync ClaudeCode web-debugger@anthropic/tools -p
  skill sync Cursor python-tools@anthropic/python-tools -g -f
```

---

## 技能格式

技能仓库的标准格式：

```
owner/
└── repo-name/
    ├── skill-a/
    │   └── SKILL.md          # 技能描述文件（必需）
    ├── skill-b/
    │   └── SKILL.md
    └── skill-c/
        └── SKILL.md
```

**注意**：每个技能目录必须包含 `SKILL.md` 文件才能被识别为有效技能。

---

## 开发指南

### 环境设置

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### 添加新的 Agent 支持

编辑 `skill_hub/utils/agent_cmd.py`，在 `config_data` 中添加新的 Agent 配置：

```python
config_data = {
    # ... 其他配置
    "NewAgent": [
        ".newagent/skills",
        "~/.newagent/skills"
    ],
}
```

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源。

---

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=youzaiAGI/agent-skills-hub&type=Date)](https://star-history.com/#youzaiAGI/agent-skills-hub&Date)

---

## 联系方式

- 作者：youzaiAGI
- 邮箱：youzaiagi@gmail.com
- 项目主页：https://github.com/youzaiAGI/agent-skills-hub


<div align="center">

**如果这个项目对你有帮助，请给个 Star ⭐**

</div>
