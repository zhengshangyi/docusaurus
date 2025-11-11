#!/bin/bash

# DNS 检查脚本

echo "=========================================="
echo "DNS 配置检查"
echo "=========================================="
echo ""

SERVER_IP="119.3.165.90"
DOMAINS=("openjiuwen.com" "www.openjiuwen.com")

echo "服务器 IP: $SERVER_IP"
echo ""

all_ok=true

for domain in "${DOMAINS[@]}"; do
    echo "检查 $domain:"
    
    # 使用多个 DNS 服务器查询
    resolved=false
    for dns in "8.8.8.8" "1.1.1.1" "223.5.5.5"; do
        ip=$(dig @$dns "$domain" A +short 2>/dev/null | head -1)
        if [ -n "$ip" ]; then
            echo "  DNS 服务器 $dns: $ip"
            if [ "$ip" = "$SERVER_IP" ]; then
                echo "  ✅ 解析正确 -> $SERVER_IP"
                resolved=true
                break
            else
                echo "  ⚠️  解析到: $ip (应该是 $SERVER_IP)"
            fi
        fi
    done
    
    if [ "$resolved" = false ]; then
        echo "  ❌ 未解析或未配置"
        all_ok=false
    fi
    
    echo ""
done

echo "=========================================="
if [ "$all_ok" = true ]; then
    echo "✅ DNS 配置正确，可以启用 HTTPS"
    echo ""
    echo "运行以下命令启用 HTTPS:"
    echo "  bash /opt/huawei/data/jiuwen/official_website/docusaurus/manual_enable_https.sh"
else
    echo "❌ DNS 未配置或未生效"
    echo ""
    echo "请按照以下步骤配置 DNS:"
    echo "1. 登录华为云 DNS 控制台"
    echo "2. 添加 A 记录:"
    echo "   - openjiuwen.com -> $SERVER_IP"
    echo "   - www.openjiuwen.com -> $SERVER_IP"
    echo "3. 等待 10-15 分钟后再次运行此脚本检查"
    echo ""
    echo "详细说明请查看: DNS_CONFIG_GUIDE.md"
fi
echo "=========================================="

