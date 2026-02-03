"""
超轻量版 - 仅Webhook，无定时轮询
专为Render免费版512MB内存优化
"""
from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
import os
from feishu_api import FeishuAPI

app = Flask(__name__)

# 加载配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 初始化飞书API
api = FeishuAPI(config['app_id'], config['app_secret'])

# Webhook配置
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN', 'your_verification_token')

# 已处理记录缓存
processed_records = set()

# 简化日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    """接收飞书Webhook事件"""
    try:
        data = request.get_json()
        
        # URL验证
        if data.get('type') == 'url_verification':
            challenge = data.get('challenge')
            logger.info(f"URL验证: {challenge}")
            return jsonify({"challenge": challenge})
        
        # Token验证
        token = os.environ.get('VERIFICATION_TOKEN', VERIFICATION_TOKEN)
        if token != 'your_verification_token' and data.get('token') != token:
            return jsonify({"error": "invalid token"}), 401
        
        # 处理事件
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            if event.get('type') == 'bitable.app_table_record.changed':
                handle_event(event)
        
        return jsonify({"code": 0})
    
    except Exception as e:
        logger.error(f"错误: {e}")
        return jsonify({"error": str(e)}), 500


def handle_event(event):
    """处理记录变更事件"""
    try:
        app_token = event.get('app_token')
        table_id = event.get('table_id')
        record_id = event.get('record_id')
        
        if app_token != config['base_config']['app_token']:
            return
        
        # 获取记录
        records = api.get_table_records(app_token, table_id)
        target_record = None
        
        for record in records:
            if record['record_id'] == record_id:
                target_record = record
                break
        
        if not target_record:
            return
        
        # 获取字段映射
        fields_list = api.get_field_list(app_token, table_id)
        field_map = {f['field_name']: f['field_id'] for f in fields_list}
        
        monitor_field_id = field_map.get(config['base_config']['monitor_field'])
        chat_id_field_id = field_map.get(config['base_config']['chat_id_field'])
        
        if not monitor_field_id or not chat_id_field_id:
            return
        
        fields = target_record.get('fields', {})
        status = fields.get(monitor_field_id)
        chat_id = fields.get(chat_id_field_id)
        
        # 处理字段值
        if isinstance(status, (list, dict)):
            status = status[0].get('text', '') if isinstance(status, list) and status else status.get('text', '')
        if isinstance(chat_id, (list, dict)):
            chat_id = chat_id[0].get('text', '') if isinstance(chat_id, list) and chat_id else chat_id.get('text', '')
        
        # 检查条件
        if status == config['base_config']['target_value'] and chat_id:
            cache_key = f"{record_id}_{chat_id}"
            if cache_key not in processed_records:
                logger.info(f"更新群头像: {chat_id}")
                if update_avatar(chat_id):
                    processed_records.add(cache_key)
                    logger.info(f"成功: {chat_id}")
    
    except Exception as e:
        logger.error(f"处理事件错误: {e}")


def update_avatar(chat_id):
    """更新群头像"""
    try:
        image_key = api.upload_image(config['base_config']['avatar_path'])
        api.update_chat_avatar(chat_id, image_key)
        return True
    except Exception as e:
        logger.error(f"更新失败: {e}")
        return False


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "mode": "webhook-only-lite"
    })


logger.info("服务启动 - 轻量Webhook模式")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
