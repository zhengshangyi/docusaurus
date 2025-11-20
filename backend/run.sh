#!/bin/bash

# 九问网站后端服务启动脚本

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "错误: .env 文件不存在"
    echo "请先复制 env.example 为 .env 并配置数据库连接信息"
    echo "运行: cp env.example .env"
    exit 1
fi

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $python_version"

# 检查依赖是否安装
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境..."
source venv/bin/activate

echo "安装依赖..."
pip install -r requirements.txt

echo "启动服务..."
python main.py

