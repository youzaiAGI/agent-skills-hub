"""
卸载技能命令模块
"""

import os
import shutil
from pathlib import Path


def uninstall_skill(target=None):
    """
    卸载skill
    :param target: 要卸载的目标 (格式: skill@repo 或 repo)
    """
    if not target:
        print("请指定要卸载的目标 (格式: skill@repo 或 repo)")
        return

    # 解析目标
    if '@' in target:
        # 格式为 skill@repo
        skill_name, repo = target.split('@', 1)
        uninstall_specific_skill(skill_name, repo)
    else:
        # 格式为 repo
        repo = target
        uninstall_all_skills_from_repo(repo)


def uninstall_all_skills_from_repo(repo):
    """卸载指定仓库的所有skill"""
    skill_hub_dir = Path.home() / '.skill-hub'
    repo_dir = skill_hub_dir / repo
    
    if not repo_dir.exists():
        print(f"仓库 {repo} 不存在")
        return
    
    try:
        shutil.rmtree(repo_dir)
        print(f"已卸载仓库 {repo} 的所有技能")
    except Exception as e:
        print(f"卸载仓库 {repo} 时出错: {e}")


def uninstall_specific_skill(skill_name, repo):
    """卸载指定仓库的指定skill"""
    skill_hub_dir = Path.home() / '.skill-hub'
    skill_dir = skill_hub_dir / repo / skill_name
    
    if not skill_dir.exists():
        print(f"技能 {skill_name}@{repo} 不存在")
        return
    
    try:
        shutil.rmtree(skill_dir)
        print(f"已卸载技能: {skill_name}@{repo}")
    except Exception as e:
        print(f"卸载技能 {skill_name}@{repo} 时出错: {e}")