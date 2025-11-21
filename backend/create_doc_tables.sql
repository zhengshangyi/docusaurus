-- ============================================
-- 多版本文档数据库表结构
-- 用于存储 Docusaurus 文档数据
-- ============================================

-- 1. 文档版本表
CREATE TABLE IF NOT EXISTS `doc_versions` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `version_name` VARCHAR(50) NOT NULL COMMENT '版本名称（如：3.9.2, current）',
    `label` VARCHAR(100) COMMENT '版本显示标签（如：3.9.2 🚧）',
    `is_current` BOOLEAN DEFAULT FALSE COMMENT '是否为当前版本',
    `is_latest` BOOLEAN DEFAULT FALSE COMMENT '是否为最新稳定版本',
    `description` TEXT COMMENT '版本描述',
    `release_date` DATE COMMENT '发布日期',
    `status` VARCHAR(20) DEFAULT 'active' COMMENT '状态（active/archived/deprecated）',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_version_name` (`version_name`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档版本表';

-- 2. 文档节点表（统一存储文档和目录）
CREATE TABLE IF NOT EXISTS `doc_nodes` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `version_id` INT NOT NULL COMMENT '所属版本ID',
    `parent_id` INT NULL COMMENT '父节点ID（NULL表示根节点）',
    `node_type` VARCHAR(20) NOT NULL COMMENT '节点类型（doc/category）',
    `title` VARCHAR(255) NOT NULL COMMENT '标题/标签',
    `slug` VARCHAR(255) COMMENT 'URL友好标识',
    `file_path` VARCHAR(500) COMMENT '文件路径（相对于版本目录）',
    `content` LONGTEXT COMMENT '文档内容（Markdown/MDX）',
    `frontmatter` JSON COMMENT 'Frontmatter元数据（JSON格式）',
    `description` TEXT COMMENT '描述/摘要',
    `author` VARCHAR(100) COMMENT '作者',
    `order` INT DEFAULT 0 COMMENT '显示顺序（用户自定义）',
    `sidebar_position` INT COMMENT '侧边栏位置（从frontmatter解析）',
    `is_active` BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    `view_count` INT DEFAULT 0 COMMENT '浏览次数',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    INDEX `idx_version_parent` (`version_id`, `parent_id`),
    INDEX `idx_version_type` (`version_id`, `node_type`),
    INDEX `idx_slug` (`slug`),
    INDEX `idx_order` (`version_id`, `parent_id`, `order`),
    CONSTRAINT `fk_doc_nodes_version` FOREIGN KEY (`version_id`) 
        REFERENCES `doc_versions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_doc_nodes_parent` FOREIGN KEY (`parent_id`) 
        REFERENCES `doc_nodes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档节点表';

-- 3. 目录配置表
CREATE TABLE IF NOT EXISTS `doc_category_config` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `node_id` INT NOT NULL COMMENT '关联的目录节点ID',
    `label` VARCHAR(255) COMMENT '目录显示标签',
    `position` INT DEFAULT 0 COMMENT '目录位置',
    `collapsed` BOOLEAN DEFAULT FALSE COMMENT '是否默认折叠',
    `link_type` VARCHAR(20) COMMENT '链接类型（doc/generated-index）',
    `link_id` VARCHAR(255) COMMENT '链接ID（当link_type为doc时）',
    `custom_props` JSON COMMENT '自定义属性（JSON格式）',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_node_id` (`node_id`),
    CONSTRAINT `fk_category_config_node` FOREIGN KEY (`node_id`) 
        REFERENCES `doc_nodes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='目录配置表';

-- 4. 文档资源表
CREATE TABLE IF NOT EXISTS `doc_assets` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `version_id` INT NOT NULL COMMENT '所属版本ID',
    `node_id` INT NULL COMMENT '关联的文档节点ID',
    `asset_type` VARCHAR(20) NOT NULL COMMENT '资源类型（image/file/video）',
    `file_name` VARCHAR(255) NOT NULL COMMENT '文件名',
    `file_path` VARCHAR(500) NOT NULL COMMENT '文件路径',
    `file_size` BIGINT COMMENT '文件大小（字节）',
    `mime_type` VARCHAR(100) COMMENT 'MIME类型',
    `url` VARCHAR(500) COMMENT '访问URL',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    INDEX `idx_version` (`version_id`),
    INDEX `idx_node` (`node_id`),
    CONSTRAINT `fk_assets_version` FOREIGN KEY (`version_id`) 
        REFERENCES `doc_versions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_assets_node` FOREIGN KEY (`node_id`) 
        REFERENCES `doc_nodes` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档资源表';

-- ============================================
-- 初始化数据示例
-- ============================================

-- 插入当前版本
INSERT INTO `doc_versions` (`version_name`, `label`, `is_current`, `is_latest`, `status`) 
VALUES ('current', 'Current 🚧', TRUE, FALSE, 'active')
ON DUPLICATE KEY UPDATE `label` = VALUES(`label`);

-- 插入示例版本
INSERT INTO `doc_versions` (`version_name`, `label`, `is_current`, `is_latest`, `status`) 
VALUES ('3.9.2', '3.9.2', FALSE, TRUE, 'active')
ON DUPLICATE KEY UPDATE `label` = VALUES(`label`);

