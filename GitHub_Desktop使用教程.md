# GitHub Desktop 上传教程（图文详解）

## 为什么用GitHub Desktop？
- ✅ 图形界面，无需命令行
- ✅ 你已经安装好了
- ✅ 拖拽即可，最简单
- ✅ 3分钟搞定

---

## 详细步骤

### 第1步：打开GitHub Desktop

1. 按 `Win键`，搜索 "GitHub Desktop"
2. 打开应用
3. 如果是第一次使用，需要登录：
   - 点击 "Sign in to GitHub.com"
   - 输入GitHub用户名和密码
   - 点击 "Sign in"

---

### 第2步：添加项目文件夹

1. 在GitHub Desktop中，点击左上角 **"File"** → **"Add local repository"**

2. 点击 **"Choose..."** 按钮

3. 选择文件夹：`E:\AI\修改头像`

4. 点击 **"选择文件夹"**

5. 这时会提示：
   ```
   This directory does not appear to be a Git repository.
   Would you like to create a repository here instead?
   ```
   
6. 点击 **"create a repository"**

7. 在弹出窗口填写：
   - **Name**: `feishu-avatar-webhook`（自动填充，不用改）
   - **Description**: `飞书群头像自动更新系统`
   - **Git Ignore**: 选择 `None`
   - **License**: 选择 `None`
   - ✅ 勾选 **"Initialize this repository with a README"**

8. 点击 **"Create repository"**

---

### 第3步：提交文件

1. 现在你会看到左侧列出了所有文件
2. 在左下角的输入框中：
   - **Summary** (必填): 输入 `Initial commit`
   - **Description** (可选): 可以留空
3. 点击蓝色按钮 **"Commit to main"**

---

### 第4步：发布到GitHub

1. 提交后，顶部会出现一个按钮 **"Publish repository"**
2. 点击它
3. 在弹出窗口中：
   - **Name**: `feishu-avatar-webhook`（已自动填充）
   - **Description**: `飞书群头像自动更新系统`
   - **Keep this code private**: ❌ **取消勾选**（我们需要公开仓库）
   - **Organization**: 选择 `None`（使用个人账号）
4. 点击 **"Publish repository"**

---

### 第5步：等待上传

- 底部会显示上传进度
- 通常需要30秒-2分钟
- 上传完成后会显示 "Last fetched just now"

---

### 第6步：验证上传成功

1. 在GitHub Desktop顶部，点击 **"Repository"** → **"View on GitHub"**
2. 会在浏览器中打开你的仓库
3. 确认所有文件都已上传

✅ **你的仓库地址：**
```
https://github.com/你的用户名/feishu-avatar-webhook
```

---

## 常见问题

### Q1: 提示需要登录GitHub
**解决：**
1. 点击 "Sign in to GitHub.com"
2. 在浏览器中登录
3. 授权GitHub Desktop

### Q2: 找不到"Publish repository"按钮
**解决：**
- 确保已经点击了 "Commit to main"
- 按钮在顶部中间位置

### Q3: 上传失败
**解决：**
1. 检查网络连接
2. 确认GitHub账号已登录
3. 重试：Repository → Push

### Q4: 提示仓库名已存在
**解决：**
1. 访问 https://github.com/你的用户名/feishu-avatar-webhook
2. 删除旧仓库（Settings → Delete this repository）
3. 重新发布

---

## 截图说明

### 界面示意：

```
┌─────────────────────────────────────────┐
│ GitHub Desktop                    - □ × │
├─────────────────────────────────────────┤
│ File  Edit  View  Repository  Branch   │
├─────────────────────────────────────────┤
│                                         │
│  Current Repository                     │
│  feishu-avatar-webhook                  │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Changes (15)                      │ │
│  │ ✓ webhook_server_hybrid.py       │ │
│  │ ✓ feishu_api.py                  │ │
│  │ ✓ config.json                    │ │
│  │ ✓ avatar.jpg                     │ │
│  │ ✓ requirements.txt               │ │
│  │ ... (更多文件)                    │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Summary (required)                     │
│  ┌───────────────────────────────────┐ │
│  │ Initial commit                    │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Description                            │
│  ┌───────────────────────────────────┐ │
│  │                                   │ │
│  └───────────────────────────────────┘ │
│                                         │
│     [Commit to main]                    │
│                                         │
└─────────────────────────────────────────┘
```

---

## 完成后

记录你的信息：
- **GitHub用户名**: _______________
- **仓库地址**: https://github.com/_______________/feishu-avatar-webhook

下一步：部署到Render.com

---

需要帮助？告诉我你在哪一步遇到问题！
