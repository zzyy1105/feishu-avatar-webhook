import requests
import json
import time
import os
from typing import Optional, Dict, Any


class FeishuAPI:
    """飞书API封装类"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None
        self.token_expire_time = 0
        self.base_url = "https://open.feishu.cn/open-apis"
    
    def get_tenant_access_token(self) -> str:
        """获取tenant_access_token"""
        # 如果token未过期,直接返回
        if self.tenant_access_token and time.time() < self.token_expire_time:
            return self.tenant_access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if result.get("code") == 0:
            self.tenant_access_token = result["tenant_access_token"]
            # 提前5分钟刷新token
            self.token_expire_time = time.time() + result["expire"] - 300
            return self.tenant_access_token
        else:
            raise Exception(f"获取token失败: {result}")
    
    def get_table_records(self, app_token: str, table_id: str, 
                         page_size: int = 100) -> list:
        """获取多维表格记录"""
        token = self.get_tenant_access_token()
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        all_records = []
        page_token = None
        
        while True:
            data = {"page_size": page_size}
            if page_token:
                data["page_token"] = page_token
            
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取表格记录失败: {result}")
            
            items = result.get("data", {}).get("items", [])
            all_records.extend(items)
            
            # 检查是否还有下一页
            page_token = result.get("data", {}).get("page_token")
            if not page_token or not result.get("data", {}).get("has_more"):
                break
        
        return all_records
    
    def upload_image(self, image_path: str) -> str:
        """上传图片并返回image_key"""
        token = self.get_tenant_access_token()
        url = f"{self.base_url}/im/v1/images"
        
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(image_path, 'rb') as f:
            files = {
                'image': (os.path.basename(image_path), f, 'image/jpeg')
            }
            data = {'image_type': 'avatar'}
            
            response = requests.post(url, headers=headers, files=files, data=data)
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"上传图片失败: {result}")
            
            return result["data"]["image_key"]
    
    def update_chat_avatar(self, chat_id: str, image_key: str) -> bool:
        """更新群聊头像"""
        token = self.get_tenant_access_token()
        url = f"{self.base_url}/im/v1/chats/{chat_id}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {"avatar": image_key}
        
        response = requests.put(url, headers=headers, json=data)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"更新群头像失败: {result}")
        
        return True
    
    def get_field_list(self, app_token: str, table_id: str) -> list:
        """获取表格字段列表"""
        token = self.get_tenant_access_token()
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(url, headers=headers)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取字段列表失败: {result}")
        
        return result.get("data", {}).get("items", [])
