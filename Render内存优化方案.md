# Render内存不足问题解决方案

## 问题原因
Render免费版只有512MB内存，当前配置使用了4个worker进程，每个进程都会加载完整的应用，导致内存超标。

---

## 已优化的配置

### 1. 减少Worker数量
从 4 个 worker 改为 1 个 worker：
```bash
gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 120 --max-requests 1000 --max-requests-jitter 50 webhook_server_hybrid:app
```

### 2. 增加定时检查间隔
从 5 分钟改为 10 分钟，减少资源占用

### 3. 添加内存管理参数
- `--max-requests 1000`: 处理1000个请求后重启worker，释放内存
- `--max-requests-jitter 50`: 随机抖动，避免同时重启

---

## 更新步骤

### 方法1：通过Render控制台修改（推荐）

1. 访问 Render 控制台：https://dashboard.render.com/
2. 进入服务 `feishu-avatar-webhook`
3. 点击左侧 **"Settings"** 标签
4. 找到 **"Build & Deploy"** 区域
5. 修改 **"Start Command"** 为：
   ```
   gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 120 --max-requests 1000 --max-requests-jitter 50 webhook_server_hybrid:app
   ```
6. 点击 **"Save Changes"**
7. 点击右上角 **"Manual Deploy"** → **"Clear build cache & deploy"**

### 方法2：推送代码更新

1. 使用GitHub Desktop提交修改
2. 推送到GitHub
3. Render自动重新部署

---

## 如果还是内存不足

### 方案A：进一步优化

修改 `config.json`，减少检查间隔：
```json
"monitor_config": {
  "check_interval": 60,  // 改为60秒（仅影响本地运行）
  "log_level": "WARNING"  // 减少日志输出
}
```

### 方案B：禁用定时轮询，只用Webhook

如果Webhook配置正确，可以禁用定时轮询：

在 `webhook_server_hybrid.py` 中注释掉调度器：
```python
# scheduler = BackgroundScheduler()
# scheduler.add_job(...)
# scheduler.start()
```

### 方案C：升级到付费版

Render付费版（$7/月）提供：
- 512MB → 2GB 内存
- 永不休眠
- 更快的CPU

### 方案D：换用其他平台

- Railway.app - 免费额度更大
- 阿里云/腾讯云轻量服务器 - ¥24/月起

---

## 推荐配置（免费版最优）

**Start Command:**
```bash
gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 120 --max-requests 1000 --max-requests-jitter 50 --preload webhook_server_hybrid:app
```

**说明：**
- `-w 1`: 只用1个worker
- `--max-requests 1000`: 定期重启释放内存
- `--preload`: 预加载应用，减少内存占用

---

## 监控内存使用

在Render日志中查看内存使用：
```
[INFO] Memory usage: XXX MB
```

如果持续接近512MB，考虑升级或优化。
