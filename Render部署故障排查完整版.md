# Render部署故障完整排查

## 当前问题：退出状态码1

这通常是Python代码运行时错误。

---

## 立即诊断步骤

### 第1步：查看详细错误日志

1. 在Render控制台，点击 **"Logs"** 标签
2. 向上滚动，找到最近一次部署的日志
3. 查找包含 **"Error"** 或 **"Traceback"** 的行
4. **复制完整的错误信息**（包括前后20行）

---

## 可能的原因和解决方案

### 原因1：config.json 或 avatar.jpg 缺失

**检查：** GitHub仓库中是否有这些文件？
```
https://github.com/zzyy1105/feishu-avatar-webhook
```

必须包含：
- webhook_simple.py ✅
- feishu_api.py ✅
- config.json ✅
- avatar.jpg ✅
- requirements.txt ✅

**如果缺失，重新上传。**

---

### 原因2：启动命令错误

**当前启动命令应该是：**
```
gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 120 webhook_simple:app
```

**检查方法：**
1. Render → Settings → Start Command
2. 确认是否正确

**如果不对，修改为：**
```
python webhook_simple.py
```
（最简单的启动方式）

---

### 原因3：Python版本问题

**检查 Python 版本：**
在Render日志中查找：
```
Python 3.x.x
```

如果是Python 2.x，需要指定Python 3。

---

### 原因4：依赖安装失败

**检查日志中是否有：**
```
Successfully installed flask-2.3.0 gunicorn-21.2.0 requests-2.31.0
```

如果没有，说明依赖安装失败。

---

## 快速修复方案

### 方案A：使用最简单的启动方式

1. Render → Settings → Start Command
2. 改为：
   ```
   python webhook_simple.py
   ```
3. Save Changes

### 方案B：添加调试信息

修改 `webhook_simple.py`，在最开始添加：

```python
import sys
print("Python version:", sys.version)
print("Python path:", sys.path)
print("Current directory:", os.getcwd())
print("Files:", os.listdir('.'))
```

这样可以在日志中看到更多信息。

---

## 临时测试方案

创建一个超级简单的测试文件：
