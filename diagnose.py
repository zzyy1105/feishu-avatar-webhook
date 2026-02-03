"""
飞书配置诊断脚本
检查应用配置、权限、事件订阅等
"""
import requests
import json

APP_ID = "cli_a9fc7a617dbadcb0"
APP_SECRET = "AkNYoHW5SMux5O5yEwQGSAQ6uPwEnKEw"
APP_TOKEN = "FbU2bnPIPawHQvsIMudcANvwnWf"
TABLE_ID = "tblp5MrI71tKK7wq"

def get_tenant_access_token():
    """获取tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if result.get("code") == 0:
        return result["tenant_access_token"]
    else:
        print(f"❌ 获取token失败: {result}")
        return None

def check_app_info(token):
    """检查应用信息"""
    print("\n" + "=" * 60)
    print("1. 检查应用信息")
    print("=" * 60)
    
    url = "https://open.feishu.cn/open-apis/application/v6/app/info"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        app_info = result.get("data", {}).get("app", {})
        print(f"✅ 应用名称: {app_info.get('app_name')}")
        print(f"✅ 应用ID: {app_info.get('app_id')}")
        print(f"✅ 应用状态: {app_info.get('status')}")
    else:
        print(f"❌ 获取应用信息失败: {result}")

def check_bitable_access(token):
    """检查多维表格访问权限"""
    print("\n" + "=" * 60)
    print("2. 检查多维表格访问权限")
    print("=" * 60)
    
    # 尝试获取表格信息
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        fields = result.get("data", {}).get("items", [])
        print(f"✅ 成功访问多维表格")
        print(f"✅ 字段数量: {len(fields)}")
        print(f"\n字段列表:")
        for field in fields:
            print(f"  - {field.get('field_name')} (ID: {field.get('field_id')})")
    else:
        print(f"❌ 无法访问多维表格: {result}")
        print(f"   错误代码: {result.get('code')}")
        print(f"   错误信息: {result.get('msg')}")

def check_event_subscription(token):
    """检查事件订阅配置"""
    print("\n" + "=" * 60)
    print("3. 检查事件订阅配置")
    print("=" * 60)
    
    # 注意：这个API可能需要特殊权限
    url = "https://open.feishu.cn/open-apis/event/v1/subscriptions"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        subscriptions = result.get("data", {}).get("subscriptions", [])
        print(f"✅ 已订阅事件数量: {len(subscriptions)}")
        for sub in subscriptions:
            print(f"  - {sub.get('event_type')}: {sub.get('status')}")
    else:
        print(f"⚠️  无法获取事件订阅列表")
        print(f"   (这可能是正常的，某些API需要特殊权限)")

def test_webhook_url():
    """测试Webhook URL可访问性"""
    print("\n" + "=" * 60)
    print("4. 测试Webhook URL可访问性")
    print("=" * 60)
    
    webhook_url = "https://feishu-avatar-webhook.onrender.com/health"
    
    try:
        response = requests.get(webhook_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Webhook服务可访问")
            print(f"   响应: {response.json()}")
        else:
            print(f"❌ Webhook服务响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 无法访问Webhook服务: {e}")

def check_app_in_bitable(token):
    """检查应用是否在多维表格的协作者列表中"""
    print("\n" + "=" * 60)
    print("5. 检查应用是否在多维表格中")
    print("=" * 60)
    
    # 获取多维表格的协作者
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        print(f"✅ 可以访问多维表格基本信息")
        app_info = result.get("data", {}).get("app", {})
        print(f"   表格名称: {app_info.get('name')}")
    else:
        print(f"❌ 无法访问多维表格: {result}")

def main():
    print("=" * 60)
    print("飞书配置诊断工具")
    print("=" * 60)
    
    # 获取token
    print("\n获取访问令牌...")
    token = get_tenant_access_token()
    
    if not token:
        print("❌ 无法继续，请检查 app_id 和 app_secret")
        return
    
    print(f"✅ Token获取成功: {token[:20]}...")
    
    # 执行检查
    check_app_info(token)
    check_bitable_access(token)
    check_event_subscription(token)
    test_webhook_url()
    check_app_in_bitable(token)
    
    # 总结
    print("\n" + "=" * 60)
    print("诊断建议")
    print("=" * 60)
    print("""
如果上面的检查都通过了，但还是收不到事件，请检查：

1. 飞书开放平台 → 事件订阅
   - 确认"请求地址"验证成功
   - 确认事件状态为"已启用"
   - 确认选择的是"应用身份订阅"

2. 飞书开放平台 → 应用发布
   - 确认最新版本已发布
   - 确认应用可用范围包含你的部门

3. 多维表格
   - 确认应用已添加为协作者
   - 确认应用有"可编辑"权限

4. 等待时间
   - 发布应用后，等待1-2分钟生效
   - 修改表格后，事件推送可能有几秒延迟

5. 尝试重新验证Webhook
   - 在事件订阅页面，点击"验证"按钮
   - 查看Render日志是否收到验证请求
    """)

if __name__ == "__main__":
    main()
