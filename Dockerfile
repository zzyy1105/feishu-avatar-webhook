FROM python:3.9-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用文件
COPY webhook_server_hybrid.py webhook_server.py
COPY feishu_api.py .
COPY config.json .
COPY avatar.jpg .

# 创建日志目录
RUN mkdir -p logs

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "webhook_server:app"]
