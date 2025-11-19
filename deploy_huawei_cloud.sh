#!/bin/bash
set -e

# Docusaurus 部署脚本
# 用于构建并部署 Docusaurus 网站到 Nginx

PROJECT_DIR="/opt/huawei/data/jiuwen/official_website/docusaurus"
WEBSITE_DIR="$PROJECT_DIR/website"
BUILD_DIR="$WEBSITE_DIR/build"
NODE_BIN="/opt/nodejs20/bin/node"

echo "=========================================="
echo "Docusaurus 部署脚本"
echo "=========================================="

# 检查 Node.js 版本
echo "检查 Node.js 版本..."
NODE_VERSION=$($NODE_BIN --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo "❌ 错误: 需要 Node.js >= 20.0，当前版本: $($NODE_BIN --version)"
    echo ""
    echo "请先安装 Node.js 20:"
    echo "  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -"
    echo "  sudo apt-get install -y nodejs"
    echo ""
    echo "或者使用 nvm:"
    echo "  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
    echo "  source ~/.bashrc"
    echo "  nvm install 20"
    echo "  nvm use 20"
    exit 1
fi

echo "✅ Node.js 版本检查通过: $($NODE_BIN --version)"
echo ""

# 设置 PATH 以确保 yarn 使用正确的 node
export PATH="/opt/nodejs20/bin:$PATH"

# 进入项目目录
cd "$PROJECT_DIR"

# 检查依赖是否已安装
if [ ! -d "$WEBSITE_DIR/node_modules" ]; then
    echo "安装依赖..."
    cd "$WEBSITE_DIR"
    yarn install --frozen-lockfile || {
        echo "❌ 依赖安装失败，尝试使用 --ignore-engines..."
        yarn install --ignore-engines
    }
    cd "$PROJECT_DIR"
else
    echo "✅ 依赖已安装"
fi

# 构建项目（只构建中文和英文）
echo ""
echo "开始构建 Docusaurus 网站（仅构建中文和英文）..."
echo "💡 内存优化模式：分别构建每个语言版本以减少内存占用"
cd "$WEBSITE_DIR"
echo "构建语言: en, zh-CN"

# 检查可用内存
AVAILABLE_MEM=$(free -m | awk 'NR==2{printf "%.0f", $7}')
echo "当前可用内存: ${AVAILABLE_MEM}MB"

# 设置 Node.js 内存限制（为系统保留至少 2GB）
# 如果可用内存少于 3GB，限制为 2GB；否则限制为 4GB
if [ "$AVAILABLE_MEM" -lt 3000 ]; then
    NODE_MEM_LIMIT="2048"
    echo "⚠️  内存紧张，限制 Node.js 内存使用为 2GB"
else
    NODE_MEM_LIMIT="4096"
    echo "✅ 设置 Node.js 内存限制为 4GB"
fi

# 清理之前的构建缓存以释放内存
echo "清理构建缓存..."
rm -rf .docusaurus/cache 2>/dev/null || true

# 清理之前的 build 目录（避免权限问题）
echo "清理之前的构建目录..."
sudo rm -rf "$BUILD_DIR" 2>/dev/null || rm -rf "$BUILD_DIR" 2>/dev/null || true

# 使用内存优化方式：分别构建每个语言版本
# 这样可以避免同时加载所有语言的内容到内存中

# 先构建英文版本
# echo ""
# echo "=========================================="
# echo "构建英文版本 (en)..."
# echo "=========================================="
# NODE_OPTIONS="--max_old_space_size=$NODE_MEM_LIMIT" BUILD_FAST=true yarn build --locale en || {
#     echo "❌ 英文版本构建失败"
#     exit 1
# }

# # 清理中间缓存（释放内存）
# echo "清理中间缓存..."
# rm -rf .docusaurus/cache 2>/dev/null || true

# 再构建中文版本（会合并到同一个 build 目录）
echo ""
echo "=========================================="
echo "构建中文版本 (zh-CN)..."
echo "=========================================="
NODE_OPTIONS="--max_old_space_size=$NODE_MEM_LIMIT" BUILD_FAST=true yarn build --locale zh-CN || {
    echo "❌ 中文版本构建失败"
    exit 1
}

# 检查构建结果
if [ ! -d "$BUILD_DIR" ] || [ -z "$(ls -A $BUILD_DIR)" ]; then
    echo "❌ 错误: build 目录不存在或为空"
    exit 1
fi

echo "✅ 构建成功！构建文件位于: $BUILD_DIR"
echo ""

# 设置文件权限
echo "设置文件权限..."
sudo chown -R www-data:www-data "$BUILD_DIR" 2>/dev/null || {
    echo "⚠️  警告: 无法设置 www-data 权限，使用当前用户权限"
    chmod -R 755 "$BUILD_DIR"
}

echo ""
echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 复制 Nginx 配置文件:"
echo "   sudo cp $PROJECT_DIR/nginx-docusaurus.conf /etc/nginx/sites-available/docusaurus"
echo ""
echo "2. 启用站点:"
echo "   sudo ln -s /etc/nginx/sites-available/docusaurus /etc/nginx/sites-enabled/"
echo ""
echo "3. 测试 Nginx 配置:"
echo "   sudo nginx -t"
echo ""
echo "4. 重启 Nginx:"
echo "   sudo systemctl reload nginx"
echo ""
echo "5. 访问网站: http://your-server-ip"
echo ""

