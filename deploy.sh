#!/bin/bash

echo "======================================"
echo "飞书Webhook服务 - 云服务器部署脚本"
echo "======================================"
echo ""

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "未检测到Docker，正在安装..."
    curl -fsSL https://get.docker.com | sh
    systemctl start docker
    systemctl enable docker
fi

# 检查Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "未检测到Docker Compose，正在安装..."
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

echo ""
echo "构建并启动服务..."
docker-compose up -d --build

echo ""
echo "======================================"
echo "部署完成！"
echo "======================================"
echo ""
echo "服务状态:"
docker-compose ps
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
echo "重启服务: docker-compose restart"
echo ""
echo "Webhook地址: http://$(curl -s ifconfig.me):5000/webhook"
echo "健康检查: http://$(curl -s ifconfig.me):5000/health"
echo ""
