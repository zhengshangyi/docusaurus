#!/bin/bash

# 后端服务重启脚本

cd "$(dirname "$0")"

echo "=========================================="
echo "重启后端服务"
echo "=========================================="

# 停止现有服务
echo "停止现有服务..."
pkill -f "python3 main.py" 2>/dev/null
sleep 2

# 检查是否停止
if ps aux | grep "python3 main.py" | grep -v grep > /dev/null; then
    echo "⚠️  警告: 服务未能完全停止，强制停止..."
    pkill -9 -f "python3 main.py" 2>/dev/null
    sleep 1
fi

# 初始化数据库
echo ""
echo "初始化数据库..."
python3 init_db.py

# 启动服务
echo ""
echo "启动服务..."
nohup python3 main.py > backend.log 2>&1 &

sleep 3

# 检查服务状态
if ps aux | grep "python3 main.py" | grep -v grep > /dev/null; then
    echo "✅ 服务启动成功"
    echo ""
    echo "服务信息:"
    echo "  - 进程 ID: $(ps aux | grep 'python3 main.py' | grep -v grep | awk '{print $2}')"
    echo "  - 监听地址: http://localhost:8000"
    echo "  - API 文档: http://localhost:8000/docs"
    echo "  - 日志文件: $(pwd)/backend.log"
    echo ""
    echo "查看日志: tail -f backend.log"
else
    echo "❌ 服务启动失败，请查看日志: backend.log"
    exit 1
fi



