"""
使用nssm将Python脚本注册为Windows服务
nssm是一个更简单的Windows服务管理工具
"""
import subprocess
import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
python_exe = sys.executable
script_path = current_dir / "monitor.py"
service_name = "FeishuAvatarMonitor"

def install_service():
    """安装服务"""
    print("=" * 60)
    print("使用NSSM安装Windows服务")
    print("=" * 60)
    print()
    
    # 检查nssm是否存在
    nssm_path = current_dir / "nssm.exe"
    if not nssm_path.exists():
        print("错误: 未找到nssm.exe")
        print("请从以下地址下载nssm:")
        print("https://nssm.cc/download")
        print("下载后将nssm.exe放到当前目录")
        return False
    
    print(f"Python路径: {python_exe}")
    print(f"脚本路径: {script_path}")
    print(f"工作目录: {current_dir}")
    print()
    
    # 安装服务
    cmd = [
        str(nssm_path), "install", service_name,
        python_exe, str(script_path)
    ]
    
    print("正在安装服务...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ 服务安装成功")
        
        # 设置工作目录
        subprocess.run([str(nssm_path), "set", service_name, "AppDirectory", str(current_dir)])
        
        # 设置服务描述
        subprocess.run([str(nssm_path), "set", service_name, "Description", 
                       "监听飞书多维表格变化，自动更新群头像"])
        
        # 设置服务启动类型为自动
        subprocess.run([str(nssm_path), "set", service_name, "Start", "SERVICE_AUTO_START"])
        
        # 启动服务
        print("正在启动服务...")
        subprocess.run([str(nssm_path), "start", service_name])
        
        print()
        print("=" * 60)
        print("服务安装并启动成功！")
        print(f"服务名称: {service_name}")
        print("服务将在系统启动时自动运行")
        print("=" * 60)
        return True
    else:
        print(f"✗ 安装失败: {result.stderr}")
        return False

def remove_service():
    """卸载服务"""
    nssm_path = current_dir / "nssm.exe"
    if not nssm_path.exists():
        print("错误: 未找到nssm.exe")
        return False
    
    print("正在停止服务...")
    subprocess.run([str(nssm_path), "stop", service_name])
    
    print("正在卸载服务...")
    result = subprocess.run([str(nssm_path), "remove", service_name, "confirm"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ 服务卸载成功")
        return True
    else:
        print(f"✗ 卸载失败: {result.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "install":
            install_service()
        elif sys.argv[1] == "remove":
            remove_service()
    else:
        print("用法:")
        print("  安装服务: python nssm_service.py install")
        print("  卸载服务: python nssm_service.py remove")
