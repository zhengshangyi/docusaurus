# 文档数据导入说明

## 📋 概述

本文档说明如何将文档数据导入到 openJiuwen V1 版本中。

## 🎯 导入的数据源

### 1. AgentStudio 文档（Markdown 格式）

- **数据源路径**: `/opt/huawei/data/jiuwen/test-agentstudio/docs/`
- **文档格式**: Markdown (.md)
- **目标目录**: openJiuwen V1 版本下的 "AgentStudio" 一级目录
- **静态资源**: 复制到 `static_assets/agentstudio/` 目录

### 2. AgentCore 文档（HTML 格式）

- **数据源路径**: `/opt/huawei/data/jiuwen/official_website/docusaurus/develop_docs_1118`
- **文档格式**: HTML (.html)
- **目标目录**: openJiuwen V1 版本下的 "AgentCore" 一级目录
- **静态资源**: 复制到 `static_assets/develop_docs/` 目录

## 🚀 使用方法

### 执行导入

```bash
cd /opt/huawei/data/jiuwen/official_website/docusaurus/backend
python3 import_docs.py
```

### 导入流程

1. **清空数据**: 自动删除所有现有的文档版本和节点数据
2. **创建版本**: 创建 "openJiuwen V1" 版本
3. **导入 AgentStudio**: 
   - 创建 "AgentStudio" 一级目录
   - 递归扫描并导入所有 Markdown 文件
   - 复制静态资源到 `static_assets/agentstudio/`
4. **导入 AgentCore**:
   - 创建 "AgentCore" 一级目录
   - 递归扫描并导入所有 HTML 文件
   - 复制静态资源到 `static_assets/develop_docs/`
5. **统计信息**: 显示导入的节点数、文档数、目录数

## 📁 目录结构

导入后的数据库结构：

```
openJiuwen V1
├── AgentStudio (一级目录)
│   ├── [子目录/文档...]
│   └── ...
└── AgentCore (一级目录)
    ├── [子目录/文档...]
    └── ...
```

## 📊 静态资源处理

### AgentStudio 静态资源

- **源目录**: `/opt/huawei/data/jiuwen/test-agentstudio/docs/`
- **目标目录**: `/opt/huawei/data/jiuwen/official_website/docusaurus/static_assets/agentstudio/`
- **支持的文件类型**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.css`, `.js`, `.woff`, `.woff2`, `.ttf`, `.eot`
- **保持相对路径结构**: 资源文件的目录结构会被保留

### AgentCore 静态资源

- **源目录**: `/opt/huawei/data/jiuwen/official_website/docusaurus/develop_docs_1118`
- **目标目录**: `/opt/huawei/data/jiuwen/official_website/docusaurus/static_assets/develop_docs/`
- **支持的文件类型**: 同上
- **跳过目录**: 自动跳过 `css`, `js`, `images`, `fonts` 等系统目录（这些会作为静态资源复制）

## 🔍 文档处理说明

### Markdown 文档处理

- 解析 frontmatter（YAML 格式）
- 从 frontmatter 或内容中提取标题
- 生成 slug（URL 友好标识）
- 保留文档的层级结构

### HTML 文档处理

- 从 `<title>` 标签或 `<h1>` 标签提取标题
- 提取 `<body>` 中的文本内容
- 移除 `<script>` 和 `<style>` 标签
- 生成 slug（URL 友好标识）
- 保留文档的层级结构

## ⚠️ 注意事项

1. **数据清空**: 每次运行导入脚本都会清空所有现有文档数据，请谨慎操作
2. **版本唯一**: 当前只支持 "openJiuwen V1" 一个版本
3. **文件编码**: 确保源文件使用 UTF-8 编码
4. **路径要求**: 确保数据源路径存在且可访问
5. **静态资源**: 静态资源会保持原有的目录结构复制到目标位置

## 📝 导入后的数据结构

### 版本信息

- **版本名称**: openJiuwen V1
- **版本标签**: openJiuwen V1
- **是否当前版本**: 是
- **是否最新版本**: 是

### 节点类型

- **category**: 目录节点（如 AgentStudio、AgentCore）
- **doc**: 文档节点（Markdown 或 HTML 文档）

### 字段说明

- **title**: 文档/目录标题
- **slug**: URL 友好标识
- **file_path**: 相对于源目录的文件路径
- **content**: 文档内容（Markdown 或提取的 HTML 文本）
- **frontmatter**: Markdown 的 frontmatter（JSON 格式，仅 Markdown 文档）
- **order**: 显示顺序
- **parent_id**: 父节点 ID（用于建立层级关系）

## 🔄 重新导入

如果需要重新导入数据：

```bash
# 直接运行导入脚本即可（会自动清空旧数据）
python3 import_docs.py
```

## 📊 查询导入的数据

### 查看版本信息

```sql
SELECT * FROM doc_versions WHERE version_name = 'openJiuwen V1';
```

### 查看文档树结构

```sql
SELECT 
    n.id,
    n.node_type,
    n.title,
    n.slug,
    n.parent_id,
    n.`order`
FROM doc_nodes n
WHERE n.version_id = (SELECT id FROM doc_versions WHERE version_name = 'openJiuwen V1')
ORDER BY n.parent_id, n.`order`, n.id;
```

### 统计信息

```sql
SELECT 
    COUNT(*) as total_nodes,
    SUM(CASE WHEN node_type = 'doc' THEN 1 ELSE 0 END) as docs,
    SUM(CASE WHEN node_type = 'category' THEN 1 ELSE 0 END) as categories
FROM doc_nodes
WHERE version_id = (SELECT id FROM doc_versions WHERE version_name = 'openJiuwen V1');
```

---

**最后更新**: 2025-11-21
