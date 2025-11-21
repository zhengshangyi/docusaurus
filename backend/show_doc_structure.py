#!/usr/bin/env python3
"""
显示数据库中的文档结构和目录树
"""

from sqlalchemy.orm import Session
from database import SessionLocal
from models import DocVersion, DocNode, DocCategoryConfig


def print_tree(db: Session, version_id: int, parent_id: int = None, indent: int = 0):
    """递归打印文档树"""
    nodes = db.query(DocNode).filter(
        DocNode.version_id == version_id,
        DocNode.parent_id == parent_id
    ).order_by(DocNode.order, DocNode.id).all()
    
    for node in nodes:
        prefix = "  " * indent
        icon = "📁" if node.node_type == "category" else "📄"
        order_info = f" [order: {node.order}]" if node.order > 0 else ""
        file_info = f" ({node.file_path})" if node.file_path else ""
        
        print(f"{prefix}{icon} {node.title}{order_info}{file_info}")
        
        # 如果是目录，递归打印子节点
        if node.node_type == "category":
            print_tree(db, version_id, node.id, indent + 1)


def show_version_info(db: Session):
    """显示版本信息"""
    versions = db.query(DocVersion).all()
    
    print("=" * 80)
    print("版本信息")
    print("=" * 80)
    
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
        
        print(f"\n版本名称: {v.version_name}")
        print(f"  标签: {v.label}")
        print(f"  是否当前版本: {v.is_current}")
        print(f"  是否最新版本: {v.is_latest}")
        print(f"  状态: {v.status}")
        print(f"  节点总数: {node_count} (文档: {doc_count}, 目录: {category_count})")
        print(f"  创建时间: {v.created_at}")
    
    return versions


def show_doc_tree(db: Session, version: DocVersion):
    """显示文档树结构"""
    print("\n" + "=" * 80)
    print(f"文档树结构 - {version.version_name}")
    print("=" * 80)
    print()
    
    print_tree(db, version.id, parent_id=None, indent=0)


def show_statistics(db: Session, version: DocVersion):
    """显示统计信息"""
    print("\n" + "=" * 80)
    print(f"统计信息 - {version.version_name}")
    print("=" * 80)
    
    # 总节点数
    total = db.query(DocNode).filter(DocNode.version_id == version.id).count()
    docs = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.node_type == 'doc'
    ).count()
    categories = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.node_type == 'category'
    ).count()
    
    print(f"\n总节点数: {total}")
    print(f"  文档数: {docs}")
    print(f"  目录数: {categories}")
    
    # 一级目录统计
    top_level = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.parent_id == None
    ).all()
    
    print(f"\n一级目录/文档数: {len(top_level)}")
    for node in top_level:
        child_count = db.query(DocNode).filter(DocNode.parent_id == node.id).count()
        print(f"  - {node.title} ({node.node_type}): {child_count} 个子节点")
    
    # 文档类型统计
    print(f"\n文档格式统计:")
    md_docs = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.node_type == 'doc',
        DocNode.file_path.like('%.md')
    ).count()
    html_docs = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.node_type == 'doc',
        DocNode.file_path.like('%.html')
    ).count()
    print(f"  Markdown 文档: {md_docs}")
    print(f"  HTML 文档: {html_docs}")


def show_detailed_list(db: Session, version: DocVersion):
    """显示详细列表"""
    print("\n" + "=" * 80)
    print(f"详细列表 - {version.version_name}")
    print("=" * 80)
    
    nodes = db.query(DocNode).filter(
        DocNode.version_id == version.id
    ).order_by(DocNode.parent_id, DocNode.order, DocNode.id).all()
    
    print(f"\n{'ID':<6} {'类型':<10} {'标题':<40} {'父ID':<8} {'顺序':<6} {'文件路径'}")
    print("-" * 80)
    
    for node in nodes:
        parent_str = str(node.parent_id) if node.parent_id else "ROOT"
        type_str = "目录" if node.node_type == "category" else "文档"
        file_path = node.file_path[:50] if node.file_path else ""
        
        print(f"{node.id:<6} {type_str:<10} {node.title[:38]:<40} {parent_str:<8} {node.order:<6} {file_path}")


def main():
    """主函数"""
    db = SessionLocal()
    try:
        # 显示版本信息
        versions = show_version_info(db)
        
        # 对每个版本显示详细信息
        for version in versions:
            # 显示文档树
            show_doc_tree(db, version)
            
            # 显示统计信息
            show_statistics(db, version)
            
            # 显示详细列表
            show_detailed_list(db, version)
        
        print("\n" + "=" * 80)
        print("查询完成")
        print("=" * 80)
        
    finally:
        db.close()


if __name__ == "__main__":
    main()

