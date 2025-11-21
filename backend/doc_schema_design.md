# 多版本文档数据库表结构设计

## 设计目标

1. **多版本支持**：支持存储多个版本的文档数据
2. **层级结构**：支持目录和子目录的无限层级嵌套
3. **自定义顺序**：支持用户自定义文档和目录的展示顺序
4. **灵活配置**：支持目录的标签、描述等配置信息
5. **元数据管理**：支持文档的 frontmatter 元数据（slug, description, tags等）

## 表结构设计

### 1. doc_versions（文档版本表）

存储文档版本的基本信息。

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| version_name | VARCHAR(50) | 版本名称（如：3.9.2, current） | NOT NULL, UNIQUE |
| label | VARCHAR(100) | 版本显示标签（如：3.9.2 🚧） | |
| is_current | BOOLEAN | 是否为当前版本 | DEFAULT FALSE |
| is_latest | BOOLEAN | 是否为最新稳定版本 | DEFAULT FALSE |
| description | TEXT | 版本描述 | |
| release_date | DATE | 发布日期 | |
| status | VARCHAR(20) | 状态（active/archived/deprecated） | DEFAULT 'active' |
| created_at | DATETIME | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | 更新时间 | DEFAULT CURRENT_TIMESTAMP ON UPDATE |

**索引：**
- UNIQUE KEY `uk_version_name` (`version_name`)
- INDEX `idx_status` (`status`)

---

### 2. doc_nodes（文档节点表）

统一存储文档和目录节点，通过 `node_type` 字段区分。

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| version_id | INT | 所属版本ID | NOT NULL, FOREIGN KEY |
| parent_id | INT | 父节点ID（NULL表示根节点） | FOREIGN KEY |
| node_type | VARCHAR(20) | 节点类型（doc/category） | NOT NULL |
| title | VARCHAR(255) | 标题/标签 | NOT NULL |
| slug | VARCHAR(255) | URL友好标识 | |
| file_path | VARCHAR(500) | 文件路径（相对于版本目录） | |
| content | LONGTEXT | 文档内容（Markdown/MDX） | |
| frontmatter | JSON | Frontmatter元数据（JSON格式） | |
| description | TEXT | 描述/摘要 | |
| author | VARCHAR(100) | 作者 | |
| order | INT | 显示顺序（用户自定义） | DEFAULT 0 |
| sidebar_position | INT | 侧边栏位置（从frontmatter解析） | |
| is_active | BOOLEAN | 是否启用 | DEFAULT TRUE |
| view_count | INT | 浏览次数 | DEFAULT 0 |
| created_at | DATETIME | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | 更新时间 | DEFAULT CURRENT_TIMESTAMP ON UPDATE |

**索引：**
- INDEX `idx_version_parent` (`version_id`, `parent_id`)
- INDEX `idx_version_type` (`version_id`, `node_type`)
- INDEX `idx_slug` (`slug`)
- INDEX `idx_order` (`version_id`, `parent_id`, `order`)
- FOREIGN KEY `fk_version` (`version_id`) REFERENCES `doc_versions`(`id`) ON DELETE CASCADE
- FOREIGN KEY `fk_parent` (`parent_id`) REFERENCES `doc_nodes`(`id`) ON DELETE CASCADE

**说明：**
- `node_type='doc'` 表示文档，`node_type='category'` 表示目录
- `parent_id=NULL` 表示根节点（顶级文档或目录）
- `file_path` 存储相对路径，如：`guides/docs/introduction.mdx`
- `frontmatter` 存储 JSON 格式的元数据，如：`{"slug": "/", "description": "..."}`
- `order` 字段用于用户自定义排序，数值越小越靠前

---

### 3. doc_category_config（目录配置表）

存储目录的额外配置信息（对应 `_category_.yml` 文件）。

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| node_id | INT | 关联的目录节点ID | NOT NULL, UNIQUE, FOREIGN KEY |
| label | VARCHAR(255) | 目录显示标签 | |
| position | INT | 目录位置 | DEFAULT 0 |
| collapsed | BOOLEAN | 是否默认折叠 | DEFAULT FALSE |
| link_type | VARCHAR(20) | 链接类型（doc/generated-index） | |
| link_id | VARCHAR(255) | 链接ID（当link_type为doc时） | |
| custom_props | JSON | 自定义属性（JSON格式） | |
| created_at | DATETIME | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | 更新时间 | DEFAULT CURRENT_TIMESTAMP ON UPDATE |

**索引：**
- UNIQUE KEY `uk_node_id` (`node_id`)
- FOREIGN KEY `fk_node` (`node_id`) REFERENCES `doc_nodes`(`id`) ON DELETE CASCADE

**说明：**
- 此表与 `doc_nodes` 表是一对一关系
- 只有 `node_type='category'` 的节点才会有对应的配置记录
- `custom_props` 可以存储其他自定义配置，如：`{"title": "...", "description": "...", "keywords": [...]}`

---

### 4. doc_assets（文档资源表）

存储文档引用的静态资源（图片、文件等）。

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| version_id | INT | 所属版本ID | NOT NULL, FOREIGN KEY |
| node_id | INT | 关联的文档节点ID | FOREIGN KEY |
| asset_type | VARCHAR(20) | 资源类型（image/file/video） | NOT NULL |
| file_name | VARCHAR(255) | 文件名 | NOT NULL |
| file_path | VARCHAR(500) | 文件路径 | NOT NULL |
| file_size | BIGINT | 文件大小（字节） | |
| mime_type | VARCHAR(100) | MIME类型 | |
| url | VARCHAR(500) | 访问URL | |
| created_at | DATETIME | 创建时间 | DEFAULT CURRENT_TIMESTAMP |

**索引：**
- INDEX `idx_version` (`version_id`)
- INDEX `idx_node` (`node_id`)
- FOREIGN KEY `fk_version` (`version_id`) REFERENCES `doc_versions`(`id`) ON DELETE CASCADE
- FOREIGN KEY `fk_node` (`node_id`) REFERENCES `doc_nodes`(`id`) ON DELETE SET NULL

---

## 表关系图

```
doc_versions (版本表)
    │
    ├── 1:N ──> doc_nodes (文档节点表)
    │              │
    │              ├── 1:1 ──> doc_category_config (目录配置表)
    │              │
    │              └── N:1 ──> doc_nodes (自关联，parent_id)
    │
    └── 1:N ──> doc_assets (资源表)
                    │
                    └── N:1 ──> doc_nodes (关联文档)
```

## 使用场景示例

### 场景1：查询某个版本的所有文档树

```sql
-- 查询版本 3.9.2 的文档树结构
SELECT 
    n.id,
    n.parent_id,
    n.node_type,
    n.title,
    n.slug,
    n.order,
    c.label as category_label,
    c.position as category_position
FROM doc_nodes n
LEFT JOIN doc_category_config c ON n.id = c.node_id
WHERE n.version_id = (SELECT id FROM doc_versions WHERE version_name = '3.9.2')
ORDER BY n.parent_id, n.order, n.id;
```

### 场景2：查询某个目录下的所有文档（按自定义顺序）

```sql
-- 查询父目录ID为 100 的所有子节点，按自定义顺序排序
SELECT * FROM doc_nodes
WHERE parent_id = 100 AND version_id = 1
ORDER BY order ASC, id ASC;
```

### 场景3：查询文档内容及元数据

```sql
-- 查询文档内容
SELECT 
    n.*,
    v.version_name,
    JSON_EXTRACT(n.frontmatter, '$.slug') as frontmatter_slug,
    JSON_EXTRACT(n.frontmatter, '$.description') as frontmatter_description
FROM doc_nodes n
JOIN doc_versions v ON n.version_id = v.id
WHERE n.node_type = 'doc' 
  AND n.slug = 'introduction'
  AND v.version_name = 'current';
```

## 设计优势

1. **统一存储**：文档和目录统一存储在 `doc_nodes` 表中，简化查询逻辑
2. **灵活扩展**：通过 JSON 字段存储 frontmatter 和自定义属性，易于扩展
3. **性能优化**：通过合理的索引设计，支持高效的层级查询和排序
4. **数据完整性**：通过外键约束保证数据一致性
5. **版本隔离**：每个版本的数据完全独立，互不干扰

## 注意事项

1. **删除策略**：使用 `ON DELETE CASCADE` 确保删除版本时自动删除相关数据
2. **JSON 字段**：MySQL 5.7+ 支持 JSON 类型，便于存储和查询结构化数据
3. **排序逻辑**：优先使用 `order` 字段，其次使用 `id` 作为默认排序
4. **文件路径**：建议使用相对路径，便于版本管理和迁移

