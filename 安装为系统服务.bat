@echo off
chcp 65001 >nul
echo ====================================
echo 安装飞书群头像更新服务
echo ====================================
echo.
echo 正在检查管理员权限...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 需要管理员权限！
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)
echo.
echo 正在安装依赖包...
pip install pywin32
echo.
echo 正在安装服务...
python service.py install
echo.
echo 正在启动服务...
python service.py start
echo.
echo ====================================
echo 服务安装完成！
echo 服务名称: FeishuAvatarMonitor
echo 服务将在系统启动时自动运行
echo ====================================
echo.
echo 管理命令:
echo   启动服务: python service.py start
echo   停止服务: python service.py stop
echo   重启服务: python service.py restart
echo   卸载服务: python service.py remove
echo.
pause
