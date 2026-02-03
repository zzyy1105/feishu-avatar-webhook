"""
Windows服务安装脚本
将监听程序注册为Windows系统服务，开机自动启动
"""
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import time
import logging
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from monitor import AvatarMonitor


class FeishuAvatarService(win32serviceutil.ServiceFramework):
    """飞书群头像更新服务"""
    
    _svc_name_ = "FeishuAvatarMonitor"
    _svc_display_name_ = "飞书群头像自动更新服务"
    _svc_description_ = "监听多维表格变化，自动更新飞书群头像"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True
        
        # 设置工作目录
        os.chdir(str(current_dir))
        
        # 设置日志
        log_dir = current_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=str(log_dir / "service.log"),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def SvcStop(self):
        """停止服务"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.is_running = False
        logging.info("服务停止请求已接收")
    
    def SvcDoRun(self):
        """运行服务"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        logging.info("服务启动")
        self.main()
    
    def main(self):
        """主循环"""
        try:
            monitor = AvatarMonitor()
            logging.info("监听器初始化成功")
            
            while self.is_running:
                try:
                    monitor.check_and_update()
                    # 等待指定时间或停止事件
                    if win32event.WaitForSingleObject(
                        self.stop_event, 
                        monitor.check_interval * 1000
                    ) == win32event.WAIT_OBJECT_0:
                        break
                except Exception as e:
                    logging.error(f"检查更新时出错: {e}", exc_info=True)
                    time.sleep(30)
        
        except Exception as e:
            logging.error(f"服务运行错误: {e}", exc_info=True)
        
        logging.info("服务已停止")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FeishuAvatarService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FeishuAvatarService)
