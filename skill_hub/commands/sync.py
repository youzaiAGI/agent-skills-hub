"""
同步技能到特定 agent 目录的命令模块
"""

import os
import shutil
from pathlib import Path
import argparse
from ..utils.agent_cmd import get_config_for_agent


def sync_skill(agent_name, target, project_level=False, global_level=False, force_sync=False):
    """
    同步技能到特定 agent 目录
    :param agent_name: agent 名称
    :param target: 要同步的目标 (格式: skill@repo)
    :param project_level: 是否同步到项目级别 (-p)
    :param global_level: 是否同步到全局级别 (-g)
    :param force_sync: 是否强制同步 (-f)
    """
    if not target:
        print("请指定要同步的目标 (格式: skill@repo)")
        return

    if '@' not in target:
        print("目标格式错误，应为 skill@repo 格式")
        return

    # 解析技能和仓库
    skill_name, repo = target.split('@', 1)
    
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

    # 源路径：~/.skill-hub/owner/repo_name/skill_name
    skill_hub_dir = Path.home() / '.skill-hub'
    source_path = skill_hub_dir / owner / repo_name / skill_name

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


def main(args=None):
    parser = argparse.ArgumentParser(description='同步技能到特定 agent 目录')
    parser.add_argument('agent_name', help='agent 名称')
    parser.add_argument('target', help='要同步的目标 (格式: skill@repo)')
    parser.add_argument('-p', '--project', action='store_true', help='同步到项目级别')
    parser.add_argument('-g', '--global', dest='global_level', action='store_true', help='同步到全局级别')
    parser.add_argument('-f', '--force', action='store_true', help='强制同步')

    parsed_args = parser.parse_args(args)

    sync_skill(
        agent_name=parsed_args.agent_name,
        target=parsed_args.target,
        project_level=parsed_args.project,
        global_level=parsed_args.global_level,
        force_sync=parsed_args.force
    )


if __name__ == "__main__":
    main()