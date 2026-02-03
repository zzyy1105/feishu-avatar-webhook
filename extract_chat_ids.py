import sys
import os
sys.path.insert(0, r'E:\python\Lib\site-packages')

import requests
import json

APP_ID = "cli_a9fc7a617dbadcb0"
APP_SECRET = "AkNYoHW5SMux5O5yEwQGSAQ6uPwEnKEw"
APP_TOKEN = "FbU2bnPIPawHQvsIMudcANvwnWf"
TABLE_ID = "tblp5MrI71tKK7wq"

# 获取token
r = requests.post(
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id': APP_ID, 'app_secret': APP_SECRET}
)
token = r.json()['tenant_access_token']
print(f"Token: {token[:20]}...")

# 获取字段列表
print("\n" + "=" * 60)
print("Getting field list...")
print("=" * 60)

r_fields = requests.get(
    f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields',
    headers={'Authorization': f'Bearer {token}'}
)

fields_result = r_fields.json()
if fields_result.get('code') != 0:
    print(f"Error getting fields: {fields_result}")
    exit()

fields = fields_result.get('data', {}).get('items', [])
field_mapping = {field['field_name']: field['field_id'] for field in fields}

print("\nFields found:")
for name, fid in field_mapping.items():
    print(f"  - {name}: {fid}")

# 找到"飞书项目群"字段
chat_field_id = field_mapping.get('飞书项目群')
if not chat_field_id:
    print("\nError: '飞书项目群' field not found!")
    exit()

print(f"\nFound chat field: {chat_field_id}")

# 获取所有记录
print("\n" + "=" * 60)
print("Getting records...")
print("=" * 60)

r_records = requests.post(
    f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search',
    headers={'Authorization': f'Bearer {token}'},
    json={'page_size': 100}
)

records_result = r_records.json()
if records_result.get('code') != 0:
    print(f"Error getting records: {records_result}")
    exit()

records = records_result.get('data', {}).get('items', [])
print(f"\nTotal records: {len(records)}")

# 提取chat_id
print("\n" + "=" * 60)
print("Extracting chat_id from group field:")
print("=" * 60)

for i, record in enumerate(records, 1):
    record_id = record['record_id']
    fields_data = record.get('fields', {})
    
    # 获取群组字段的值
    chat_field_value = fields_data.get(chat_field_id)
    
    print(f"\n{i}. Record ID: {record_id}")
    print(f"   Raw value: {chat_field_value}")
    print(f"   Type: {type(chat_field_value)}")
    
    # 尝试提取chat_id
    if chat_field_value:
        if isinstance(chat_field_value, list):
            for item in chat_field_value:
                if isinstance(item, dict):
                    # 可能的字段名：chat_id, id, open_chat_id
                    chat_id = (item.get('chat_id') or 
                              item.get('id') or 
                              item.get('open_chat_id') or
                              item.get('text'))
                    if chat_id:
                        print(f"   >>> chat_id: {chat_id}")
                        print(f"   >>> Use this in table!")
        elif isinstance(chat_field_value, dict):
            chat_id = (chat_field_value.get('chat_id') or 
                      chat_field_value.get('id') or 
                      chat_field_value.get('open_chat_id') or
                      chat_field_value.get('text'))
            if chat_id:
                print(f"   >>> chat_id: {chat_id}")
                print(f"   >>> Use this in table!")
        elif isinstance(chat_field_value, str):
            print(f"   >>> chat_id: {chat_field_value}")
            print(f"   >>> Use this in table!")

print("\n" + "=" * 60)
