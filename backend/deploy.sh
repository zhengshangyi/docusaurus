#!/bin/bash

# 九问后端服务部署脚本

set -e

echo "=========================================="
echo "九问后端服务部署脚本"
echo "=========================================="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"

# 检查 MySQL
echo ""
echo "检查 MySQL 服务..."
if command -v mysql &> /dev/null; then
    echo "✓ MySQL 客户端已安装"
else
    echo "⚠ MySQL 客户端未安装"
fi

if netstat -tlnp 2>/dev/null | grep -q 3306 || ss -tlnp 2>/dev/null | grep -q 3306; then
    echo "✓ MySQL 服务正在运行 (端口 3306)"
else
    echo "⚠ MySQL 服务未运行"
    echo ""
    echo "请先安装并启动 MySQL:"
    echo "  sudo apt-get install mysql-server"
    echo "  sudo systemctl start mysql"
    echo "  sudo mysql_secure_installation"
    echo ""
    echo "或者使用 Docker 运行 MySQL:"
    echo "  docker run -d --name jiuwen_mysql \\"
    echo "    -e MYSQL_ROOT_PASSWORD=Poisson@123 \\"
    echo "    -e MYSQL_DATABASE=jiuwen \\"
    echo "    -p 3306:3306 mysql:8.0"
    echo ""
    read -p "是否继续部署？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo ""
    echo "创建 .env 文件..."
    cp env.example .env
    echo "✓ .env 文件已创建，请检查配置"
fi

# 安装 Python 依赖
echo ""
echo "安装 Python 依赖..."
python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user --quiet
echo "✓ 依赖安装完成"

# 初始化数据库
echo ""
echo "初始化数据库..."
if python3 init_db.py 2>/dev/null; then
    echo "✓ 数据库初始化成功"
else
    echo "⚠ 数据库初始化失败，请检查 MySQL 连接配置"
    echo "  可以稍后手动运行: python3 init_db.py"
fi

# 启动服务
echo ""
echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo ""
echo "启动服务:"
echo "  python3 main.py"
echo ""
echo "或者使用后台运行:"
echo "  nohup python3 main.py > backend.log 2>&1 &"
echo ""
echo "访问 API 文档:"
echo "  http://localhost:8000/docs"
echo ""

