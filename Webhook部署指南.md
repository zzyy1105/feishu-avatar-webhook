# 飞书Webhook方案部署指南

## 方案优势
- ✅ **零成本** - 无需购买服务器
- ✅ **实时响应** - 数据变化立即触发
- ✅ **高可用** - 飞书官方保障
- ✅ **无需轮询** - 节省资源

## 部署步骤

### 第一步: 准备Webhook服务器

你需要一个公网可访问的服务器来接收飞书的事件推送。有以下选择：

#### 选项A: 使用免费云平台（推荐新手）

**1. Render.com (推荐)**
- 注册: https://render.com
- 免费额度: 750小时/月
- 自动休眠，有请求时自动唤醒

**2. Railway.app**
- 注册: https://railway.app
- 免费额度: $5/月

**3. Fly.io**
- 注册: https://fly.io
- 免费额度: 3个小型应用

#### 选项B: 使用云服务器
- 阿里云/腾讯云/华为云
- 最低配置即可（1核1G）
- 成本: 约10-30元/月

#### 选项C: 内网穿透（临时测试）
使用 ngrok 或 frp 将本地服务暴露到公网

### 第二步: 部署Webhook服务

#### 方法1: 使用Docker部署（推荐）

1. 创建 `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "webhook_server:app"]
```

2. 创建 `requirements.txt`:
```
flask==2.3.0
gunicorn==21.2.0
requests==2.31.0
```

3. 构建并运行:
```bash
docker build -t feishu-webhook .
docker run -d -p 5000:5000 feishu-webhook
```

#### 方法2: 直接部署

1. 安装依赖:
```bash
pip install flask gunicorn requests
```

2. 启动服务:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 webhook_server:app
```

### 第三步: 配置飞书开放平台

1. **进入飞书开放平台**
   - 访问: https://open.feishu.cn/
   - 进入你的应用

2. **开启事件订阅**
   - 进入"事件订阅"页面
   - 请求地址: `http://你的服务器IP:5000/webhook`
   - 复制"Verification Token"到 `webhook_server.py` 的 `VERIFICATION_TOKEN`
   - 如果启用加密，复制"Encrypt Key"到 `ENCRYPT_KEY`

3. **订阅事件**
   添加以下事件:
   - `多维表格记录变更` (bitable.app_table_record.changed)
   
   权限要求:
   - `bitable:app` - 查看、评论、编辑和管理多维表格

4. **保存并发布**
   - 点击"保存"
   - 发布新版本

### 第四步: 测试

1. 修改多维表格中的"发机通道申请状态"为"已通过"
2. 查看服务器日志，应该能看到事件接收记录
3. 检查对应飞书群的头像是否更新

## 配置文件说明

修改 `webhook_server.py` 中的配置:

```python
# 从飞书开放平台获取
VERIFICATION_TOKEN = "your_verification_token"
ENCRYPT_KEY = "your_encrypt_key"  # 可选
```

## 监控和日志

- 日志文件: `logs/webhook_YYYYMMDD.log`
- 健康检查: `http://你的服务器IP:5000/health`

## 故障排查

### 问题1: 飞书无法推送事件
- 检查服务器是否公网可访问
- 检查防火墙是否开放5000端口
- 检查Verification Token是否正确

### 问题2: 收到事件但未更新头像
- 查看日志文件排查错误
- 检查app_id和app_secret是否正确
- 检查应用权限是否完整

### 问题3: 服务频繁重启
- 检查内存是否充足
- 查看错误日志
- 考虑增加服务器配置

## 成本对比

| 方案 | 月成本 | 优点 | 缺点 |
|------|--------|------|------|
| Render免费版 | ¥0 | 零成本 | 15分钟无请求会休眠 |
| Railway免费版 | ¥0 | 零成本 | 每月$5额度 |
| 云服务器最低配 | ¥10-30 | 稳定可靠 | 需要运维 |
| Serverless | ¥0-10 | 按需付费 | 冷启动延迟 |

## 推荐配置

**测试环境**: Render.com 免费版
**生产环境**: 云服务器 + Docker部署

## 下一步

选择一个部署方案后，我可以为你生成对应的详细部署脚本和配置文件。

你想使用哪种方案？
1. 免费云平台（Render/Railway）
2. 购买云服务器
3. 本地+内网穿透（仅测试）
