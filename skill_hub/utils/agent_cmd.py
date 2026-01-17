import json
import os

config_data = {
  "ClaudeCode": [
    ".claude/skills",
    "~/.claude/skills"
  ],
  "Gemini": [
    ".gemini/skills",
    "~/.gemini/skills"
  ],
  "Codex": [
    ".codex/skills",
    "~/.codex/skills"
  ],
  "OpenCode": [
    ".opencode/skill",
    "~/.config/opencode/skill"
  ],
  "Cursor": [
    ".cursor/skills",
    "~/.cursor/skills"
  ],
  "Antigravity": [
    ".agent/skills",
    "~/.gemini/antigravity/skills"
  ],
  "Windsurf": [
    ".windsurf/skills",
    "~/.codeium/windsurf/skills"
  ],
  "Amp": [
    ".agents/skills",
    "~/.config/agents/skills"
  ],
  "Qwen": [
    ".qwen/skills",
    "~/.qwen/skills"
  ],
  "Qoder": [
    ".qoder/skills",
    "~/.qoder/skills"
  ],
  "KiloCode": [
    ".kilocode/skills",
    "~/.kilocode/skills"
  ],
  "RooCode": [
    ".roo/skills",
    "~/.roo/skills"
  ],
  "Goose": [
    ".goose/skills",
    "~/.config/goose/skills"
  ]
}

def get_agent_config(config_data):
    agent_path_config = {}

    """获取IDE的配置信息"""
    for key, value in config_data.items():
        if not isinstance(value, list) or len(value) != 2:
            continue

        full_project_skill_path = os.path.join(os.getcwd(), value[0])
        # 检查用户目录路径是否存在 (将 ~ 替换为实际的用户主目录)
        full_user_skill_path = os.path.expanduser(value[1])
        
        agent_path_config[key] = {
            "project_path": full_project_skill_path,
            "project_exists": os.path.exists(full_project_skill_path.rsplit('/', 1)[0]),
            "global_path": full_user_skill_path ,
            "global_exists": os.path.exists(full_user_skill_path.rsplit('/', 1)[0])
        }

    return agent_path_config

def get_installed_agents():
    """检查IDE是否安装，以及安装了哪些"""
    installed_ide = []
    for ide, config in get_agent_config(config_data=config_data).items():
        if config["project_exists"] or config["global_exists"]:
            installed_ide.append(ide)
    
    return installed_ide

def get_project_installed_agents():
    """检查项目是否安装，以及安装了哪些"""
    return [key for key, value in get_agent_config(config_data=config_data).items() if value["project_exists"]]

def get_project_installed_agent_paths():
    """获取项目安装的技能路径"""
    return [value["project_path"] for key, value in get_agent_config(config_data=config_data).items() if value["project_exists"]]

def get_global_installed_agents():
    """检查全局是否安装，以及安装了哪些"""
    return [key for key, value in get_agent_config(config_data=config_data).items() if value["global_exists"]]

def get_global_installed_agent_paths():
    """获取全局安装的技能路径"""
    return [value["global_path"] for key, value in get_agent_config(config_data=config_data).items() if value["global_exists"]]

def get_config_for_agent(agent_name):
    return get_agent_config(config_data=config_data).get(agent_name, {})

# 使用示例
if __name__ == "__main__":
    # installed = check_ide_installation()
    # if installed:
    #     print("已安装的IDE:")
    #     for ide in installed:
    #         print(f"- {ide}")
    # else:
    #     print("未检测到任何IDE安装")
    print("Installed Agents:", get_installed_agents())
    print("Project Installed Agents:", get_project_installed_agents())
    print("Project Installed Agent Paths:", get_project_installed_agent_paths())
    print("Global Installed Agents:", get_global_installed_agents())
    print("Global Installed Agent Paths:", get_global_installed_agent_paths())
    print("Config for ClaudeCode:", get_config_for_agent("ClaudeCode"))
