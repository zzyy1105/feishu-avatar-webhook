# Render服务故障排查指南

## 问题：访问 /health 显示"您的应用即将上线"

这说明服务还没有正常启动。

---

## 排查步骤

### 第1步：检查部署状态

1. 登录 Render 控制台：https://dashboard.render.com/
2. 点击你的服务 `feishu-avatar-webhook`
3. 查看顶部状态：
   - ✅ **Live**（绿色）- 正常运行
   - 🔄 **Deploying**（黄色）- 正在部署，等待完成
   - ❌ **Deploy failed**（红色）- 部署失败

### 第2步：查看日志

1. 在服务详情页，点击 **"Logs"** 标签
2. 查看最新的日志输出

---

## 常见问题和解决方案

### 问题1：部署失败（Deploy failed）

**查看日志中的错误信息：**

#### 错误A：找不到模块
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方法：**
检查 `requirements.txt` 是否完整，应该包含：
```
flask==2.3.0
gunicorn==21.2.0
requests==2.31.0
APScheduler==3.10.4
```

#### 错误B：启动命令错误
```
Error: No module named 'webhook_server_hybrid'
```

**解决方法：**
检查 Start Command 是否正确：
```
gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 webhook_server_hybrid:app
```

注意：
- 文件名是 `webhook_server_hybrid`（不是 webhook_server）
- 中间是冒号 `:`
- app 是小写

#### 错误C：端口绑定错误
```
Error binding to port
```

**解决方法：**
确认 Start Command 中使用的是 `$PORT`（大写），不是固定端口号。

---

### 问题2：一直显示 Deploying

**可能原因：**
- 首次部署需要较长时间（5-10分钟）
- 网络问题导致下载依赖慢

**解决方法：**
- 耐心等待
- 查看 Logs 了解进度

---

### 问题3：服务启动后立即崩溃

**查看日志中的错误：**

#### 错误：配置文件问题
```
FileNotFoundError: config.json
```

**原因：** GitHub仓库中缺少文件

**解决方法：**
确认以下文件都已上传到GitHub：
- webhook_server_hybrid.py
- feishu_api.py
- config.json
- avatar.jpg
- requirements.txt

---

## 立即检查清单

请按以下步骤检查：

### ✅ 第1步：确认文件已上传

访问你的GitHub仓库：
```
https://github.com/你的用户名/feishu-avatar-webhook
```

确认以下文件存在：
- [ ] webhook_server_hybrid.py
- [ ] feishu_api.py
- [ ] config.json
- [ ] avatar.jpg
- [ ] requirements.txt
- [ ] render.yaml

### ✅ 第2步：检查Render配置

在Render控制台，点击 **"Settings"** 标签，确认：

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 webhook_server_hybrid:app
```

**如果配置错误：**
1. 修改配置
2. 点击 **"Save Changes"**
3. 点击右上角 **"Manual Deploy"** → **"Deploy latest commit"**

### ✅ 第3步：查看详细日志

1. 点击 **"Logs"** 标签
2. 复制最后20-30行日志
3. 告诉我日志内容，我帮你分析

---

## 快速修复方案

如果以上都检查过了还是不行，尝试：

### 方案1：手动触发重新部署

1. 在Render控制台
2. 点击右上角 **"Manual Deploy"**
3. 选择 **"Clear build cache & deploy"**
4. 等待重新部署

### 方案2：检查环境变量

1. 点击 **"Environment"** 标签
2. 确认 `VERIFICATION_TOKEN` 已添加
3. 如果没有，先不加，等服务正常启动后再加

### 方案3：简化启动命令测试

临时修改 Start Command 为：
```
python webhook_server_hybrid.py
```

看是否能启动，如果能启动，再改回：
```
gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 webhook_server_hybrid:app
```

---

## 需要帮助

请告诉我：
1. Render服务的状态（Live / Deploying / Failed）
2. Logs标签中的最新日志（最后20行）
3. GitHub仓库中是否有所有必需文件

我会帮你快速定位问题！
