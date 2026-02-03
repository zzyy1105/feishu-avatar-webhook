"""
飞书Webhook方案 - 基于事件订阅的实时更新
无需服务器持续运行，飞书主动推送变更事件
"""
from flask import Flask, request, jsonify
import json
import hashlib
import base64
from feishu_api import FeishuAPI
import logging
from datetime import datetime
import os

app = Flask(__name__)

# 加载配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 初始化飞书API
api = FeishuAPI(config['app_id'], config['app_secret'])

# Webhook配置（需要在飞书开放平台配置）
VERIFICATION_TOKEN = "your_verification_token"  # 在飞书开放平台获取
ENCRYPT_KEY = "your_encrypt_key"  # 在飞书开放平台获取（如果启用加密）

# 设置日志
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/webhook_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def verify_signature(timestamp, nonce, encrypt_key, body):
    """验证请求签名"""
    # 按照飞书文档要求拼接字符串
    sign_str = f"{timestamp}{nonce}{encrypt_key}{body}"
    # 计算SHA-256
    sign = hashlib.sha256(sign_str.encode()).hexdigest()
    return sign


@app.route('/webhook', methods=['POST'])
def webhook():
    """接收飞书Webhook事件"""
    try:
        # 获取请求数据
        data = request.get_json()
        logger.info(f"收到Webhook请求: {json.dumps(data, ensure_ascii=False)}")
        
        # 验证Token
        if data.get('token') != VERIFICATION_TOKEN:
            logger.warning("Token验证失败")
            return jsonify({"error": "invalid token"}), 401
        
        # URL验证（首次配置时）
        if data.get('type') == 'url_verification':
            challenge = data.get('challenge')
            logger.info(f"URL验证: {challenge}")
            return jsonify({"challenge": challenge})
        
        # 处理事件回调
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            event_type = data.get('event', {}).get('type')
            
            logger.info(f"事件类型: {event_type}")
            
            # 处理多维表格记录变更事件
            if event_type == 'bitable.app_table_record.changed':
                handle_record_changed(event)
        
        return jsonify({"code": 0, "msg": "success"})
    
    except Exception as e:
        logger.error(f"处理Webhook时出错: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def handle_record_changed(event):
    """处理记录变更事件"""
    try:
        # 获取变更信息
        app_token = event.get('app_token')
        table_id = event.get('table_id')
        record_id = event.get('record_id')
        
        logger.info(f"记录变更: app_token={app_token}, table_id={table_id}, record_id={record_id}")
        
        # 检查是否是我们监听的表格
        if app_token != config['base_config']['app_token']:
            logger.info("不是目标表格，忽略")
            return
        
        # 获取记录详情
        records = api.get_table_records(app_token, table_id)
        
        # 查找变更的记录
        target_record = None
        for record in records:
            if record['record_id'] == record_id:
                target_record = record
                break
        
        if not target_record:
            logger.warning(f"未找到记录: {record_id}")
            return
        
        fields = target_record.get('fields', {})
        
        # 获取字段映射
        field_list = api.get_field_list(app_token, table_id)
        field_mapping = {field['field_name']: field['field_id'] for field in field_list}
        
        monitor_field_id = field_mapping.get(config['base_config']['monitor_field'])
        chat_id_field_id = field_mapping.get(config['base_config']['chat_id_field'])
        
        # 获取字段值
        status = fields.get(monitor_field_id)
        chat_id = fields.get(chat_id_field_id)
        
        # 处理字段值
        if isinstance(status, list) and len(status) > 0:
            status = status[0].get('text', '')
        elif isinstance(status, dict):
            status = status.get('text', '')
        
        if isinstance(chat_id, list) and len(chat_id) > 0:
            chat_id = chat_id[0].get('text', '')
        elif isinstance(chat_id, dict):
            chat_id = chat_id.get('text', '')
        
        logger.info(f"字段值: 状态={status}, 群组={chat_id}")
        
        # 检查是否满足条件
        if status == config['base_config']['target_value'] and chat_id:
            logger.info(f"条件满足，开始更新群头像: {chat_id}")
            update_avatar(chat_id)
        else:
            logger.info("条件不满足，跳过")
    
    except Exception as e:
        logger.error(f"处理记录变更时出错: {e}", exc_info=True)


def update_avatar(chat_id):
    """更新群头像"""
    try:
        avatar_path = config['base_config']['avatar_path']
        
        # 上传图片
        logger.info(f"上传头像: {avatar_path}")
        image_key = api.upload_image(avatar_path)
        logger.info(f"图片上传成功: {image_key}")
        
        # 更新群头像
        logger.info(f"更新群头像: {chat_id}")
        api.update_chat_avatar(chat_id, image_key)
        logger.info(f"群头像更新成功: {chat_id}")
        
    except Exception as e:
        logger.error(f"更新头像失败: {e}", exc_info=True)


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("飞书Webhook服务启动")
    logger.info(f"监听端口: 5000")
    logger.info("=" * 60)
    
    # 生产环境建议使用gunicorn或uwsgi
    app.run(host='0.0.0.0', port=5000, debug=False)
