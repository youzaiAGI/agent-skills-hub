"""
搜索技能命令模块 - 多标签页界面，支持搜索skill和repo
"""

import curses
import requests
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from skill_hub.commands.install import install_skill
from skill_hub.utils.agent_cmd import (
    get_installed_agents,
    get_project_installed_agents,
    get_global_installed_agents
)
from skill_hub.commands.sync import sync_skill_single


# 每页显示数量
PAGE_SIZE = 20

skill_md_url = 'https://skill-hub.oss-cn-shanghai.aliyuncs.com/skills/{owner}/{repo}/{skill_name}.md'


def search_skills():
    """搜索技能命令 - 多标签页界面"""
    try:
        if not sys.stdout.isatty():
            print("搜索命令需要在交互式终端中运行")
            return
        curses.wrapper(_search_ui)
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        if 'curses' in str(e) or 'ERR' in str(e):
            print("搜索界面启动失败: 当前终端可能不支持 curses")
            print("请尝试在支持 curses 的终端中运行")
        else:
            print(f"搜索界面启动失败: {e}")


def _search_ui(stdscr):
    """搜索交互界面主函数"""
    curses.curs_set(1)
    stdscr.nodelay(0)
    stdscr.timeout(-1)

    tabs = [
        {'name': 'skill', 'display': 'Skill', 'type': 'skill'},
        {'name': 'repo', 'display': 'Repo', 'type': 'repo'}
    ]
    current_tab = 0

    tab_states = [
        {'page': 1, 'current_row': 0, 'scroll_offset': 0, 'search_text': "", 'filtered_data': [], 'total_count': 0},
        {'page': 1, 'current_row': 0, 'scroll_offset': 0, 'search_text': "", 'filtered_data': [], 'total_count': 0}
    ]

    # 初始加载数据
    _load_tab_data(tabs[current_tab], tab_states[current_tab])

    # 初始显示
    _draw_main_screen(stdscr, tabs, current_tab, tab_states[current_tab])

    while True:
        # 获取用户输入
        key = stdscr.getch()

        # 处理ESC键退出
        if key == 27:
            break

        current_state = tab_states[current_tab]

        # 处理左右箭头键切换标签页
        if key == curses.KEY_LEFT:
            current_tab = (current_tab - 1) % len(tabs)
            _load_tab_data(tabs[current_tab], tab_states[current_tab])

        elif key == curses.KEY_RIGHT:
            current_tab = (current_tab + 1) % len(tabs)
            _load_tab_data(tabs[current_tab], tab_states[current_tab])

        # 处理回车键（进入详情页）
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
            current_state = tab_states[current_tab]
            current_data = current_state['filtered_data']
            if current_data and 0 <= current_state['current_row'] < len(current_data):
                selected_item = current_data[current_state['current_row']]
                _show_detail_view(stdscr, tabs[current_tab], selected_item)
                _load_tab_data(tabs[current_tab], tab_states[current_tab])

        # 字母数字搜索
        elif 32 <= key <= 126:
            current_state['search_text'] += chr(key)
            current_state['page'] = 1
            current_state['current_row'] = 0
            current_state['scroll_offset'] = 0
            _load_tab_data(tabs[current_tab], current_state)

        # 退格键
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            if current_state['search_text']:
                current_state['search_text'] = current_state['search_text'][:-1]
                current_state['page'] = 1
                current_state['current_row'] = 0
                current_state['scroll_offset'] = 0
                _load_tab_data(tabs[current_tab], current_state)

        # 方向键 - 上下移动光标
        elif key == curses.KEY_UP:
            if current_state['current_row'] > 0:
                current_state['current_row'] -= 1
        elif key == curses.KEY_DOWN:
            if current_state['current_row'] < len(current_state['filtered_data']) - 1:
                current_state['current_row'] += 1

        # Page Up - 上一页
        elif key == curses.KEY_PPAGE:
            if current_state['page'] > 1:
                current_state['page'] -= 1
                current_state['current_row'] = 0
                current_state['scroll_offset'] = 0
                _load_tab_data(tabs[current_tab], current_state)

        # Page Down - 下一页
        elif key == curses.KEY_NPAGE:
            current_state = tab_states[current_tab]
            total_pages = (current_state['total_count'] + PAGE_SIZE - 1) // PAGE_SIZE if current_state['total_count'] > 0 else 1
            if current_state['page'] < total_pages:
                current_state['page'] += 1
                current_state['current_row'] = 0
                current_state['scroll_offset'] = 0
                _load_tab_data(tabs[current_tab], current_state)

        # 处理完输入后，更新滚动偏移并重绘
        current_state = tab_states[current_tab]
        height, width = stdscr.getmaxyx()
        max_display_items = height - 4
        _update_scroll_offset(current_state, max_display_items)
        _draw_main_screen(stdscr, tabs, current_tab, current_state)


def _draw_main_screen(stdscr, tabs, current_tab, state):
    """绘制主界面"""
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    current_data = state['filtered_data']

    # 显示标签页
    current_x = 0
    for i, tab in enumerate(tabs):
        tab_text = f"[{tab['display']}]" if i == current_tab else f" {tab['display']} "
        stdscr.addstr(0, current_x, tab_text, curses.A_REVERSE if i == current_tab else 0)
        current_x += len(tab_text) + 1

    stdscr.addstr(0, width - 60, "(左右箭头切换tab, FN+上下/Page翻页, ESC退出)")

    # 显示搜索框和页码
    search_display = f"搜索: {state['search_text']}_ "
    total_pages = (state['total_count'] + PAGE_SIZE - 1) // PAGE_SIZE if state['total_count'] > 0 else 1
    page_info = f"第{state['page']}/{total_pages}页"
    full_line = search_display + page_info
    stdscr.addstr(1, 0, full_line)

    # 显示列表
    max_display_items = height - 4
    scroll_offset = state['scroll_offset']

    for idx in range(min(len(current_data), max_display_items)):
        display_idx = scroll_offset + idx
        if display_idx >= len(current_data):
            break

        item = current_data[display_idx]
        prefix = "> " if display_idx == state['current_row'] else "  "
        display_item = item.replace('\t', '  ')
        try:
            if display_idx == state['current_row']:
                stdscr.addstr(idx + 3, 0, prefix + display_item, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 3, 0, prefix + display_item)
        except:
            break

    stdscr.refresh()


def _update_scroll_offset(state, max_display_items):
    """更新滚动偏移量"""
    current_row = state['current_row']
    scroll_offset = state['scroll_offset']

    if current_row < scroll_offset:
        state['scroll_offset'] = current_row
    elif current_row >= scroll_offset + max_display_items:
        state['scroll_offset'] = current_row - max_display_items + 1


def _load_tab_data(tab, state):
    """加载标签页数据"""
    from skill_hub.utils.skill_mng import get_skills, get_repos

    if tab['type'] == 'skill':
        data, total = get_skills(state['search_text'], state['page'], PAGE_SIZE)
        state['filtered_data'] = data
        state['total_count'] = total
    else:
        data, total = get_repos(state['search_text'], state['page'], PAGE_SIZE)
        state['filtered_data'] = data
        state['total_count'] = total


def _show_detail_view(stdscr, tab, selected_item):
    """显示详情页"""
    if tab['type'] == 'skill':
        _show_skill_detail_options(stdscr, selected_item)
    else:
        _show_repo_detail_options(stdscr, selected_item)


def _show_skill_detail_options(stdscr, skill_str):
    """显示skill详情选项"""
    stdscr.clear()
    options = [
        "查看SKILL.md",
        "仅安装到 ~/.skill-hub",
        "安装并同步到项目",
        "安装并同步到全局"
    ]
    choice = _show_options_menu(stdscr, f"技能详情: {skill_str}", options)

    if choice == 0:
        _view_skill_md_online(stdscr, skill_str)
    elif choice == 1:
        _install_skill_only(stdscr, skill_str)
    elif choice == 2:
        _install_and_sync_to_project(stdscr, skill_str)
    elif choice == 3:
        _install_and_sync_to_global(stdscr, skill_str)


def _show_repo_detail_options(stdscr, repo_str):
    """显示repo详情选项"""
    clean_repo = repo_str.split('\t')[0].strip()

    stdscr.clear()
    options = [
        "仅安装到 ~/.skill-hub",
        "安装并同步到项目",
        "安装并同步到全局"
    ]
    choice = _show_options_menu(stdscr, f"仓库详情: {clean_repo}", options)

    if choice == 0:
        _install_repo_only(stdscr, clean_repo)
    elif choice == 1:
        _install_repo_and_sync_to_project(stdscr, clean_repo)
    elif choice == 2:
        _install_repo_and_sync_to_global(stdscr, clean_repo)


def _show_options_menu(stdscr, title, options):
    """显示选项菜单"""
    curses.curs_set(0)
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title)

        for idx, option in enumerate(options):
            prefix = "> " if idx == current_row else "  "
            if idx == current_row:
                stdscr.addstr(idx + 2, 0, prefix + option, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, prefix + option)

        stdscr.addstr(len(options) + 3, 0, "(上下箭头选择, 回车确认, ESC返回)")
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
            return -1
        elif key == curses.KEY_UP:
            current_row = max(0, current_row - 1)
        elif key == curses.KEY_DOWN:
            current_row = min(len(options) - 1, current_row + 1)
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
            return current_row


def _parse_skill_info(skill_str):
    """解析技能字符串，提取技能名和仓库信息"""
    if '@' in skill_str:
        parts = skill_str.split('@')
        skill_name = parts[0]
        repo = parts[1]
        return skill_name, repo
    return None, skill_str


def _view_skill_md_online(stdscr, skill_str):
    """从线上查看SKILL.md"""
    skill_name, repo = _parse_skill_info(skill_str)

    if not skill_name or not repo:
        stdscr.clear()
        stdscr.addstr(0, 0, "无法解析技能信息")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return

    repo_parts = repo.split('/')
    if len(repo_parts) != 2:
        stdscr.clear()
        stdscr.addstr(0, 0, "无效的仓库格式")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return

    owner, repo_name = repo_parts
    url = skill_md_url.format(owner=owner, repo=repo_name, skill_name=skill_name)

    stdscr.clear()
    stdscr.addstr(0, 0, f"正在下载: {url}")
    stdscr.addstr(1, 0, "请稍候...")
    stdscr.refresh()

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
        _show_file_content(stdscr, f"SKILL.md - {skill_str}", content)
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"下载失败: {e}")
        stdscr.addstr(2, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()


def _show_file_content(stdscr, title, content):
    """显示文件内容，支持翻页"""
    lines = content.split('\n')
    current_line = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title)

        height, width = stdscr.getmaxyx()
        display_lines = height - 3
        end_line = min(current_line + display_lines, len(lines))

        for i in range(current_line, end_line):
            if i < len(lines):
                line_content = lines[i][:width - 1]
                stdscr.addstr(i - current_line + 2, 0, line_content)

        position_info = f"第 {current_line + 1}-{end_line} 行，共 {len(lines)} 行 (上下箭头翻页, ESC返回)"
        stdscr.addstr(height - 1, 0, position_info[:width - 1])
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
            break
        elif key == curses.KEY_UP:
            if current_line > 0:
                current_line = max(0, current_line - 1)
        elif key == curses.KEY_DOWN:
            if current_line + display_lines < len(lines):
                current_line += 1
        elif key == curses.KEY_PPAGE:
            current_line = max(0, current_line - display_lines)
        elif key == curses.KEY_NPAGE:
            current_line = min(len(lines) - display_lines, current_line + display_lines)


def _install_skill_only(stdscr, skill_str):
    """仅安装skill到 ~/.skill-hub"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"正在安装: {skill_str}")
    stdscr.addstr(1, 0, "请稍候...")
    stdscr.refresh()

    try:
        import sys
        original_stdout = sys.stdout
        output_buffer = io.StringIO()

        def print_to_buffer(*args, **kwargs):
            output_buffer.write(' '.join(str(arg) for arg in args) + '\n')

        sys.stdout = print_to_buffer
        try:
            install_skill(skill_str, force_update=False)
        finally:
            sys.stdout = original_stdout

        output = output_buffer.getvalue()
        stdscr.clear()
        stdscr.addstr(0, 0, "安装完成:")
        line_num = 1
        for line in output.split('\n'):
            if line:
                stdscr.addstr(line_num, 0, line[:79])  # 限制每行最多80字符
                line_num += 1
        if line_num == 1:
            stdscr.addstr(0, 0, "安装完成（无输出信息）")
        stdscr.addstr(line_num + 1, 0, "按任意键返回...")
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"安装失败: {e}")
        stdscr.addstr(1, 0, "按任意键返回...")

    stdscr.refresh()
    stdscr.getch()


def _install_and_sync_to_project(stdscr, skill_str):
    """安装skill并同步到项目"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"正在安装: {skill_str}")
    stdscr.addstr(1, 0, "请稍候...")
    stdscr.refresh()

    try:
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            install_skill(skill_str, force_update=False)
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"安装失败: {e}")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return

    installed_agents = get_installed_agents()
    project_agents = get_project_installed_agents()

    selected_agents = _show_multi_select_menu(
        stdscr,
        "选择要同步到项目的Agents",
        installed_agents,
        project_agents
    )

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
            except Exception:
                error_occurred = True

        stdscr.clear()
        if error_occurred:
            stdscr.addstr(0, 0, "部分同步操作失败")
        else:
            stdscr.addstr(0, 0, "安装并同步完成！")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "安装完成，但未选择同步目标")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()


def _install_and_sync_to_global(stdscr, skill_str):
    """安装skill并同步到全局"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"正在安装: {skill_str}")
    stdscr.addstr(1, 0, "请稍候...")
    stdscr.refresh()

    try:
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            install_skill(skill_str, force_update=False)
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"安装失败: {e}")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return

    installed_agents = get_installed_agents()
    global_agents = get_global_installed_agents()

    selected_agents = _show_multi_select_menu(
        stdscr,
        "选择要同步到全局的Agents",
        installed_agents,
        global_agents
    )

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
            except Exception:
                error_occurred = True

        stdscr.clear()
        if error_occurred:
            stdscr.addstr(0, 0, "部分同步操作失败")
        else:
            stdscr.addstr(0, 0, "安装并同步完成！")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "安装完成，但未选择同步目标")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()


def _install_repo_only(stdscr, repo_str):
    """仅安装repo到 ~/.skill-hub"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"正在更新仓库: {repo_str}")
    stdscr.addstr(1, 0, "请稍候...")
    stdscr.refresh()

    try:
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            install_skill(repo_str, force_update=True)

        stdscr.clear()
        stdscr.addstr(0, 0, f"更新完成: {repo_str}")
        stdscr.addstr(1, 0, "按任意键返回...")
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"更新失败: {e}")
        stdscr.addstr(1, 0, "按任意键返回...")

    stdscr.refresh()
    stdscr.getch()


def _install_repo_and_sync_to_project(stdscr, repo_str):
    """安装repo并同步到项目"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"正在更新仓库: {repo_str}")
    stdscr.addstr(1, 0, "请稍候...")
    stdscr.refresh()

    try:
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            install_skill(repo_str, force_update=True)
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"更新失败: {e}")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return

    installed_agents = get_installed_agents()
    project_agents = get_project_installed_agents()

    selected_agents = _show_multi_select_menu(
        stdscr,
        "选择要同步到项目的Agents",
        installed_agents,
        project_agents
    )

    if selected_agents:
        stdscr.clear()
        stdscr.addstr(0, 0, "正在同步...")
        stdscr.refresh()

        error_occurred = False
        for agent in selected_agents:
            try:
                sync_skill_single(
                    agent_name=agent,
                    target=repo_str,
                    project_level=True,
                    global_level=False,
                    force_sync=True
                )
            except Exception:
                error_occurred = True

        stdscr.clear()
        if error_occurred:
            stdscr.addstr(0, 0, "部分同步操作失败")
        else:
            stdscr.addstr(0, 0, "更新并同步完成！")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "更新完成，但未选择同步目标")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()


def _install_repo_and_sync_to_global(stdscr, repo_str):
    """安装repo并同步到全局"""
    stdscr.clear()
    stdscr.addstr(0, 0, f"正在更新仓库: {repo_str}")
    stdscr.addstr(1, 0, "请稍候...")
    stdscr.refresh()

    try:
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            install_skill(repo_str, force_update=True)
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"更新失败: {e}")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
        return

    installed_agents = get_installed_agents()
    global_agents = get_global_installed_agents()

    selected_agents = _show_multi_select_menu(
        stdscr,
        "选择要同步到全局的Agents",
        installed_agents,
        global_agents
    )

    if selected_agents:
        stdscr.clear()
        stdscr.addstr(0, 0, "正在同步...")
        stdscr.refresh()

        error_occurred = False
        for agent in selected_agents:
            try:
                sync_skill_single(
                    agent_name=agent,
                    target=repo_str,
                    project_level=False,
                    global_level=True,
                    force_sync=True
                )
            except Exception:
                error_occurred = True

        stdscr.clear()
        if error_occurred:
            stdscr.addstr(0, 0, "部分同步操作失败")
        else:
            stdscr.addstr(0, 0, "更新并同步完成！")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "更新完成，但未选择同步目标")
        stdscr.addstr(1, 0, "按任意键返回...")
        stdscr.refresh()
        stdscr.getch()


def _show_multi_select_menu(stdscr, title, all_items, selected_items):
    """显示多选菜单"""
    curses.curs_set(0)
    current_row = 0
    scroll_offset = 0
    selected_flags = [item in selected_items for item in all_items]

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title)

        height, width = stdscr.getmaxyx()
        max_display_items = height - 4

        start_idx = scroll_offset
        end_idx = min(scroll_offset + max_display_items, len(all_items))

        for i in range(start_idx, end_idx):
            marker = "[x]" if selected_flags[i] else "[ ]"
            display_row = i - scroll_offset
            display_text = f"  {marker} {all_items[i]}"

            if i == current_row:
                display_text = f"> {marker} {all_items[i]}"
                stdscr.addstr(display_row + 2, 0, display_text, curses.A_REVERSE)
            else:
                stdscr.addstr(display_row + 2, 0, display_text)

        stdscr.addstr(min(max_display_items + 3, height - 1), 0, "(上下箭头移动, 空格键选择/取消, 回车确认, ESC返回)")
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
            return []
        elif key == curses.KEY_UP:
            if current_row > 0:
                current_row -= 1
                if current_row < scroll_offset:
                    scroll_offset = current_row
        elif key == curses.KEY_DOWN:
            if current_row < len(all_items) - 1:
                current_row += 1
                if current_row >= scroll_offset + max_display_items:
                    scroll_offset = current_row - max_display_items + 1
        elif key == ord(' '):
            selected_flags[current_row] = not selected_flags[current_row]
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
            return [all_items[i] for i in range(len(all_items)) if selected_flags[i]]
