#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
repo 命令模块 - 用于管理自定义仓库
包含 add 和 rm 子命令
"""

from skill_hub.utils.skill_mng import add_custom_repo, rm_custom_repo


def repo_command(target=None, subcommand=None):
    """
    repo 命令主函数
    :param target: 仓库名称或URL
    :param subcommand: 子命令 ('add' 或 'rm')
    """
    if subcommand == 'add':
        if not target:
            print("错误: add 子命令需要指定仓库名称或URL")
            return
        add_custom_repo(target)
    elif subcommand == 'rm':
        if not target:
            print("错误: rm 子命令需要指定仓库名称")
            return
        rm_custom_repo(target)
    else:
        print("错误: 请指定有效的子命令 (add 或 rm)")
        return


if __name__ == "__main__":
    # 用于测试
    import sys
    if len(sys.argv) < 2:
        print("用法: python repo.py <add|rm> <repo_name>")
        sys.exit(1)
    
    subcommand = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else None
    repo_command(target, subcommand)