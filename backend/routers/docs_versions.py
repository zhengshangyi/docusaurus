"""
文档版本和目录结构相关 API 路由
从文档中心目录读取版本信息和文档列表
"""
import os
import re
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime

# 文档中心目录路径
DOCS_ROOT = "/opt/huawei/data/jiuwen/test-agentstudio/docs/文档中心"
# AgentCore 文档目录路径
AGENTCORE_DOCS_ROOT = "/opt/huawei/data/jiuwen/official_website/docusaurus/develop_docs_1118"
# 图片根目录路径
IMAGES_ROOT = "/opt/huawei/data/jiuwen/test-agentstudio/docs/images"

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


def get_doc_title_from_path(file_path: str) -> str:
    """从文件路径获取文档标题"""
    # 移除扩展名
    name = os.path.splitext(os.path.basename(file_path))[0]
    # 去掉末尾的"V1"或"v1"后缀
    if name.endswith('V1'):
        name = name[:-2]
    elif name.endswith('v1'):
        name = name[:-2]
    return name


def scan_docs_directory(docs_dir: str) -> List[DocItem]:
    """扫描文档目录，返回文档列表"""
    if not os.path.exists(docs_dir):
        return []
    
    result = []
    items = sorted(os.listdir(docs_dir), key=lambda x: (
        os.path.isdir(os.path.join(docs_dir, x)),
        x
    ))
    
    for item in items:
        item_path = os.path.join(docs_dir, item)
        relative_path = os.path.relpath(item_path, DOCS_ROOT)
        
        if os.path.isdir(item_path):
            # 递归扫描子目录
            children = scan_docs_directory(item_path)
            result.append(DocItem(
                title=get_doc_title_from_path(item),
                path=relative_path.replace("\\", "/"),
                type="directory",
                children=children if children else None
            ))
        elif item.endswith('.md'):
            # Markdown 文件
            result.append(DocItem(
                title=get_doc_title_from_path(item),
                path=relative_path.replace("\\", "/"),
                type="file"
            ))
    
    return result


def read_markdown_title(file_path: str) -> str:
    """读取 Markdown 文件的第一行标题（如果有）"""
    try:
        if not os.path.exists(file_path):
            return get_doc_title_from_path(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            # 如果第一行是 Markdown 标题（以 # 开头），提取标题文本
            if first_line.startswith('#'):
                title = first_line.lstrip('#').strip()
                if title:
                    return title
        return get_doc_title_from_path(file_path)
    except Exception:
        return get_doc_title_from_path(file_path)


def markdown_to_html(markdown_text: str) -> str:
    """将 Markdown 文本转换为 HTML（简单实现）"""
    html = markdown_text
    
    # 标题转换
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 粗体
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
    
    # 斜体
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
    
    # 代码块
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
    
    # 列表
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    
    html = re.sub(r'^\d+\. (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>)', r'<ol>\1</ol>', html, flags=re.DOTALL)
    
    # 段落
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<'):
            html_paragraphs.append(f'<p>{para}</p>')
        else:
            html_paragraphs.append(para)
    html = '\n\n'.join(html_paragraphs)
    
    # 换行
    html = html.replace('\n', '<br>')
    
    return html


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
def get_doc_versions():
    """
    获取文档版本列表
    目前只有一个版本：Agent Studio V1
    """
    from datetime import datetime
    today = datetime.now().strftime("%Y/%m/%d")
    
    versions = [
        DocVersion(
            name="openJiuwen V1.0",
            label="openJiuwen V1.0",
            release_date=today,
            type="openJiuwen"
        ),
    ]
    
    return DocVersionsResponse(
        versions=versions,
        current="openJiuwen V1.0"
    )


@router.get("/versions/{version_name}", response_model=DocVersionDetailResponse)
def get_doc_version_detail(version_name: str):
    """
    获取指定版本的文档详情
    整合 AgentStudio 和 AgentCore 两组文档
    """
    # 验证版本是否存在
    versions_response = get_doc_versions()
    version = next((v for v in versions_response.versions if v.name == version_name), None)
    
    if not version:
        raise HTTPException(status_code=404, detail=f"版本 {version_name} 不存在")
    
    # 扫描 AgentStudio 文档目录（现有文档）
    agentstudio_docs = scan_docs_directory_with_titles(DOCS_ROOT, DOCS_ROOT)
    
    # 扫描 AgentCore 文档目录（develop_docs_1118）
    agentcore_docs = scan_docs_directory_with_titles(AGENTCORE_DOCS_ROOT, AGENTCORE_DOCS_ROOT)
    
    # 包装 AgentStudio 文档，路径需要添加前缀以区分
    agentstudio_wrapped = []
    if agentstudio_docs:
        # 为 AgentStudio 的文档路径添加前缀
        def add_prefix_to_paths(items: List[DocItem], prefix: str) -> List[DocItem]:
            """为文档路径添加前缀"""
            result = []
            for item in items:
                new_path = f"{prefix}/{item.path}" if item.path else prefix
                if item.type == "directory" and item.children:
                    new_children = add_prefix_to_paths(item.children, prefix)
                    result.append(DocItem(
                        title=item.title,
                        path=new_path,
                        type=item.type,
                        children=new_children if new_children else None
                    ))
                else:
                    result.append(DocItem(
                        title=item.title,
                        path=new_path,
                        type=item.type,
                        children=None
                    ))
            return result
        
        agentstudio_docs_with_prefix = add_prefix_to_paths(agentstudio_docs, "AgentStudio")
        agentstudio_wrapped.append(DocItem(
            title="AgentStudio",
            path="AgentStudio",
            type="directory",
            children=agentstudio_docs_with_prefix
        ))
    
    # 包装 AgentCore 文档，路径需要添加前缀以区分
    agentcore_wrapped = []
    if agentcore_docs:
        agentcore_docs_with_prefix = add_prefix_to_paths(agentcore_docs, "AgentCore")
        agentcore_wrapped.append(DocItem(
            title="AgentCore",
            path="AgentCore",
            type="directory",
            children=agentcore_docs_with_prefix
        ))
    
    # 合并两组文档
    docs = agentstudio_wrapped + agentcore_wrapped
    
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
            
            # 提取文本内容，保留基本格式
            # 这里我们返回 HTML 内容，让前端处理
            content = str(main_content)
            # 转换图片路径
            if html_file_path:
                content = convert_html_image_paths(content, html_file_path)
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
                
                content = str(body)
                if html_file_path:
                    content = convert_html_image_paths(content, html_file_path)
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


@router.get("/doc-content")
def get_doc_content(version: str, path: str):
    """
    获取文档内容
    支持 Markdown 和 HTML 文件
    """
    # 判断是 AgentStudio 还是 AgentCore 的文档
    if path.startswith("AgentStudio/"):
        # AgentStudio 文档：从 DOCS_ROOT 读取
        relative_path = path[len("AgentStudio/"):]
        file_path = os.path.join(DOCS_ROOT, relative_path.lstrip('/'))
        abs_base_root = os.path.abspath(DOCS_ROOT)
    elif path.startswith("AgentCore/"):
        # AgentCore 文档：从 AGENTCORE_DOCS_ROOT 读取
        relative_path = path[len("AgentCore/"):]
        file_path = os.path.join(AGENTCORE_DOCS_ROOT, relative_path.lstrip('/'))
        abs_base_root = os.path.abspath(AGENTCORE_DOCS_ROOT)
    else:
        # 兼容旧路径格式（直接路径）
        file_path = os.path.join(DOCS_ROOT, path.lstrip('/'))
        abs_base_root = os.path.abspath(DOCS_ROOT)
    
    # 安全检查：确保文件在文档目录内
    abs_file_path = os.path.abspath(file_path)
    
    if not abs_file_path.startswith(abs_base_root):
        raise HTTPException(status_code=403, detail="无权访问该文件")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文档不存在")
    
    # 支持 Markdown 和 HTML 文件
    if not (file_path.endswith('.md') or file_path.endswith('.html')):
        raise HTTPException(status_code=400, detail="只能访问 Markdown 或 HTML 文件")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果是 Markdown 文件
        if file_path.endswith('.md'):
            # 转换图片路径为 API 路径
            content = convert_image_paths(content, file_path)
            title = read_markdown_title(file_path)
        else:
            # 如果是 HTML 文件，提取主要内容
            # 对于 HTML，我们可以：
            # 1. 直接返回 HTML（前端需要支持 HTML 渲染）
            # 2. 转换为 Markdown（需要 HTML 到 Markdown 的转换）
            # 这里我们尝试提取主要内容并转换为 Markdown
            html_content = extract_html_content(content, file_path)
            # 尝试转换为 Markdown，如果转换失败则返回 HTML
            try:
                content = html_to_markdown(html_content)
                # 如果转换后内容为空，使用原始 HTML
                if not content.strip():
                    content = html_content
            except:
                content = html_content
            
            # 从 HTML 中提取标题
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                title_tag = soup.find('title') or soup.find('h1')
                if title_tag:
                    title = title_tag.get_text().strip()
                else:
                    title = get_doc_title_from_path(file_path)
            except:
                title = get_doc_title_from_path(file_path)
        
        # 返回内容，前端需要根据文件类型决定如何渲染
        return {
            "version": version,
            "path": path,
            "content": content,
            "title": title,
            "file_type": "html" if file_path.endswith('.html') else "markdown"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取文件失败: {str(e)}")

