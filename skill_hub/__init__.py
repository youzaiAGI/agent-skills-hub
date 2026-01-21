#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Hub - 技能包管理系统
命令行工具，用于管理AI助手的技能包
"""

import argparse
import sys
import os
from pathlib import Path
__version__ = '1.1.0'

def main():
    parser = argparse.ArgumentParser(description='Skill Hub - 技能包管理系统')
    parser.add_argument('-v', '--version', action='store_true', help='显示版本')
    
    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # install 命令
    install_parser = subparsers.add_parser('install', help='安装skill')
    install_parser.add_argument('target', nargs='?', help='要安装的目标 (格式: skill@repo 或 repo)')
    install_parser.add_argument('-u', '--update', action='store_true', help='强制更新')
    
    # update 命令
    update_parser = subparsers.add_parser('update', help='更新skill')
    update_parser.add_argument('target', nargs='?', help='要更新的目标 (格式: skill@repo 或 repo)')
    
    # uninstall 命令
    uninstall_parser = subparsers.add_parser('uninstall', help='卸载skill')
    uninstall_parser.add_argument('target', nargs='?', help='要卸载的目标 (格式: skill@repo 或 repo)')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='查看已安装的skill')
    

    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索skill')
    search_parser.add_argument('query', nargs='?', help='搜索关键词')
    
    # manage 命令
    manage_parser = subparsers.add_parser('manage', help='管理已安装的skills和agents')
    
    # sync 命令
    sync_parser = subparsers.add_parser('sync', help='同步skill到agent目录')
    sync_parser.add_argument('agent_name', help='agent名称')
    sync_parser.add_argument('target', help='要同步的目标 (格式: skill@repo 或 repo)')
    sync_parser.add_argument('-p', '--project', action='store_true', help='同步到项目级别')
    sync_parser.add_argument('-g', '--global', dest='global_level', action='store_true', help='同步到全局级别')
    sync_parser.add_argument('-f', '--force', action='store_true', help='强制同步')
    
    # repo 命令
    repo_parser = subparsers.add_parser('repo', help='管理自定义仓库')
    repo_subparsers = repo_parser.add_subparsers(dest='subcommand', help='repo 子命令', metavar='{add,rm}')
    repo_add_parser = repo_subparsers.add_parser('add', help='添加自定义仓库')
    repo_add_parser.add_argument('repo_name', help='仓库名称或URL (格式: owner/repo 或 https://github.com/owner/repo)')
    repo_rm_parser = repo_subparsers.add_parser('rm', help='删除自定义仓库')
    repo_rm_parser.add_argument('repo_name', help='仓库名称 (格式: owner/repo)')

    args = parser.parse_args()
    
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    # 处理版本号
    if args.version:
        print(f"Agent Skills Hub {__version__}")
        return
    
    # 根据子命令调用相应函数
    if args.command == 'install':
        from skill_hub.commands.install import install_skill
        install_skill(args.target, args.update)
    elif args.command == 'update':
        from skill_hub.commands.update import update_skill
        update_skill(args.target)
    elif args.command == 'uninstall':
        from skill_hub.commands.uninstall import uninstall_skill
        uninstall_skill(args.target)
    elif args.command == 'list':
        from skill_hub.commands.list import list_skills
        list_skills()

    elif args.command == 'search':
        from skill_hub.commands.search import search_skills
        search_skills(args.query)
    elif args.command == 'manage':
        from skill_hub.commands.manage import manage_skills
        manage_skills()
    elif args.command == 'sync':
        from skill_hub.commands.sync import sync_skill
        sync_skill(
            agent_name=args.agent_name,
            target=args.target,
            project_level=args.project,
            global_level=args.global_level,
            force_sync=args.force
        )
    elif args.command == 'repo':
        if args.subcommand is None:  # 如果没有提供子命令，则显示帮助
            repo_parser.print_help()
        else:
            from skill_hub.commands.repo import repo_command
            repo_command(args.repo_name, args.subcommand)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()