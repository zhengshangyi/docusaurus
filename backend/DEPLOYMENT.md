# 后端服务部署指南

## 前置要求

### 1. Python 环境
- Python 3.9+ (当前: Python 3.10.12)
- pip 包管理器

### 2. MySQL 数据库
需要安装并运行 MySQL 8.0 或更高版本。

## 快速部署

### 方式一：使用部署脚本（推荐）

```bash
cd backend
./deploy.sh
```

### 方式二：手动部署

#### 1. 安装 MySQL

**选项 A: 使用 apt 安装**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql_secure_installation
```

**选项 B: 使用 Docker**
```bash
docker run -d \
  --name jiuwen_mysql \
  -e MYSQL_ROOT_PASSWORD=Poisson@123 \
  -e MYSQL_DATABASE=jiuwen \
  -e MYSQL_CHARACTER_SET_SERVER=utf8mb4 \
  -e MYSQL_COLLATION_SERVER=utf8mb4_unicode_ci \
  -p 3306:3306 \
  mysql:8.0 \
  --default-authentication-plugin=mysql_native_password
```

#### 2. 配置数据库

编辑 `.env` 文件，确认数据库配置：
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Poisson@123
DB_NAME=jiuwen
```

#### 3. 安装 Python 依赖

```bash
cd backend
python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

#### 4. 初始化数据库

```bash
python3 init_db.py
```

#### 5. 启动服务

**开发模式（前台运行）:**
```bash
python3 main.py
```

**生产模式（后台运行）:**
```bash
nohup python3 main.py > backend.log 2>&1 &
```

**使用 systemd 服务（推荐生产环境）:**
```bash
# 复制服务文件
sudo cp jiuwen-backend.service /etc/systemd/system/

# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start jiuwen-backend

# 设置开机自启
sudo systemctl enable jiuwen-backend

# 查看状态
sudo systemctl status jiuwen-backend

# 查看日志
sudo journalctl -u jiuwen-backend -f
```

## 验证部署

### 1. 检查服务状态

```bash
# 检查进程
ps aux | grep "python3 main.py"

# 检查端口
netstat -tlnp | grep 8000
# 或
ss -tlnp | grep 8000
```

### 2. 测试 API

```bash
# 健康检查
curl http://localhost:8000/health

# 查看 API 文档
curl http://localhost:8000/docs
```

### 3. 访问 API 文档

在浏览器中打开：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 常见问题

### 1. MySQL 连接失败

**错误信息:**
```
Can't connect to MySQL server on 'localhost'
```

**解决方法:**
- 检查 MySQL 服务是否运行: `sudo systemctl status mysql`
- 检查端口是否监听: `netstat -tlnp | grep 3306`
- 检查防火墙设置
- 确认 `.env` 文件中的数据库配置正确

### 2. 端口被占用

**错误信息:**
```
Address already in use
```

**解决方法:**
```bash
# 查找占用端口的进程
lsof -i :8000
# 或
netstat -tlnp | grep 8000

# 停止占用端口的进程或修改 APP_PORT
```

### 3. 依赖安装失败

**解决方法:**
- 使用国内镜像源（已在脚本中配置）
- 检查网络连接
- 增加超时时间: `pip install --timeout 100 ...`

### 4. 数据库初始化失败

**解决方法:**
- 确认 MySQL 服务正在运行
- 检查数据库用户权限
- 手动创建数据库:
  ```sql
  CREATE DATABASE jiuwen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

## 生产环境建议

1. **使用 systemd 管理服务** - 自动重启、日志管理
2. **配置反向代理** - 使用 Nginx 作为反向代理
3. **启用 HTTPS** - 使用 SSL 证书
4. **数据库备份** - 定期备份 MySQL 数据
5. **监控和日志** - 配置日志轮转和监控

## Nginx 反向代理配置示例

```nginx
server {
    listen 80;
    server_name api.openjiuwen.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 日志查看

```bash
# 查看应用日志
tail -f backend.log

# 查看 systemd 日志
sudo journalctl -u jiuwen-backend -f

# 查看错误日志
grep ERROR backend.log
```

