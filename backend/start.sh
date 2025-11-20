#!/bin/bash

# 启动后端服务脚本

cd "$(dirname "$0")"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "错误: .env 文件不存在"
    echo "请先运行: cp env.example .env"
    exit 1
fi

# 检查依赖
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "安装依赖..."
    python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
fi

# 启动服务
echo "启动后端服务..."
echo "访问地址: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
echo ""
python3 main.py

