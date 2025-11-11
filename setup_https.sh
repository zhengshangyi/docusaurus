#!/bin/bash
set -e

# 完整的 HTTPS 配置脚本
# 自动检查 DNS、获取证书、启用 HTTPS

SERVER_IP="119.3.165.90"
DOMAINS=("openjiuwen.com" "www.openjiuwen.com")
CONFIG_FILE="/opt/huawei/data/jiuwen/official_website/docusaurus/nginx-docusaurus.conf"

echo "=========================================="
echo "HTTPS 完整配置脚本"
echo "=========================================="
echo "服务器 IP: $SERVER_IP"
echo "域名: ${DOMAINS[*]}"
echo ""

# 检查 DNS 解析
check_dns() {
    local all_ok=true
    
    echo "检查 DNS 解析..."
    for domain in "${DOMAINS[@]}"; do
        local ip=$(dig @8.8.8.8 "$domain" A +short 2>/dev/null | head -1)
        if [ -n "$ip" ] && [ "$ip" = "$SERVER_IP" ]; then
            echo "  ✅ $domain -> $SERVER_IP"
        else
            echo "  ❌ $domain -> ${ip:-未解析}"
            all_ok=false
        fi
    done
    echo ""
    
    if [ "$all_ok" = false ]; then
        echo "❌ DNS 解析未生效"
        echo ""
        echo "请先在华为云 DNS 控制台配置以下 A 记录："
        echo "  - openjiuwen.com -> $SERVER_IP"
        echo "  - www.openjiuwen.com -> $SERVER_IP"
        echo ""
        echo "配置步骤："
        echo "  1. 登录华为云控制台"
        echo "  2. 进入 '云解析服务 DNS'"
        echo "  3. 找到域名 openjiuwen.com，点击 '解析'"
        echo "  4. 添加两条 A 记录（@ 和 www）"
        echo "  5. 等待 10-15 分钟后再次运行此脚本"
        echo ""
        echo "详细说明请查看: SETUP_HTTPS_COMPLETE.md"
        exit 1
    fi
    
    echo "✅ DNS 解析检查通过"
    echo ""
}

# 获取 SSL 证书
get_certificate() {
    echo "=========================================="
    echo "获取 SSL 证书"
    echo "=========================================="
    
    # 检查证书是否已存在
    if [ -f "/etc/letsencrypt/live/openjiuwen.com/fullchain.pem" ]; then
        echo "✅ SSL 证书已存在"
        return 0
    fi
    
    echo "停止 Nginx（certbot 需要临时使用 80 端口）..."
    sudo /usr/local/nginx/sbin/nginx -s stop 2>/dev/null || true
    
    echo "正在获取 Let's Encrypt 证书..."
    if sudo certbot certonly --standalone \
        -d openjiuwen.com \
        -d www.openjiuwen.com \
        --non-interactive \
        --agree-tos \
        --email admin@openjiuwen.com 2>&1; then
        echo "✅ 证书获取成功"
    else
        echo "❌ 证书获取失败"
        echo "启动 Nginx..."
        sudo /usr/local/nginx/sbin/nginx
        exit 1
    fi
    
    echo "启动 Nginx..."
    sudo /usr/local/nginx/sbin/nginx
    echo ""
}

# 启用 HTTPS 配置
enable_https() {
    echo "=========================================="
    echo "启用 HTTPS 配置"
    echo "=========================================="
    
    # 备份配置
    if [ ! -f "${CONFIG_FILE}.backup" ]; then
        cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"
        echo "✅ 已备份原配置文件"
    fi
    
    # 启用 HTTPS 重定向
    if grep -q "^[[:space:]]*return 301 https" "$CONFIG_FILE"; then
        echo "✅ HTTPS 重定向已启用"
    else
        sed -i 's/# return 301 https:\/\/$server_name$request_uri;/return 301 https:\/\/$server_name$request_uri;/' "$CONFIG_FILE"
        echo "✅ 已启用 HTTPS 重定向"
    fi
    
    # 检查 HTTPS server 块是否已启用
    if grep -q "^server {" "$CONFIG_FILE" && grep -q "^[[:space:]]*listen 443" "$CONFIG_FILE"; then
        echo "✅ HTTPS server 配置已启用"
    else
        # 取消注释 HTTPS server 块（第 58-118 行）
        sed -i '58,118s/^#//' "$CONFIG_FILE"
        echo "✅ 已启用 HTTPS server 配置"
    fi
    
    echo ""
}

# 重新加载 Nginx
reload_nginx() {
    echo "=========================================="
    echo "重新加载 Nginx"
    echo "=========================================="
    
    # 测试配置
    echo "测试 Nginx 配置..."
    if sudo /usr/local/nginx/sbin/nginx -t; then
        echo "✅ 配置测试通过"
    else
        echo "❌ 配置测试失败"
        exit 1
    fi
    
    echo ""
    echo "重新加载 Nginx..."
    sudo /usr/local/nginx/sbin/nginx -s reload
    echo "✅ Nginx 已重新加载"
    echo ""
}

# 主流程
main() {
    # 1. 检查 DNS
    check_dns
    
    # 2. 获取证书
    get_certificate
    
    # 3. 启用 HTTPS 配置
    enable_https
    
    # 4. 重新加载 Nginx
    reload_nginx
    
    echo "=========================================="
    echo "✅ HTTPS 配置完成！"
    echo "=========================================="
    echo ""
    echo "请访问以下地址验证："
    echo "  https://openjiuwen.com"
    echo "  https://www.openjiuwen.com"
    echo ""
    echo "HTTP 请求会自动重定向到 HTTPS"
    echo ""
    echo "如果遇到问题，请检查："
    echo "  - Nginx 错误日志: /var/log/nginx/docusaurus-error.log"
    echo "  - Certbot 日志: /var/log/letsencrypt/letsencrypt.log"
    echo "  - 华为云安全组是否开放 80 和 443 端口"
}

# 运行主流程
main

