import json
import time
import os
import logging
from datetime import datetime
from feishu_api import FeishuAPI


class AvatarMonitor:
    """飞书群头像监听更新器"""
    
    def __init__(self, config_path: str = "config.json"):
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 初始化飞书API
        self.api = FeishuAPI(
            self.config['app_id'],
            self.config['app_secret']
        )
        
        # 配置参数
        self.app_token = self.config['base_config']['app_token']
        self.table_id = self.config['base_config']['table_id']
        self.monitor_field = self.config['base_config']['monitor_field']
        self.target_value = self.config['base_config']['target_value']
        self.chat_id_field = self.config['base_config']['chat_id_field']
        self.avatar_path = self.config['base_config']['avatar_path']
        self.check_interval = self.config['monitor_config']['check_interval']
        
        # 状态缓存文件
        self.cache_file = "status_cache.json"
        self.status_cache = self.load_cache()
        
        # 字段映射缓存
        self.field_mapping = {}
        
        # 设置日志
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"monitor_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=getattr(logging, self.config['monitor_config']['log_level']),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_cache(self) -> dict:
        """加载状态缓存"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_cache(self):
        """保存状态缓存"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.status_cache, f, ensure_ascii=False, indent=2)
    
    def get_field_mapping(self):
        """获取字段名称到field_id的映射"""
        if self.field_mapping:
            return self.field_mapping
        
        try:
            fields = self.api.get_field_list(self.app_token, self.table_id)
            self.field_mapping = {field['field_name']: field['field_id'] for field in fields}
            self.logger.info(f"字段映射: {self.field_mapping}")
            return self.field_mapping
        except Exception as e:
            self.logger.error(f"获取字段映射失败: {e}")
            return {}
    
    def check_and_update(self):
        """检查表格并更新头像"""
        try:
            # 获取字段映射
            field_mapping = self.get_field_mapping()
            if not field_mapping:
                self.logger.error("无法获取字段映射,跳过本次检查")
                return
            
            monitor_field_id = field_mapping.get(self.monitor_field)
            chat_id_field_id = field_mapping.get(self.chat_id_field)
            
            if not monitor_field_id or not chat_id_field_id:
                self.logger.error(f"未找到必要字段: {self.monitor_field} 或 {self.chat_id_field}")
                return
            
            # 获取所有记录
            records = self.api.get_table_records(self.app_token, self.table_id)
            self.logger.info(f"获取到 {len(records)} 条记录")
            
            # 检查每条记录
            for record in records:
                record_id = record['record_id']
                fields = record.get('fields', {})
                
                # 获取字段值
                status = fields.get(monitor_field_id)
                chat_id = fields.get(chat_id_field_id)
                
                # 处理状态字段(可能是文本或选项类型)
                if isinstance(status, list) and len(status) > 0:
                    status = status[0].get('text', '')
                elif isinstance(status, dict):
                    status = status.get('text', '')
                
                # 处理chat_id字段
                if isinstance(chat_id, list) and len(chat_id) > 0:
                    chat_id = chat_id[0].get('text', '')
                elif isinstance(chat_id, dict):
                    chat_id = chat_id.get('text', '')
                
                self.logger.debug(f"记录 {record_id}: 状态={status}, 群组={chat_id}")
                
                # 检查是否需要更新
                if status == self.target_value and chat_id:
                    # 检查是否已处理过
                    if self.status_cache.get(record_id) == self.target_value:
                        continue
                    
                    self.logger.info(f"发现状态变更: 记录 {record_id}, 群组 {chat_id}")
                    
                    # 更新头像
                    if self.update_avatar(chat_id):
                        # 更新缓存
                        self.status_cache[record_id] = self.target_value
                        self.save_cache()
                        self.logger.info(f"成功更新群 {chat_id} 的头像")
                    else:
                        self.logger.error(f"更新群 {chat_id} 的头像失败")
        
        except Exception as e:
            self.logger.error(f"检查更新时出错: {e}", exc_info=True)
    
    def update_avatar(self, chat_id: str) -> bool:
        """更新群头像"""
        try:
            # 上传图片
            self.logger.info(f"正在上传头像图片: {self.avatar_path}")
            image_key = self.api.upload_image(self.avatar_path)
            self.logger.info(f"图片上传成功, image_key: {image_key}")
            
            # 更新群头像
            self.logger.info(f"正在更新群 {chat_id} 的头像")
            self.api.update_chat_avatar(chat_id, image_key)
            
            return True
        except Exception as e:
            self.logger.error(f"更新头像失败: {e}", exc_info=True)
            return False
    
    def run(self):
        """运行监听服务"""
        self.logger.info("=" * 60)
        self.logger.info("飞书群头像自动更新服务启动")
        self.logger.info(f"监听表格: {self.app_token}")
        self.logger.info(f"监听字段: {self.monitor_field}")
        self.logger.info(f"目标值: {self.target_value}")
        self.logger.info(f"检查间隔: {self.check_interval}秒")
        self.logger.info("=" * 60)
        
        while True:
            try:
                self.logger.info(f"开始检查... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                self.check_and_update()
                self.logger.info(f"检查完成,等待 {self.check_interval} 秒")
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                self.logger.info("收到停止信号,服务退出")
                break
            except Exception as e:
                self.logger.error(f"运行时错误: {e}", exc_info=True)
                self.logger.info(f"等待 {self.check_interval} 秒后重试")
                time.sleep(self.check_interval)


if __name__ == "__main__":
    monitor = AvatarMonitor()
    monitor.run()
