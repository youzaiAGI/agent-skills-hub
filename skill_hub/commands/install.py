"""
安装技能命令模块
"""

import os
import subprocess
import shutil
from pathlib import Path
import tempfile
import requests
from urllib.parse import urljoin
import sys
from io import StringIO
import threading
import queue


def install_skill(target=None, force_update=False):
    """
    安装skill
    :param target: 要安装的目标 (格式: skill@repo 或 repo)，或者文件路径
    :param force_update: 是否强制更新
    """
    if not target:
        print("请指定要安装的目标 (格式: skill@repo 或 repo)，或提供包含目标列表的文件路径")
        return

    # 检查target是否为文件路径
    target_path = Path(target)
    # 检查是否为绝对路径或相对路径的文件
    if target_path.exists() and target_path.is_file():
        # 如果target是文件，则从文件读取安装目标
        install_from_file(target_path, force_update)
        return
    
    # 如果不是文件路径，则按照原来的逻辑处理单个目标
    if '@' in target:
        # 格式为 skill@repo
        skill_name, repo = target.split('@', 1)
        install_specific_skill(skill_name, repo, force_update)
    else:
        # 格式为 repo，格式为 owner/repo_name
        repo = target
        install_all_skills_from_repo(repo, force_update)


def install_from_file(file_path, force_update=False):
    """从文件读取目标列表并安装"""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not targets:
        print(f"文件 {file_path} 中没有找到有效的安装目标")
        return
    
    print(f"从文件 {file_path} 读取到 {len(targets)} 个安装目标")
    
    for target in targets:
        print(f"\n正在处理: {target}")
        if '@' in target:
            # 格式为 skill@repo
            skill_name, repo = target.split('@', 1)
            install_specific_skill(skill_name, repo, force_update)
        else:
            # 格式为 repo，格式为 owner/repo_name
            repo = target
            install_all_skills_from_repo(repo, force_update)


def install_all_skills_from_repo(repo, force_update=False):
    """安装指定仓库的所有skill"""
    skill_hub_dir = Path.home() / '.skill-hub'
    
    # 解析 repo 为 owner/repo_name 格式
    repo_parts = repo.split('/')
    if len(repo_parts) != 2:
        print(f"无效的仓库格式: {repo}，应为 owner/repo_name 格式")
        return
    
    owner, repo_name = repo_parts
    repo_dir = skill_hub_dir / owner / repo_name
    
    # 如果存在且不是强制更新，则跳过
    if repo_dir.exists() and not force_update:
        print(f"仓库 {repo} 已存在，跳过安装。使用 -u 参数强制更新。")
        return
    
    # 如果是强制更新，删除已存在的目录
    if force_update and repo_dir.exists():
        print(f"正在删除旧的仓库 {repo}...")
        shutil.rmtree(repo_dir)
    
    # 创建目录
    repo_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"正在安装仓库 {repo} 的所有技能...")
    
    # 从GitHub克隆仓库到临时目录
    temp_dir = Path(tempfile.mkdtemp())
    try:
        repo_url = f"https://github.com/{repo}"
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', '--quiet', repo_url, str(temp_dir)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60  # 60秒超时
        )
        
        # 检查根目录是否有SKILL.md，如果有则将整个仓库作为一个技能
        root_skill_md = temp_dir / 'SKILL.md'
        if root_skill_md.exists():
            skill_name = repo_name  # 使用仓库名作为技能名
            target_skill_dir = repo_dir / skill_name  # 创建子目录，保持与install_specific_skill一致
            # 清空目标目录并复制内容
            if target_skill_dir.exists():
                shutil.rmtree(target_skill_dir)
            target_skill_dir.mkdir(parents=True, exist_ok=True)
            for item in temp_dir.iterdir():
                dest_item = target_skill_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest_item)
                else:
                    shutil.copy2(item, dest_item)
            print(f"已安装技能: {skill_name}@{repo}")
        else:
            # 查找带有SKILL.md的子目录
            for root, dirs, files in os.walk(temp_dir):
                if 'SKILL.md' in files:
                    skill_dir = Path(root)
                    skill_name = skill_dir.name
                    
                    target_skill_dir = repo_dir / skill_name
                    if not target_skill_dir.exists():
                        # 复制技能目录
                        shutil.copytree(skill_dir, target_skill_dir)
                        print(f"已安装技能: {skill_name}@{repo}")
                    else:
                        print(f"技能 {skill_name}@{repo} 已存在")
    except subprocess.CalledProcessError as e:
        print(f"无法克隆仓库 {repo}: {e}")
        print(f"错误输出: {e.stderr.decode() if hasattr(e, 'stderr') else 'N/A'}")
    except subprocess.TimeoutExpired:
        print(f"克隆仓库 {repo} 超时（60秒）")
    except Exception as e:
        print(f"安装仓库 {repo} 时出错: {e}")
    finally:
        # 清理临时目录
        try:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        except:
            pass  # 如果临时目录清理失败，忽略错误


def install_specific_skill(skill_name, repo, force_update=False):
    """安装指定仓库的指定skill"""
    skill_hub_dir = Path.home() / '.skill-hub'
    
    # 解析 repo 为 owner/repo_name 格式
    repo_parts = repo.split('/')
    if len(repo_parts) != 2:
        print(f"无效的仓库格式: {repo}，应为 owner/repo_name 格式")
        return
    
    owner, repo_name = repo_parts
    skill_dir = skill_hub_dir / owner / repo_name / skill_name
    
    # 如果存在且不是强制更新，则跳过
    if skill_dir.exists() and not force_update:
        print(f"技能 {skill_name}@{repo} 已存在，跳过安装。使用 -u 参数强制更新。")
        return
    
    # 如果是强制更新，删除已存在的目录
    if force_update and skill_dir.exists():
        print(f"正在删除旧的技能 {skill_name}@{repo}...")
        shutil.rmtree(skill_dir)
    
    # 创建目录
    skill_dir.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"正在安装技能 {skill_name}@{repo}...")
    
    # 从GitHub克隆仓库到临时目录
    temp_dir = Path(tempfile.mkdtemp())
    try:
        repo_url = f"https://github.com/{repo}"
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', '--quiet', repo_url, str(temp_dir)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60  # 60秒超时
        )
        
        # 检查根目录是否有SKILL.md，如果是请求的技能名匹配仓库名，则使用整个仓库
        root_skill_md = temp_dir / 'SKILL.md'
        if root_skill_md.exists() and skill_name == repo_name:
            # 将临时目录的所有内容直接复制到目标位置
            skill_dir.parent.mkdir(parents=True, exist_ok=True)  # 确保父目录存在
            if skill_dir.exists():
                # 先清空目标目录
                shutil.rmtree(skill_dir)
            # 创建目标目录并复制内容
            skill_dir.mkdir(parents=True, exist_ok=True)
            for item in temp_dir.iterdir():
                dest_item = skill_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest_item)
                else:
                    shutil.copy2(item, dest_item)
            print(f"已安装技能: {skill_name}@{repo}")
        else:
            # 在仓库中查找指定的技能目录
            found = False
            for root, dirs, files in os.walk(temp_dir):
                if Path(root).name == skill_name and 'SKILL.md' in files:
                    source_skill_dir = Path(root)
                    # 复制技能目录
                    shutil.copytree(source_skill_dir, skill_dir)
                    print(f"已安装技能: {skill_name}@{repo}")
                    found = True
                    break
            
            if not found:
                print(f"在仓库 {repo} 中未找到技能 {skill_name} 或该技能没有SKILL.md文件")
                # 如果创建了目录但没找到技能，删除空目录
                if skill_dir.exists() and not any(skill_dir.iterdir()):
                    skill_dir.rmdir()
    except subprocess.CalledProcessError as e:
        print(f"无法克隆仓库 {repo}: {e}")
        print(f"错误输出: {e.stderr.decode() if hasattr(e, 'stderr') else 'N/A'}")
    except subprocess.TimeoutExpired:
        print(f"克隆仓库 {repo} 超时（60秒）")
    except Exception as e:
        print(f"安装技能 {skill_name}@{repo} 时出错: {e}")
    finally:
        # 清理临时目录
        try:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        except:
            pass  # 如果临时目录清理失败，忽略错误


def install_all_skills_from_repo_silent(repo, force_update=False):
    """静默安装指定仓库的所有skill（不输出到终端）"""
    # 保存原始stdout
    original_stdout = sys.stdout
    
    # 创建一个StringIO对象来捕获输出
    captured_output = StringIO()
    
    # 用于捕获异常
    exception_occurred = None
    
    try:
        # 重定向stdout到StringIO
        sys.stdout = captured_output
        
        # 调用正常的安装函数
        install_all_skills_from_repo(repo, force_update)
        
    except Exception as e:
        # 记录异常但不立即抛出
        exception_occurred = e
    finally:
        # 恢复原始stdout
        sys.stdout = original_stdout
        
        # 获取捕获的输出
        output = captured_output.getvalue()
        
        # 如果有异常，现在才抛出
        if exception_occurred:
            raise exception_occurred
        
        # 返回捕获的输出
        return output


def install_specific_skill_silent(skill_name, repo, force_update=False):
    """静默安装指定仓库的指定skill（不输出到终端）"""
    # 保存原始stdout
    original_stdout = sys.stdout
    
    # 创建一个StringIO对象来捕获输出
    captured_output = StringIO()
    
    # 用于捕获异常
    exception_occurred = None
    
    try:
        # 重定向stdout到StringIO
        sys.stdout = captured_output
        
        # 调用正常的安装函数
        install_specific_skill(skill_name, repo, force_update)
        
    except Exception as e:
        # 记录异常但不立即抛出
        exception_occurred = e
    finally:
        # 恢复原始stdout
        sys.stdout = original_stdout
        
        # 获取捕获的输出
        output = captured_output.getvalue()
        
        # 如果有异常，现在才抛出
        if exception_occurred:
            raise exception_occurred
        
        # 返回捕获的输出
        return output