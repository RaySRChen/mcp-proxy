#!/bin/bash

# MCP Proxy 部署腳本
# 使用方法: ./deploy.sh

set -e

echo "==============================="
echo "MCP Proxy 部署腳本"
echo "==============================="

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo "錯誤: Docker 未安裝。請先安裝 Docker。"
    exit 1
fi

# 檢查 Docker Compose 是否安裝
if ! command -v docker-compose &> /dev/null; then
    echo "錯誤: Docker Compose 未安裝。請先安裝 Docker Compose。"
    exit 1
fi

# 檢查 .env 文件
if [ ! -f .env ]; then
    echo "錯誤: .env 文件不存在。請創建 .env 文件並設置必要的環境變量。"
    exit 1
fi

# 載入環境變量
source .env

echo "正在停止現有的容器..."
docker-compose -f docker-compose.prod.yml down

echo "正在構建新的映像..."
docker-compose -f docker-compose.prod.yml build --no-cache

echo "正在啟動服務..."
docker-compose -f docker-compose.prod.yml up -d

echo "等待服務啟動..."
sleep 10

# 檢查服務狀態
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "✅ 部署成功！"
    echo "服務運行在: http://${HOST}:${PORT}"
    echo "傳輸協議: ${TRANSPORT}"
    echo ""
    echo "查看日誌: docker-compose -f docker-compose.prod.yml logs -f"
    echo "停止服務: docker-compose -f docker-compose.prod.yml down"
else
    echo "❌ 部署失敗！"
    echo "查看錯誤日誌:"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi
