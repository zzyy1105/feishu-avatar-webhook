"""
获取飞书群chat_id的工具脚本
"""
import requests
import json

# 配置
APP_ID = "cli_a9fc7a617dbadcb0"
APP_SECRET = "AkNYoHW5SMux5O5yEwQGSAQ6uPwEnKEw"

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

def get_chat_list():
    """获取机器人所在的群列表"""
    token = get_tenant_access_token()
    url = "https://open.feishu.cn/open-apis/im/v1/chats"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "page_size": 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if result.get("code") == 0:
        chats = result.get("data", {}).get("items", [])
        print("=" * 80)
        print("机器人所在的群列表：")
        print("=" * 80)
        
        for i, chat in enumerate(chats, 1):
            chat_id = chat.get("chat_id")
            name = chat.get("name", "未命名")
            description = chat.get("description", "")
            
            print(f"\n{i}. 群名称: {name}")
            print(f"   群ID (chat_id): {chat_id}")
            if description:
                print(f"   描述: {description}")
            print(f"   复制这个ID填入多维表格的"群组"字段: {chat_id}")
        
        print("\n" + "=" * 80)
        print(f"共找到 {len(chats)} 个群")
        print("=" * 80)
        
        return chats
    else:
        print(f"获取群列表失败: {result}")
        return []

if __name__ == "__main__":
    try:
        chats = get_chat_list()
        
        if not chats:
            print("\n提示：")
            print("1. 确认机器人已被添加到群中")
            print("2. 确认应用已开通 im:chat 权限")
            print("3. 确认应用版本已发布")
    except Exception as e:
        print(f"错误: {e}")
