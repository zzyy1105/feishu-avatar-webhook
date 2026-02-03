@echo off
chcp 65001 >nul
echo ====================================
echo GitHub 代码上传助手
echo ====================================
echo.

REM 设置Git路径
set "GIT_PATH=C:\Users\Administrator\AppData\Local\GitHubDesktop\app-3.5.4\resources\app\git\cmd\git.exe"

REM 检查Git是否存在
if not exist "%GIT_PATH%" (
    echo 错误: 未找到Git
    echo 请确认GitHub Desktop已安装
    pause
    exit /b 1
)

echo 找到Git: %GIT_PATH%
echo.

:input_username
set /p github_username="请输入你的GitHub用户名: "
if "%github_username%"=="" (
    echo 用户名不能为空！
    goto input_username
)

echo.
echo 正在配置Git用户信息...
"%GIT_PATH%" config --global user.name "%github_username%"
"%GIT_PATH%" config --global user.email "%github_username%@users.noreply.github.com"

echo.
echo 正在初始化Git仓库...
"%GIT_PATH%" init

echo.
echo 添加所有文件...
"%GIT_PATH%" add .

echo.
echo 提交代码...
"%GIT_PATH%" commit -m "Initial commit: 飞书群头像自动更新系统"

echo.
echo 关联远程仓库...
"%GIT_PATH%" remote add origin https://github.com/%github_username%/feishu-avatar-webhook.git

echo.
echo 推送到GitHub...
"%GIT_PATH%" branch -M main
"%GIT_PATH%" push -u origin main

echo.
if errorlevel 1 (
    echo ====================================
    echo 上传失败！
    echo ====================================
    echo.
    echo 可能的原因:
    echo 1. 仓库还未在GitHub上创建
    echo 2. 用户名或密码错误
    echo 3. 网络连接问题
    echo.
    echo 请先在GitHub上创建仓库:
    echo 1. 访问 https://github.com/new
    echo 2. Repository name: feishu-avatar-webhook
    echo 3. 选择 Public
    echo 4. 不勾选任何选项
    echo 5. 点击 Create repository
    echo.
    echo 然后重新运行此脚本
) else (
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
)

echo.
pause
