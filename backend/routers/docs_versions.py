"""
文档版本和目录结构相关 API 路由
从数据库查询版本信息和文档列表
"""
import os
import re
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from models import DocVersion as DocVersionModel, DocNode

# 静态资源根目录
STATIC_ASSETS_ROOT = "/opt/huawei/data/jiuwen/official_website/docusaurus/static_assets"

# AgentStudio 文档和图片目录
AGENTSTUDIO_DOCS_DIR = "/opt/huawei/data/jiuwen/test-agentstudio/docs"
IMAGES_ROOT = os.path.join(STATIC_ASSETS_ROOT, "agentstudio", "images")

# AgentCore 文档目录
AGENTCORE_DOCS_ROOT = "/opt/huawei/data/jiuwen/official_website/docusaurus/develop_docs_1118"

# 文档根目录（用于兼容性）
DOCS_ROOT = AGENTSTUDIO_DOCS_DIR

router = APIRouter(prefix="/api/docs-versions", tags=["docs-versions"])


class DocVersion(BaseModel):
    """文档版本信息"""
    name: str  # 版本名称，如 "1.0.4"
    label: str  # 显示标签，如 "1.0.4 LTS"
    release_date: Optional[str] = None  # 发布日期
    type: Optional[str] = None  # 版本类型，如 "LTS", "STS"


class DocItem(BaseModel):
    """文档项信息"""
    title: str  # 文档标题
    path: str  # 文档路径（相对于文档中心目录）
    type: str  # 类型：file 或 directory
    children: Optional[List['DocItem']] = None  # 子项（仅目录类型有）
    file_path: Optional[str] = None  # 如果目录有同名文件，存储文件路径（用于点击目录时打开文件）


class DocVersionDetail(BaseModel):
    """文档版本详情"""
    version: DocVersion
    docs: List[DocItem]  # 该版本的文档列表


class DocVersionsResponse(BaseModel):
    """文档版本列表响应"""
    versions: List[DocVersion]
    current: Optional[str] = None  # 当前默认版本


class DocVersionDetailResponse(BaseModel):
    """文档版本详情响应"""
    version: DocVersion
    docs: List[DocItem]




def find_node_by_path_recursive(db: Session, version_id: int, path_parts: List[str], parent_id: Optional[int] = None, index: int = 0) -> Optional[DocNode]:
    """
    递归查找匹配路径的节点
    """
    if index >= len(path_parts):
        return None
    
    current_part = path_parts[index]
    
    # 查询当前层级的节点
    nodes = db.query(DocNode).filter(
        DocNode.version_id == version_id,
        DocNode.parent_id == parent_id,
        DocNode.is_active == True
    ).all()
    
    for node in nodes:
        # 匹配标题或 file_path（支持部分匹配）
        title_match = node.title == current_part
        file_path_match = False
        if node.file_path:
            # 检查 file_path 是否包含当前部分，或者文件名匹配
            file_name = os.path.basename(node.file_path)
            file_name_no_ext = os.path.splitext(file_name)[0]
            file_path_match = (
                current_part in node.file_path or
                current_part == file_name or
                current_part == file_name_no_ext
            )
        
        if title_match or file_path_match:
            if index == len(path_parts) - 1:
                # 最后一个部分，如果是文档节点，返回它
                if node.node_type == "doc":
                    return node
            else:
                # 继续查找子节点
                result = find_node_by_path_recursive(db, version_id, path_parts, node.id, index + 1)
                if result:
                    return result
    
    return None


def scan_docs_directory_with_titles(docs_dir: str, base_dir: str = None) -> List[DocItem]:
    """扫描文档目录，从文件内容读取标题
    保持原有顺序，并处理同名文件和目录的情况
    
    Args:
        docs_dir: 要扫描的目录路径
        base_dir: 基础目录路径，用于计算相对路径。如果为 None，则使用 docs_dir
    """
    if not os.path.exists(docs_dir):
        return []
    
    if base_dir is None:
        base_dir = docs_dir
    
    result = []
    # 保持原有顺序，不排序
    items = os.listdir(docs_dir)
    
    # 需要跳过的文件和目录（资源文件等）
    skip_items = {
        'css', 'fonts', 'FontAwesome', 'images', 'js', 
        '404.html', 'index.html', 'print.html', 'toc.html',
        'SECURITY.html', 'favicon.png', 'favicon.svg',
        'book.js', 'clipboard.min.js', 'elasticlunr.min.js',
        'highlight.css', 'highlight.js', 'mark.min.js',
        'searcher.js', 'searchindex.js', 'toc.js',
        'ayu-highlight.css', 'tomorrow-night.css'
    }
    
    # 优先显示的文件（排到最前面）
    priority_files = ['产品简介', '产品介绍']
    
    # 用于跟踪已处理的项，处理同名文件和目录的情况
    processed_items = {}
    
    # 分离优先文件和普通文件
    priority_items = []
    normal_items = []
    
    for item in items:
        # 跳过资源文件和特殊文件
        if item in skip_items:
            continue
        
        # 获取基础名称（去掉扩展名）
        base_name = os.path.splitext(item)[0] if not os.path.isdir(os.path.join(docs_dir, item)) else item
        
        # 如果是优先文件，放到优先列表
        if base_name in priority_files:
            priority_items.append(item)
        else:
            normal_items.append(item)
    
    # 对普通文件进行排序：如果以数字开头，按数字大小排序
    def sort_key(item: str) -> tuple:
        """排序键：优先按数字排序，然后按字母排序"""
        base_name = os.path.splitext(item)[0] if not os.path.isdir(os.path.join(docs_dir, item)) else item
        
        # 检查是否以数字开头
        import re
        match = re.match(r'^(\d+)', base_name)
        if match:
            # 以数字开头，提取数字部分
            num = int(match.group(1))
            # 返回 (0, 数字, 完整名称) 用于排序，0表示数字类型
            return (0, num, base_name)
        else:
            # 不以数字开头，按字母排序
            # 返回 (1, 0, 完整名称) 用于排序，1表示字母类型
            return (1, 0, base_name)
    
    # 对普通文件进行排序
    normal_items.sort(key=sort_key)
    
    # 先处理优先文件，再处理普通文件
    for item in priority_items + normal_items:
        item_path = os.path.join(docs_dir, item)
        relative_path = os.path.relpath(item_path, base_dir)
        
        # 获取基础名称（去掉扩展名），用于检查是否有同名文件和目录
        base_name = os.path.splitext(item)[0] if not os.path.isdir(item_path) else item
        
        if os.path.isdir(item_path):
            # 检查是否有同名的 HTML 文件
            html_file_path = os.path.join(docs_dir, f"{base_name}.html")
            has_html_file = os.path.exists(html_file_path) and os.path.isfile(html_file_path)
            
            # 递归扫描子目录
            children = scan_docs_directory_with_titles(item_path, base_dir)
            
            if has_html_file:
                # 如果存在同名 HTML 文件，创建一个特殊的目录项
                # 点击目录名打开同名文件，点击图标展开/收起目录
                html_relative_path = os.path.relpath(html_file_path, base_dir).replace("\\", "/")
                
                # 不将同名文件作为子项，只存储在 file_path 中
                # 这样点击目录名时打开文件，点击图标时展开子目录
                result.append(DocItem(
                    title=get_doc_title_from_path(item),
                    path=relative_path.replace("\\", "/"),
                    type="directory",
                    children=children if children else None,
                    file_path=html_relative_path  # 存储同名文件路径，用于点击目录名时打开
                ))
                processed_items[base_name] = True
            elif children:  # 只添加有内容的目录
                result.append(DocItem(
                    title=get_doc_title_from_path(item),
                    path=relative_path.replace("\\", "/"),
                    type="directory",
                    children=children if children else None
                ))
        elif item.endswith('.md') or item.endswith('.html'):
            # 检查是否已经作为目录的一部分处理了
            if base_name not in processed_items:
                result.append(DocItem(
                    title=get_doc_title_from_path(item),
                    path=relative_path.replace("\\", "/"),
                    type="file"
                ))
    
    return result


@router.get("/versions", response_model=DocVersionsResponse)
def get_doc_versions(db: Session = Depends(get_db)):
    """
    获取文档版本列表（从数据库查询）
    """
    # 从数据库查询所有活跃的版本
    db_versions = db.query(DocVersionModel).filter(
        DocVersionModel.status == "active"
    ).order_by(DocVersionModel.created_at.desc()).all()
    
    versions = []
    current_version_name = None
    
    for db_version in db_versions:
        version = DocVersion(
            name=db_version.version_name,
            label=db_version.label or db_version.version_name,
            release_date=db_version.release_date.strftime("%Y/%m/%d") if db_version.release_date else None,
            type=None  # 可以根据需要添加类型字段
        )
        versions.append(version)
        
        # 找到当前版本
        if db_version.is_current:
            current_version_name = db_version.version_name
    
    # 如果没有设置当前版本，使用第一个版本
    if not current_version_name and versions:
        current_version_name = versions[0].name
    
    return DocVersionsResponse(
        versions=versions,
        current=current_version_name
    )


def build_doc_tree(nodes: List[DocNode], parent_id: Optional[int] = None) -> List[DocItem]:
    """
    将数据库节点列表构建为文档树结构
    """
    # 筛选出指定父节点的子节点，并按 order 排序
    children = [node for node in nodes if node.parent_id == parent_id]
    children.sort(key=lambda x: (x.order or 0, x.id))
    
    result = []
    for node in children:
        # 构建当前节点的路径
        # 对于根节点，使用 title 作为路径
        if parent_id is None:
            path = node.title
        else:
            # 找到父节点路径
            parent_node = next((n for n in nodes if n.id == parent_id), None)
            if parent_node:
                parent_path = get_node_path(parent_node, nodes)
                path = f"{parent_path}/{node.title}" if parent_path else node.title
            else:
                path = node.title
        
        if node.node_type == "category":
            # 目录节点
            node_children = build_doc_tree(nodes, node.id)
            doc_item = DocItem(
                title=node.title,
                path=path,
                type="directory",
                children=node_children if node_children else None,
                file_path=node.file_path  # 如果有同名文件，存储文件路径
            )
        else:
            # 文档节点 - 如果有 file_path，使用 file_path 作为唯一标识
            # 这样可以区分同名的文档
            doc_path = node.file_path if node.file_path else path
            doc_item = DocItem(
                title=node.title,
                path=path,  # 显示路径
                type="file",
                file_path=doc_path  # 实际文件路径，用于区分同名文档
            )
        
        result.append(doc_item)
    
    return result


def get_node_path(node: DocNode, all_nodes: List[DocNode]) -> str:
    """
    获取节点的完整路径
    """
    if node.parent_id is None:
        return node.title
    
    parent = next((n for n in all_nodes if n.id == node.parent_id), None)
    if parent:
        parent_path = get_node_path(parent, all_nodes)
        return f"{parent_path}/{node.title}" if parent_path else node.title
    
    return node.title


@router.get("/versions/{version_name}", response_model=DocVersionDetailResponse)
def get_doc_version_detail(version_name: str, db: Session = Depends(get_db)):
    """
    获取指定版本的文档详情（从数据库查询）
    """
    # 从数据库查询版本
    db_version = db.query(DocVersionModel).filter(
        DocVersionModel.version_name == version_name,
        DocVersionModel.status == "active"
    ).first()
    
    if not db_version:
        raise HTTPException(status_code=404, detail=f"版本 {version_name} 不存在")
    
    # 构建版本响应对象
    version = DocVersion(
        name=db_version.version_name,
        label=db_version.label or db_version.version_name,
        release_date=db_version.release_date.strftime("%Y/%m/%d") if db_version.release_date else None,
        type=None
    )
    
    # 查询该版本下的所有节点
    all_nodes = db.query(DocNode).filter(
        DocNode.version_id == db_version.id,
        DocNode.is_active == True
    ).all()
    
    # 构建文档树（只包含根节点，即 parent_id 为 None 的节点）
    docs = build_doc_tree(all_nodes, parent_id=None)
    
    return DocVersionDetailResponse(
        version=version,
        docs=docs
    )


def convert_image_paths(markdown_content: str, md_file_path: str) -> str:
    """
    将 Markdown 中的相对图片路径转换为 API 路径
    """
    import urllib.parse
    
    # 获取 Markdown 文件所在目录
    md_dir = os.path.dirname(os.path.abspath(md_file_path))
    
    # 匹配 Markdown 图片语法: ![alt text](<path>) 或 ![alt text](path)
    def replace_image_path(match):
        full_match = match.group(0)
        alt_text = match.group(1)
        image_path = match.group(2).strip('<>')  # 移除可能的尖括号
        
        # 如果是绝对路径或 http/https 链接，或者是已经处理过的 /api/ 路径，直接返回
        if image_path.startswith('http://') or image_path.startswith('https://') or (image_path.startswith('/') and not image_path.startswith('/api/')):
            return full_match
        # 如果已经是 /api/ 路径，说明已经处理过，直接返回
        if image_path.startswith('/api/'):
            return full_match
        
        # 解析相对路径
        # 处理 Windows 和 Linux 路径分隔符
        image_path = image_path.replace('\\', '/')
        
        # 构建完整路径
        if image_path.startswith('../'):
            # 相对路径，需要从 Markdown 文件目录开始解析
            full_image_path = os.path.normpath(os.path.join(md_dir, image_path))
        else:
            # 相对当前目录
            full_image_path = os.path.normpath(os.path.join(md_dir, image_path))
        
        # 转换为绝对路径
        full_image_path = os.path.abspath(full_image_path)
        
        # 确保图片在允许的目录内（images 目录）
        abs_images_root = os.path.abspath(IMAGES_ROOT)
        abs_docs_root = os.path.abspath(DOCS_ROOT)
        
        # 检查图片是否在 images 目录下，或者相对于 docs 目录
        if full_image_path.startswith(abs_images_root):
            # 计算相对路径（相对于 images 根目录）
            relative_path = os.path.relpath(full_image_path, abs_images_root)
            relative_path = relative_path.replace('\\', '/')
            # 对路径进行 URL 编码（分段编码，保留路径分隔符）
            path_parts = relative_path.split('/')
            encoded_parts = [urllib.parse.quote(part, safe='') for part in path_parts]
            encoded_path = '/'.join(encoded_parts)
            # 转换为 API 路径
            api_path = f"/api/docs-versions/images/{encoded_path}"
            return f"![{alt_text}]({api_path})"
        elif full_image_path.startswith(abs_docs_root):
            # 如果在文档目录内，也可以尝试处理
            # 这里可能需要根据实际情况调整
            relative_path = os.path.relpath(full_image_path, abs_docs_root)
            relative_path = relative_path.replace('\\', '/')
            path_parts = relative_path.split('/')
            encoded_parts = [urllib.parse.quote(part, safe='') for part in path_parts]
            encoded_path = '/'.join(encoded_parts)
            api_path = f"/api/docs-versions/images-from-docs/{encoded_path}"
            return f"![{alt_text}]({api_path})"
        else:
            # 不在允许的目录内，保持原样
            return full_match
    
    # 匹配图片语法: ![alt](path) 或 ![alt](<path>)
    # 需要特殊处理带尖括号的情况
    # 先匹配带尖括号的: ![alt](<path>)
    pattern1 = r'!\[([^\]]*)\]\(<([^>]+)>\)'
    result = re.sub(pattern1, replace_image_path, markdown_content)
    # 再匹配不带尖括号的: ![alt](path)，但排除已经处理过的 /api/ 路径
    pattern2 = r'!\[([^\]]*)\]\(((?!/api/)[^\)]+)\)'
    result = re.sub(pattern2, replace_image_path, result)
    
    return result


@router.get("/images/{image_path:path}")
async def get_image(image_path: str):
    """
    获取文档图片（从 IMAGES_ROOT 目录）
    """
    import urllib.parse
    
    # URL 解码路径
    decoded_path = urllib.parse.unquote(image_path)
    
    # 构建完整文件路径
    file_path = os.path.join(IMAGES_ROOT, decoded_path.lstrip('/'))
    
    # 安全检查：确保文件在图片目录内
    abs_images_root = os.path.abspath(IMAGES_ROOT)
    abs_file_path = os.path.abspath(file_path)
    
    if not abs_file_path.startswith(abs_images_root):
        raise HTTPException(status_code=403, detail="无权访问该文件")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="图片不存在")
    
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=400, detail="不是有效的图片文件")
    
    # 检查文件扩展名
    ext = os.path.splitext(file_path)[1].lower()
    allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp']
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    return FileResponse(file_path)


@router.get("/images-from-agentcore/{image_path:path}")
async def get_agentcore_image(image_path: str):
    """
    获取 AgentCore 文档中的图片（从 AGENTCORE_DOCS_ROOT/images 目录）
    """
    import urllib.parse
    
    # URL 解码路径
    decoded_path = urllib.parse.unquote(image_path)
    
    # 构建完整文件路径
    file_path = os.path.join(AGENTCORE_DOCS_ROOT, "images", decoded_path.lstrip('/'))
    
    # 安全检查：确保文件在 AgentCore 图片目录内
    abs_agentcore_images = os.path.abspath(os.path.join(AGENTCORE_DOCS_ROOT, "images"))
    abs_file_path = os.path.abspath(file_path)
    
    if not abs_file_path.startswith(abs_agentcore_images):
        raise HTTPException(status_code=403, detail="无权访问该文件")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="图片不存在")
    
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=400, detail="不是有效的图片文件")
    
    # 检查文件扩展名
    ext = os.path.splitext(file_path)[1].lower()
    allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp']
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    return FileResponse(file_path)


def convert_html_image_paths(html_content: str, html_file_path: str) -> str:
    """将 HTML 中的相对图片路径转换为 API 路径"""
    import urllib.parse
    import re
    
    # 获取 HTML 文件所在目录
    html_dir = os.path.dirname(os.path.abspath(html_file_path))
    
    # 判断是否是 AgentCore 文档
    abs_agentcore_root = os.path.abspath(AGENTCORE_DOCS_ROOT)
    abs_html_file = os.path.abspath(html_file_path)
    is_agentcore = abs_html_file.startswith(abs_agentcore_root)
    
    def replace_img_src(match):
        full_match = match.group(0)
        # 对于 pattern: r'<img([^>]*?)\s+src=(["\'])([^"\']+)\2([^>]*)>'
        # group(1) = img 标签中 src 之前的部分
        # group(2) = 引号类型 (" 或 ')
        # group(3) = src 的值
        # group(4) = src 之后的部分
        try:
            before_src = match.group(1) or ''
            quote = match.group(2) or '"'
            src = match.group(3) or ''
            after_src = match.group(4) or ''
        except IndexError:
            return full_match
        
        if not src:
            return full_match
        
        src = src.strip('"\'')
        
        # 如果是绝对路径或 http/https 链接，或者是已经处理过的 /api/ 路径，直接返回
        if src.startswith('http://') or src.startswith('https://') or src.startswith('/api/'):
            return full_match
        
        # 解析相对路径
        src = src.replace('\\', '/')
        
        # 构建完整路径
        full_image_path = os.path.normpath(os.path.join(html_dir, src))
        full_image_path = os.path.abspath(full_image_path)
        
        # 如果是 AgentCore 文档的图片
        if is_agentcore:
            abs_agentcore_images = os.path.abspath(os.path.join(AGENTCORE_DOCS_ROOT, "images"))
            # 检查图片是否在 images 目录下
            if full_image_path.startswith(abs_agentcore_images):
                relative_path = os.path.relpath(full_image_path, abs_agentcore_images)
                relative_path = relative_path.replace('\\', '/')
                path_parts = relative_path.split('/')
                encoded_parts = [urllib.parse.quote(part, safe='') for part in path_parts]
                encoded_path = '/'.join(encoded_parts)
                api_path = f"/api/docs-versions/images-from-agentcore/{encoded_path}"
                # 替换 src 属性值，保持其他属性不变
                return f'<img{before_src} src={quote}{api_path}{quote}{after_src}>'
        
        # 处理 AgentStudio 或其他图片 - 转换为静态资源路径
        # 检查是否是静态资源目录中的图片
        abs_static_assets = os.path.abspath(STATIC_ASSETS_ROOT)
        if full_image_path.startswith(abs_static_assets):
            # 计算相对于 static_assets 的路径
            relative_path = os.path.relpath(full_image_path, abs_static_assets)
            relative_path = relative_path.replace('\\', '/')
            static_path = f"/static_assets/{relative_path}"
            return f'<img{before_src} src={quote}{static_path}{quote}{after_src}>'
        
        # 如果图片路径包含 images，尝试转换为静态资源路径
        if 'images' in src.lower():
            # 移除相对路径前缀
            clean_src = src.lstrip('./')
            while clean_src.startswith('../'):
                clean_src = clean_src[3:]
            
            # 判断是 AgentStudio 还是 AgentCore
            agentstudio_keywords = ['提示词', '模型管理', 'workflow', '代码节点', '变量聚合节点', 
                                   '文本编辑节点', '输入节点', '输出节点', '智能体', '插件']
            if any(keyword in clean_src for keyword in agentstudio_keywords):
                static_path = f"/static_assets/agentstudio/{clean_src}"
            else:
                static_path = f"/static_assets/develop_docs/{clean_src}"
            return f'<img{before_src} src={quote}{static_path}{quote}{after_src}>'
        
        # 其他情况保持原样
        return full_match
    
    # 匹配 <img> 标签，支持多种格式：
    # <img src="...">
    # <img src='...'>
    # <img ... src="..." ...>
    # 使用更灵活的正则表达式
    pattern = r'<img([^>]*?)\s+src=(["\'])([^"\']+)\2([^>]*)>'
    result = re.sub(pattern, replace_img_src, html_content, flags=re.IGNORECASE)
    
    return result


def extract_html_content(html_content: str, html_file_path: str = None) -> str:
    """从 HTML 文件中提取主要内容（只提取 <main> 标签内的内容）"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找主要内容区域 - 只提取 <main> 标签内的内容
        main_content = soup.find('main')
        
        if main_content:
            # 移除不需要的元素
            # 移除 mdbook-help-container（Keyboard shortcuts 帮助）
            for help_container in main_content.find_all(id='mdbook-help-container'):
                help_container.decompose()
            
            # 移除 menu-bar（主题选择器和标题）
            for menu_bar in main_content.find_all(class_='menu-bar'):
                menu_bar.decompose()
            
            # 移除 sidebar
            for sidebar in main_content.find_all(id='sidebar'):
                sidebar.decompose()
            
            # 移除 search-wrapper
            for search_wrapper in main_content.find_all(id='search-wrapper'):
                search_wrapper.decompose()
            
            # 移除 nav-wrapper（导航按钮）
            for nav_wrapper in main_content.find_all(class_='nav-wrapper'):
                nav_wrapper.decompose()
            
            # 移除 nav-wide-wrapper
            for nav_wide in main_content.find_all(class_='nav-wide-wrapper'):
                nav_wide.decompose()
            
            # 移除所有 script 标签
            for script in main_content.find_all('script'):
                script.decompose()
            
            # 移除所有 style 标签
            for style in main_content.find_all('style'):
                style.decompose()
            
            # 移除包含 "openJiuwen Developer docs" 的元素及其父元素
            # 查找所有包含该文本的元素
            for element in main_content.find_all(text=True):
                if element and "openJiuwen Developer docs" in element:
                    parent = element.parent
                    if parent:
                        # 移除整个父元素（通常是标题或链接）
                        parent.decompose()
            
            # 移除 menu-title（包含 "openJiuwen Developer docs" 的标题）
            for menu_title in main_content.find_all(class_='menu-title'):
                menu_title.decompose()
            
            # 移除 h1.menu-title
            for h1 in main_content.find_all('h1', class_='menu-title'):
                h1.decompose()
            
            # 移除 sidebar-toggle-anchor
            for sidebar_toggle in main_content.find_all(id='sidebar-toggle-anchor'):
                sidebar_toggle.decompose()
            
            # 移除 page-wrapper
            for page_wrapper in main_content.find_all(id='page-wrapper'):
                page_wrapper.decompose()
            for page_wrapper in main_content.find_all(class_='page-wrapper'):
                page_wrapper.decompose()
            
            # 移除 page div
            for page_div in main_content.find_all(class_='page'):
                page_div.decompose()
            
            # 移除 body-container
            for body_container in main_content.find_all(id='body-container'):
                body_container.decompose()
            
            # 移除 menu-bar-hover-placeholder
            for placeholder in main_content.find_all(id='menu-bar-hover-placeholder'):
                placeholder.decompose()
            
            # 移除 right-buttons（打印按钮等）
            for right_buttons in main_content.find_all(class_='right-buttons'):
                right_buttons.decompose()
            
            # 移除 searchresults-outer
            for searchresults in main_content.find_all(id='searchresults-outer'):
                searchresults.decompose()
            for searchresults in main_content.find_all(class_='searchresults-outer'):
                searchresults.decompose()
            
            # 移除 searchresults-header
            for searchresults_header in main_content.find_all(id='searchresults-header'):
                searchresults_header.decompose()
            for searchresults_header in main_content.find_all(class_='searchresults-header'):
                searchresults_header.decompose()
            
            # 移除 searchresults
            for searchresults in main_content.find_all(id='searchresults'):
                searchresults.decompose()
            
            # 使用正则表达式移除所有包含 "openJiuwen Developer docs" 的标签
            # 先转换为字符串，然后用正则表达式清理
            content = str(main_content)
            # 移除包含 "openJiuwen Developer docs" 的整个标签及其内容
            content = re.sub(r'<[^>]*>.*?openJiuwen Developer docs.*?</[^>]*>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除包含 "openJiuwen Developer docs" 的标签（自闭合标签）
            content = re.sub(r'<[^>]*openJiuwen Developer docs[^>]*>', '', content, flags=re.IGNORECASE)
            # 移除纯文本中的 "openJiuwen Developer docs"
            content = re.sub(r'openJiuwen Developer docs[^<]*', '', content, flags=re.IGNORECASE)
            
            # 使用正则表达式移除其他不需要的元素
            # 移除 body-container
            content = re.sub(r'<div[^>]*id=["\']body-container["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 sidebar-toggle-anchor
            content = re.sub(r'<input[^>]*id=["\']sidebar-toggle-anchor["\'][^>]*>', '', content, flags=re.IGNORECASE)
            # 移除 page-wrapper
            content = re.sub(r'<div[^>]*id=["\']page-wrapper["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<div[^>]*class=["\'][^"\']*page-wrapper[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 page div
            content = re.sub(r'<div[^>]*class=["\']page["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 menu-title
            content = re.sub(r'<h1[^>]*class=["\']menu-title["\'][^>]*>.*?</h1>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<[^>]*class=["\']menu-title["\'][^>]*>.*?</[^>]*>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 menu-bar-hover-placeholder
            content = re.sub(r'<div[^>]*id=["\']menu-bar-hover-placeholder["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 right-buttons
            content = re.sub(r'<div[^>]*class=["\']right-buttons["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 searchresults-outer
            content = re.sub(r'<div[^>]*id=["\']searchresults-outer["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<div[^>]*class=["\']searchresults-outer[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 searchresults-header
            content = re.sub(r'<div[^>]*id=["\']searchresults-header["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<div[^>]*class=["\']searchresults-header["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 searchresults
            content = re.sub(r'<ul[^>]*id=["\']searchresults["\'][^>]*>.*?</ul>', '', content, flags=re.DOTALL | re.IGNORECASE)
            
            # 转换图片路径
            if html_file_path:
                content = convert_html_image_paths(content, html_file_path)
            # 再次使用 convert_image_paths_in_content 确保所有图片路径都正确
            content = convert_image_paths_in_content(content, html_file_path)
            return content
        else:
            # 如果没有找到 main 标签，尝试从 body 中提取，但过滤掉不需要的元素
            body = soup.find('body')
            if body:
                # 移除不需要的元素
                for help_container in body.find_all(id='mdbook-help-container'):
                    help_container.decompose()
                for menu_bar in body.find_all(class_='menu-bar'):
                    menu_bar.decompose()
                for sidebar in body.find_all(id='sidebar'):
                    sidebar.decompose()
                for search_wrapper in body.find_all(id='search-wrapper'):
                    search_wrapper.decompose()
                for nav_wrapper in body.find_all(class_='nav-wrapper'):
                    nav_wrapper.decompose()
                for nav_wide in body.find_all(class_='nav-wide-wrapper'):
                    nav_wide.decompose()
                for script in body.find_all('script'):
                    script.decompose()
                for style in body.find_all('style'):
                    style.decompose()
                
                # 移除包含 "openJiuwen Developer docs" 的元素
                for element in body.find_all(text=True):
                    if element and "openJiuwen Developer docs" in element:
                        parent = element.parent
                        if parent:
                            parent.decompose()
                
                # 移除 menu-title
                for menu_title in body.find_all(class_='menu-title'):
                    menu_title.decompose()
                for h1 in body.find_all('h1', class_='menu-title'):
                    h1.decompose()
                
                # 移除 sidebar-toggle-anchor
                for sidebar_toggle in body.find_all(id='sidebar-toggle-anchor'):
                    sidebar_toggle.decompose()
                
                # 移除 page-wrapper
                for page_wrapper in body.find_all(id='page-wrapper'):
                    page_wrapper.decompose()
                for page_wrapper in body.find_all(class_='page-wrapper'):
                    page_wrapper.decompose()
                
                # 移除 page div
                for page_div in body.find_all(class_='page'):
                    page_div.decompose()
                
                # 移除 body-container
                for body_container in body.find_all(id='body-container'):
                    body_container.decompose()
                
                # 移除 menu-bar-hover-placeholder
                for placeholder in body.find_all(id='menu-bar-hover-placeholder'):
                    placeholder.decompose()
                
                # 移除 right-buttons
                for right_buttons in body.find_all(class_='right-buttons'):
                    right_buttons.decompose()
                
                # 移除 searchresults-outer
                for searchresults in body.find_all(id='searchresults-outer'):
                    searchresults.decompose()
                for searchresults in body.find_all(class_='searchresults-outer'):
                    searchresults.decompose()
                
                # 移除 searchresults-header
                for searchresults_header in body.find_all(id='searchresults-header'):
                    searchresults_header.decompose()
                for searchresults_header in body.find_all(class_='searchresults-header'):
                    searchresults_header.decompose()
                
                # 移除 searchresults
                for searchresults in body.find_all(id='searchresults'):
                    searchresults.decompose()
                
                content = str(body)
                # 使用正则表达式清理
                content = re.sub(r'<[^>]*>.*?openJiuwen Developer docs.*?</[^>]*>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<[^>]*openJiuwen Developer docs[^>]*>', '', content, flags=re.IGNORECASE)
                content = re.sub(r'openJiuwen Developer docs[^<]*', '', content, flags=re.IGNORECASE)
                
                # 使用正则表达式移除其他不需要的元素
                content = re.sub(r'<div[^>]*id=["\']body-container["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<input[^>]*id=["\']sidebar-toggle-anchor["\'][^>]*>', '', content, flags=re.IGNORECASE)
                content = re.sub(r'<div[^>]*id=["\']page-wrapper["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<div[^>]*class=["\'][^"\']*page-wrapper[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<div[^>]*class=["\']page["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<h1[^>]*class=["\']menu-title["\'][^>]*>.*?</h1>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<[^>]*class=["\']menu-title["\'][^>]*>.*?</[^>]*>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<div[^>]*id=["\']menu-bar-hover-placeholder["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<div[^>]*class=["\']right-buttons["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<div[^>]*id=["\']searchresults-outer["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<div[^>]*class=["\']searchresults-outer[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<div[^>]*id=["\']searchresults-header["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<div[^>]*class=["\']searchresults-header["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<ul[^>]*id=["\']searchresults["\'][^>]*>.*?</ul>', '', content, flags=re.DOTALL | re.IGNORECASE)
                
                if html_file_path:
                    content = convert_html_image_paths(content, html_file_path)
                    # 再次使用 convert_image_paths_in_content 确保所有图片路径都正确
                    content = convert_image_paths_in_content(content, html_file_path)
                return content
            return html_content
    except ImportError:
        # 如果没有 BeautifulSoup，使用简单的正则表达式提取
        # 提取 <main> 标签内的内容
        import re
        main_match = re.search(r'<main[^>]*>(.*?)</main>', html_content, re.DOTALL | re.IGNORECASE)
        if main_match:
            content = main_match.group(1)
            # 移除不需要的元素（使用正则表达式）
            # 移除 mdbook-help-container
            content = re.sub(r'<div[^>]*id=["\']mdbook-help-container["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 menu-bar
            content = re.sub(r'<div[^>]*class=["\'][^"\']*menu-bar[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 sidebar
            content = re.sub(r'<nav[^>]*id=["\']sidebar["\'][^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 search-wrapper
            content = re.sub(r'<div[^>]*id=["\']search-wrapper["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 nav-wrapper
            content = re.sub(r'<nav[^>]*class=["\'][^"\']*nav-wrapper[^"\']*["\'][^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 nav-wide-wrapper
            content = re.sub(r'<nav[^>]*class=["\'][^"\']*nav-wide-wrapper[^"\']*["\'][^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 script 标签
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 style 标签
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除包含 "openJiuwen Developer docs" 的内容
            content = re.sub(r'<[^>]*>.*?openJiuwen Developer docs.*?</[^>]*>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<[^>]*openJiuwen Developer docs[^>]*>', '', content, flags=re.IGNORECASE)
            content = re.sub(r'openJiuwen Developer docs[^<]*', '', content, flags=re.IGNORECASE)
            
            if html_file_path:
                content = convert_html_image_paths(content, html_file_path)
            return content
        return html_content
    except Exception:
        return html_content


def html_to_markdown(html_content: str) -> str:
    """将 HTML 内容转换为 Markdown（简单实现）"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取文本内容
        # 这里可以添加更复杂的转换逻辑
        text = soup.get_text(separator='\n\n', strip=True)
        return text
    except ImportError:
        # 如果没有 BeautifulSoup，返回原始 HTML
        return html_content
    except Exception:
        return html_content


def convert_image_paths_in_content(content: str, file_path: Optional[str] = None, is_agentstudio_doc: Optional[bool] = None) -> str:
    """
    将文档内容中的图片相对路径转换为静态资源 URL
    """
    import urllib.parse
    
    # 处理 Markdown 格式的图片: ![alt](<path>) 或 ![alt](path)
    def replace_markdown_image(match):
        # 处理两种格式: ![alt](<path>) 或 ![alt](path)
        if match.group(2):  # 带尖括号的格式
            alt_text = match.group(1) or ''
            image_path = match.group(2).strip('<>') if match.group(2) else ''
        else:  # 不带尖括号的格式
            alt_text = match.group(3) or ''
            image_path = match.group(4) or ''
        
        if not image_path:
            return match.group(0)
        
        # 如果是绝对 URL 或已经是 API 路径，需要检查是否需要 URL 编码
        if image_path.startswith('http://') or image_path.startswith('https://') or image_path.startswith('/api/'):
            return match.group(0)
        
        # 如果已经是 /static_assets/ 路径，检查是否需要 URL 编码中文字符
        if image_path.startswith('/static_assets/'):
            # 检查路径中是否包含中文字符
            try:
                # 尝试解码，如果成功说明已经编码过
                decoded = urllib.parse.unquote(image_path)
                if decoded == image_path:
                    # 没有编码过，检查是否有中文字符
                    if any('\u4e00' <= char <= '\u9fff' for char in image_path):
                        # 包含中文字符，需要编码
                        path_parts = image_path.split('/')
                        encoded_parts = []
                        for part in path_parts:
                            if part:
                                encoded_parts.append(urllib.parse.quote(part, safe=''))
                            else:
                                encoded_parts.append('')
                        encoded_path = '/'.join(encoded_parts)
                        return f"![{alt_text}]({encoded_path})"
            except:
                pass
            # 已经编码过或不需要编码，直接返回
            return match.group(0)
        
        # 处理相对路径
        # 图片路径格式: ../../images/xxx.png 或 images/xxx.png
        # 需要转换为: /static_assets/agentstudio/images/xxx.png 或 /static_assets/develop_docs/images/xxx.png
        
        # 移除开头的 ../
        image_path = image_path.lstrip('./')
        while image_path.startswith('../'):
            image_path = image_path[3:]
        
        # 判断是 AgentStudio 还是 AgentCore 的图片
        # 根据路径特征判断
        # AgentStudio 的特征：提示词、模型管理、workflow、代码节点、变量聚合节点、文本编辑节点、输入节点、输出节点等
        agentstudio_keywords = ['提示词', '模型管理', 'workflow', '代码节点', '变量聚合节点', 
                               '文本编辑节点', '输入节点', '输出节点', '智能体', '插件', 
                               '意图识别', '提问器', '大模型配置']
        
        # 如果明确指定了文档类型，优先使用
        if is_agentstudio_doc is not None:
            is_agentstudio = is_agentstudio_doc
        else:
            # 如果 file_path 存在，根据文件路径判断更准确
            is_agentstudio = False
            if file_path:
                # 检查文件路径是否来自 AgentStudio 目录
                if 'agentstudio' in file_path.lower() or 'test-agentstudio' in file_path.lower() or '文档中心' in file_path:
                    is_agentstudio = True
                elif any(keyword in image_path for keyword in agentstudio_keywords):
                    is_agentstudio = True
            else:
                # 如果没有 file_path，根据图片路径特征判断
                is_agentstudio = any(keyword in image_path for keyword in agentstudio_keywords)
        
        if is_agentstudio:
            # AgentStudio 图片
            static_path = f"/static_assets/agentstudio/{image_path}"
        else:
            # AgentCore 图片
            static_path = f"/static_assets/develop_docs/{image_path}"
        
        # 对路径中的中文字符进行 URL 编码（只编码路径部分，不编码整个 URL）
        # 将路径分割成部分，对每个部分进行编码
        path_parts = static_path.split('/')
        encoded_parts = []
        for part in path_parts:
            if part:
                # 对每个路径段进行 URL 编码（保留 / 分隔符）
                encoded_parts.append(urllib.parse.quote(part, safe=''))
            else:
                encoded_parts.append('')
        encoded_path = '/'.join(encoded_parts)
        
        return f"![{alt_text}]({encoded_path})"
    
    # 匹配 Markdown 图片语法 - 先匹配带尖括号的，再匹配不带尖括号的
    pattern1 = r'!\[([^\]]*)\]\(<([^>]+)>\)'
    content = re.sub(pattern1, replace_markdown_image, content)
    pattern2 = r'!\[([^\]]*)\]\(([^\)]+)\)'
    content = re.sub(pattern2, replace_markdown_image, content)
    
    # 处理 HTML 格式的图片: <img src="path">
    def replace_html_image(match):
        before_src = match.group(1) or ''
        quote = match.group(2) or '"'
        src = match.group(3) or ''
        after_src = match.group(4) or ''
        
        if not src:
            return match.group(0)
        
        src = src.strip('"\'')
        
        # 如果是绝对 URL 或已经是 API 路径，需要检查是否需要 URL 编码
        if src.startswith('http://') or src.startswith('https://') or src.startswith('/api/'):
            return match.group(0)
        
        # 如果已经是 /static_assets/ 路径，检查是否需要 URL 编码中文字符
        if src.startswith('/static_assets/'):
            # 检查路径中是否包含中文字符
            try:
                decoded = urllib.parse.unquote(src)
                if decoded == src:
                    # 没有编码过，检查是否有中文字符
                    if any('\u4e00' <= char <= '\u9fff' for char in src):
                        # 包含中文字符，需要编码
                        path_parts = src.split('/')
                        encoded_parts = []
                        for part in path_parts:
                            if part:
                                encoded_parts.append(urllib.parse.quote(part, safe=''))
                            else:
                                encoded_parts.append('')
                        encoded_path = '/'.join(encoded_parts)
                        return f'<img{before_src} src={quote}{encoded_path}{quote}{after_src}>'
            except:
                pass
            # 已经编码过或不需要编码，直接返回
            return match.group(0)
        
        # 处理相对路径
        src = src.lstrip('./')
        while src.startswith('../'):
            src = src[3:]
        
        # 判断图片来源
        if 'images' in src.lower():
            # 根据路径特征判断
            agentstudio_keywords = ['提示词', '模型管理', 'workflow', '代码节点', '变量聚合节点', 
                                   '文本编辑节点', '输入节点', '输出节点', '智能体', '插件',
                                   '意图识别', '提问器', '大模型配置']
            
            # 如果明确指定了文档类型，优先使用
            if is_agentstudio_doc is not None:
                is_agentstudio = is_agentstudio_doc
            else:
                # 如果 file_path 存在，根据文件路径判断更准确
                is_agentstudio = False
                if file_path:
                    # 检查文件路径是否来自 AgentStudio 目录
                    if 'agentstudio' in file_path.lower() or 'test-agentstudio' in file_path.lower() or '文档中心' in file_path:
                        is_agentstudio = True
                    elif any(keyword in src for keyword in agentstudio_keywords):
                        is_agentstudio = True
                else:
                    # 如果没有 file_path，根据图片路径特征判断
                    is_agentstudio = any(keyword in src for keyword in agentstudio_keywords)
            
            if is_agentstudio:
                static_path = f"/static_assets/agentstudio/{src}"
            else:
                static_path = f"/static_assets/develop_docs/{src}"
        else:
            static_path = src
        
        # 对路径中的中文字符进行 URL 编码
        if static_path.startswith('/static_assets/'):
            path_parts = static_path.split('/')
            encoded_parts = []
            for part in path_parts:
                if part:
                    encoded_parts.append(urllib.parse.quote(part, safe=''))
                else:
                    encoded_parts.append('')
            static_path = '/'.join(encoded_parts)
        
        return f'<img{before_src} src={quote}{static_path}{quote}{after_src}>'
    
    # 匹配 HTML img 标签
    html_pattern = r'<img([^>]*?)\s+src=(["\'])([^"\']+)\2([^>]*)>'
    content = re.sub(html_pattern, replace_html_image, content, flags=re.IGNORECASE)
    
    return content


def clean_unwanted_html_fragments(content: str) -> str:
    """
    清理内容中不需要的 HTML 片段
    删除用户指定的特定字符串（body-container、page-wrapper、menu-title 等）
    """
    if not content:
        return content
    
    # 用户指定的需要删除的完整字符串（精确匹配）
    unwanted_string = (
        "\n    \n        </div>\n    </div>\n    <div id=\"body-container\">\n        "
        "<!-- Work around some values being stored in localStorage wrapped in quotes -->\n        \n\n        "
        "<!-- Set the theme before any content is loaded, prevents flash -->\n        \n\n        "
        "<input type=\"checkbox\" id=\"sidebar-toggle-anchor\" class=\"hidden\">\n\n        "
        "<!-- Hide / unhide sidebar before it is displayed -->\n        \n\n        \n\n        "
        "<div id=\"page-wrapper\" class=\"page-wrapper\">\n\n            <div class=\"page\">\n                "
        "<div id=\"menu-bar-hover-placeholder\"></div>\n                \n\n                    "
        "<h1 class=\"menu-title\">openJiuwen Developer docs</h1>\n\n                    "
        "<div class=\"right-buttons\">\n                        "
        "<a href=\"../../print.html\" title=\"Print this book\" aria-label=\"Print this book\">\n                            "
        "<i id=\"print-button\" class=\"fa fa-print\"></i>\n                        </a>\n\n                    </div>\n                </div>\n\n                \n                        </div>\n                    </form>\n                    "
        "<div id=\"searchresults-outer\" class=\"searchresults-outer hidden\">\n                        "
        "<div id=\"searchresults-header\" class=\"searchresults-header\"></div>\n                        "
        "<ul id=\"searchresults\">\n                        </ul>\n                    </div>\n                </div>\n\n                "
        "<!-- Apply ARIA attributes after the sidebar and the sidebar toggle button are added to the DOM -->\n                \n\n                "
    )
    
    # 直接删除精确字符串
    content = content.replace(unwanted_string, '')
    
    # 也尝试删除变体（href 路径可能不同）
    # 使用正则表达式匹配，允许 href 路径变化
    unwanted_pattern = (
        r'\n\s*\n\s*</div>\s*</div>\s*'
        r'<div[^>]*id=["\']body-container["\'][^>]*>\s*'
        r'<!-- Work around some values being stored in localStorage wrapped in quotes -->.*?'
        r'<!-- Set the theme before any content is loaded, prevents flash -->.*?'
        r'<input[^>]*type=["\']checkbox["\'][^>]*id=["\']sidebar-toggle-anchor["\'][^>]*class=["\']hidden["\'][^>]*>.*?'
        r'<!-- Hide / unhide sidebar before it is displayed -->.*?'
        r'<div[^>]*id=["\']page-wrapper["\'][^>]*class=["\']page-wrapper["\'][^>]*>.*?'
        r'<div[^>]*class=["\']page["\'][^>]*>.*?'
        r'<div[^>]*id=["\']menu-bar-hover-placeholder["\'][^>]*></div>.*?'
        r'<h1[^>]*class=["\']menu-title["\'][^>]*>openJiuwen Developer docs</h1>.*?'
        r'<div[^>]*class=["\']right-buttons["\'][^>]*>.*?</div>.*?'
        r'</div>.*?</div>.*?</form>.*?'
        r'<div[^>]*id=["\']searchresults-outer["\'][^>]*class=["\']searchresults-outer hidden["\'][^>]*>.*?'
        r'<div[^>]*id=["\']searchresults-header["\'][^>]*class=["\']searchresults-header["\'][^>]*></div>.*?'
        r'<ul[^>]*id=["\']searchresults["\'][^>]*>.*?</ul>.*?'
        r'</div>.*?</div>.*?'
        r'<!-- Apply ARIA attributes after the sidebar and the sidebar toggle button are added to the DOM -->.*?'
    )
    content = re.sub(unwanted_pattern, '', content, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
    
    # 清理多余的空白行
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    return content.strip()


@router.get("/doc-content")
def get_doc_content(
    version: str = Query(..., description="版本名称"),
    path: str = Query(..., description="文档路径"),
    db: Session = Depends(get_db)
):
    """
    获取文档内容（从数据库查询）
    """
    # 查询版本
    db_version = db.query(DocVersionModel).filter(
        DocVersionModel.version_name == version,
        DocVersionModel.status == "active"
    ).first()
    
    if not db_version:
        raise HTTPException(status_code=404, detail=f"版本 {version} 不存在")
    
    # 根据路径查找文档节点
    # 路径可能是完整路径（如 "AgentStudio/文档中心/提示词/0.快速入门.md"）或节点标题路径
    # 我们需要通过路径匹配找到对应的节点
    
    # 先尝试通过 file_path 精确匹配
    doc_node = db.query(DocNode).filter(
        DocNode.version_id == db_version.id,
        DocNode.file_path == path,
        DocNode.node_type == "doc",
        DocNode.is_active == True
    ).first()
    
    # 如果没找到，尝试通过路径构建查找
    if not doc_node:
        # 路径可能是 "AgentStudio/文档中心/模型介绍" 这样的格式
        # 需要找到对应的节点
        path_parts = [p for p in path.split('/') if p]  # 移除空字符串
        
        # 使用递归函数查找节点
        doc_node = find_node_by_path_recursive(db, db_version.id, path_parts, parent_id=None, index=0)
    
    # 如果还是没找到，尝试通过 file_path 的部分匹配（处理 URL 编码问题）
    if not doc_node:
        # 尝试解码后的路径匹配
        import urllib.parse
        decoded_path = urllib.parse.unquote(path)
        if decoded_path != path:
            doc_node = db.query(DocNode).filter(
                DocNode.version_id == db_version.id,
                DocNode.file_path == decoded_path,
                DocNode.node_type == "doc",
                DocNode.is_active == True
            ).first()
        
        # 如果还是没找到，尝试通过路径的最后一部分（文件名）匹配
        if not doc_node and path_parts:
            last_part = path_parts[-1]
            # 查找所有匹配的节点
            candidates = db.query(DocNode).filter(
                DocNode.version_id == db_version.id,
                DocNode.node_type == "doc",
                DocNode.is_active == True
            ).all()
            
            # 尝试通过标题和路径匹配
            for node in candidates:
                # 检查标题是否匹配
                if node.title == last_part:
                    # 检查路径是否匹配（通过父节点路径）
                    node_path_parts = []
                    current = node
                    while current:
                        node_path_parts.insert(0, current.title)
                        if current.parent_id:
                            current = next((n for n in candidates if n.id == current.parent_id), None)
                        else:
                            break
                    
                    # 比较路径
                    if len(node_path_parts) == len(path_parts):
                        if all(node_path_parts[i] == path_parts[i] for i in range(len(path_parts))):
                            doc_node = node
                            break
    
    if not doc_node:
        raise HTTPException(status_code=404, detail=f"文档不存在: {path}")
    
    if doc_node.node_type != "doc":
        raise HTTPException(status_code=400, detail="指定的路径不是文档节点")
    
    # 获取文档内容
    content = doc_node.content or ""
    
    # 判断文件类型（根据 file_path 或 content 特征）
    file_type = "markdown"
    if doc_node.file_path and doc_node.file_path.endswith('.html'):
        file_type = "html"
    elif content.strip().startswith('<') and '<html' in content.lower():
        file_type = "html"
    
    # 对于 HTML 内容，需要处理 CSS 和 JS 链接
    if file_type == "html":
        # 转换 HTML 中的相对路径为静态资源路径
        def replace_html_asset_path(match):
            tag = match.group(1)  # link 或 script
            attr = match.group(2)  # href 或 src
            quote = match.group(3)  # 引号
            path = match.group(4)  # 路径
            rest = match.group(5)  # 其余部分
            
            if not path:
                return match.group(0)
            
            # 如果是绝对路径或已经是静态资源路径，直接返回
            if path.startswith('http://') or path.startswith('https://') or path.startswith('/static_assets/'):
                return match.group(0)
            
            # 处理相对路径
            path = path.lstrip('./')
            while path.startswith('../'):
                path = path[3:]
            
            # 转换为静态资源路径
            new_path = f"/static_assets/develop_docs/{path}"
            return f'<{tag} {attr}={quote}{new_path}{quote}{rest}>'
        
        # 处理 link[rel="stylesheet"] 标签
        content = re.sub(
            r'<link([^>]*?)\s+href=(["\'])([^"\']+)\2([^>]*)>',
            replace_html_asset_path,
            content,
            flags=re.IGNORECASE
        )
        
        # 处理 script[src] 标签
        content = re.sub(
            r'<script([^>]*?)\s+src=(["\'])([^"\']+)\2([^>]*)>',
            replace_html_asset_path,
            content,
            flags=re.IGNORECASE
        )
    
    # 判断文档是否属于 AgentStudio（通过检查父节点路径）
    is_agentstudio_doc = False
    if doc_node:
        # 检查文档的父节点路径，看是否在 AgentStudio 目录下
        current_node = doc_node
        while current_node and current_node.parent_id:
            parent_node = db.query(DocNode).filter(DocNode.id == current_node.parent_id).first()
            if parent_node:
                if parent_node.title == "AgentStudio":
                    is_agentstudio_doc = True
                    break
                elif parent_node.title == "AgentCore":
                    is_agentstudio_doc = False
                    break
                current_node = parent_node
            else:
                break
        
        # 如果通过父节点无法判断，根据 file_path 判断
        if not is_agentstudio_doc and doc_node.file_path:
            # AgentStudio 的文档路径通常包含 "文档中心"
            if '文档中心' in doc_node.file_path:
                is_agentstudio_doc = True
    
    # 转换图片路径，传入文档类型信息
    content = convert_image_paths_in_content(content, doc_node.file_path, is_agentstudio_doc=is_agentstudio_doc)
    
    # 清理不需要的 HTML 片段（body-container、page-wrapper 等）
    content = clean_unwanted_html_fragments(content)
    
    # 增加浏览次数
    doc_node.view_count = (doc_node.view_count or 0) + 1
    db.commit()
    
    return {
        "version": version,
        "path": path,
        "content": content,
        "title": doc_node.title,
        "file_type": file_type
    }

