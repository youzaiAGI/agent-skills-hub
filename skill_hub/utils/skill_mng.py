
skills_url = 'https://skill-hub.oss-cn-shanghai.aliyuncs.com/skill.list'
repos_url = 'https://skill-hub.oss-cn-shanghai.aliyuncs.com/repo.sort'

import os
import requests
from pathlib import Path
import time
import subprocess

skill_hub_dir = Path.home() / '.skill-hub'

def download_skill_files(file_path):
    """下载技能列表和仓库排序文件到 ~/.skill-hub 目录"""
    skill_hub_dir.mkdir(exist_ok=True)
    
    files_to_download = {
        'skill.list': skills_url,
        'repo.sort': repos_url
    }

    filename = file_path.name
    url = files_to_download.get(filename, '')

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"成功下载 {filename} 到 {file_path}")
    except Exception as e:
        print(f"下载 {filename} 时出错: {e}")

def _search(skill_file_path, search="", page=1, size=50):
    """搜索技能文件中的技能，返回 (结果列表, 总数)"""
    if not skill_file_path.exists():
        # 如果文件不存在，下载文件
        download_skill_files(skill_file_path)
    else:
        # 检查文件修改时间，如果超过24小时则重新下载
        file_modified_time = skill_file_path.stat().st_mtime
        current_time = time.time()
        if current_time - file_modified_time > 24 * 60 * 60:  # 24小时 = 24 * 60 * 60 秒
            download_skill_files(skill_file_path)

    try:
        # 计算分页起始位置
        start_index = (page - 1) * size
        end_index = start_index + size
        if search:
            # 使用grep搜索包含关键词的行
            result = subprocess.run(['grep', '-i', search, str(skill_file_path)],
                                  capture_output=True, text=True)
            all_matching_lines = result.stdout.strip().split('\n') if result.stdout else []
            # 过滤空行
            all_matching_lines = [line for line in all_matching_lines if line.strip()]
        else:
            # 读取所有行
            with open(skill_file_path, 'r', encoding='utf-8') as f:
                all_matching_lines = [line.strip() for line in f.readlines() if line.strip()]

        total_count = len(all_matching_lines)

        # 根据分页参数选择对应的数据
        selected_lines = all_matching_lines[start_index:end_index]

        # 返回结果和总数
        return selected_lines, total_count

    except Exception as e:
        print(f"读取技能文件时出错: {e}")
        return [], 0

def get_skills(search = "", page=1, size=50):
    # 读取 skill_hub_dir / skill.list 文件
    skill_file_path = skill_hub_dir / 'skill.list'
    return _search(skill_file_path, search, page, size)

def get_repos(search = "", page=1, size=50):
    # 读取 skill_hub_dir / repo.sort 文件
    skill_file_path = skill_hub_dir / 'repo.sort'
    return _search(skill_file_path, search, page, size)

if __name__ == "__main__":  
    print(get_repos("", 2, 3))
