import sys
import os
sys.path.insert(0, r'E:\python\Lib\site-packages')

import requests
import json

APP_ID = "cli_a9fc7a617dbadcb0"
APP_SECRET = "AkNYoHW5SMux5O5yEwQGSAQ6uPwEnKEw"

print("=" * 60)
print("Getting chat_id for all groups...")
print("=" * 60)

# Step 1: Get token
print("\nStep 1: Getting access token...")
r = requests.post(
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id': APP_ID, 'app_secret': APP_SECRET}
)

if r.status_code != 200:
    print(f"Error: HTTP {r.status_code}")
    print(r.text)
    exit()

result = r.json()
if result.get('code') != 0:
    print(f"Error: {result}")
    exit()

token = result['tenant_access_token']
print(f"Success! Token: {token[:20]}...")

# Step 2: Get all chats where bot is a member
print("\nStep 2: Getting all chats...")
r2 = requests.get(
    'https://open.feishu.cn/open-apis/im/v1/chats',
    headers={'Authorization': f'Bearer {token}'},
    params={'page_size': 100}
)

if r2.status_code != 200:
    print(f"Error: HTTP {r2.status_code}")
    print(r2.text)
    exit()

result2 = r2.json()
print(f"API Response code: {result2.get('code')}")
print(f"API Response msg: {result2.get('msg')}")

if result2.get('code') != 0:
    print(f"\nError getting chats: {result2}")
    print("\nPossible reasons:")
    print("1. Bot not added to any groups yet")
    print("2. Missing 'im:chat' permission")
    print("3. App not published")
    exit()

chats = result2.get('data', {}).get('items', [])

print("\n" + "=" * 60)
print(f"Found {len(chats)} group(s):")
print("=" * 60)

if not chats:
    print("\nNo groups found!")
    print("\nTo fix this:")
    print("1. Add your bot to a Feishu group")
    print("2. Make sure app has 'im:chat' permission")
    print("3. Make sure app version is published")
else:
    for i, chat in enumerate(chats, 1):
        chat_id = chat.get('chat_id')
        name = chat.get('name', 'No name')
        description = chat.get('description', '')
        
        print(f"\n{i}. Group name: {name}")
        print(f"   chat_id: {chat_id}")
        print(f"   >>> Copy this to your table: {chat_id}")
        if description:
            print(f"   Description: {description}")

print("\n" + "=" * 60)
print("Next steps:")
print("1. Copy the chat_id above")
print("2. Open your Feishu table")
print("3. Paste chat_id into 'chat id' field")
print("4. Set status to '已通过'")
print("5. Save and test!")
print("=" * 60)
