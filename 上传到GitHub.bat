@echo off
chcp 65001 >nul
echo ====================================
echo GitHub 代码上传助手
echo ====================================
echo.

:input_username
set /p github_username="请输入你的GitHub用户名: "
if "%github_username%"=="" (
    echo 用户名不能为空！
    goto input_username
)

echo.
echo 正在初始化Git仓库...
git init

echo.
echo 添加所有文件...
git add .

echo.
echo 提交代码...
git commit -m "Initial commit: 飞书群头像自动更新系统"

echo.
echo 关联远程仓库...
git remote add origin https://github.com/%github_username%/feishu-avatar-webhook.git

echo.
echo 推送到GitHub...
git branch -M main
git push -u origin main

echo.
echo ====================================
echo 上传完成！
echo ====================================
echo.
echo 你的仓库地址:
echo https://github.com/%github_username%/feishu-avatar-webhook
echo.
echo 下一步：
echo 1. 访问 https://render.com
echo 2. 使用GitHub登录
echo 3. 创建Web Service并连接你的仓库
echo.
pause
