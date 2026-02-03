@echo off
chcp 65001 >nul
echo ====================================
echo 飞书群头像自动更新服务
echo ====================================
echo.
echo 正在检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python,请先安装Python
    pause
    exit /b 1
)
echo.
echo 正在检查依赖包...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo 正在安装 requests...
    pip install requests
)
echo.
echo 启动监听服务...
echo 按 Ctrl+C 可停止服务
echo.
python monitor.py
pause
