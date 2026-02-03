# 飞书群头像自动更新系统

## 功能说明
当多维表格中"发机通道申请状态"字段变更为"已通过"时,自动更新对应飞书群的头像。

## 文件说明
- `config.json` - 配置文件(存储app_id、app_secret等)
- `avatar.jpg` - 新的群头像图片
- `monitor.py` - 主监听脚本
- `feishu_api.py` - 飞书API封装
- `logs/` - 日志目录

## 使用前准备

### 1. 飞书应用权限配置
请确保你的飞书应用已开通以下权限:

**多维表格权限:**
- `bitable:app` - 查看、评论、编辑和管理多维表格
- `bitable:app:readonly` - 查看多维表格

**群聊权限:**
- `im:chat` - 获取与更新群组信息
- `im:chat:readonly` - 获取群组信息

**图片上传权限:**
- `im:resource` - 上传图片、文件等资源

### 2. 配置步骤
1. 前往飞书开放平台: https://open.feishu.cn/
2. 进入你的应用 -> 权限管理
3. 添加上述权限并发布新版本
4. 在"凭证与基础信息"中确认 app_id 和 app_secret

### 3. 多维表格设置
确保多维表格中包含以下字段:
- `发机通道申请状态` - 监听此字段变化
- `群组` - 存储飞书群的 chat_id

## 安装依赖
```bash
pip install requests schedule
```

## 运行方式

### 方式1: 临时运行（推荐测试时使用）
双击 `启动服务.bat`

### 方式2: 持续运行（自动重启）
双击 `启动服务_持续运行.bat`
- 服务异常退出会自动重启
- 关闭窗口即停止服务

### 方式3: 注册为Windows系统服务（推荐生产环境）

#### 选项A: 使用pywin32（需要管理员权限）
1. 右键点击 `安装为系统服务.bat`
2. 选择"以管理员身份运行"
3. 服务将在后台运行，开机自动启动

管理命令:
```bash
python service.py start   # 启动服务
python service.py stop    # 停止服务
python service.py restart # 重启服务
python service.py remove  # 卸载服务
```

#### 选项B: 使用NSSM（更简单，推荐）
1. 下载NSSM: https://nssm.cc/download
2. 将 nssm.exe 放到当前目录
3. 以管理员身份运行命令提示符
4. 执行: `python nssm_service.py install`

### 方式4: 使用任务计划程序
1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器: 系统启动时
4. 操作: 启动程序
   - 程序: `python.exe`的完整路径
   - 参数: `monitor.py`
   - 起始于: `E:\AI\修改头像`

## 注意事项
- 脚本会每30秒检查一次多维表格
- 状态变化会记录在 logs/monitor.log
- 首次运行会创建状态缓存文件
- 系统服务方式运行时，即使关机重启也会自动启动
