"""
列出已安装技能命令模块
"""

import os
from pathlib import Path


def list_skills():
    """列出当前已经安装的skill"""
    skill_hub_dir = Path.home() / '.skill-hub'
    
    if not skill_hub_dir.exists():
        print("没有已安装的技能")
        return
    
    installed_skills = []
    
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
                        installed_skills.append(f"{skill_name}@{owner_name}/{repo_name}")
                    else:
                        # 遍历仓库目录下的所有子文件夹（可能包含多个技能）
                        for skill_dir in repo_dir.iterdir():
                            if skill_dir.is_dir():
                                skill_name = skill_dir.name
                                # 检查这个技能目录下是否有SKILL.md
                                skill_md_path = skill_dir / 'SKILL.md'
                                if skill_md_path.exists():
                                    installed_skills.append(f"{skill_name}@{owner_name}/{repo_name}")
                                else:
                                    # 检查子目录中是否有SKILL.md
                                    for sub_dir in skill_dir.iterdir():
                                        if sub_dir.is_dir():
                                            sub_skill_md_path = sub_dir / 'SKILL.md'
                                            if sub_skill_md_path.exists():
                                                # 这里应该用子目录的名字作为技能名
                                                sub_skill_name = sub_dir.name
                                                installed_skills.append(f"{sub_skill_name}@{owner_name}/{repo_name}")
    
    if not installed_skills:
        print("没有已安装的技能")
        return
    
    print("已安装的技能:")
    for skill in sorted(installed_skills):
        print(f"  {skill}")