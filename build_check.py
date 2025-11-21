#!/usr/bin/env python3
"""
构建状态检查脚本 - 验证项目构建准备状态
"""

import os
import sys
import subprocess

def check_python_version():
    """检查Python版本"""
    print("正在检查Python版本...")
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python版本符合要求")
        return True
    else:
        print("❌ Python版本过低，需要3.8+")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n正在检查依赖包...")
    required_packages = [
        'PyQt5',
        'qfluentwidgets',
        'pyinstaller'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def check_files():
    """检查关键文件"""
    print("\n正在检查关键文件...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'icon.ico',
        'logo.png',
        '.github/workflows/build.yml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
            missing_files.append(file_path)
    
    return len(missing_files) == 0, missing_files

def check_project_structure():
    """检查项目结构"""
    print("\n正在检查项目结构...")
    
    required_dirs = [
        'view',
        'view/pages',
        'view/common',
        'view/components',
        'source'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ {dir_path}/ 目录存在")
        else:
            print(f"❌ {dir_path}/ 目录不存在")
            missing_dirs.append(dir_path)
    
    return len(missing_dirs) == 0, missing_dirs

def main():
    """主检查函数"""
    print("=" * 60)
    print("ITLToolkit 构建状态检查")
    print("=" * 60)
    
    all_passed = True
    
    # 检查Python版本
    if not check_python_version():
        all_passed = False
    
    # 检查依赖
    deps_ok, missing_deps = check_dependencies()
    if not deps_ok:
        all_passed = False
        print(f"\n需要安装以下包: {', '.join(missing_deps)}")
        print("运行: pip install -r requirements.txt")
    
    # 检查文件
    files_ok, missing_files = check_files()
    if not files_ok:
        all_passed = False
        print(f"\n缺少文件: {', '.join(missing_files)}")
    
    # 检查项目结构
    structure_ok, missing_dirs = check_project_structure()
    if not structure_ok:
        all_passed = False
        print(f"\n缺少目录: {', '.join(missing_dirs)}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有检查通过！项目已准备好构建")
        print("\nGitHub Actions 工作流使用说明:")
        print("1. 访问 GitHub 仓库页面")
        print("2. 点击 Actions 标签")
        print("3. 选择 'Build ITLToolkit' 工作流")
        print("4. 点击 'Run workflow' 按钮")
        print("5. 输入版本号 (例如: 1.0.0)")
        print("6. 等待构建完成")
        print("\n构建产物将在 Actions 页面下载")
    else:
        print("❌ 检查未通过，请修复上述问题")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())