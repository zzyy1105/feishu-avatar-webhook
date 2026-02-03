"""
简化版Webhook服务 - 专为Render免费版优化
移除定时轮询，只保留Webhook功能
"""
from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
import os
import sys

app = Flask(__name__)

# 简化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# 全局变量
config = None
api = None
processed_records = set()

def init_app():
    """初始化应用"""
    global config, api
    
    try:
        # 加载配置
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info("配置加载成功")
        
        # 延迟导入，减少启动内存
        from feishu_api import FeishuAPI
        api = FeishuAPI(config['app_id'], config['app_secret'])
        logger.info("飞书API初始化成功")
        
        return True
    except Exception as e:
        logger.error(f"初始化失败: {e}")
        return False


@app.route('/webhook', methods=['POST'])
def webhook():
    """接收飞书Webhook事件"""
    try:
        data = request.get_json()
        
        # URL验证（首次配置）
        if data.get('type') == 'url_verification':
            challenge = data.get('challenge')
            logger.info(f"URL验证: {challenge}")
            return jsonify({"challenge": challenge})
        
        # Token验证
        token = os.environ.get('VERIFICATION_TOKEN', 'your_verification_token')
        if token != 'your_verification_token' and data.get('token') != token:
            logger.warning("Token验证失败")
            return jsonify({"error": "invalid token"}), 401
        
        # 处理事件
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            event_type = event.get('type')
            
            if event_type == 'bitable.app_table_record.changed':
                logger.info("收到记录变更事件")
                handle_record_change(event)
        
        return jsonify({"code": 0, "msg": "success"})
    
    except Exception as e:
        logger.error(f"Webhook错误: {e}")
        return jsonify({"error": str(e)}), 500


def handle_record_change(event):
    """处理记录变更"""
    try:
        if not config or not api:
            logger.error("服务未初始化")
            return
        
        app_token = event.get('app_token')
        table_id = event.get('table_id')
        record_id = event.get('record_id')
        
        # 检查是否是目标表格
        if app_token != config['base_config']['app_token']:
            logger.info("非目标表格，忽略")
            return
        
        logger.info(f"处理记录: {record_id}")
        
        # 获取记录详情
        records = api.get_table_records(app_token, table_id)
        target_record = None
        
        for record in records:
            if record['record_id'] == record_id:
                target_record = record
                break
        
        if not target_record:
            logger.warning(f"未找到记录: {record_id}")
            return
        
        # 获取字段映射
        field_list = api.get_field_list(app_token, table_id)
        field_mapping = {field['field_name']: field['field_id'] for field in field_list}
        
        monitor_field_id = field_mapping.get(config['base_config']['monitor_field'])
        chat_id_field_id = field_mapping.get(config['base_config']['chat_id_field'])
        
        if not monitor_field_id or not chat_id_field_id:
            logger.error("未找到必要字段")
            return
        
        # 获取字段值
        fields = target_record.get('fields', {})
        status = fields.get(monitor_field_id)
        chat_id = fields.get(chat_id_field_id)
        
        # 处理字段值格式
        if isinstance(status, list) and len(status) > 0:
            status = status[0].get('text', '')
        elif isinstance(status, dict):
            status = status.get('text', '')
        
        if isinstance(chat_id, list) and len(chat_id) > 0:
            chat_id = chat_id[0].get('text', '')
        elif isinstance(chat_id, dict):
            chat_id = chat_id.get('text', '')
        
        logger.info(f"状态={status}, 群组={chat_id}")
        
        # 检查条件
        if status == config['base_config']['target_value'] and chat_id:
            cache_key = f"{record_id}_{chat_id}"
            
            if cache_key not in processed_records:
                logger.info(f"条件满足，更新群头像: {chat_id}")
                
                if update_avatar(chat_id):
                    processed_records.add(cache_key)
                    logger.info(f"成功更新: {chat_id}")
                else:
                    logger.error(f"更新失败: {chat_id}")
        else:
            logger.info("条件不满足，跳过")
    
    except Exception as e:
        logger.error(f"处理记录错误: {e}", exc_info=True)


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
        
        return True
    except Exception as e:
        logger.error(f"更新头像失败: {e}", exc_info=True)
        return False


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "mode": "webhook-only",
        "initialized": config is not None and api is not None
    })


@app.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        "service": "飞书群头像自动更新",
        "mode": "webhook-only",
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook"
        }
    })


# 启动时初始化
logger.info("=" * 60)
logger.info("飞书群头像自动更新服务")
logger.info("模式: Webhook Only (轻量版)")
logger.info("=" * 60)

if init_app():
    logger.info("服务初始化成功")
else:
    logger.error("服务初始化失败")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
