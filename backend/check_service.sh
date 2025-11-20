#!/bin/bash

# 后端服务连通性验证脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
HOST="${APP_HOST:-localhost}"
PORT="${APP_PORT:-8000}"
BASE_URL="http://${HOST}:${PORT}"

# 统计
PASSED=0
FAILED=0

# 打印函数
print_header() {
    echo ""
    echo "=========================================="
    echo "$1"
    echo "=========================================="
}

print_test() {
    echo -n "测试: $1 ... "
}

print_pass() {
    echo -e "${GREEN}✓ 通过${NC}"
    ((PASSED++))
}

print_fail() {
    echo -e "${RED}✗ 失败${NC}"
    echo "  错误: $1"
    ((FAILED++))
}

print_warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 测试函数
test_process() {
    print_test "检查服务进程"
    if pgrep -f "python3 main.py" > /dev/null 2>&1; then
        PID=$(pgrep -f "python3 main.py" | head -n 1)
        print_pass
        echo "  进程 ID: $PID"
    else
        print_fail "未找到运行中的服务进程"
        return 1
    fi
}

test_port() {
    print_test "检查端口监听"
    if netstat -tlnp 2>/dev/null | grep -q ":${PORT}" || ss -tlnp 2>/dev/null | grep -q ":${PORT}"; then
        print_pass
    else
        print_fail "端口 ${PORT} 未在监听"
        return 1
    fi
}

test_http_endpoint() {
    local endpoint=$1
    local expected_status=${2:-200}
    local description=${3:-$endpoint}
    local follow_redirect=${4:-false}
    
    print_test "$description"
    
    # 使用临时文件存储响应
    local temp_file=$(mktemp)
    local http_code
    
    if [ "$follow_redirect" = "true" ]; then
        http_code=$(curl -s -L -o "$temp_file" -w "%{http_code}" "${BASE_URL}${endpoint}" 2>&1)
    else
        http_code=$(curl -s -o "$temp_file" -w "%{http_code}" "${BASE_URL}${endpoint}" 2>&1)
    fi
    
    local body=$(cat "$temp_file" 2>/dev/null)
    rm -f "$temp_file"
    
    # 接受 200 或 307 (临时重定向，FastAPI 会自动处理)
    if [ "$http_code" = "$expected_status" ] || [ "$http_code" = "307" ]; then
        print_pass
        if [ "$http_code" = "307" ]; then
            echo "  注意: 返回 307 重定向（FastAPI 自动处理）"
        fi
        if [ -n "$body" ] && [ "$body" != "null" ] && [ ${#body} -gt 0 ]; then
            local preview=$(echo "$body" | head -c 100 | tr -d '\n')
            if [ ${#body} -gt 100 ]; then
                echo "  响应: ${preview}..."
            else
                echo "  响应: ${preview}"
            fi
        fi
        return 0
    else
        print_fail "HTTP 状态码: $http_code (期望: $expected_status)"
        if [ -n "$body" ] && [ ${#body} -gt 0 ]; then
            echo "  响应内容: $(echo "$body" | head -c 200)"
        fi
        return 1
    fi
}

test_health() {
    test_http_endpoint "/health" 200 "健康检查端点"
}

test_root() {
    test_http_endpoint "/" 200 "根路径"
}

test_api_endpoints() {
    local endpoints=(
        "/api/documents/"
        "/api/blogs/"
        "/api/news/"
        "/api/community/calendar/"
        "/api/community/intro/"
        "/api/discussions/"
    )
    
    for endpoint in "${endpoints[@]}"; do
        test_http_endpoint "$endpoint" 200 "API 端点: $endpoint"
    done
}

test_docs() {
    test_http_endpoint "/docs" 200 "API 文档页面"
}

# 主函数
main() {
    print_header "后端服务连通性验证"
    echo "服务地址: ${BASE_URL}"
    echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # 检查依赖
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}错误: 未找到 curl 命令，请先安装${NC}"
        exit 1
    fi
    
    # 执行测试
    echo ""
    print_header "1. 进程检查"
    test_process || print_warn "进程检查失败，但继续测试 HTTP 连接"
    
    echo ""
    print_header "2. 端口检查"
    test_port || print_warn "端口检查失败，但继续测试 HTTP 连接"
    
    echo ""
    print_header "3. HTTP 端点测试"
    test_health
    test_root
    test_docs
    
    echo ""
    print_header "4. API 端点测试"
    test_api_endpoints
    
    # 输出总结
    echo ""
    print_header "测试总结"
    echo "总测试数: $((PASSED + FAILED))"
    echo -e "${GREEN}通过: ${PASSED}${NC}"
    echo -e "${RED}失败: ${FAILED}${NC}"
    echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    if [ $FAILED -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ 所有测试通过！后端服务运行正常。${NC}"
        exit 0
    else
        echo ""
        echo -e "${RED}✗ 部分测试失败，请检查后端服务状态。${NC}"
        exit 1
    fi
}

# 运行主函数
main

