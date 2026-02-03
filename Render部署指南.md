# Render.com 免费部署指南

## 优势
- ✅ 完全免费
- ✅ 自动HTTPS
- ✅ 自动部署
- ✅ 无需信用卡

## 限制
- ⚠️ 15分钟无请求会休眠
- ⚠️ 每月750小时免费额度
- ⚠️ 冷启动需要30-60秒

## 部署步骤

### 1. 准备GitHub仓库

首先将代码上传到GitHub:

```bash
# 在项目目录下执行
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/feishu-avatar-webhook.git
git push -u origin main
```

### 2. 注册Render账号

1. 访问: https://render.com
2. 使用GitHub账号登录
3. 授权Render访问你的仓库

### 3. 创建Web Service

1. 点击"New +" → "Web Service"
2. 选择你的GitHub仓库
3. 配置如下:

**基本设置:**
- Name: `feishu-avatar-webhook`
- Region: `Singapore` (离中国最近)
- Branch: `main`
- Runtime: `Python 3`

**构建设置:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 webhook_server:app`

**计划:**
- Instance Type: `Free`

4. 点击"Create Web Service"

### 4. 等待部署

- 首次部署需要3-5分钟
- 部署成功后会显示服务URL
- 例如: `https://feishu-avatar-webhook.onrender.com`

### 5. 配置飞书Webhook

1. 复制Render提供的URL
2. 进入飞书开放平台
3. 事件订阅 → 请求地址: `https://你的服务.onrender.com/webhook`
4. 保存并发布

### 6. 测试

访问: `https://你的服务.onrender.com/health`

应该返回:
```json
{
  "status": "ok",
  "timestamp": "2024-xx-xx..."
}
```

## 注意事项

### 休眠问题
免费版15分钟无请求会休眠，首次请求需要30-60秒唤醒。

**解决方案:**
1. 使用外部监控服务定时ping（如UptimeRobot）
2. 升级到付费版（$7/月）

### 环境变量

如果需要配置敏感信息，在Render控制台添加环境变量:
- Settings → Environment → Add Environment Variable

### 查看日志

在Render控制台:
- Logs → 实时查看应用日志

### 自动部署

推送到GitHub后自动触发部署:
```bash
git add .
git commit -m "Update"
git push
```

## 成本

- 免费版: $0/月
- 付费版: $7/月 (无休眠，更快响应)

## 故障排查

### 部署失败
- 检查 requirements.txt 是否正确
- 查看构建日志

### 无法访问
- 检查防火墙
- 确认URL正确

### Webhook不响应
- 检查飞书配置
- 查看Render日志

## 推荐配置

**生产环境建议:**
1. 使用付费版避免休眠
2. 配置自定义域名
3. 启用监控告警

**测试环境:**
免费版完全够用
