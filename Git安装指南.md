# Git安装和使用指南

## 第一步：安装Git

### 方式1：使用winget安装（Windows 10/11自带）
打开命令提示符或PowerShell，执行：
```
winget install --id Git.Git -e --source winget
```

### 方式2：下载安装包
1. 访问：https://git-scm.com/download/win
2. 下载Windows版本
3. 双击安装，一路"Next"即可（使用默认设置）

### 方式3：使用国内镜像（更快）
1. 访问：https://registry.npmmirror.com/binary.html?path=git-for-windows/
2. 下载最新版本（如：Git-2.43.0-64-bit.exe）
3. 双击安装

## 第二步：验证安装

安装完成后，**重新打开**命令提示符，输入：
```
git --version
```

应该看到类似：`git version 2.43.0.windows.1`

## 第三步：配置Git

首次使用需要配置用户名和邮箱：
```
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

## 第四步：运行上传脚本

配置完成后，双击运行 `上传到GitHub.bat`

---

## 如果不想安装Git

请使用方案B：手动上传到GitHub（见下方）
