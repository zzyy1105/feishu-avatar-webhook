"""
将应用添加到多维表格的脚本
"""
import requests
import json

# 配置
APP_ID = "cli_a9fc7a617dbadcb0"
APP_SECRET = "AkNYoHW5SMux5O5yEwQGSAQ6uPwEnKEw"
APP_TOKEN = "FbU2bnPIPawHQvsIMudcANvwnWf"

def get_tenant_access_token():
    """获取tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if result.get("code") == 0:
        return result["tenant_access_token"]
    else:
        raise Exception(f"获取token失败: {result}")

def add_app_to_bitable():
    """将应用添加到多维表格"""
    token = get_tenant_access_token()
    
    # 添加协作者
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{APP_TOKEN}/members"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "member_type": "openid",
        "member_id": APP_ID,
        "perm": "edit"  # 可编辑权限
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    print("=" * 80)
    if result.get("code") == 0:
        print("✅ 成功将应用添加到多维表格！")
        print(f"应用ID: {APP_ID}")
        print(f"权限: 可编辑")
    else:
        print("❌ 添加失败")
        print(f"错误信息: {result}")
        print()
        print("可能的原因:")
        print("1. 应用权限不足，需要先在飞书开放平台添加 bitable:app 权限")
        print("2. 应用版本未发布")
        print("3. 需要手动在多维表格界面添加")
    print("=" * 80)
    
    return result

if __name__ == "__main__":
    try:
        add_app_to_bitable()
    except Exception as e:
        print(f"错误: {e}")
