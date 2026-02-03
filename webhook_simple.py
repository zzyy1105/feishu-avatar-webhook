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
        
        # 记录所有收到的请求
        logger.info("=" * 60)
        logger.info("收到Webhook请求")
        
        # 判断是v1.0还是v2.0格式
        schema = data.get('schema', '1.0')
        
        if schema == '2.0':
            # v2.0格式
            header = data.get('header', {})
            event_type = header.get('event_type')
            token = header.get('token')
            
            logger.info(f"Schema: 2.0")
            logger.info(f"事件类型: {event_type}")
            logger.info(f"完整数据: {json.dumps(data, ensure_ascii=False)}")
            logger.info("=" * 60)
            
            # 处理事件
            if event_type in ['drive.file.bitable_record_changed_v1',
                             'drive.file.bitable_field_changed_v1']:
                logger.info("收到多维表格变更事件 (v2.0)")
                event_data = data.get('event', {})
                handle_record_change(event_data)
            else:
                logger.info(f"未处理的事件类型: {event_type}")
            
            # v2.0需要返回空JSON
            return jsonify({})
        
        else:
            # v1.0格式
            request_type = data.get('type')
            logger.info(f"Schema: 1.0")
            logger.info(f"请求类型: {request_type}")
            logger.info(f"完整数据: {json.dumps(data, ensure_ascii=False)}")
            logger.info("=" * 60)
            
            # URL验证（首次配置）
            if request_type == 'url_verification':
                challenge = data.get('challenge')
                logger.info(f"URL验证: {challenge}")
                return jsonify({"challenge": challenge})
            
            # Token验证
            token = os.environ.get('VERIFICATION_TOKEN', 'your_verification_token')
            if token != 'your_verification_token' and data.get('token') != token:
                logger.warning(f"Token验证失败: 期望={token}, 实际={data.get('token')}")
                return jsonify({"error": "invalid token"}), 401
            
            # 处理事件
            if request_type == 'event_callback':
                event = data.get('event', {})
                event_type = event.get('type')
                
                logger.info(f"事件类型: {event_type}")
                
                # 支持多个事件类型
                if event_type in ['bitable.app_table_record.changed', 
                                 'bitable.app_table_field.changed',
                                 'drive.file.bitable_field_changed_v1',
                                 'drive.file.bitable_record_changed_v1',
                                 'bitable_app_table_record_changed',
                                 'bitable_app_table_field_changed']:
                    logger.info("收到多维表格变更事件 (v1.0)")
                    handle_record_change(event)
                else:
                    logger.info(f"未处理的事件类型: {event_type}")
            
            return jsonify({"code": 0, "msg": "success"})
    
    except Exception as e:
        logger.error(f"Webhook错误: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def handle_record_change(event):
    """处理记录变更"""
    try:
        if not config or not api:
            logger.error("服务未初始化")
            return
        
        # v2.0事件的数据在object字段中
        event_data = event.get('object', event)
        
        app_token = event_data.get('app_token')
        table_id = event_data.get('table_id')
        record_id = event_data.get('record_id')
        
        logger.info(f"事件数据: app_token={app_token}, table_id={table_id}, record_id={record_id}")
        
        # 检查是否是目标表格
        if app_token != config['base_config']['app_token']:
            logger.info(f"非目标表格，忽略")
            return
        
        logger.info(f"处理记录: {record_id}")
        
        # 直接获取单条记录，而不是获取所有记录（节省内存）
        # 注意：这里简化处理，直接从事件中获取信息
        # 如果需要完整记录数据，可以调用单条记录API
        
        # 获取字段映射
        field_list = api.get_field_list(app_token, table_id)
        field_mapping = {field['field_name']: field['field_id'] for field in field_list}
        
        monitor_field_id = field_mapping.get(config['base_config']['monitor_field'])
        chat_id_field_id = field_mapping.get(config['base_config']['chat_id_field'])
        
        if not monitor_field_id or not chat_id_field_id:
            logger.error("未找到必要字段")
            return
        
        # 获取单条记录（而不是所有记录）
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
            headers = {"Authorization": f"Bearer {api.get_tenant_access_token()}"}
            
            import requests
            response = requests.get(url, headers=headers)
            result = response.json()
            
            if result.get('code') != 0:
                logger.error(f"获取记录失败: {result}")
                return
            
            target_record = result.get('data', {}).get('record', {})
            
        except Exception as e:
            logger.error(f"获取记录异常: {e}")
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
        elif isinstance(chat_id, str):
            chat_id = chat_id.strip()
        
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
    import psutil
    import os
    
    # 获取当前进程
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "mode": "webhook-only",
        "initialized": config is not None and api is not None,
        "memory": {
            "rss_mb": round(memory_info.rss / 1024 / 1024, 2),  # 实际物理内存
            "vms_mb": round(memory_info.vms / 1024 / 1024, 2),  # 虚拟内存
            "percent": round(process.memory_percent(), 2)
        }
    })


@app.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        "service": "飞书群头像自动更新",
        "mode": "webhook-only",
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook",
            "test": "/test-webhook"
        }
    })
def test_webhook():
    """测试Webhook功能"""
    logger.info("=" * 60)
    logger.info("手动测试Webhook")
    logger.info("=" * 60)
    
    # 模拟一个事件
    test_event = {
        "type": "event_callback",
        "event": {
            "type": "bitable.app_table_record.changed",
            "app_token": config['base_config']['app_token'],
            "table_id": config['base_config']['table_id'],
            "record_id": "test_record_id"
        }
    }
    
    logger.info(f"模拟事件: {json.dumps(test_event, ensure_ascii=False)}")
    
    try:
        handle_record_change(test_event['event'])
        return jsonify({"status": "ok", "msg": "测试完成，查看日志"})
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        return jsonify({"status": "error", "msg": str(e)}), 500


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
