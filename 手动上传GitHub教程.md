# 手动上传到GitHub教程（无需Git）

## 准备文件

需要上传以下文件到GitHub：

### 核心文件（必须）
- ✅ webhook_server_hybrid.py
- ✅ feishu_api.py
- ✅ config.json
- ✅ avatar.jpg
- ✅ requirements.txt
- ✅ render.yaml
- ✅ Dockerfile
- ✅ .gitignore

### 文档文件（可选）
- README_GITHUB.md
- 完整部署步骤.md
- 混合模式部署指南.md
- 等其他.md文件

---

## 详细步骤

### 第1步：创建GitHub仓库

1. 访问 https://github.com
2. 登录你的账号
3. 点击右上角 "+" → "New repository"
4. 填写信息：
   - **Repository name**: `feishu-avatar-webhook`
   - **Description**: `飞书群头像自动更新系统`
   - **Public** 或 **Private**: 选择 Public（公开）
   - ❌ 不要勾选 "Add a README file"
   - ❌ 不要勾选 "Add .gitignore"
   - ❌ 不要勾选 "Choose a license"
5. 点击 "Create repository"

### 第2步：上传文件

创建完仓库后，你会看到一个空仓库页面。

#### 方式1：网页直接上传（推荐）

1. 在仓库页面，点击 "uploading an existing file"
2. 打开文件夹 `E:\AI\修改头像`
3. **选择以下文件**拖拽到浏览器：
   ```
   webhook_server_hybrid.py
   feishu_api.py
   config.json
   avatar.jpg
   requirements.txt
   render.yaml
   Dockerfile
   .gitignore
   README_GITHUB.md
   ```
4. 在下方 "Commit changes" 填写：
   - Commit message: `Initial commit`
5. 点击 "Commit changes"

#### 方式2：逐个上传

1. 点击 "Add file" → "Upload files"
2. 选择文件上传
3. 重复直到所有文件上传完成

### 第3步：重命名README

1. 上传完成后，点击 `README_GITHUB.md`
2. 点击右上角铅笔图标（编辑）
3. 将文件名改为 `README.md`
4. 点击 "Commit changes"

### 第4步：验证

刷新仓库页面，应该看到：
- ✅ 所有文件已上传
- ✅ README.md 显示在页面下方
- ✅ 仓库地址：`https://github.com/你的用户名/feishu-avatar-webhook`

---

## 注意事项

### ⚠️ config.json 包含敏感信息

你的 `config.json` 包含 app_id 和 app_secret，建议：

**选项1：使用环境变量（推荐）**
1. 修改 `config.json`，将敏感信息替换为占位符：
```json
{
  "app_id": "your_app_id_here",
  "app_secret": "your_app_secret_here",
  ...
}
```
2. 上传到GitHub
3. 在Render配置真实的环境变量

**选项2：使用私有仓库**
- 创建仓库时选择 "Private"
- 只有你能看到代码

### ⚠️ avatar.jpg 文件

确保 `avatar.jpg` 是你想要设置的群头像图片

---

## 完成后

记录你的仓库地址：
```
https://github.com/你的用户名/feishu-avatar-webhook
```

下一步：部署到Render.com

---

## 需要帮助？

如果上传过程中遇到问题：
1. 截图错误信息
2. 告诉我具体哪一步出错
3. 我会帮你解决
