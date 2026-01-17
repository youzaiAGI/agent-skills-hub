"""
查看技能仓库列表命令模块
"""

import requests
import curses
from pathlib import Path
import threading
import queue


def show_repo_list():
    """查看skill仓库列表"""
    try:
        # 获取仓库列表
        response = requests.get('https://skill-hub.oss-cn-shanghai.aliyuncs.com/repo.sort')
        repos = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
        
        if not repos:
            print("没有找到可用的仓库")
            return
        
        # 启动交互界面
        curses.wrapper(lambda stdscr: _repo_selection_ui(stdscr, repos))
        
    except Exception as e:
        print(f"获取仓库列表失败: {e}")


def _repo_selection_ui(stdscr, repos):
    """仓库选择交互界面"""
    # 初始化curses
    curses.curs_set(0)  # 隐藏光标
    stdscr.nodelay(0)
    stdscr.timeout(-1)  # 阻塞等待输入
    
    current_row = 0
    search_text = ""
    filtered_repos = repos[:]
    
    while True:
        stdscr.clear()
        
        # 获取屏幕尺寸
        height, width = stdscr.getmaxyx()
        
        # 显示标题和搜索框
        stdscr.addstr(0, 0, "选择仓库 (ESC 退出, 回车安装, 输入搜索):")
        
        # 截断搜索文本以适应屏幕宽度
        display_search = search_text + "_"
        if len(display_search) > width - 9:  # 9是"搜索: "的长度
            display_search = display_search[:width - 9]
        
        stdscr.addstr(1, 0, f"搜索: {display_search}")
        
        # 根据搜索文本过滤仓库列表
        if search_text:
            filtered_repos = [repo for repo in repos if search_text.lower() in repo.lower()]
        else:
            filtered_repos = repos[:]
        
        # 显示仓库列表，确保不超过屏幕高度
        max_display_items = height - 4  # 留出标题和搜索框的空间
        for idx in range(min(len(filtered_repos), max_display_items)):
            repo = filtered_repos[idx]
            prefix = "> " if idx == current_row else "  "
            try:
                if idx == current_row:
                    stdscr.addstr(idx + 3, 0, prefix + repo, curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 3, 0, prefix + repo)
            except:
                # 如果添加字符串失败（例如超出边界），则跳过
                break
        
        stdscr.refresh()
        
        # 获取用户输入
        key = stdscr.getch()
        
        # 处理ESC键退出
        if key == 27:  # ESC键
            break
        # 处理回车键安装
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
            if filtered_repos and len(filtered_repos) > current_row >= 0:
                selected_repo = filtered_repos[current_row]
                
                # 创建队列用于线程间通信
                result_queue = queue.Queue()
                
                def install_worker():
                    try:
                        # 执行静默安装
                        from skill_hub.commands.install import install_all_skills_from_repo_silent
                        install_all_skills_from_repo_silent(selected_repo)
                        result_queue.put(('success', f"仓库 {selected_repo} 安装完成"))
                    except Exception as e:
                        result_queue.put(('error', f"安装失败: {str(e)}"))
                
                # 启动安装线程
                install_thread = threading.Thread(target=install_worker)
                install_thread.daemon = True
                install_thread.start()
                
                # 显示安装进度
                stdscr.clear()
                stdscr.addstr(0, 0, f"正在安装仓库: {selected_repo}")
                stdscr.addstr(2, 0, "请稍候...")
                stdscr.refresh()
                
                # 等待安装完成
                install_thread.join(timeout=60)  # 60秒超时
                
                stdscr.clear()
                if install_thread.is_alive():
                    stdscr.addstr(0, 0, "安装超时，请稍后重试")
                else:
                    try:
                        status, message = result_queue.get_nowait()
                        stdscr.addstr(0, 0, message)
                    except queue.Empty:
                        stdscr.addstr(0, 0, "安装完成")
                
                stdscr.addstr(2, 0, "按任意键继续...")
                stdscr.refresh()
                stdscr.getch()
        # 处理字母数字搜索
        elif 32 <= key <= 126:  # ASCII字符范围
            search_text += chr(key)
            current_row = 0  # 重置选中项
        # 处理退格键
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            search_text = search_text[:-1]
            current_row = 0  # 重置选中项
        # 处理方向键
        elif key == curses.KEY_UP:
            current_row = max(0, current_row - 1)
        elif key == curses.KEY_DOWN:
            current_row = min(len(filtered_repos) - 1, current_row + 1)
        # 处理其他控制键
        elif key == curses.KEY_DC:  # Delete键
            search_text = ""
            current_row = 0