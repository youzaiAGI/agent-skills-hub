"""
技能管理命令模块 - 多标签页界面，包含本地技能管理和Agent已安装技能管理
"""

import os
import json
import curses
from pathlib import Path
import threading
import queue
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from skill_hub.utils.agent_cmd import (
    get_installed_agents, 
    get_project_installed_agents, 
    get_global_installed_agents
)
from skill_hub.commands.list import get_skill_hub_skills, get_agent_skills
from skill_hub.commands.update import update_skill
from skill_hub.commands.uninstall import uninstall_skill
from skill_hub.commands.sync import sync_skill_single


def manage_skills():
    """技能管理命令 - 多标签页界面"""
    try:
        while True:
            # 每次循环重新获取数据
            skill_hub_skills = get_skill_hub_skills()
            
            # 获取已安装的agents
            installed_agents = get_installed_agents()

            # 准备标签页数据
            tabs = []
            # 第一个标签页是skill-hub
            tabs.append({'name': 'skill-hub', 'data': skill_hub_skills[:], 'type': 'skill-hub'})
            
            # 后续标签页根据已安装的agents生成
            for agent_name in installed_agents:
                agent_data = get_agent_skills(agent_name)
                # 合并项目和全局技能，添加来源标识
                combined_data = []
                for skill in agent_data.get('project_skills', []):
                    combined_data.append(f"(project) {skill}")
                for skill in agent_data.get('global_skills', []):
                    combined_data.append(f"(global) {skill}")
                    
                tabs.append({
                    'name': agent_name, 
                    'data': combined_data[:], 
                    'type': 'agent',
                    'agent_name': agent_name
                })

            # 启动交互界面
            result = curses.wrapper(lambda stdscr: _multi_tab_management_ui(stdscr, tabs))
            # 如果返回值表示需要刷新，则重新开始循环
            if result != "refresh":
                break

    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"技能管理界面启动失败: {e}")


def _tabs_data_changed(old_tabs, new_tabs):
    """比较tabs数据是否发生了变化"""
    if len(old_tabs) != len(new_tabs):
        return True
    
    for old_tab, new_tab in zip(old_tabs, new_tabs):
        if old_tab['name'] != new_tab['name'] or old_tab['type'] != new_tab['type']:
            return True
        if old_tab['data'] != new_tab['data']:
            return True
    
    return False


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
            try:
                if current_x < width - 1:
                    safe_tab_text = tab_text[:width - current_x - 1] if len(tab_text) > width - current_x else tab_text
                    stdscr.addstr(0, current_x, safe_tab_text, curses.A_REVERSE if i == current_tab else 0)
                    current_x += len(safe_tab_text) + 1
                else:
                    break
            except:
                break

        # 显示说明文字
        try:
            if width > 25:
                stdscr.addstr(0, max(0, width - 25), "(左右箭头切换, ESC退出)")
        except:
            pass

        # 获取当前标签页的数据
        current_state = tab_states[current_tab]
        current_data = current_state['filtered_data']
        current_search = current_state['search_text']

        # 显示搜索框
        try:
            search_text = f"搜索: {current_search}_"
            stdscr.addstr(1, 0, search_text[:width - 1])
        except:
            stdscr.addstr(1, 0, f"搜索:_")
        
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
        # 处理回车键（进入详情页）
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
            if current_data and len(current_data) > current_state['current_row'] >= 0:
                selected_item = current_data[current_state['current_row']]
                # 进入详情页前记录当前数据
                original_data = [tab['data'][:] for tab in tabs]
                # 进入详情页
                _show_detail_view(stdscr, tabs[current_tab], selected_item)
                # 从详情页返回后，检查数据是否有变化
                updated_tabs = _refresh_tabs_data()
                if _tabs_data_changed(tabs, updated_tabs):
                    return "refresh"  # 返回刷新信号
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
    
    return None  # 正常退出



def _refresh_tabs_data():
    """刷新tabs数据"""
    # 获取最新的skill-hub中的所有技能
    skill_hub_skills = get_skill_hub_skills()
    
    # 获取最新的已安装的agents
    installed_agents = get_installed_agents()

    # 准备标签页数据
    tabs = []
    # 第一个标签页是skill-hub
    tabs.append({'name': 'skill-hub', 'data': skill_hub_skills[:], 'type': 'skill-hub'})
    
    # 后续标签页根据已安装的agents生成
    for agent_name in installed_agents:
        agent_data = get_agent_skills(agent_name)
        # 合并项目和全局技能，添加来源标识
        combined_data = []
        for skill in agent_data.get('project_skills', []):
            combined_data.append(f"(project) {skill}")
        for skill in agent_data.get('global_skills', []):
            combined_data.append(f"(global) {skill}")
            
        tabs.append({
            'name': agent_name, 
            'data': combined_data[:], 
            'type': 'agent',
            'agent_name': agent_name
        })
    
    return tabs


def _show_detail_view(stdscr, tab, selected_item):
    """显示详情页"""
    # 移除项目/全局标记以便正确解析技能名称
    clean_item = selected_item
    source_type = None
    if selected_item.startswith("(project) "):
        source_type = "project"
        clean_item = selected_item[10:]  # 移除 "(project) " 前缀
    elif selected_item.startswith("(global) "):
        source_type = "global"
        clean_item = selected_item[9:]  # 移除 "(global) " 前缀

    if tab['type'] == 'skill-hub':
        # skill-hub 标签页的详情选项
        options = [
            "查看SKILL.md",
            "更新skill",
            "删除skill",
            "同步到项目",
            "同步到全局"
        ]
        choice = _show_options_menu(stdscr, f"技能详情: {clean_item}", options)
        
        if choice == 0:  # 查看SKILL.md
            _view_skill_md(stdscr, clean_item)
        elif choice == 1:  # 更新skill
            _update_skill(stdscr, clean_item)
        elif choice == 2:  # 删除skill
            _uninstall_skill(stdscr, clean_item)
        elif choice == 3:  # 同步到项目
            _sync_to_project(stdscr, clean_item)
        elif choice == 4:  # 同步到全局
            _sync_to_global(stdscr, clean_item)
    elif tab['type'] == 'agent':
        # agent 标签页的详情选项
        options = [
            "查看SKILL.md",
            "删除skill"
        ]
        choice = _show_options_menu(stdscr, f"技能详情: {clean_item}", options)
        
        if choice == 0:  # 查看SKILL.md
            _view_agent_skill_md(stdscr, clean_item, tab['agent_name'], source_type)
        elif choice == 1:  # 删除skill
            _remove_agent_skill(stdscr, clean_item, tab['agent_name'], source_type)


def _show_options_menu(stdscr, title, options):
    """显示选项菜单"""
    curses.curs_set(0)
    current_row = 0
    
    while True:
        stdscr.clear()
        
        # 显示标题
        stdscr.addstr(0, 0, title)
        
        # 显示选项
        for idx, option in enumerate(options):
            prefix = "> " if idx == current_row else "  "
            if idx == current_row:
                stdscr.addstr(idx + 2, 0, prefix + option, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, prefix + option)
        
        # 显示说明
        stdscr.addstr(len(options) + 3, 0, "(上下箭头选择, 回车确认, ESC返回)")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == 27:  # ESC键返回
            return -1
        elif key == curses.KEY_UP:
            current_row = max(0, current_row - 1)
        elif key == curses.KEY_DOWN:
            current_row = min(len(options) - 1, current_row + 1)
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:  # 回车键确认
            return current_row


def _parse_skill_info(skill_str):
    """解析技能字符串，提取技能名和仓库信息"""
    if '@' in skill_str:
        parts = skill_str.split('@')
        skill_name = parts[0]
        repo = parts[1]
        return skill_name, repo
    else:
        # 如果只有仓库名，返回None作为技能名
        return None, skill_str


def _view_skill_md(stdscr, skill_str):
    """查看技能的SKILL.md文件"""
    skill_name, repo = _parse_skill_info(skill_str)
    
    if not repo:
        stdscr.clear()
        stdscr.addstr(0, 0, "无法解析技能信息")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return
    
    # 构建SKILL.md路径
    repo_parts = repo.split('/')
    if len(repo_parts) != 2:
        stdscr.clear()
        stdscr.addstr(0, 0, "无效的仓库格式")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return
    
    owner, repo_name = repo_parts
    skill_hub_dir = Path.home() / '.skill-hub'
    
    if skill_name:
        # 特定技能的SKILL.md
        skill_md_path = skill_hub_dir / owner / repo_name / skill_name / 'SKILL.md'
    else:
        # 整个仓库作为技能的SKILL.md
        skill_md_path = skill_hub_dir / owner / repo_name / 'SKILL.md'
    
    if not skill_md_path.exists():
        stdscr.clear()
        stdscr.addstr(0, 0, f"SKILL.md 文件不存在: {skill_md_path}")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return
    
    # 读取并显示SKILL.md内容
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"读取文件失败: {e}")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return
    
    # 显示内容（支持翻页）
    _show_file_content(stdscr, f"SKILL.md - {skill_str}", content)


def _show_file_content(stdscr, title, content):
    """显示文件内容，支持翻页"""
    lines = content.split('\n')
    current_line = 0
    
    while True:
        stdscr.clear()
        
        # 显示标题
        stdscr.addstr(0, 0, title)
        
        # 获取屏幕尺寸
        height, width = stdscr.getmaxyx()
        
        # 计算可显示的行数（预留标题和底部说明空间）
        display_lines = height - 3
        end_line = min(current_line + display_lines, len(lines))
        
        # 显示内容行
        for i in range(current_line, end_line):
            if i < len(lines):
                # 截断过长的行以适应屏幕宽度
                line_content = lines[i][:width-1]
                stdscr.addstr(i - current_line + 2, 0, line_content)
        
        # 显示位置信息
        position_info = f"第 {current_line+1}-{end_line} 行，共 {len(lines)} 行 (上下箭头翻页, ESC返回)"
        stdscr.addstr(height - 1, 0, position_info[:width-1])
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == 27:  # ESC键返回
            break
        elif key == curses.KEY_UP:
            if current_line > 0:
                current_line = max(0, current_line - 1)
        elif key == curses.KEY_DOWN:
            if current_line + display_lines < len(lines):
                current_line += 1
        elif key == curses.KEY_PPAGE:  # Page Up
            current_line = max(0, current_line - display_lines)
        elif key == curses.KEY_NPAGE:  # Page Down
            current_line = min(len(lines) - display_lines, current_line + display_lines)


def _update_skill(stdscr, skill_str):
    """更新技能"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"正在更新技能: {skill_str}")
    stdscr.addstr(1, 0, "请稍候...")
    stdscr.refresh()
    
    # 捕获更新过程中的输出
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()
    
    try:
        # 重定向stdout和stderr来捕获update_skill函数的输出
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            update_skill(skill_str)
        
        # 获取捕获的输出
        output = output_buffer.getvalue()
        error = error_buffer.getvalue()
        
        # 清屏并显示结果
        stdscr.clear()
        stdscr.addstr(0, 0, f"已更新技能: {skill_str}")
        stdscr.addstr(1, 0, "更新完成！")
        
        # 如果有输出信息，显示在界面上（限制显示行数）
        if output:
            output_lines = output.strip().split('\n')
            for i, line in enumerate(output_lines[:3]):  # 最多显示3行输出
                if i < 3:
                    stdscr.addstr(3+i, 0, line[:min(len(line), 60)])  # 限制每行长度
        
        stdscr.addstr(6, 0, "按任意键返回...")
        
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"更新失败: {e}")
        stdscr.addstr(1, 0, "按任意键返回...")
    
    stdscr.refresh()
    stdscr.getch()


def _uninstall_skill(stdscr, skill_str):
    """卸载技能"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"确认删除技能: {skill_str} ? (y/N)")
    stdscr.refresh()
    
    # 获取用户确认
    key = stdscr.getch()
    stdscr.clear()
    if key in [ord('y'), ord('Y')]:
        try:
            uninstall_skill(skill_str)
            stdscr.addstr(0, 0, f"已卸载技能: {skill_str}")
            stdscr.addstr(1, 0, "删除完成！")
            stdscr.addstr(2, 0, "按任意键返回...")
        except Exception as e:
            stdscr.addstr(0, 0, f"删除失败: {e}")
            stdscr.addstr(1, 0, "按任意键返回...")
    else:
        stdscr.addstr(0, 0, "取消删除")
        stdscr.addstr(1, 0, "按任意键返回...")
    
    stdscr.refresh()
    stdscr.getch()


def _sync_to_project(stdscr, skill_str):
    """同步到项目"""
    # 获取已安装的agents
    installed_agents = get_installed_agents()
    project_agents = get_project_installed_agents()
    
    # 显示agent选择列表（多选）
    selected_agents = _show_multi_select_menu(stdscr, "选择要同步到项目的Agents", installed_agents, project_agents)
    
    if selected_agents:
        stdscr.clear()
        stdscr.addstr(0, 0, "正在同步...")
        stdscr.refresh()
        
        error_occurred = False
        for agent in selected_agents:
            try:
                sync_skill_single(
                    agent_name=agent,
                    target=skill_str,
                    project_level=True,
                    global_level=False,
                    force_sync=True
                )
            except Exception as e:
                stdscr.addstr(1, 0, f"同步到 {agent} 失败: {e}")
                stdscr.refresh()
                error_occurred = True
        
        stdscr.clear()
        if error_occurred:
            stdscr.addstr(0, 0, "部分同步操作失败")
            stdscr.addstr(1, 0, "请检查错误信息")
        else:
            stdscr.addstr(0, 0, "同步完成！")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "未选择任何Agent")
        stdscr.addstr(1, 0, "同步已取消")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()


def _sync_to_global(stdscr, skill_str):
    """同步到全局"""
    # 获取已安装的agents
    installed_agents = get_installed_agents()
    global_agents = get_global_installed_agents()
    
    # 显示agent选择列表（多选）
    selected_agents = _show_multi_select_menu(stdscr, "选择要同步到全局的Agents", installed_agents, global_agents)
    
    if selected_agents:
        stdscr.clear()
        stdscr.addstr(0, 0, "正在同步...")
        stdscr.refresh()
        
        error_occurred = False
        for agent in selected_agents:
            try:
                sync_skill_single(
                    agent_name=agent,
                    target=skill_str,
                    project_level=False,
                    global_level=True,
                    force_sync=True
                )
            except Exception as e:
                stdscr.addstr(1, 0, f"同步到 {agent} 失败: {e}")
                stdscr.refresh()
                error_occurred = True
        
        stdscr.clear()
        if error_occurred:
            stdscr.addstr(0, 0, "部分同步操作失败")
            stdscr.addstr(1, 0, "请检查错误信息")
        else:
            stdscr.addstr(0, 0, "同步完成！")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "未选择任何Agent")
        stdscr.addstr(1, 0, "同步已取消")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()


def _show_multi_select_menu(stdscr, title, all_items, selected_items):
    """显示多选菜单"""
    curses.curs_set(0)
    current_row = 0
    # 创建选中状态列表
    selected_flags = [item in selected_items for item in all_items]
    
    while True:
        stdscr.clear()
        
        # 显示标题
        stdscr.addstr(0, 0, title)
        
        # 显示选项
        for idx, item in enumerate(all_items):
            marker = "[x]" if selected_flags[idx] else "[ ]"
            prefix = "> " if idx == current_row else "  "
            display_text = f"{prefix}{marker} {item}"
            
            if idx == current_row:
                stdscr.addstr(idx + 2, 0, display_text, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, display_text)
        
        # 显示说明
        stdscr.addstr(len(all_items) + 3, 0, "(上下箭头移动, 空格键选择/取消, 回车确认, ESC返回)")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == 27:  # ESC键返回
            return []
        elif key == curses.KEY_UP:
            current_row = max(0, current_row - 1)
        elif key == curses.KEY_DOWN:
            current_row = min(len(all_items) - 1, current_row + 1)
        elif key == ord(' '):  # 空格键切换选中状态
            selected_flags[current_row] = not selected_flags[current_row]
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:  # 回车键确认
            # 返回选中的项目
            return [all_items[i] for i in range(len(all_items)) if selected_flags[i]]


def _view_agent_skill_md(stdscr, skill_name, agent_name, source_type):
    """查看agent中技能的SKILL.md文件"""
    from skill_hub.utils.agent_cmd import get_config_for_agent
    
    # 如果技能名称包含 ' -> '，则只取前面的部分作为实际目录名
    actual_skill_name = skill_name.split(' -> ')[0]
    
    # 根据源类型获取正确的路径
    if source_type == "project":
        skill_path = Path(get_config_for_agent(agent_name).get("project_path", '')) / actual_skill_name
    else:  # global
        skill_path = Path(get_config_for_agent(agent_name).get("global_path", '')) / actual_skill_name
    
    skill_md_path = skill_path / 'SKILL.md'
    
    # 如果路径是软链接，需要解析真实路径
    if skill_path.is_symlink():
        skill_md_path = skill_path.resolve() / 'SKILL.md'
    
    if not skill_md_path.exists():
        stdscr.clear()
        stdscr.addstr(0, 0, f"SKILL.md 文件不存在: {skill_md_path}")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return
    
    # 读取并显示SKILL.md内容
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"读取文件失败: {e}")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return
    
    # 显示内容（支持翻页）
    _show_file_content(stdscr, f"SKILL.md - {skill_name} ({agent_name})", content)


def _remove_agent_skill(stdscr, skill_name, agent_name, source_type):
    """删除agent中的技能"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"确认删除技能: {skill_name} ? (y/N)")
    stdscr.refresh()
    
    # 获取用户确认
    key = stdscr.getch()
    stdscr.clear()
    if key in [ord('y'), ord('Y')]:
        from skill_hub.utils.agent_cmd import get_config_for_agent
        import shutil
        
        # 如果技能名称包含 ' -> '，则只取前面的部分作为实际目录名
        actual_skill_name = skill_name.split(' -> ')[0]
        
        # 根据源类型获取正确的路径
        if source_type == "project":
            skill_path = Path(get_config_for_agent(agent_name).get("project_path", '')) / actual_skill_name
        else:  # global
            skill_path = Path(get_config_for_agent(agent_name).get("global_path", '')) / actual_skill_name
        
        try:
            if skill_path.is_symlink():
                # 如果是软链接，取消软链接
                skill_path.unlink()
                stdscr.addstr(0, 0, f"已取消软链接: {skill_path}")
                stdscr.addstr(1, 0, "删除成功！")
                stdscr.addstr(2, 0, "按任意键返回...")
            elif skill_path.is_dir():
                # 如果是目录，删除目录
                shutil.rmtree(skill_path)
                stdscr.addstr(0, 0, f"已删除目录: {skill_path}")
                stdscr.addstr(1, 0, "删除成功！")
                stdscr.addstr(2, 0, "按任意键返回...")
            else:
                stdscr.addstr(0, 0, f"技能路径不存在: {skill_path}")
                stdscr.addstr(1, 0, "按任意键返回...")
        except Exception as e:
            stdscr.addstr(0, 0, f"删除失败: {e}")
            stdscr.addstr(1, 0, "按任意键返回...")
    else:
        stdscr.addstr(0, 0, "取消删除")
        stdscr.addstr(1, 0, "按任意键返回...")
    
    stdscr.refresh()
    stdscr.getch()