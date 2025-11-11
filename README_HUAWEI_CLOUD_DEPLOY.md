# Docusaurus 网站部署指南（华为云服务器）

本文档介绍如何在华为云服务器上部署 Docusaurus 前端项目，使用 Nginx 作为 Web 服务器。

## 📋 目录

- [前置要求](#前置要求)
- [快速开始](#快速开始)
- [详细部署步骤](#详细部署步骤)
- [配置说明](#配置说明)
- [访问方式](#访问方式)
- [HTTPS 配置](#https-配置)
- [维护与更新](#维护与更新)
- [故障排查](#故障排查)

## 前置要求

### 系统要求

- **操作系统**: Linux (Ubuntu 20.04+ 推荐)
- **Node.js**: >= 20.0 (本项目使用 `/opt/nodejs20/bin/node`)
- **内存**: 建议 4GB 以上（构建过程需要较多内存）
- **磁盘空间**: 至少 5GB 可用空间

### 软件依赖

- Node.js 20.x
- Yarn 包管理器
- Nginx (将从源码编译安装)
- Git (用于克隆项目)

### 华为云服务器配置

- 已创建并配置华为云 ECS 实例
- 已获取服务器公网 IP 地址
- 已配置安全组规则（开放 80 和 443 端口）

## 快速开始

### 1. 克隆项目

```bash
cd /opt/huawei/data/jiuwen/official_website
git clone https://github.com/zhengshangyi/docusaurus.git docusaurus
cd docusaurus
```

### 2. 运行部署脚本

```bash
bash deploy_huawei_cloud.sh
```

部署脚本会自动完成：
- ✅ 检查 Node.js 版本
- ✅ 安装项目依赖
- ✅ 构建 Docusaurus 网站（英文和中文版本）
- ✅ 设置文件权限

### 3. 配置 Nginx

```bash
# 复制配置文件
sudo cp nginx-docusaurus.conf /usr/local/nginx/conf/

# 更新主配置文件（如果使用源码编译的 Nginx）
# 编辑 /usr/local/nginx/conf/nginx.conf，添加：
# include /opt/huawei/data/jiuwen/official_website/docusaurus/nginx-docusaurus.conf;

# 测试并启动 Nginx
sudo /usr/local/nginx/sbin/nginx -t
sudo /usr/local/nginx/sbin/nginx
```

### 4. 访问网站

- **HTTP**: `http://您的服务器IP`
- **HTTPS**: `https://您的域名`（需要先配置 DNS 和 SSL 证书）

## 详细部署步骤

### 步骤 1: 环境准备

#### 1.1 安装 Node.js 20

如果系统没有 Node.js 20，可以使用项目指定的路径：

```bash
# 确保 /opt/nodejs20/bin/node 可用
/opt/nodejs20/bin/node -v
```

或者安装 Node.js 20：

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 1.2 安装 Yarn

```bash
npm install -g yarn
```

#### 1.3 安装 Nginx

本项目使用从源码编译的 Nginx（支持 SSL），安装步骤：

```bash
# 下载 Nginx 源码
cd /tmp
wget http://nginx.org/download/nginx-1.24.0.tar.gz
tar -xzf nginx-1.24.0.tar.gz

# 下载 PCRE 库（如果未安装）
wget https://sourceforge.net/projects/pcre/files/pcre/8.45/pcre-8.45.tar.gz
tar -xzf pcre-8.45.tar.gz

# 配置并编译（支持 SSL）
cd nginx-1.24.0
./configure --prefix=/usr/local/nginx \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-pcre=/tmp/pcre-8.45

# 编译和安装
make -j$(nproc)
sudo make install
```

### 步骤 2: 项目部署

#### 2.1 准备项目

```bash
# 进入项目目录
cd /opt/huawei/data/jiuwen/official_website/docusaurus

# 检查项目结构
ls -la
```

#### 2.2 运行部署脚本

```bash
bash deploy_huawei_cloud.sh
```

部署脚本会：
1. 检查 Node.js 版本（使用 `/opt/nodejs20/bin/node`）
2. 安装项目依赖（如果未安装）
3. 清理构建缓存
4. 构建英文版本（`--locale en`）
5. 构建中文版本（`--locale zh-CN`）
6. 设置文件权限

#### 2.3 验证构建结果

```bash
# 检查构建目录
ls -lh website/build

# 查看构建大小
du -sh website/build
```

### 步骤 3: 配置 Nginx

#### 3.1 复制配置文件

```bash
sudo cp nginx-docusaurus.conf /usr/local/nginx/conf/
```

#### 3.2 更新 Nginx 主配置

编辑 `/usr/local/nginx/conf/nginx.conf`，在 `http` 块中添加：

```nginx
http {
    # ... 其他配置 ...
    
    # 包含 Docusaurus 站点配置
    include /opt/huawei/data/jiuwen/official_website/docusaurus/nginx-docusaurus.conf;
}
```

或者直接修改主配置文件，将 Docusaurus 配置内容包含进去。

#### 3.3 测试并启动 Nginx

```bash
# 测试配置
sudo /usr/local/nginx/sbin/nginx -t

# 启动 Nginx
sudo /usr/local/nginx/sbin/nginx

# 检查运行状态
ps aux | grep nginx
```

### 步骤 4: 配置防火墙和安全组

#### 4.1 服务器防火墙

```bash
# 如果使用 ufw
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw status

# 如果使用 iptables
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

#### 4.2 华为云安全组

在华为云控制台配置：

1. 进入 "弹性云服务器 ECS"
2. 找到您的服务器，点击服务器名称
3. 点击 "安全组" 标签
4. 点击安全组名称进入规则管理
5. 添加入方向规则：
   - **规则 1**: TCP:80, 源地址: 0.0.0.0/0
   - **规则 2**: TCP:443, 源地址: 0.0.0.0/0

## 配置说明

### deploy_huawei_cloud.sh 脚本说明

部署脚本的主要功能：

- **Node.js 版本检查**: 确保使用 Node.js >= 20.0
- **依赖管理**: 自动安装项目依赖（使用 yarn）
- **内存优化**: 根据可用内存自动调整 Node.js 内存限制
- **分语言构建**: 分别构建每个语言版本以减少内存占用
- **权限设置**: 自动设置构建文件的权限

**关键配置**:
- Node.js 路径: `/opt/nodejs20/bin/node`
- 项目目录: `/opt/huawei/data/jiuwen/official_website/docusaurus`
- 构建目录: `website/build`

### Nginx 配置说明

`nginx-docusaurus.conf` 配置文件包含：

- **HTTP 服务器**: 监听 80 端口，支持 IP 和域名访问
- **HTTPS 服务器**: 监听 443 端口（需要配置 SSL 证书）
- **SPA 路由支持**: 使用 `try_files` 支持客户端路由
- **静态资源缓存**: 优化静态资源加载
- **Gzip 压缩**: 减少传输大小

**主要配置项**:
- 网站根目录: `/opt/huawei/data/jiuwen/official_website/docusaurus/website/build`
- 日志文件: `/var/log/nginx/docusaurus-access.log` 和 `docusaurus-error.log`
- 支持域名: `openjiuwen.com` 和 `www.openjiuwen.com`

## 访问方式

### 通过 IP 访问

如果只配置了 IP 访问（未配置 DNS）：

```
http://您的服务器IP
例如: http://119.3.165.90
```

**配置要求**:
- Nginx 配置中的 `server_name` 设置为 `_`（接受所有请求）
- 华为云安全组开放 80 端口

### 通过域名访问

如果配置了 DNS：

```
http://openjiuwen.com
https://openjiuwen.com（需要配置 SSL 证书）
```

**配置要求**:
- DNS A 记录指向服务器 IP
- Nginx 配置中的 `server_name` 包含域名
- 如需 HTTPS，需要配置 SSL 证书

## HTTPS 配置

### 前置条件

1. **DNS 配置**: 域名已解析到服务器 IP
2. **Nginx SSL 支持**: Nginx 已编译 SSL 模块
3. **Certbot 安装**: Let's Encrypt 证书工具已安装

### 快速配置

#### 方法 1: 使用自动化脚本（推荐）

```bash
# 1. 在华为云 DNS 控制台配置 DNS A 记录
#    - openjiuwen.com -> 您的服务器IP
#    - www.openjiuwen.com -> 您的服务器IP

# 2. 等待 DNS 生效（10-15 分钟）

# 3. 运行自动化脚本
bash setup_https.sh
```

脚本会自动完成：
- ✅ 检查 DNS 解析
- ✅ 获取 Let's Encrypt SSL 证书
- ✅ 启用 HTTPS 配置
- ✅ 重新加载 Nginx

#### 方法 2: 手动配置

详细步骤请参考：`SETUP_HTTPS_COMPLETE.md`

### 验证 HTTPS

配置完成后，访问：
- `https://openjiuwen.com`
- `https://www.openjiuwen.com`

浏览器应显示锁图标，表示 HTTPS 配置成功。

### 证书自动续期

Let's Encrypt 证书每 90 天需要续期，设置自动续期：

```bash
sudo crontab -e
# 添加以下行
0 3 1 * * /snap/bin/certbot renew --quiet && /usr/local/nginx/sbin/nginx -s reload
```

## 维护与更新

### 更新网站内容

1. **更新源代码**
   ```bash
   cd /opt/huawei/data/jiuwen/official_website/docusaurus
   git pull  # 或从其他源更新代码
   ```

2. **重新部署**
   ```bash
   bash deploy_huawei_cloud.sh
   ```

3. **重新加载 Nginx**（通常不需要，但建议）
   ```bash
   sudo /usr/local/nginx/sbin/nginx -s reload
   ```

### 查看日志

```bash
# 访问日志
sudo tail -f /var/log/nginx/docusaurus-access.log

# 错误日志
sudo tail -f /var/log/nginx/docusaurus-error.log

# Nginx 错误日志
sudo tail -f /usr/local/nginx/logs/error.log
```

### 监控服务状态

```bash
# 检查 Nginx 运行状态
ps aux | grep nginx

# 检查端口监听
sudo netstat -tlnp | grep nginx
# 或
sudo ss -tlnp | grep nginx

# 测试网站响应
curl -I http://localhost
```

### 重启服务

```bash
# 重启 Nginx
sudo /usr/local/nginx/sbin/nginx -s reload  # 重新加载配置（推荐）
sudo /usr/local/nginx/sbin/nginx -s stop    # 停止
sudo /usr/local/nginx/sbin/nginx            # 启动
```

## 故障排查

### 问题 1: 部署脚本失败

**症状**: `deploy_huawei_cloud.sh` 执行失败

**可能原因**:
- Node.js 版本不正确
- 内存不足
- 依赖安装失败

**解决方法**:
```bash
# 检查 Node.js 版本
/opt/nodejs20/bin/node -v

# 检查可用内存
free -h

# 手动安装依赖
cd website
yarn install --frozen-lockfile
```

### 问题 2: 无法访问网站

**症状**: 浏览器无法打开网站

**检查清单**:
1. ✅ Nginx 是否运行: `ps aux | grep nginx`
2. ✅ 端口是否监听: `sudo netstat -tlnp | grep 80`
3. ✅ 防火墙是否开放端口
4. ✅ **华为云安全组是否配置**（最重要！）
5. ✅ 构建文件是否存在: `ls -la website/build`

**解决方法**:
```bash
# 检查 Nginx 配置
sudo /usr/local/nginx/sbin/nginx -t

# 查看错误日志
sudo tail -50 /var/log/nginx/docusaurus-error.log

# 测试本地访问
curl http://localhost
```

### 问题 3: HTTPS 无法访问

**症状**: HTTP 正常，但 HTTPS 无法访问

**检查清单**:
1. ✅ SSL 证书是否存在: `ls -la /etc/letsencrypt/live/openjiuwen.com/`
2. ✅ Nginx 配置是否正确: `sudo /usr/local/nginx/sbin/nginx -t`
3. ✅ 安全组是否开放 443 端口
4. ✅ DNS 是否解析正确

**解决方法**:
```bash
# 检查证书
sudo certbot certificates

# 测试配置
sudo /usr/local/nginx/sbin/nginx -t

# 查看错误日志
sudo tail -f /var/log/nginx/docusaurus-error.log
```

### 问题 4: 构建内存不足

**症状**: 构建过程中内存溢出

**解决方法**:
- 增加服务器内存
- 或修改 `deploy_huawei_cloud.sh` 中的内存限制
- 或分别构建每个语言版本（脚本已自动处理）

### 问题 5: DNS 解析失败

**症状**: 域名无法解析

**解决方法**:
```bash
# 检查 DNS 解析
dig @8.8.8.8 openjiuwen.com A +short

# 使用检查脚本
bash check_dns.sh
```

## 项目结构

```
docusaurus/
├── deploy_huawei_cloud.sh       # 部署脚本
├── nginx-docusaurus.conf        # Nginx 配置文件
├── website/                     # 网站源码目录
│   ├── build/                   # 构建输出目录（部署后生成）
│   ├── src/                     # 源代码
│   └── package.json             # 项目依赖
├── setup_https.sh               # HTTPS 配置脚本
├── check_dns.sh                 # DNS 检查脚本
├── README.md                    # 本文档
└── SETUP_HTTPS_COMPLETE.md     # HTTPS 详细配置指南
```

## 相关文档

- [HTTPS 完整配置指南](SETUP_HTTPS_COMPLETE.md)
- [IP 访问指南](IP_ACCESS_GUIDE.md)
- [DNS 配置指南](DNS_SETUP_STEPS.md)
- [访问信息](ACCESS_INFO.md)

## 技术支持

如遇到问题，请检查：
1. Nginx 错误日志: `/var/log/nginx/docusaurus-error.log`
2. Nginx 访问日志: `/var/log/nginx/docusaurus-access.log`
3. Certbot 日志: `/var/log/letsencrypt/letsencrypt.log`

## 许可证

本项目遵循原 Docusaurus 项目的许可证。

---

**最后更新**: 2025-11-11  
**维护者**: 郑尚奕
