<div align="center">

**[English](README_EN.md)** | 简体中文

# Agent Skills Hub

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-orange.svg)](https://github.com/youzaiAGI/agent-skills-hub)

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

## 版本更新日志 (Release Notes)

### v1.1.0
- **新增 Trae 支持**：现在支持 Trae AI Agent 的技能管理
- **新增自定义仓库功能**：通过 `skill repo add` 和 `skill repo rm` 命令管理自定义技能仓库
- **优化命令行体验**：改进了命令行界面和交互逻辑
- **修复已知问题**：解决了一些同步和安装过程中的问题

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
| Trae | `.trae/skills` | `~/.trae/skills` |
| OpenCode | `.opencode/skills` | `~/.config/opencode/skills` |
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
# 输出: Agent Skills Hub v1.1.0
```

---

## 核心功能

### 交互式搜索

`skill search` 提供了一个直观的 TUI（终端用户界面）搜索功能，让你轻松发现和安装技能。

```bash
skill search
```
<img width="1722" height="916" alt="image" src="https://github.com/user-attachments/assets/a58165cf-7713-4a73-ac6e-e18ce9a6efd6" />

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

在 `~/.skill-hub/` 目录下创建 `skill_custom.list` 文件，每行添加一个自定义技能：

```
skill-name@owner/repo
another-skill@owner/repo
```
并手动**删除 `~/.skill-hub/skill.list` 文件**

当使用 `skill search` 命令时，系统会自动将自定义技能追加到主技能列表中，与官方技能一起搜索和管理。

---

### 交互式管理

`skill manage` 提供图形化的技能管理界面，统一管理已安装的技能和 Agent。

```bash
skill manage
```
<img width="1722" height="916" alt="image" src="https://github.com/user-attachments/assets/ce97c652-22d8-4c62-9983-39224c0ac1cc" />

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

每个技能会显示同步状态：

```
(project)  pdf -> pdf@anthropics/skills
(global)   skill-creator -> skill-creator@ComposioHQ/awesome-claude-skills
```

---

## 命令行工具

除了交互式界面，Agent Skills Hub 也提供了完整的命令行工具集。

### install - 安装技能

```bash
skill install [options] <target>

参数:
  target        要安装的目标 (格式: skill@repo 或 repo 或 txt文件路径)

选项:
  -u, --update  强制更新已安装的技能

示例:
  skill install pdf@anthropics/skills
  skill install -u pdf@anthropics/skills  # 强制更新
  skill install anthropics/skills     # 安装整个仓库
  skill install /path/skills.txt   # 每行是一个 skill@repo 或 repo，方便团队协作
```

### update - 更新技能

```bash
skill update <target>

示例:
  skill update pdf@anthropics/skills
  skill update anthropics/skills
```

### uninstall - 卸载技能

```bash
skill uninstall <target>

示例:
  skill uninstall pdf@anthropics/skills
  skill uninstall anthropics/skills
```

### list - 列出已安装技能

```bash
skill list
```

### search - 搜索技能

```bash
skill search [query]

参数:
  query        搜索关键词（可选）

示例:
  skill search                    # 打开交互式搜索界面
  skill search python            # 直接搜索包含 'python' 的技能
  skill search web               # 直接搜索包含 'web' 的技能
```

### sync - 同步技能到 Agent

```bash
skill sync <agent_name> <target> [options]

参数:
  agent_name    Agent 名称（如 ClaudeCode、Cursor 等）
  target        要同步的目标 (格式: skill@repo 或 repo 或 文件)

选项:
  -p, --project          同步到项目级别
  -g, --global           同步到全局级别
  -f, --force            强制同步（覆盖已存在的技能）

示例:
  skill sync ClaudeCode pdf@anthropics/skills -p # 同步到 .cursor/skills
  skill sync Cursor pdf@anthropics/skills -g -f # 同步到 ~/.cursor/skills
  skill sync Cursor /path/skills.txt    # 文件每行是一个 skill@repo 或 repo

```

### repo - 管理自定义仓库

```bash
skill repo {add,rm}

子命令:
  add        添加自定义仓库
  rm         删除自定义仓库

示例:
  skill repo add youzaiAGI/agent-skills-hub     # 添加自定义仓库
  skill repo add https://github.com/youzaiAGI/agent-skills-hub  # 也可以使用完整URL
  skill repo rm youzaiAGI/agent-skills-hub      # 删除自定义仓库
  skill repo                                    # 显示帮助信息
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
