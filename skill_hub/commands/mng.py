"""
技能管理命令模块 - 多标签页界面，包含本地技能管理和IDE特定技能管理
"""

import os
import json
import curses
from pathlib import Path
import threading
import queue


def manage_skills():
    """技能管理命令 - 多标签页界面"""
    try:
        # 获取本地已安装的技能列表
        skill_hub_dir = Path.home() / '.skill-hub'
        local_skills = []
        if skill_hub_dir.exists():
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
                                local_skills.append(f"{skill_name}@{owner_name}/{repo_name}")
                            else:
                                # 遍历仓库目录下的所有子文件夹（可能包含多个技能）
                                for skill_dir in repo_dir.iterdir():
                                    if skill_dir.is_dir():
                                        skill_name = skill_dir.name
                                        # 检查这个技能目录下是否有SKILL.md
                                        skill_md_path = skill_dir / 'SKILL.md'
                                        if skill_md_path.exists():
                                            local_skills.append(f"{skill_name}@{owner_name}/{repo_name}")
                                        else:
                                            # 检查子目录中是否有SKILL.md
                                            for sub_dir in skill_dir.iterdir():
                                                if sub_dir.is_dir():
                                                    sub_skill_md_path = sub_dir / 'SKILL.md'
                                                    if sub_skill_md_path.exists():
                                                        # 这里应该用子目录的名字作为技能名
                                                        sub_skill_name = sub_dir.name
                                                        local_skills.append(f"{sub_skill_name}@{owner_name}/{repo_name}")

        # 从agent_cmd.py获取已安装的IDE
        from skill_hub.utils.agent_cmd import check_ide_installation
        installed_ide_list = check_ide_installation()

        # 准备标签页数据
        tabs = []
        # 第一个标签页是skill-hub
        tabs.append({'name': 'skill-hub', 'data': local_skills[:]})
        
        # 后续标签页根据check_ide_installation的结果生成
        for ide_name in installed_ide_list:
            tabs.append({'name': ide_name, 'data': []})  # 初始为空，后续可扩展添加具体技能

        # 启动交互界面
        curses.wrapper(lambda stdscr: _multi_tab_management_ui(stdscr, tabs))

    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"技能管理界面启动失败: {e}")


def _multi_tab_management_ui(stdscr, tabs):
    """多标签页技能管理交互界面"""
    # 初始化curses
    curses.curs_set(0)  # 隐藏光标
    stdscr.nodelay(0)
    stdscr.timeout(-1)  # 阻塞等待输入
    
    # 当前选中的标签页
    current_tab = 0
    
    # 为每个标签页维护状态
    tab_states = []
    for tab in tabs:
        state = {
            'current_row': 0,
            'search_text': "",
            'filtered_data': tab['data'][:]
        }
        tab_states.append(state)
    
    while True:
        stdscr.clear()
        
        # 获取屏幕尺寸
        height, width = stdscr.getmaxyx()
        
        # 显示标签页
        tab_titles = [tab['name'] for tab in tabs]
        current_x = 0
        for i, title in enumerate(tab_titles):
            tab_text = f"[{title}]" if i == current_tab else f" {title} "
            stdscr.addstr(0, current_x, tab_text, curses.A_REVERSE if i == current_tab else 0)
            current_x += len(tab_text) + 1  # +1 for spacing
        
        # 显示说明文字
        stdscr.addstr(0, width - 25, "(左右箭头切换, ESC退出)")
        
        # 获取当前标签页的数据
        current_state = tab_states[current_tab]
        current_data = current_state['filtered_data']
        current_search = current_state['search_text']
        
        # 显示搜索框
        stdscr.addstr(1, 0, f"搜索: {current_search}_")
        
        # 显示列表内容，确保不超过屏幕高度
        max_display_items = height - 4  # 留出标题、搜索框和底部说明的空间
        for idx in range(min(len(current_data), max_display_items)):
            item = current_data[idx]
            prefix = "> " if idx == current_state['current_row'] else "  "
            try:
                if idx == current_state['current_row']:
                    stdscr.addstr(idx + 3, 0, prefix + item, curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 3, 0, prefix + item)
            except:
                # 如果添加字符串失败（例如超出边界），则跳过
                break
        
        stdscr.refresh()
        
        # 获取用户输入
        key = stdscr.getch()
        
        # 处理ESC键退出
        if key == 27:  # ESC键
            break
        # 处理左右箭头键切换标签页
        elif key == curses.KEY_LEFT:
            current_tab = (current_tab - 1) % len(tabs) if len(tabs) > 0 else 0
        elif key == curses.KEY_RIGHT:
            current_tab = (current_tab + 1) % len(tabs) if len(tabs) > 0 else 0
        # 处理回车键（未来可以用于查看详情等操作）
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
            if current_data and len(current_data) > current_state['current_row'] >= 0:
                selected_item = current_data[current_state['current_row']]
                # 暂时只是显示选择的信息，后续可扩展功能
                stdscr.clear()
                stdscr.addstr(0, 0, f"选择了: {selected_item}")
                stdscr.addstr(2, 0, "按任意键继续...")
                stdscr.refresh()
                stdscr.getch()
        # 处理字母数字搜索
        elif 32 <= key <= 126:  # ASCII字符范围
            current_state['search_text'] += chr(key)
            current_state['current_row'] = 0  # 重置选中项
            # 更新过滤列表
            if current_state['search_text']:
                current_state['filtered_data'] = [item for item in tabs[current_tab]['data'] if current_state['search_text'].lower() in item.lower()]
            else:
                current_state['filtered_data'] = tabs[current_tab]['data'][:]
        # 处理退格键
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            current_state['search_text'] = current_state['search_text'][:-1]
            current_state['current_row'] = 0  # 重置选中项
            # 更新过滤列表
            if current_state['search_text']:
                current_state['filtered_data'] = [item for item in tabs[current_tab]['data'] if current_state['search_text'].lower() in item.lower()]
            else:
                current_state['filtered_data'] = tabs[current_tab]['data'][:]
        # 处理方向键
        elif key == curses.KEY_UP:
            current_state['current_row'] = max(0, current_state['current_row'] - 1)
        elif key == curses.KEY_DOWN:
            current_state['current_row'] = min(len(current_state['filtered_data']) - 1, current_state['current_row'] + 1)
        # 处理其他控制键
        elif key == curses.KEY_DC:  # Delete键
            current_state['search_text'] = ""
            current_state['current_row'] = 0
            # 重置过滤列表
            current_state['filtered_data'] = tabs[current_tab]['data'][:]