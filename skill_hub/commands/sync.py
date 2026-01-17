"""
同步技能到特定 agent 目录的命令模块
"""

import os
import shutil
from pathlib import Path
import argparse
from typing import Any
from ..utils.agent_cmd import get_config_for_agent


def sync_skill_from_file(file_path, agent_name, project_level=False, global_level=False, force_sync=False):
    """从文件读取目标列表并同步"""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not targets:
        print(f"文件 {file_path} 中没有找到有效的同步目标")
        return
    
    print(f"从文件 {file_path} 读取到 {len(targets)} 个同步目标")
    
    for target in targets:
        print(f"\n正在处理: {target}")
        sync_skill_single(
            agent_name=agent_name,
            target=target,
            project_level=project_level,
            global_level=global_level,
            force_sync=force_sync
        )


def sync_skill_single(agent_name, target, project_level=False, global_level=False, force_sync=False):
    """同步单个技能或仓库"""
    skill_name = None
    repo = None
    
    if '@' in target:
        # 格式为 skill@repo
        skill_name, repo = target.split('@', 1)
    else:
        # 格式为 repo，同步整个仓库的所有技能
        repo = target

    # 解析仓库为 owner/repo_name 格式
    repo_parts = repo.split('/')
    if len(repo_parts) != 2:
        print(f"无效的仓库格式: {repo}，应为 owner/repo_name 格式")
        return
    
    owner, repo_name = repo_parts

    # 获取 agent 配置
    agent_config = get_config_for_agent(agent_name)
    if not agent_config:
        print(f"未找到 agent '{agent_name}' 的配置")
        return

    # 确定目标路径：如果同时指定了 -p 和 -g，默认使用 -g；如果没有指定，默认使用 -p
    if global_level:
        target_base_path = agent_config.get('global_path')
        if not target_base_path:
            print(f"agent '{agent_name}' 没有全局路径配置")
            return
    else:  # 默认为项目级别
        target_base_path = agent_config.get('project_path')
        if not target_base_path:
            print(f"agent '{agent_name}' 没有项目路径配置")
            return

    # 确保目标路径存在
    target_base_path = Path(target_base_path).expanduser()
    target_base_path.parent.mkdir(parents=True, exist_ok=True)

    # 源路径：~/.skill-hub/owner/repo_name
    skill_hub_dir = Path.home() / '.skill-hub'
    repo_source_path = skill_hub_dir / owner / repo_name

    if not repo_source_path.exists():
        print(f"源仓库路径不存在: {repo_source_path}")
        return

    if skill_name:
        # 同步特定技能
        source_path = repo_source_path / skill_name

        if not source_path.exists():
            print(f"源技能路径不存在: {source_path}")
            return

        # 目标路径：agent 对应的技能目录下的技能名
        target_path = target_base_path / skill_name

        # 检查目标路径是否已存在
        if target_path.exists():
            if force_sync:
                # 强制同步：删除已存在的目标
                if target_path.is_symlink():
                    target_path.unlink()
                    print(f"已删除现有软链接: {target_path}")
                elif target_path.is_dir():
                    shutil.rmtree(target_path)
                    print(f"已删除现有目录: {target_path}")
            else:
                # 非强制同步：如果目标是目录且包含 SKILL.md 文件，则不进行同步
                if target_path.is_dir():
                    skill_md_path = target_path / 'SKILL.md'
                    if skill_md_path.exists():
                        print(f"目标目录 {target_path} 已存在且包含 SKILL.md 文件，跳过同步。使用 -f 参数强制同步。")
                        return

        # 创建目标目录（如果不存在）
        target_base_path.mkdir(parents=True, exist_ok=True)

        # 创建软链接
        try:
            # 如果目标已存在（非强制模式下），先删除
            if target_path.exists():
                if target_path.is_symlink():
                    target_path.unlink()
                elif target_path.is_dir():
                    shutil.rmtree(target_path)
            
            # 创建软链接
            target_path.symlink_to(source_path.resolve())
            print(f"已创建软链接: {target_path} -> {source_path.resolve()}")
        except OSError as e:
            print(f"创建软链接失败: {e}")
    else:
        # 同步整个仓库的所有技能
        # 遍历仓库目录中的所有子目录（这些应该是技能目录）
        for item in repo_source_path.iterdir():
            if item.is_dir():
                # 检查此目录是否包含 SKILL.md 文件，以确认它是一个技能
                skill_md_path = item / 'SKILL.md'
                if skill_md_path.exists():
                    skill_name = item.name
                    source_path = item  # 源路径就是这个子目录
                    
                    # 目标路径：agent 对应的技能目录下的技能名
                    target_path = target_base_path / skill_name

                    # 检查目标路径是否已存在
                    if target_path.exists():
                        if force_sync:
                            # 强制同步：删除已存在的目标
                            if target_path.is_symlink():
                                target_path.unlink()
                                print(f"已删除现有软链接: {target_path}")
                            elif target_path.is_dir():
                                shutil.rmtree(target_path)
                                print(f"已删除现有目录: {target_path}")
                        else:
                            # 非强制同步：如果目标是目录且包含 SKILL.md 文件，则不进行同步
                            if target_path.is_dir():
                                target_skill_md_path = target_path / 'SKILL.md'
                                if target_skill_md_path.exists():
                                    print(f"目标目录 {target_path} 已存在且包含 SKILL.md 文件，跳过同步。使用 -f 参数强制同步。")
                                    continue  # 继续处理下一个技能

                    # 创建目标目录（如果不存在）
                    target_base_path.mkdir(parents=True, exist_ok=True)

                    # 创建软链接
                    try:
                        # 如果目标已存在（非强制模式下），先删除
                        if target_path.exists():
                            if target_path.is_symlink():
                                target_path.unlink()
                            elif target_path.is_dir():
                                shutil.rmtree(target_path)
                        
                        # 创建软链接
                        target_path.symlink_to(source_path.resolve())
                        print(f"已创建软链接: {target_path} -> {source_path.resolve()}")
                    except OSError as e:
                        print(f"创建软链接失败: {e}")


def sync_skill(agent_name, target, project_level=False, global_level=False, force_sync=False):
    """
    同步技能到特定 agent 目录
    :param agent_name: agent 名称
    :param target: 要同步的目标 (格式: skill@repo 或 repo)，或者文件路径
    :param project_level: 是否同步到项目级别 (-p)
    :param global_level: 是否同步到全局级别 (-g)
    :param force_sync: 是否强制同步 (-f)
    """
    if not target:
        print("请指定要同步的目标 (格式: skill@repo 或 repo)，或提供包含目标列表的文件路径")
        return

    # 检查target是否为文件路径
    target_path = Path(target)
    # 检查是否为绝对路径或相对路径的文件
    if target_path.exists() and target_path.is_file():
        # 如果target是文件，则从文件读取同步目标
        sync_skill_from_file(target_path, agent_name, project_level, global_level, force_sync)
        return
    
    sync_skill_single(agent_name, target, project_level, global_level, force_sync)


def find_conflicting_skills_in_projects(skill_names, agent_name):
    """
    检查在项目安装路径下是否存在同名skill目录
    :param skill_name: 要检查的技能名称
    :param agent_name: agent名称
    :return: 包含同名skill的项目路径列表
    """
    conflicting_paths = []
    project_path = get_config_for_agent(agent_name).get("project_path", '')

    for skill_name in skill_names:
        skill_path = Path(project_path) / skill_name
        skill_md_path = skill_path / 'SKILL.md'
        if skill_path.exists() and skill_path.is_dir() and skill_md_path.exists():
            conflicting_paths.append(str(skill_path))
    
    return conflicting_paths

def find_conflicting_skills_in_global(skill_names, agent_name):
    """
    检查在全局安装路径下是否存在同名skill目录
    :param skill_names: 要检查的技能名称列表
    :return: 包含同名skill的全局路径列表
    """
    conflicting_paths = []
    global_path = get_config_for_agent(agent_name).get("global_path", '')

    for skill_name in skill_names:
        skill_path = Path(global_path) / skill_name
        skill_md_path = skill_path / 'SKILL.md'
        if skill_path.exists() and skill_path.is_dir() and skill_md_path.exists():
            conflicting_paths.append(str(skill_path))
    
    return conflicting_paths