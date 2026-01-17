"""
搜索技能命令模块 - 包含技能搜索和仓库列表功能
"""

import requests
import curses
from pathlib import Path
import threading
import queue


def search_skills():
    """搜索skill和repo的综合界面"""
    try:
        # 获取技能列表
        skill_response = requests.get('https://skill-hub.oss-cn-shanghai.aliyuncs.com/skill.list')
        skills = [line.strip() for line in skill_response.text.strip().split('\n') if line.strip()]
        
        # 获取仓库列表
        repo_response = requests.get('https://skill-hub.oss-cn-shanghai.aliyuncs.com/repo.sort')
        repos = [line.strip() for line in repo_response.text.strip().split('\n') if line.strip()]
        
        # 启动交互界面
        curses.wrapper(lambda stdscr: _combined_selection_ui(stdscr, skills, repos))
        
    except Exception as e:
        print(f"获取数据失败: {e}")


def _combined_selection_ui(stdscr, skills, repos):
    """组合选择交互界面，包含技能和仓库标签页"""
    # 初始化curses
    curses.curs_set(0)  # 隐藏光标
    stdscr.nodelay(0)
    stdscr.timeout(-1)  # 阻塞等待输入
    
    # 当前选中的标签页 (0: skills, 1: repos)
    current_tab = 0
    
    # 每个标签页的当前选中行
    current_rows = [0, 0]
    
    # 每个标签页的搜索文本
    search_texts = ["", ""]
    
    # 每个标签页的过滤结果
    filtered_lists = [skills[:], repos[:]]
    
    while True:
        stdscr.clear()
        
        # 获取屏幕尺寸
        height, width = stdscr.getmaxyx()
        
        # 显示标签页
        tab_titles = ["Skills", "Repos"]
        for i, title in enumerate(tab_titles):
            tab_text = f"[{title}]" if i == current_tab else f" {title} "
            stdscr.addstr(0, i * 10, tab_text, curses.A_REVERSE if i == current_tab else 0)
        
        # 显示说明文字
        stdscr.addstr(0, width - 25, "(左右箭头切换, ESC退出)")
        
        # 获取当前标签页的数据
        current_list = filtered_lists[current_tab]
        current_search = search_texts[current_tab]
        current_row = current_rows[current_tab]
        
        # 显示搜索框
        stdscr.addstr(1, 0, f"搜索: {current_search}_")
        
        # 显示列表内容，确保不超过屏幕高度
        max_display_items = height - 4  # 留出标题、搜索框和底部说明的空间
        for idx in range(min(len(current_list), max_display_items)):
            item = current_list[idx]
            prefix = "> " if idx == current_row else "  "
            try:
                if idx == current_row:
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
            current_tab = 0
        elif key == curses.KEY_RIGHT:
            current_tab = 1
        # 处理回车键安装
        elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
            if current_list and len(current_list) > current_row >= 0:
                selected_item = current_list[current_row]
                
                # 创建队列用于线程间通信
                result_queue = queue.Queue()
                
                def install_worker():
                    try:
                        if current_tab == 0:  # Skills标签页
                            # 执行技能静默安装
                            from skill_hub.commands.install import install_specific_skill
                            if '@' in selected_item:
                                skill_name, repo = selected_item.split('@', 1)
                                # 如果repo部分包含\t分隔符，取第一部分
                                real_repo = repo.split('\t')[0]
                                install_specific_skill(skill_name, real_repo)
                            result_queue.put(('success', f"技能 {selected_item} 安装完成"))
                        else:  # Repos标签页
                            # 执行仓库静默安装
                            from skill_hub.commands.install import install_all_skills_from_repo
                            # 按\t分割并取第一部分作为真实的仓库名
                            real_repo = selected_item.split('\t')[0]
                            install_all_skills_from_repo(real_repo)
                            result_queue.put(('success', f"仓库 {selected_item} 安装完成"))
                    except Exception as e:
                        result_queue.put(('error', f"安装失败: {str(e)}"))
                
                # 启动安装线程
                install_thread = threading.Thread(target=install_worker)
                install_thread.daemon = True
                install_thread.start()
                
                # 显示安装进度
                stdscr.clear()
                stdscr.addstr(0, 0, f"正在安装{'技能' if current_tab == 0 else '仓库'}: {selected_item}")
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
            search_texts[current_tab] += chr(key)
            current_rows[current_tab] = 0  # 重置选中项
            # 更新过滤列表
            if current_tab == 0:  # Skills标签页
                if search_texts[current_tab]:
                    filtered_lists[0] = [skill for skill in skills if search_texts[current_tab].lower() in skill.lower()]
                else:
                    filtered_lists[0] = skills[:]
            else:  # Repos标签页
                if search_texts[current_tab]:
                    filtered_lists[1] = [repo for repo in repos if search_texts[current_tab].lower() in repo.lower()]
                else:
                    filtered_lists[1] = repos[:]
        # 处理退格键
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            search_texts[current_tab] = search_texts[current_tab][:-1]
            current_rows[current_tab] = 0  # 重置选中项
            # 更新过滤列表
            if current_tab == 0:  # Skills标签页
                if search_texts[current_tab]:
                    filtered_lists[0] = [skill for skill in skills if search_texts[current_tab].lower() in skill.lower()]
                else:
                    filtered_lists[0] = skills[:]
            else:  # Repos标签页
                if search_texts[current_tab]:
                    filtered_lists[1] = [repo for repo in repos if search_texts[current_tab].lower() in repo.lower()]
                else:
                    filtered_lists[1] = repos[:]
        # 处理方向键
        elif key == curses.KEY_UP:
            current_rows[current_tab] = max(0, current_rows[current_tab] - 1)
        elif key == curses.KEY_DOWN:
            if current_tab == 0:  # Skills标签页
                current_rows[current_tab] = min(len(filtered_lists[0]) - 1, current_rows[current_tab] + 1)
            else:  # Repos标签页
                current_rows[current_tab] = min(len(filtered_lists[1]) - 1, current_rows[current_tab] + 1)
        # 处理其他控制键
        elif key == curses.KEY_DC:  # Delete键
            search_texts[current_tab] = ""
            current_rows[current_tab] = 0
            # 重置过滤列表
            if current_tab == 0:  # Skills标签页
                filtered_lists[0] = skills[:]
            else:  # Repos标签页
                filtered_lists[1] = repos[:]