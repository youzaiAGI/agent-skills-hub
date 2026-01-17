#!/usr/bin/env python3
"""
Skill Hub - 技能包管理系统
命令行工具，用于管理AI助手的技能包
"""

import argparse
import sys
import os
from pathlib import Path


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
    
    # list 命
    list_parser = subparsers.add_parser('list', help='查看已安装的skill')
    

    
    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索skill')
    
    # mng 命令
    mng_parser = subparsers.add_parser('mng', help='技能管理')
    
    args = parser.parse_args()
    
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    # 处理版本号
    if args.version:
        print("Skill Hub v1.0.0")
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
        search_skills()
    elif args.command == 'mng':
        from skill_hub.commands.mng import manage_skills
        manage_skills()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()