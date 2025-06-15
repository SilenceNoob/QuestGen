#!/bin/bash

# 智能题目生成系统 Docker 部署脚本

set -e

echo "🚀 开始部署智能题目生成系统..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 检查 .env 文件是否存在
if [ ! -f ".env" ]; then
    echo "⚠️  .env 文件不存在，正在从模板创建..."
    cp .env.example .env
    echo "📝 请编辑 .env 文件，配置您的 API 密钥和其他设置"
    echo "💡 特别注意配置 DEEPSEEK_API_KEY"
    read -p "配置完成后按回车继续..."
fi

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down

# 构建镜像
echo "🔨 构建 Docker 镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

echo "✅ 部署完成！"
echo "🌐 应用访问地址: http://localhost:5000"
echo "📋 查看日志: docker-compose logs -f"
echo "🛑 停止服务: docker-compose down"
echo "🔄 重启服务: docker-compose restart"