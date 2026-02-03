"""
混合模式：Webhook + 定时轮询
- Webhook: 实时响应（主要方式）
- 轮询: 每5分钟检查一次（兜底方案）
"""
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import json
import hashlib
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
VERIFICATION_TOKEN = "your_verification_token"
ENCRYPT_KEY = "your_encrypt_key"

# 已处理记录缓存（避免重复处理）
processed_records = set()
CACHE_FILE = "processed_cache.json"

# 设置日志
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/hybrid_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_processed_cache():
    """加载已处理记录缓存"""
    global processed_records
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                processed_records = set(json.load(f))
        except:
            processed_records = set()


def save_processed_cache():
    """保存已处理记录缓存"""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(processed_records), f)


def check_and_update():
    """定时检查并更新（轮询模式）"""
    try:
        logger.info("=" * 60)
        logger.info(f"开始定时检查 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        
        app_token = config['base_config']['app_token']
        table_id = config['base_config']['table_id']
        
        # 获取字段映射
        field_list = api.get_field_list(app_token, table_id)
        field_mapping = {field['field_name']: field['field_id'] for field in field_list}
        
        monitor_field_id = field_mapping.get(config['base_config']['monitor_field'])
        chat_id_field_id = field_mapping.get(config['base_config']['chat_id_field'])
        
        if not monitor_field_id or not chat_id_field_id:
            logger.error(f"未找到必要字段")
            return
        
        # 获取所有记录
        records = api.get_table_records(app_token, table_id)
        logger.info(f"获取到 {len(records)} 条记录")
        
        updated_count = 0
        
        for record in records:
            record_id = record['record_id']
            fields = record.get('fields', {})
            
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
            
            # 检查是否满足条件且未处理过
            if status == config['base_config']['target_value'] and chat_id:
                cache_key = f"{record_id}_{chat_id}"
                
                if cache_key not in processed_records:
                    logger.info(f"[轮询] 发现新记录: {record_id}, 群组: {chat_id}")
                    
                    if update_avatar(chat_id):
                        processed_records.add(cache_key)
                        save_processed_cache()
                        updated_count += 1
                        logger.info(f"[轮询] 成功更新群 {chat_id} 的头像")
        
        logger.info(f"定时检查完成，更新了 {updated_count} 个群头像")
        logger.info("=" * 60)
    
    except Exception as e:
        logger.error(f"定时检查时出错: {e}", exc_info=True)


@app.route('/webhook', methods=['POST'])
def webhook():
    """接收飞书Webhook事件"""
    try:
        data = request.get_json()
        logger.info(f"[Webhook] 收到请求: {data.get('type')}")
        
        # URL验证（首次配置时，不验证token）
        if data.get('type') == 'url_verification':
            challenge = data.get('challenge')
            logger.info(f"[Webhook] URL验证: {challenge}")
            return jsonify({"challenge": challenge})
        
        # 其他请求验证Token
        token = os.environ.get('VERIFICATION_TOKEN', VERIFICATION_TOKEN)
        if token != 'your_verification_token' and data.get('token') != token:
            logger.warning(f"[Webhook] Token验证失败: 期望={token}, 实际={data.get('token')}")
            return jsonify({"error": "invalid token"}), 401
        
        # 处理事件
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            event_type = event.get('type')
            
            logger.info(f"[Webhook] 事件类型: {event_type}")
            
            if event_type == 'bitable.app_table_record.changed':
                handle_webhook_event(event)
        
        return jsonify({"code": 0, "msg": "success"})
    
    except Exception as e:
        logger.error(f"[Webhook] 处理时出错: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def handle_webhook_event(event):
    """处理Webhook事件"""
    try:
        app_token = event.get('app_token')
        table_id = event.get('table_id')
        record_id = event.get('record_id')
        
        if app_token != config['base_config']['app_token']:
            return
        
        # 获取记录详情
        records = api.get_table_records(app_token, table_id)
        target_record = None
        
        for record in records:
            if record['record_id'] == record_id:
                target_record = record
                break
        
        if not target_record:
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
        
        # 检查条件
        if status == config['base_config']['target_value'] and chat_id:
            cache_key = f"{record_id}_{chat_id}"
            
            if cache_key not in processed_records:
                logger.info(f"[Webhook] 条件满足，更新群头像: {chat_id}")
                
                if update_avatar(chat_id):
                    processed_records.add(cache_key)
                    save_processed_cache()
                    logger.info(f"[Webhook] 成功更新群 {chat_id} 的头像")
    
    except Exception as e:
        logger.error(f"[Webhook] 处理事件时出错: {e}", exc_info=True)


def update_avatar(chat_id):
    """更新群头像"""
    try:
        avatar_path = config['base_config']['avatar_path']
        
        # 上传图片
        image_key = api.upload_image(avatar_path)
        
        # 更新群头像
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
        "processed_count": len(processed_records),
        "mode": "hybrid (webhook + polling)"
    })


@app.route('/force-check', methods=['POST'])
def force_check():
    """手动触发检查"""
    check_and_update()
    return jsonify({"msg": "检查已触发"})


# 初始化
load_processed_cache()

# 创建定时任务调度器
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=check_and_update,
    trigger="interval",
    minutes=5,  # 每5分钟检查一次
    id='check_update_job',
    name='定时检查多维表格',
    replace_existing=True
)
scheduler.start()

logger.info("=" * 60)
logger.info("飞书群头像自动更新服务启动（混合模式）")
logger.info("模式: Webhook实时响应 + 5分钟定时轮询")
logger.info("=" * 60)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
