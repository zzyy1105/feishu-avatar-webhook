# 飞书Webhook验证失败排查指南

## 问题：Challenge code没有返回

---

## 立即检查清单

### ✅ 第1项：确认Render服务正常运行

1. 访问 Render 控制台：https://dashboard.render.com/
2. 查看服务状态：
   - 必须是 **Live** ✅（绿色）
   - 如果是 **Deploying** 🔄，等待部署完成
   - 如果是 **Failed** ❌，查看日志修复错误

3. 测试健康检查：
   - 访问：`https://你的服务URL/health`
   - 必须返回JSON数据：
     ```json
     {
       "status": "ok",
       "timestamp": "...",
       "processed_count": 0,
       "mode": "hybrid (webhook + polling)"
     }
     ```
   - 如果显示"您的应用即将上线"，说明服务还没启动成功

---

### ✅ 第2项：检查VERIFICATION_TOKEN配置

**重要：首次验证时不需要配置VERIFICATION_TOKEN！**

1. 在Render控制台，点击 **"Environment"** 标签
2. 如果已经添加了 `VERIFICATION_TOKEN`：
   - 点击右侧的 **删除按钮（垃圾桶图标）**
   - 删除这个环境变量
   - 点击 **"Save Changes"**
   - 等待服务重启（1-2分钟）

**为什么要删除？**
- 首次验证时，飞书会发送一个特殊的验证请求
- 这个请求不需要验证token
- 验证成功后，再添加token用于后续事件

---

### ✅ 第3项：修复代码中的token验证逻辑

代码中的token验证可能太严格，导致验证失败。

我需要修改 `webhook_server_hybrid.py` 文件。

---

## 修复方案

### 方案1：临时禁用Token验证（推荐）

修改 `webhook_server_hybrid.py`，让它在验证阶段不检查token。
