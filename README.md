
<div align="center">

**[English](README_EN.md)** | **[简体中文](README.md)**

# Agent Skills Hub

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.6.10-orange.svg)](https://github.com/youzaiAGI/agent-skills-hub)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/youzaiAGI/agent-skills-hub)

**AI Agent 技能包统一管理工具**



</div>

---

## 概述

Agent Skills Hub 是一个统一的技能包管理系统，让你可以轻松地安装、管理和同步技能包到不同的 AI Agents（如 Claude、Cursor、Windsurf 等）。

### 核心特性

- **统一管理**：一个工具管理多个 AI Agents 的技能包
- **交互式搜索**：通过交互式界面发现新技能
- **灵活同步**：支持项目级和全局技能同步
- **广泛支持**：支持 Claude、Cursor、Windsurf、Gemini、Antigravity、Codex、Trae、OpenCode、GitHubCopilot、CodeBuddy、Factory、Amp、Qwen、Qoder、KiloCode、RooCode、Goose、Kimi 等 18+ AI Agents
- **跨平台**：支持 Windows、Linux 和 macOS

---

## 更新日志

### v1.6.10
- **新增 OpenClaw 支持**：完整支持 OpenClaw AI Agent 的技能管理
- **版本升级**：基础版本编号调整至 1.6.x

### v1.5.1
- **新增 Windows 支持**：完全兼容 Windows 系统，支持 Windows 终端和路径处理
- **优化路径处理**：使用 pathlib 跨平台路径处理，修复 Windows 路径分隔符问题
- **改进同步机制**：Windows 上自动降级软链接为目录复制，无需管理员权限

### v1.5.0
- **新增跨项目技能管理**：支持导出/导入技能列表，实现类似 `pip install -r requirements.txt` 的批量管理体验
- **精选热门技能仓库**：从 40 个热门 GitHub 仓库精选 240+ 技能，涵盖编程、写作、数据分析等领域
- **新增更多 Agent 支持**：现已支持 Claude、Cursor、Windsurf、Gemini、Antigravity、Codex、Trae、OpenCode、GitHubCopilot、CodeBuddy、Factory、Amp、Qwen、Qoder、KiloCode、RooCode、Goose、Kimi 等 18+ AI Agents

### v1.1.0
- **新增 Trae 支持**：现在支持 Trae AI Agent 的技能管理
- **新增自定义仓库功能**：通过 `skill repo add` 和 `skill repo rm` 命令管理自定义技能仓库
- **改进命令行体验**：增强命令行界面和交互逻辑
- **修复已知问题**：解决同步和安装过程中的一些问题

---

## 支持的 Agents

Agent Skills Hub 支持以下 AI Agents：

| Agent | 项目路径 | 全局路径 |
|-------|--------------|-------------|
| ClaudeCode | `.claude/skills` | `~/.claude/skills` |
| Gemini | `.gemini/skills` | `~/.gemini/skills` |
| Codex | `.codex/skills` | `~/.codex/skills` |
| OpenClaw | `.openclaw/skills` | `~/.openclaw/skills` |
| OpenCode | `.opencode/skill` | `~/.config/opencode/skill` |
| Cursor | `.cursor/skills` | `~/.cursor/skills` |
| Antigravity | `.agent/skills` | `~/.gemini/antigravity/skills` |
| Trae | `.trae/skills` | `~/.trae/skills` |
| Windsurf | `.windsurf/skills` | `~/.codeium/windsurf/skills` |
| GitHubCopilot | `.github/skills` | `~/.copilot/skills` |
| CodeBuddy | `.codebuddy/skills` | `~/.codebuddy/skills` |
| Factory | `.factory/skills` | `~/.factory/skills` |
| Amp | `.agents/skills` | `~/.config/agents/skills` |
| Qwen | `.qwen/skills` | `~/.qwen/skills` |
| Qoder | `.qoder/skills` | `~/.qoder/skills` |
| KiloCode | `.kilocode/skills` | `~/.kilocode/skills` |
| RooCode | `.roo/skills` | `~/.roo/skills` |
| Goose | `.goose/skills` | `~/.config/goose/skills` |
| Kimi | `.kimi/skills` | `~/.kimi/skills` |

---

## 安装

### 通过 pip 安装

```bash
pip install agent-skills-hub
```

### 从源码安装

#### Windows

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
python -m venv venv
venv\Scripts\activate
pip install -e .
```

#### Linux / macOS

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
python -m venv venv
source venv/bin/activate
pip install -e .
```

### 验证安装

```bash
skill --version
# 输出: Agent Skills Hub v1.6.10
```

---

## 核心功能

### 交互式搜索

`skill search` 提供直观的 TUI（终端用户界面）搜索功能，方便发现和安装技能。

```bash
skill search
```

#### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `←` `→` | 切换 Skill/Repo 标签页 |
| 字母键 | 实时搜索过滤 |
| `↑` `↓` | 移动光标选择 |
| `Page Up` / `Page Down` | 翻页导航 |
| `Enter` | 查看详情并安装/同步 |
| `ESC` | 退出 |

#### 安装选项

进入技能详情后，可以选择以下操作：

| 选项 | 说明 |
|------|------|
| 查看 SKILL.md | 在线浏览技能文档 |
| 仅安装到 ~/.skill-hub | 仅下载技能到本地缓存 |
| 安装并同步到项目 | 安装并选择 Agent 同步到项目 |
| 安装并同步到全局 | 安装并选择 Agent 同步到全局 |

---

### 交互式管理

`skill manage` 提供图形化的技能管理界面，统一管理已安装的技能和 Agents。

```bash
skill manage
```

#### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `←` `→` | 切换标签页 (Skill-Hub / Agent) |
| 字母键 | 实时搜索过滤 |
| `↑` `↓` | 移动光标选择 |
| `Enter` | 进入技能详情 |
| `ESC` | 退出 |

#### 标签页结构

| 标签 | 功能 | 数据源 |
|-----|------|--------|
| **Skill-Hub** | ~/.skill-hub 中所有技能 | `~/.skill-hub` |
| **ClaudeCode** | 同步到 ClaudeCode 的技能 | `.claude/skills` `~/.claude/skills` |
| **Cursor** | 同步到 Cursor 的技能 | `.cursor/skills` `~/.cursor/skills` |
| ... | 其他已安装的 Agents | - |

#### Skill-Hub 标签页操作

进入技能后，可以执行以下操作：

| 选项 | 说明 |
|------|------|
| 查看 SKILL.md | 预览本地技能文档文件 |
| 更新技能 | 调用更新命令更新技能 |
| 删除技能 | 调用卸载命令删除（需确认） |
| 同步到项目 | 选择 Agents 同步到项目级（默认选中当前项目 Agents） |
| 同步到全局 | 选择 Agents 同步到全局（默认选中全局 Agents） |

#### Agent 标签页操作

进入技能后，可以执行以下操作：

| 选项 | 说明 |
|------|------|
| 查看 SKILL.md | 预览 Agent 目录中的技能文档 |
| 删除技能 | 移除软链接或目录（需确认） |

#### Agent 标签页列表格式

每个技能显示其同步级别：

```
(project)  python-tools
(project)  python-tools -> python-tools@anthropic/python-tools
(global)   git-workflow
(global)   git-workflow -> git-workflow@anthropic/git-workflow
```

### 跨项目技能管理

v1.5.0 引入跨项目技能管理，让你可以像 `pip install -r requirements.txt` 一样管理 AI Agent 技能！

#### 导出当前项目技能列表

```bash
skill list > skills.txt
```

这会生成一个包含所有已安装技能的列表文件，格式如下：

```
skill-name@repo-owner/repo-name
another-skill@repo-owner/repo-name
...
```

#### 从技能列表批量安装

```bash
skill install skills.txt
```

这会一次性安装列表中的所有技能，非常适合团队协作和项目迁移。

#### 批量同步到指定 Agent

```bash
skill sync ClaudeCode skills.txt -p
```

这会将列表中的所有技能同步到指定 Agent 的项目级目录（如 ClaudeCode）。

#### 完整工作流示例

1. 导出项目 A 的技能：
   ```bash
   skill list > skills.txt
   ```

2. 将 skills.txt 复制到项目 B

3. 在项目 B 中安装技能：
   ```bash
   skill install skills.txt
   ```

4. 同步到指定 Agent：
   ```bash
   skill sync ClaudeCode skills.txt -p  # 同步到项目级
   skill sync ClaudeCode skills.txt -g  # 同步到全局
   ```

这个功能让团队成员之间共享技能配置变得异常简单，就像 Python 的 requirements.txt 一样！

---

## 命令行工具

除了交互式界面，Agent Skills Hub 还提供完整的命令行工具集。

### install - 安装技能

```bash
skill install [options] <target>

参数:
  target        要安装的目标 (格式: skill@repo 或 repo 或 txt 文件路径)

选项:
  -u, --update  强制更新已安装的技能

示例:
  skill install web-debugger@anthropic/tools
  skill install -u web-debugger@anthropic/tools  # 强制更新
  skill install anthropic/python-tools            # 安装整个仓库
  skill install /path/skills.txt   # 每行为 skill@repo 或 repo，方便团队协作
```

> **提示**: 你可以使用 `skill list > skills.txt` 生成技能列表文件，然后使用 `skill install skills.txt` 批量安装技能，就像 Python 中的 `pip install -r requirements.txt` 一样方便！

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

### search - 搜索技能

```bash
skill search [query]

参数:
  query        搜索关键词 (可选)

示例:
  skill search                    # 打开交互式搜索界面
  skill search python            # 直接搜索包含 'python' 的技能
  skill search web               # 直接搜索包含 'web' 的技能
```

### sync - 同步技能到 Agent

```bash
skill sync <agent_name> <target> [options]

参数:
  agent_name    Agent 名称 (如 ClaudeCode, Cursor 等)
  target        要同步的目标 (格式: skill@repo 或 repo 或文件)

选项:
  -p, --project          同步到项目级
  -g, --global           同步到全局
  -f, --force            强制同步 (覆盖已存在的技能)

示例:
  skill sync ClaudeCode web-debugger@anthropic/tools -p
  skill sync Cursor python-tools@anthropic/python-tools -g -f
  skill sync Cursor /path/skills.txt    # 每行为 skill@repo 或 repo
```

> **提示**: 配合 `skill list > skills.txt`，可以实现跨项目技能同步，像 `pip install -r requirements.txt` 一样批量处理技能！

### repo - 管理自定义仓库

```bash
skill repo {add,rm}

子命令:
  add        添加自定义仓库
  rm         删除自定义仓库

示例:
  skill repo add youzaiAGI/agent-skills-hub     # 添加自定义仓库
  skill repo add https://github.com/youzaiAGI/agent-skills-hub  # 也支持完整 URL
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
    │   └── SKILL.md          # 技能描述文件 (必需)
    ├── skill-b/
    │   └── SKILL.md
    └── skill-c/
        └── SKILL.md
```

**注意**: 每个技能目录必须包含 `SKILL.md` 文件才能被识别为有效技能。

---

## 开发指南

### 环境设置

#### Windows

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
python -m venv venv
venv\Scripts\activate
pip install -e .
```

#### Linux / macOS

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
python -m venv venv
source venv/bin/activate
pip install -e .
```

### 添加新 Agent 支持

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

本项目基于 [MIT 许可证](LICENSE) 开源。

---

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=youzaiAGI/agent-skills-hub&type=Date)](https://star-history.com/#youzaiAGI/agent-skills-hub&Date)

---

## 联系方式

- 作者: youzaiAGI
- 邮箱: youzaiagi@gmail.com
- 项目主页: https://github.com/youzaiAGI/agent-skills-hub



<div align="center">

**如果这个项目对你有帮助，请给它一个 Star ⭐**

</div>
