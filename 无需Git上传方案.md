# 无需Git - 快速上传方案

## 方法1：创建压缩包上传（最简单）

### 第1步：准备文件

我已经为你准备好了所有需要的文件在：
```
E:\AI\修改头像
```

### 第2步：选择要上传的文件

**必须上传的核心文件：**
1. webhook_server_hybrid.py
2. feishu_api.py
3. config.json
4. avatar.jpg
5. requirements.txt
6. render.yaml
7. Dockerfile
8. .gitignore
9. README_GITHUB.md

### 第3步：上传到GitHub

#### 3.1 创建GitHub仓库
1. 访问 https://github.com
2. 登录账号
3. 点击右上角 "+" → "New repository"
4. 填写：
   - Repository name: `feishu-avatar-webhook`
   - Description: `飞书群头像自动更新`
   - 选择 **Public**
   - **不要**勾选任何选项
5. 点击 "Create repository"

#### 3.2 上传文件
1. 在新建的仓库页面，点击 "uploading an existing file"
2. 打开文件夹 `E:\AI\修改头像`
3. **按住Ctrl键**，选择上面列出的9个文件
4. 拖拽到浏览器窗口
5. 等待上传完成
6. 在底部填写：
   - Commit message: `Initial commit`
7. 点击 "Commit changes"

#### 3.3 重命名README
1. 点击 `README_GITHUB.md` 文件
2. 点击右上角铅笔图标（编辑）
3. 将文件名改为 `README.md`
4. 点击 "Commit changes"

### 第4步：完成
✅ 你的仓库地址：`https://github.com/你的用户名/feishu-avatar-webhook`

---

## 方法2：使用GitHub Desktop（图形界面）

### 下载安装
1. 访问：https://desktop.github.com/
2. 下载并安装
3. 使用GitHub账号登录

### 上传步骤
1. File → Add Local Repository
2. 选择 `E:\AI\修改头像`
3. 点击 "Publish repository"
4. 填写仓库名：`feishu-avatar-webhook`
5. 点击 "Publish"

---

## 我的建议

**立即使用方法1（网页上传）**
- 无需安装任何软件
- 5分钟搞定
- 最简单直接

等你熟悉流程后，再考虑学习Git命令。

---

## 需要帮助？

告诉我：
1. 你的GitHub用户名是什么？
2. 你现在进行到哪一步了？
3. 遇到什么问题？

我会一步步指导你！
