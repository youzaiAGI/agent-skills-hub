import curses


def _wrap_line(line, width):
    """将长行按宽度自动换行"""
    # 处理制表符
    line = line.replace('\t', '  ')
    if width <= 1:
        return [line] if line else []

    result = []
    current_line = line
    while len(current_line) > width:
        # 尝试在空格处换行
        break_pos = current_line.rfind(' ', 0, width)
        if break_pos > 0:
            result.append(current_line[:break_pos])
            current_line = current_line[break_pos + 1:]  # 跳过空格
        else:
            # 没有空格，强制在width处截断
            result.append(current_line[:width])
            current_line = current_line[width:]
    if current_line:
        result.append(current_line)
    return result or []


def _display_wrapped_lines(stdscr, lines, start_row, height, width):
    """显示自动换行后的多行，返回实际使用的行数"""
    display_row = start_row
    for line in lines:
        wrapped_lines = _wrap_line(line, width)
        for wrapped_line in wrapped_lines:
            if display_row >= height - 1:
                break
            # 确保不超过终端宽度，避免 curses 错误
            safe_line = wrapped_line[:width]
            try:
                stdscr.addstr(display_row, 0, safe_line)
                display_row += 1
            except:
                break
    return display_row - start_row


def show_file_content(stdscr, title, content):
    """显示文件内容，支持翻页和自动换行"""
    lines = content.split('\n')
    current_line = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title)

        height, width = stdscr.getmaxyx()
        display_lines = height - 3
        end_line = min(current_line + display_lines, len(lines))

        display_row = 2
        for i in range(current_line, end_line):
            display_row += _display_wrapped_lines(stdscr, [lines[i]], display_row, height, width)

        position_info = f"第 {current_line + 1}-{end_line} 行，共 {len(lines)} 行 (ESC返回)"
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
