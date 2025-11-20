# 后端服务部署状态

## ✅ 部署完成

**部署时间**: 2025-11-15 18:13

### 部署状态

- ✅ MySQL 8.0 已安装并运行
- ✅ 数据库 `jiuwen` 已创建
- ✅ 所有数据表已初始化（5个表）
- ✅ Python 依赖已安装
- ✅ 后端服务已启动并运行
- ✅ API 接口正常响应

### 服务信息

**后端服务**:
- 状态: ✅ 运行中
- 进程 ID: 1178841
- 监听地址: `0.0.0.0:8000`
- 日志文件: `/opt/huawei/data/jiuwen/official_website/docusaurus/backend/backend.log`

**MySQL 服务**:
- 状态: ✅ 运行中
- 端口: `3306`
- 数据库: `jiuwen`
- 用户: `root`

### 已创建的数据表

1. **documents** - 文档表
2. **blogs** - 博客表
3. **news** - 新闻资讯表
4. **community_calendar** - 社区日历表
5. **community_intro** - 社区介绍表

### API 访问地址

- **API 根路径**: http://localhost:8000/
- **健康检查**: http://localhost:8000/health
- **Swagger 文档**: http://localhost:8000/docs
- **ReDoc 文档**: http://localhost:8000/redoc

### API 端点

- `/api/documents` - 文档管理
- `/api/blogs` - 博客管理
- `/api/news` - 新闻管理
- `/api/community/calendar` - 社区日历
- `/api/community/intro` - 社区介绍

### 服务管理命令

**查看服务状态**:
```bash
ps aux | grep "python3 main.py"
```

**查看日志**:
```bash
tail -f /opt/huawei/data/jiuwen/official_website/docusaurus/backend/backend.log
```

**停止服务**:
```bash
pkill -f "python3 main.py"
```

**重启服务**:
```bash
cd /opt/huawei/data/jiuwen/official_website/docusaurus/backend
nohup python3 main.py > backend.log 2>&1 &
```

**使用 systemd 管理** (推荐生产环境):
```bash
sudo cp jiuwen-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start jiuwen-backend
sudo systemctl enable jiuwen-backend
```

### 测试 API

```bash
# 健康检查
curl http://localhost:8000/health

# 获取文档列表
curl http://localhost:8000/api/documents/

# 获取博客列表
curl http://localhost:8000/api/blogs/

# 获取新闻列表
curl http://localhost:8000/api/news/
```

### 下一步

1. 前端可以通过 `http://localhost:8000/api/` 访问后端 API
2. 在浏览器中访问 `http://localhost:8000/docs` 查看完整的 API 文档
3. 开始使用 API 创建和管理内容

---

**部署完成！** 🎉

