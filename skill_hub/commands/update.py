"""
更新技能命令模块
"""

import os
import shutil
import tempfile
import subprocess
from pathlib import Path
import requests


def update_skill(target=None):
    """
    更新skill
    :param target: 要更新的目标 (格式: skill@repo 或 repo)
    """
    if not target:
        print("请指定要更新的目标 (格式: skill@repo 或 repo)")
        return

    # 解析目标
    if '@' in target:
        # 格式为 skill@repo
        skill_name, repo = target.split('@', 1)
        update_specific_skill(skill_name, repo)
    else:
        # 格式为 repo，格式为 owner/repo_name
        repo = target
        update_all_skills_from_repo(repo)


def update_all_skills_from_repo(repo):
    """更新指定仓库的所有skill"""
    skill_hub_dir = Path.home() / '.skill-hub'
    
    # 解析 repo 为 owner/repo_name 格式
    repo_parts = repo.split('/')
    if len(repo_parts) != 2:
        print(f"无效的仓库格式: {repo}，应为 owner/repo_name 格式")
        return
    
    owner, repo_name = repo_parts
    repo_dir = skill_hub_dir / owner / repo_name
    
    print(f"正在更新仓库 {repo} 的所有技能...")
    
    # 从远程获取技能列表
    try:
        response = requests.get('https://skill-hub.oss-cn-shanghai.aliyuncs.com/skill.list')
        skill_list = response.text.strip().split('\n')
        
        # 过滤出属于当前仓库的技能
        repo_skills = []
        for skill in skill_list:
            if skill.endswith(f'@{repo}'):
                skill_name = skill.split('@')[0]
                repo_skills.append(skill_name)
        
        # 为每个技能创建或更新目录
        for skill_name in repo_skills:
            # 如果是整个仓库作为技能的情况
            if skill_name == repo_name:
                skill_dir = repo_dir  # 直接使用仓库目录
            else:
                skill_dir = repo_dir / skill_name  # 子技能目录
            
            # 如果存在则删除后重新创建
            if skill_dir.exists():
                shutil.rmtree(skill_dir)
            
            # 从GitHub克隆仓库到临时目录并复制技能
            temp_dir = Path(tempfile.mkdtemp())
            try:
                repo_url = f"https://github.com/{repo}"
                result = subprocess.run(
                    ['git', 'clone', repo_url, str(temp_dir)],
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
                    skill_dir.mkdir(parents=True, exist_ok=True)  # 创建目标目录
                    for item in temp_dir.iterdir():
                        dest_item = skill_dir / item.name
                        if item.is_dir():
                            shutil.copytree(item, dest_item)
                        else:
                            shutil.copy2(item, dest_item)
                    print(f"已更新技能: {skill_name}@{repo}")
                else:
                    # 在仓库中查找指定的技能目录
                    found = False
                    for root, dirs, files in os.walk(temp_dir):
                        if Path(root).name == skill_name and 'SKILL.md' in files:
                            source_skill_dir = Path(root)
                            # 复制技能目录
                            shutil.copytree(source_skill_dir, skill_dir)
                            print(f"已更新技能: {skill_name}@{repo}")
                            found = True
                            break
                    
                    if not found:
                        print(f"在仓库 {repo} 中未找到技能 {skill_name}")
                        # 如果创建了目录但没找到技能，删除空目录
                        if skill_dir.exists() and not any(skill_dir.iterdir()):
                            skill_dir.rmdir()
            except subprocess.CalledProcessError as e:
                print(f"无法克隆仓库 {repo}: {e}")
                print(f"错误输出: {e.stderr.decode() if hasattr(e, 'stderr') else 'N/A'}")
            except subprocess.TimeoutExpired:
                print(f"克隆仓库 {repo} 超时（60秒）")
            except Exception as e:
                print(f"更新技能 {skill_name}@{repo} 时出错: {e}")
            finally:
                # 清理临时目录
                try:
                    if temp_dir.exists():
                        shutil.rmtree(temp_dir)
                except:
                    pass  # 如果临时目录清理失败，忽略错误
                    
    except Exception as e:
        print(f"获取技能列表失败: {e}")


def update_specific_skill(skill_name, repo):
    """更新指定仓库的指定skill"""
    skill_hub_dir = Path.home() / '.skill-hub'
    
    # 解析 repo 为 owner/repo_name 格式
    repo_parts = repo.split('/')
    if len(repo_parts) != 2:
        print(f"无效的仓库格式: {repo}，应为 owner/repo_name 格式")
        return
    
    owner, repo_name = repo_parts
    skill_dir = skill_hub_dir / owner / repo_name / skill_name
    
    print(f"正在更新技能 {skill_name}@{repo}...")
    
    # 如果存在则删除后重新创建
    if skill_dir.exists():
        shutil.rmtree(skill_dir)
    
    # 创建父目录
    skill_dir.parent.mkdir(parents=True, exist_ok=True)
    
    # 从GitHub克隆仓库到临时目录
    temp_dir = Path(tempfile.mkdtemp())
    try:
        repo_url = f"https://github.com/{repo}"
        result = subprocess.run(
            ['git', 'clone', repo_url, str(temp_dir)],
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
            skill_dir.mkdir(parents=True, exist_ok=True)  # 创建目标目录
            for item in temp_dir.iterdir():
                dest_item = skill_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest_item)
                else:
                    shutil.copy2(item, dest_item)
            print(f"已更新技能: {skill_name}@{repo}")
        else:
            # 在仓库中查找指定的技能目录
            found = False
            for root, dirs, files in os.walk(temp_dir):
                if Path(root).name == skill_name and 'SKILL.md' in files:
                    source_skill_dir = Path(root)
                    # 复制技能目录
                    shutil.copytree(source_skill_dir, skill_dir)
                    print(f"已更新技能: {skill_name}@{repo}")
                    found = True
                    break
            
            if not found:
                print(f"在仓库 {repo} 中未找到技能 {skill_name}")
                # 如果创建了目录但没找到技能，删除空目录
                if skill_dir.exists() and not any(skill_dir.iterdir()):
                    skill_dir.rmdir()
    except subprocess.CalledProcessError as e:
        print(f"无法克隆仓库 {repo}: {e}")
        print(f"错误输出: {e.stderr.decode() if hasattr(e, 'stderr') else 'N/A'}")
    except subprocess.TimeoutExpired:
        print(f"克隆仓库 {repo} 超时（60秒）")
    except Exception as e:
        print(f"更新技能 {skill_name}@{repo} 时出错: {e}")
    finally:
        # 清理临时目录
        try:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        except:
            pass  # 如果临时目录清理失败，忽略错误