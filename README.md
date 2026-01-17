<div align="center">

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
# 输出: Skill Hub v1.0.0
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
| **ClaudeCode** | ClaudeCode 已同步的技能 | `.claude_code/skills` `~/.claude_code/skills` |
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

输出示例：

```
# Skill Hub 中的所有技能 (~/.skill-hub)
python-tools@anthropic/python-tools
git-workflow@anthropic/git-workflow

# 当前项目中已同步的技能 (/path/to/project)
python-tools@anthropic/python-tools

# 全局已同步的技能 (~/.claude/skills)
git-workflow@anthropic/git-workflow
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

## 目录结构

```
~/.skill-hub/              # 技能缓存目录
└── owner/
    └── repo-name/
        ├── skill-a/
        │   └── SKILL.md
        └── skill-b/
            └── SKILL.md

<project>/.claude/skills/  # 项目级技能（软链接）
├── skill-a -> ~/.skill-hub/owner/repo-name/skill-a/
└── skill-b -> ~/.skill-hub/owner/repo-name/skill-b/

~/.claude/skills/          # 全局级技能（软链接）
└── skill-c -> ~/.skill-hub/owner/repo-name/skill-c/
```

---

## 开发指南

### 环境设置

```bash
# clone 仓库
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
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

### 运行测试

```bash
# 使用模块方式运行
python -m skill_hub <command>

# 或使用安装的命令
skill <command>
```

---

## 配置文件

技能列表和仓库排序文件会在首次运行时自动下载到 `~/.skill-hub/` 目录：

- `~/.skill-hub/skill.list` - 可用技能列表
- `~/.skill-hub/repo.sort` - 仓库排序列表

这些文件会自动每 24 小时更新一次。

---

## 常见问题

### Q: 如何查看某个技能的详细信息？

A: 使用 `skill search` 命令进入交互式界面，选择技能后按 Enter，然后选择"查看 SKILL.md"。

### Q: 同步失败怎么办？

A: 检查以下几点：
1. 目标 Agent 的目录是否存在
2. 确保使用 `-p` 或 `-g` 指定同步级别
3. 使用 `-f` 参数强制覆盖已存在的技能

### Q: 支持从本地文件批量安装吗？

A: 支持。创建一个包含目标列表的文件（每行一个），然后：

```bash
skill install skills.txt
```

文件格式示例：
```
web-debugger@anthropic/tools
python-tools@anthropic/python-tools
```

### Q: 如何同步到多个 Agent？

A: 逐个同步，或在 `skill search` 交互界面中选择"安装并同步"时，会显示多选菜单让你选择多个 Agent。

---

## 版本历史

### v1.0.1
- 添加自动换行显示长输出
- 改进同步输出格式
- 优化搜索界面交互

### v1.0.0
- 初始版本发布
- 支持基本的安装、卸载、搜索、同步功能

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源。

---

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 联系方式

- 作者：youzaiAGI
- 邮箱：youzaiagi@gmail.com
- 项目主页：https://github.com/youzaiAGI/agent-skills-hub

---

## 致谢

感谢所有使用和贡献本项目的开发者！

<div align="center">

**如果这个项目对你有帮助，请给个 Star ⭐**

</div>
