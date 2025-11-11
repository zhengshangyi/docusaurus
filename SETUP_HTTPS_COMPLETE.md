# 完整 HTTPS 配置指南

## 目标
通过 `https://openjiuwen.com` 访问网站

## 服务器信息
- **公网 IP**: `119.3.165.90`
- **域名**: `openjiuwen.com` 和 `www.openjiuwen.com`

## 步骤 1: 配置 DNS（在华为云控制台）

### 1.1 登录华为云控制台
1. 访问：https://console.huaweicloud.com
2. 进入 "域名与网站" > "云解析服务 DNS"
3. 或直接访问：https://console.huaweicloud.com/dns

### 1.2 添加 A 记录
找到域名 `openjiuwen.com`，点击 "解析"，添加以下两条记录：

**记录 1 - 主域名：**
- 主机记录：`@`（或留空）
- 记录类型：`A`
- 记录值：`119.3.165.90`
- TTL：`600`

**记录 2 - www 子域名：**
- 主机记录：`www`
- 记录类型：`A`
- 记录值：`119.3.165.90`
- TTL：`600`

### 1.3 验证 DNS 配置
配置完成后，等待 5-10 分钟，然后运行：

```bash
bash /opt/huawei/data/jiuwen/official_website/docusaurus/check_dns.sh
```

应该看到两个域名都解析到 `119.3.165.90`

## 步骤 2: 启用 HTTPS（自动化）

DNS 生效后，运行以下命令自动完成 HTTPS 配置：

```bash
bash /opt/huawei/data/jiuwen/official_website/docusaurus/setup_https.sh
```

这个脚本会：
1. 检查 DNS 是否生效
2. 获取 Let's Encrypt SSL 证书
3. 启用 HTTPS 配置
4. 重新加载 Nginx

## 步骤 3: 验证访问

配置完成后，访问：
- ✅ https://openjiuwen.com
- ✅ https://www.openjiuwen.com
- ✅ http://openjiuwen.com（会自动重定向到 HTTPS）

## 手动配置（如果自动化脚本失败）

### 2.1 获取 SSL 证书

```bash
# 停止 Nginx
sudo /usr/local/nginx/sbin/nginx -s stop

# 获取证书
sudo certbot certonly --standalone \
    -d openjiuwen.com \
    -d www.openjiuwen.com \
    --non-interactive \
    --agree-tos \
    --email admin@openjiuwen.com

# 启动 Nginx
sudo /usr/local/nginx/sbin/nginx
```

### 2.2 启用 HTTPS 配置

编辑 `/opt/huawei/data/jiuwen/official_website/docusaurus/nginx-docusaurus.conf`：

1. **启用 HTTPS 重定向**（取消注释第 9 行）：
   ```nginx
   return 301 https://$server_name$request_uri;
   ```

2. **启用 HTTPS server 块**（取消注释第 58-118 行）

### 2.3 重新加载 Nginx

```bash
sudo /usr/local/nginx/sbin/nginx -t
sudo /usr/local/nginx/sbin/nginx -s reload
```

## 重要提示

### 华为云安全组配置

确保安全组已开放以下端口：
- **80 端口**（HTTP，用于证书验证和重定向）
- **443 端口**（HTTPS）

配置方法：
1. 进入服务器详情页
2. 点击 "安全组" 标签
3. 添加入方向规则：
   - TCP:80, 源地址: 0.0.0.0/0
   - TCP:443, 源地址: 0.0.0.0/0

## 故障排查

### DNS 未生效
- 等待 10-15 分钟（DNS 传播时间）
- 使用不同 DNS 服务器查询：`dig @8.8.8.8 openjiuwen.com`

### 证书获取失败
- 确认 DNS 已生效
- 确认 80 端口已开放
- 确认 Nginx 已停止（certbot 需要临时使用 80 端口）

### HTTPS 无法访问
- 检查证书文件：`ls -la /etc/letsencrypt/live/openjiuwen.com/`
- 检查 Nginx 配置：`sudo /usr/local/nginx/sbin/nginx -t`
- 检查错误日志：`sudo tail -f /var/log/nginx/docusaurus-error.log`

## 证书自动续期

Let's Encrypt 证书每 90 天需要续期，设置自动续期：

```bash
sudo crontab -e
# 添加以下行（每月 1 号凌晨 3 点检查续期）
0 3 1 * * /snap/bin/certbot renew --quiet && /usr/local/nginx/sbin/nginx -s reload
```

