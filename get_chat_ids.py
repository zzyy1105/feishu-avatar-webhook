import sys
import os
sys.path.insert(0, r'E:\python\Lib\site-packages')

import requests
import json

APP_ID = "cli_a9fc7a617dbadcb0"
APP_SECRET = "AkNYoHW5SMux5O5yEwQGSAQ6uPwEnKEw"

# 获取token
r = requests.post(
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id': APP_ID, 'app_secret': APP_SECRET}
)
token = r.json()['tenant_access_token']

# 获取群列表
r2 = requests.get(
    'https://open.feishu.cn/open-apis/im/v1/chats',
    headers={'Authorization': f'Bearer {token}'},
    params={'page_size': 100}
)

result = r2.json()
chats = result.get('data', {}).get('items', [])

print("=" * 60)
print("Bot chat list:")
print("=" * 60)

if chats:
    for i, chat in enumerate(chats, 1):
        print(f"\n{i}. Name: {chat.get('name', 'No name')}")
        print(f"   chat_id: {chat.get('chat_id')}")
        print(f"   Copy this ID to table: {chat.get('chat_id')}")
else:
    print("No chats found")
    print("\nTips:")
    print("1. Make sure bot is added to groups")
    print("2. Check app has im:chat permission")

print("\n" + "=" * 60)
