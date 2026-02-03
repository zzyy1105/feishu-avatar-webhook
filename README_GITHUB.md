# 飞书群头像自动更新系统

当飞书多维表格中"发机通道申请状态"字段变更为"已通过"时，自动更新对应飞书群的头像。

## ✨ 特性

- 🚀 Webhook实时响应（0延迟）
- 🛡️ 定时轮询兜底（5分钟）
- 🔄 自动去重避免重复处理
- 📝 完整日志记录
- 💰 完全免费部署

## 🏗️ 架构

```
混合模式 = Webhook（实时） + 定时轮询（兜底）
```

- 正常情况：Webhook立即响应
- 服务休眠：5分钟内轮询检测并处理

## 🚀 快速部署

### 部署到Render.com（推荐）

1. Fork本仓库到你的GitHub
2. 访问 [Render.com](https://render.com) 并登录
3. 创建新的Web Service
4. 连接你的GitHub仓库
5. 自动部署完成

详细步骤见：[Render部署指南.md](Render部署指南.md)

## 📋 配置

### 1. 修改配置文件

编辑 `config.json`：
```json
{
  "app_id": "你的app_id",
  "app_secret": "你的app_secret",
  "base_config": {
    "app_token": "你的多维表格token",
    "table_id": "你的表格id",
    "monitor_field": "发机通道申请状态",
    "target_value": "已通过",
    "chat_id_field": "群组",
    "avatar_path": "avatar.jpg"
  }
}
```

### 2. 替换头像图片

将你的头像图片替换 `avatar.jpg`

### 3. 配置飞书Webhook

在 `webhook_server_hybrid.py` 中设置：
```python
VERIFICATION_TOKEN = "从飞书开放平台获取"
ENCRYPT_KEY = "从飞书开放平台获取（可选）"
```

## 📚 文档

- [Render部署指南](Render部署指南.md) - Render.com部署教程
- [混合模式部署指南](混合模式部署指南.md) - 混合模式说明
- [休眠问题解决方案](休眠问题解决方案.md) - 所有方案对比
- [Webhook部署指南](Webhook部署指南.md) - Webhook详细说明

## 🔧 API端点

- `GET /health` - 健康检查
- `POST /webhook` - 飞书事件接收
- `POST /force-check` - 手动触发检查

## 📊 监控

使用 [UptimeRobot](https://uptimerobot.com) 监控服务状态并保活：
- URL: `https://你的服务.onrender.com/health`
- 间隔: 5分钟

## 💡 成本

- Render.com: 免费
- UptimeRobot: 免费
- 总成本: **¥0/月**

## 📝 许可

MIT License
