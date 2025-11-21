#!/usr/bin/env python3
"""
文档数据查询测试脚本
演示如何查询多版本文档数据
"""

from sqlalchemy.orm import Session
from database import SessionLocal
from models import DocVersion, DocNode, DocCategoryConfig


def get_doc_tree(db: Session, version_name: str, parent_id: int = None):
    """获取文档树结构"""
    version = db.query(DocVersion).filter(DocVersion.version_name == version_name).first()
    if not version:
        return None
    
    nodes = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.parent_id == parent_id
    ).order_by(DocNode.order, DocNode.id).all()
    
    result = []
    for node in nodes:
        node_data = {
            'id': node.id,
            'type': node.node_type,
            'title': node.title,
            'slug': node.slug,
            'order': node.order,
            'children': []
        }
        
        # 如果是目录，获取子节点
        if node.node_type == 'category':
            node_data['children'] = get_doc_tree(db, version_name, node.id)
            # 获取目录配置
            config = db.query(DocCategoryConfig).filter(DocCategoryConfig.node_id == node.id).first()
            if config:
                node_data['config'] = {
                    'label': config.label,
                    'position': config.position,
                    'collapsed': config.collapsed
                }
        
        result.append(node_data)
    
    return result


def print_tree(tree, indent=0):
    """打印树形结构"""
    for item in tree:
        prefix = "  " * indent
        node_type = "📁" if item['type'] == 'category' else "📄"
        print(f"{prefix}{node_type} {item['title']} (order: {item['order']})")
        if item.get('children'):
            print_tree(item['children'], indent + 1)


def main():
    """主函数"""
    db = SessionLocal()
    try:
        # 查询当前版本的文档树
        print("=" * 60)
        print("当前版本 (current) 的文档树结构：")
        print("=" * 60)
        tree = get_doc_tree(db, "current")
        if tree:
            print_tree(tree)
        
        print("\n" + "=" * 60)
        print("版本统计信息：")
        print("=" * 60)
        versions = db.query(DocVersion).order_by(DocVersion.version_name).all()
        for v in versions:
            node_count = db.query(DocNode).filter(DocNode.version_id == v.id).count()
            doc_count = db.query(DocNode).filter(
                DocNode.version_id == v.id,
                DocNode.node_type == 'doc'
            ).count()
            category_count = db.query(DocNode).filter(
                DocNode.version_id == v.id,
                DocNode.node_type == 'category'
            ).count()
            print(f"{v.version_name:10} | 当前: {v.is_current} | 最新: {v.is_latest} | "
                  f"节点: {node_count} (文档: {doc_count}, 目录: {category_count})")
        
    finally:
        db.close()


if __name__ == "__main__":
    main()

