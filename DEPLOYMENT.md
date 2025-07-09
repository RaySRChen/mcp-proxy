# MCP Proxy 雲端部署指南

## 概述

這個 MCP Proxy 服務器可以將多個 MCP 服務器整合在一起，提供統一的 API 接口。支持部署到任何支持 Docker 的雲端 VM。

## 部署前準備

### 1. 系統要求
- Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- 最少 2GB RAM
- 最少 10GB 磁盤空間
- 外部 IP 地址
- 開放的端口 80, 443, 8000

### 2. 安裝依賴

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y docker.io docker-compose git

# CentOS/RHEL
sudo yum install -y docker docker-compose git

# 啟動 Docker 服務
sudo systemctl start docker
sudo systemctl enable docker

# 將當前用戶加入 docker 組
sudo usermod -aG docker $USER
# 需要重新登錄才能生效
```

## 部署步驟

### 1. 上傳代碼到 VM

```bash
# 方法 1: 使用 git clone（如果代碼在 Git 倉庫）
git clone <your-repo-url>
cd mcp-proxy

# 方法 2: 使用 scp 上傳
scp -r /path/to/mcp-proxy user@your-vm-ip:/home/user/
```

### 2. 配置環境變量

檢查並修改 `.env` 文件：

```bash
# 編輯 .env 文件
nano .env

# 重要配置項：
# HOST=0.0.0.0  # 必須設置為 0.0.0.0 允許外部訪問
# PORT=8000     # 服務端口
# TRANSPORT=sse # 傳輸協議
```

### 3. 部署選項

#### 選項 A: 簡單部署（推薦）

```bash
# 給部署腳本執行權限
chmod +x deploy.sh

# 執行部署
./deploy.sh
```

#### 選項 B: 使用 Docker Compose

```bash
# 使用生產環境配置
docker-compose -f docker-compose.prod.yml up -d

# 查看運行狀態
docker-compose -f docker-compose.prod.yml ps
```

#### 選項 C: 使用 Nginx 反向代理

```bash
# 使用帶有 Nginx 的完整配置
docker-compose -f docker-compose.full.yml up -d

# 這將在端口 80 上提供服務
```

### 4. 配置防火牆

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

## 驗證部署

### 1. 檢查服務狀態

```bash
# 查看容器狀態
docker-compose -f docker-compose.prod.yml ps

# 查看服務日誌
docker-compose -f docker-compose.prod.yml logs -f
```

### 2. 測試 API 訪問

```bash
# 健康檢查
curl -X GET http://YOUR_VM_IP:8000/health

# 使用測試腳本
python test_api.py http://YOUR_VM_IP:8000
```

### 3. 從外部訪問

```bash
# 替換 YOUR_VM_IP 為實際的 VM 外部 IP
curl -X GET http://YOUR_VM_IP:8000/health
```

## 常用管理命令

### 查看日誌

```bash
# 查看所有日誌
docker-compose -f docker-compose.prod.yml logs

# 實時查看日誌
docker-compose -f docker-compose.prod.yml logs -f

# 查看特定服務日誌
docker-compose -f docker-compose.prod.yml logs mcp-proxy
```

### 重啟服務

```bash
# 重啟服務
docker-compose -f docker-compose.prod.yml restart

# 重新構建並重啟
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

### 停止服務

```bash
# 停止服務
docker-compose -f docker-compose.prod.yml down

# 停止並刪除數據卷
docker-compose -f docker-compose.prod.yml down -v
```

## 安全建議

### 1. 使用 HTTPS

建議使用 Let's Encrypt 或其他 SSL 證書：

```bash
# 安裝 Certbot
sudo apt install certbot python3-certbot-nginx

# 獲取 SSL 證書
sudo certbot --nginx -d your-domain.com
```

### 2. 配置訪問控制

在 `nginx.conf` 中添加 IP 白名單：

```nginx
location / {
    allow 203.0.113.0/24;  # 允許特定 IP 段
    deny all;              # 拒絕其他所有訪問
    
    proxy_pass http://mcp_proxy;
    # ... 其他配置
}
```

### 3. 環境變量安全

- 不要在代碼中硬編碼 API 密鑰
- 使用強密碼和安全的 API 密鑰
- 定期輪換密鑰

## 故障排除

### 常見問題

1. **端口被占用**
   ```bash
   # 查看端口占用
   sudo netstat -tulpn | grep :8000
   
   # 修改 .env 文件中的端口
   ```

2. **Docker 權限問題**
   ```bash
   # 將用戶添加到 docker 組
   sudo usermod -aG docker $USER
   
   # 重新登錄生效
   ```

3. **服務無法啟動**
   ```bash
   # 查看詳細錯誤日誌
   docker-compose -f docker-compose.prod.yml logs
   
   # 檢查資源使用情況
   docker stats
   ```

### 性能監控

```bash
# 查看容器資源使用
docker stats

# 查看系統資源
htop
df -h
```

## 更新部署

```bash
# 拉取最新代碼
git pull origin main

# 重新部署
./deploy.sh
```

## 支持的 MCP 工具

當前配置支持以下 MCP 工具：

- **context7**: 文檔檢索和上下文分析
- **fetch**: 網頁抓取和內容提取
- **time**: 時間和時區轉換
- **sequential-thinking**: 序列化思維處理
- **exa**: 網頁搜索和研究
- **line-bot**: LINE 機器人集成

## 技術支持

如果遇到問題，請檢查：
1. 服務日誌
2. 防火牆設置
3. 環境變量配置
4. Docker 服務狀態

---

**注意**: 請確保所有的 API 密鑰和敏感信息都妥善保護，不要暴露在公共網絡中。
