import json
import os

def check_ide_installation():
    """检查IDE是否安装，以及安装了哪些"""
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    
    if not os.path.exists(config_file):
        print(f"配置文件 {config_file} 不存在")
        return []
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return []
    
    installed_ide = []
    
    for key, value in config_data.items():
        if not isinstance(value, list) or len(value) != 2:
            continue
            
        current_dir_path, user_dir_path = value
        
        # 去掉路径末尾的 /skills 或 /skill
        if current_dir_path.endswith('/skills') :
            current_dir_path = current_dir_path[:-7]
        elif current_dir_path.endswith('/skill'):
            current_dir_path = current_dir_path[:-6]
            
        if user_dir_path.endswith('/skills'):
            user_dir_path = user_dir_path[:-7]
        elif user_dir_path.endswith('/skill'):
            user_dir_path = user_dir_path[:-6]
        
        # 检查当前目录附加的路径是否存在
        full_current_path = os.path.join(os.getcwd(), current_dir_path.lstrip('/'))
        
        # 检查用户目录路径是否存在 (将 ~ 替换为实际的用户主目录)
        expanded_user_path = os.path.expanduser(user_dir_path)
        
        # 如果两个路径中任意一个存在，则认为该IDE已安装
        if os.path.exists(full_current_path) or os.path.exists(expanded_user_path):
            installed_ide.append(key)
    
    return installed_ide

def get_ide_path(ide, project=False, global_=False):
    """
    获取某个IDE的路径
    
    Args:
        ide: IDE名称（配置文件中的key）
        project: 是否返回项目路径（当前目录+第一个元素）
        global_: 是否返回全局路径（用户目录，即第二个元素）
    
    Returns:
        str: IDE路径的绝对路径
    """
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    
    if not os.path.exists(config_file):
        print(f"配置文件 {config_file} 不存在")
        return None
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return None
    
    if ide not in config_data:
        print(f"IDE {ide} 未在配置文件中找到")
        return None
    
    value = config_data[ide]
    if not isinstance(value, list) or len(value) != 2:
        print(f"IDE {ide} 的配置格式不正确")
        return None
    
    current_dir_path, user_dir_path = value
    paths= []
    
    # 根据参数决定返回哪个路径
    if project:
        # 返回当前目录+第一个元素的绝对路径
        full_current_path = os.path.join(os.getcwd(), current_dir_path.lstrip('/'))
        paths.append(os.path.abspath(full_current_path))
    if global_:
        # 返回用户目录的绝对路径（展开~符号）
        expanded_user_path = os.path.expanduser(user_dir_path)
        paths.append(os.path.abspath(expanded_user_path))
    return paths


# 使用示例
if __name__ == "__main__":
    # installed = check_ide_installation()
    # if installed:
    #     print("已安装的IDE:")
    #     for ide in installed:
    #         print(f"- {ide}")
    # else:
    #     print("未检测到任何IDE安装")

    print(get_ide_path('Antigravity', project=True, global_=True))
