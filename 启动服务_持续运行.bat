@echo off
chcp 65001 >nul
title 飞书群头像自动更新服务

:start
echo ====================================
echo 飞书群头像自动更新服务
echo 启动时间: %date% %time%
echo ====================================
echo.

python monitor.py

echo.
echo [%date% %time%] 服务异常退出，5秒后自动重启...
timeout /t 5 /nobreak
goto start
