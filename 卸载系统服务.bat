@echo off
chcp 65001 >nul
echo ====================================
echo 卸载飞书群头像更新服务
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
echo 正在停止服务...
python service.py stop
echo.
echo 正在卸载服务...
python service.py remove
echo.
echo ====================================
echo 服务已卸载
echo ====================================
pause
