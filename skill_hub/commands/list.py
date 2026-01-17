"""
列出已安装技能命令模块
"""

import os
from pathlib import Path
from skill_hub.utils.agent_cmd import get_project_installed_agent_paths, get_global_installed_agent_paths
from ..utils.agent_cmd import get_config_for_agent


def list_skills():
    """列出当前已经安装的skill"""
    skill_hub_skills = get_skill_hub_skills()
    project_skills = get_project_skills()
    global_skills = get_global_skills()
    
    if skill_hub_skills:
        print_section("# Skill Hub 中的所有技能 (~/.skill-hub)", skill_hub_skills)
    
    if project_skills:
        print_section(f"# 当前项目中已同步的技能 ({os.getcwd()})", project_skills)
    else:
        print(f"# 当前项目暂无技能同步 ({os.getcwd()})")
        print()  # 添加空行分隔
        
    global_path = os.path.expanduser("~/")
    if global_skills:
        print_section(f"# 全局已同步的技能 ({global_path})", global_skills)  
    else:
        print(f"# 全局暂无技能同步 ({global_path})")
        print()  # 添加空行分隔


def get_skill_hub_skills():
    """获取 Skill Hub 中的所有技能"""
    skill_hub_dir = Path.home() / '.skill-hub'
    skills = []
    
    if not skill_hub_dir.exists():
        return skills
    
    # 遍历 ~/.skill-hub 目录下的所有文件夹
    for owner_dir in skill_hub_dir.iterdir():
        if owner_dir.is_dir():
            owner_name = owner_dir.name
            # 遍历所有仓库目录
            for repo_dir in owner_dir.iterdir():
                if repo_dir.is_dir():
                    repo_name = repo_dir.name
                    # 检查仓库目录下是否有SKILL.md（整个仓库作为一个技能的情况）
                    root_skill_md = repo_dir / 'SKILL.md'
                    if root_skill_md.exists():
                        # 整个仓库作为技能，skill_name与repo_name相同
                        skill_name = repo_name
                        skills.append(f"{skill_name}@{owner_name}/{repo_name}")
                    else:
                        # 遍历仓库目录下的所有子文件夹（可能包含多个技能）
                        for skill_dir in repo_dir.iterdir():
                            if skill_dir.is_dir():
                                skill_name = skill_dir.name
                                # 检查这个技能目录下是否有SKILL.md
                                skill_md_path = skill_dir / 'SKILL.md'
                                if skill_md_path.exists():
                                    skills.append(f"{skill_name}@{owner_name}/{repo_name}")
    
    return sorted(set(skills))

def get_agent_skills(agent_name):
    """获取当前项目中agent已安装的技能"""
    """获取当前项目中已同步的技能"""

    def get_skills_from_path(path):
        skills = []
        path_obj = Path(path)
        if path_obj.exists():
            # 遍历项目技能目录下的所有子目录
            for skill_dir in path_obj.iterdir():
                if skill_dir.is_dir():
                    # 检查这个技能目录下是否有SKILL.md
                    skill_md_path = skill_dir / 'SKILL.md'
                    if skill_md_path.exists():
                        # 检查是否是软链接
                        if skill_dir.is_symlink():
                            # 如果是软链接，找到目标并确定对应的 skill@repo
                            target_path = skill_dir.resolve()
                            skill_repo = get_skill_repo_from_path(target_path)
                            if skill_repo:
                                skills.append(f"{skill_dir.name} -> {skill_repo}")
                            else:
                                skills.append(f"{skill_dir.name}")
                        else:
                            # 只是一个普通目录，返回技能名称
                            skills.append(skill_dir.name)
    
        return sorted(set(skills))
    project_path = get_config_for_agent(agent_name).get("project_path", '')
    global_path = get_config_for_agent(agent_name).get("global_path", '')

    return {
        "project_skills": get_skills_from_path(project_path),"global_skills": get_skills_from_path(global_path)
    }

def get_project_skills():
    """获取当前项目中已同步的技能"""
    skills = []
    project_paths = get_project_installed_agent_paths()
    
    for project_path in project_paths:
        project_path_obj = Path(project_path)
        if project_path_obj.exists():
            # 遍历项目技能目录下的所有子目录
            for skill_dir in project_path_obj.iterdir():
                if skill_dir.is_dir():
                    # 检查这个技能目录下是否有SKILL.md
                    skill_md_path = skill_dir / 'SKILL.md'
                    if skill_md_path.exists():
                        # 检查是否是软链接
                        if skill_dir.is_symlink():
                            # 如果是软链接，找到目标并确定对应的 skill@repo
                            target_path = skill_dir.resolve()
                            skill_repo = get_skill_repo_from_path(target_path)
                            if skill_repo:
                                skills.append(skill_repo)
                            else:
                                skills.append(skill_dir.name)
                        else:
                            # 只是一个普通目录，返回技能名称
                            skills.append(skill_dir.name)
    
    return sorted(set(skills))


def get_global_skills():
    """获取全局目录中已同步的技能"""
    skills = []
    global_paths = get_global_installed_agent_paths()
    
    for global_path in global_paths:
        global_path_obj = Path(global_path)
        if global_path_obj.exists():
            # 遍历全局技能目录下的所有子目录
            for skill_dir in global_path_obj.iterdir():
                if skill_dir.is_dir():
                    # 检查这个技能目录下是否有SKILL.md
                    skill_md_path = skill_dir / 'SKILL.md'
                    if skill_md_path.exists():
                        # 检查是否是软链接
                        if skill_dir.is_symlink():
                            # 如果是软链接，找到目标并确定对应的 skill@repo
                            target_path = skill_dir.resolve()
                            skill_repo = get_skill_repo_from_path(target_path)
                            if skill_repo:
                                skills.append(skill_repo)
                            else:
                                skills.append(skill_dir.name)
                        else:
                            # 只是一个普通目录，返回技能名称
                            skills.append(skill_dir.name)
    
    return sorted(set(skills))


def get_skill_repo_from_path(skill_path):
    """
    从技能路径反推 skill@repo 格式
    """
    # 获取 ~/.skill-hub 目录
    skill_hub_dir = Path.home() / '.skill-hub'
    
    # 确保路径在 ~/.skill-hub 目录下
    try:
        relative_path = skill_path.relative_to(skill_hub_dir)
        parts = str(relative_path).split('/')
        if len(parts) >= 3:  # owner/repo/skill 或 owner/repo 形式
            owner = parts[0]
            repo = parts[1]
            if len(parts) >= 3 and parts[2] != 'SKILL.md':  # 包含具体技能目录
                skill = parts[2]
                return f"{skill}@{owner}/{repo}"
            else:  # 可能是整个仓库作为技能
                return f"{repo}@{owner}/{repo}"
    except ValueError:
        pass
    
    return None


def print_section(title, skills):
    """打印技能列表段落"""
    print(f"{title}")
    for skill in skills:
        print(f"{skill}")
    print()  # 添加空行分隔