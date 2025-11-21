#!/usr/bin/env python3
"""
文档数据导入脚本
导入 AgentStudio MD 文档和 develop_docs HTML 文档到 openJiuwen V1 版本
"""

import os
import re
import json
import shutil
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from html.parser import HTMLParser
from html import unescape

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import DocVersion, DocNode, DocCategoryConfig, Base

# 项目路径
PROJECT_ROOT = Path("/opt/huawei/data/jiuwen/official_website/docusaurus")
STATIC_ASSETS_DIR = PROJECT_ROOT / "static_assets"
AGENTSTUDIO_ASSETS_DIR = STATIC_ASSETS_DIR / "agentstudio"
DEVELOP_DOCS_ASSETS_DIR = STATIC_ASSETS_DIR / "develop_docs"

# 数据源路径
AGENTSTUDIO_DOCS_DIR = Path("/opt/huawei/data/jiuwen/test-agentstudio/docs")
DEVELOP_DOCS_DIR = Path("/opt/huawei/data/jiuwen/official_website/docusaurus/develop_docs_1118")

# 版本信息
VERSION_NAME = "openJiuwen V1"
VERSION_LABEL = "openJiuwen V1"


class HTMLContentExtractor(HTMLParser):
    """HTML 内容提取器，提取 body 中的文本内容"""
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.content_parts = []
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
        self.current_tag = tag
        
    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
        self.current_tag = None
        
    def handle_data(self, data):
        if self.in_body and self.current_tag not in ['script', 'style']:
            cleaned = data.strip()
            if cleaned:
                self.content_parts.append(cleaned)
    
    def get_content(self) -> str:
        """获取提取的文本内容"""
        return '\n\n'.join(self.content_parts)


def extract_html_content(html_file: Path) -> str:
    """从 HTML 文件中提取主要内容，保留 HTML 标签"""
    import re
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 使用 BeautifulSoup 提取主要内容
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 查找主要内容区域 - 只提取 <main> 标签内的内容
            # 先尝试在 body-container 内查找 main
            body_container = soup.find(id='body-container')
            if body_container:
                main_content = body_container.find('main')
            else:
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
                
                # 移除所有 style 标签（但保留 link 标签引用外部 CSS）
                for style in main_content.find_all('style'):
                    style.decompose()
                
                # 移除包含不需要文本的元素
                # 查找所有包含 "Keyboard shortcuts"、"Press" 等文本的元素
                for element in main_content.find_all(text=True):
                    parent = element.parent
                    if parent and any(unwanted in element for unwanted in [
                        "Keyboard shortcuts", "Press ←", "Press →", "Press S", "Press /",
                        "Press ?", "Press Esc", "Auto Light Rust Coal Navy Ayu",
                        "openJiuwen Developer docs"
                    ]):
                        # 如果父元素只包含这个文本，移除整个元素
                        if parent.get_text(strip=True) == element.strip():
                            parent.decompose()
                        else:
                            # 否则只移除文本节点
                            element.extract()
                
                # 移除 menu-title（包含 "openJiuwen Developer docs" 的标题）
                for menu_title in main_content.find_all(class_='menu-title'):
                    menu_title.decompose()
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
                
                # 返回 HTML 内容（保留标签）
                # 确保只返回 main 标签内的内容，不包含任何外层容器
                # main_content 已经是 main 标签本身，直接转换为字符串即可
                html_str = str(main_content)
                
                # 使用正则表达式移除其他不需要的元素（双重保险）
                # 移除 body-container
                html_str = re.sub(r'<div[^>]*id=["\']body-container["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                html_str = re.sub(r'^.*?<div[^>]*id=["\']body-container["\'][^>]*>', '', html_str, flags=re.IGNORECASE | re.DOTALL)
                # 移除 sidebar-toggle-anchor
                html_str = re.sub(r'<input[^>]*id=["\']sidebar-toggle-anchor["\'][^>]*>', '', html_str, flags=re.IGNORECASE)
                # 移除 page-wrapper
                html_str = re.sub(r'<div[^>]*id=["\']page-wrapper["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                html_str = re.sub(r'<div[^>]*class=["\'][^"\']*page-wrapper[^"\']*["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                # 移除 page div
                html_str = re.sub(r'<div[^>]*class=["\']page["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                # 移除 menu-title
                html_str = re.sub(r'<h1[^>]*class=["\']menu-title["\'][^>]*>.*?</h1>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                html_str = re.sub(r'<[^>]*class=["\']menu-title["\'][^>]*>.*?</[^>]*>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                # 移除 menu-bar-hover-placeholder
                html_str = re.sub(r'<div[^>]*id=["\']menu-bar-hover-placeholder["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                # 移除 right-buttons
                html_str = re.sub(r'<div[^>]*class=["\']right-buttons["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                # 移除 searchresults-outer
                html_str = re.sub(r'<div[^>]*id=["\']searchresults-outer["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                html_str = re.sub(r'<div[^>]*class=["\']searchresults-outer[^"\']*["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                # 移除 searchresults-header
                html_str = re.sub(r'<div[^>]*id=["\']searchresults-header["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                html_str = re.sub(r'<div[^>]*class=["\']searchresults-header["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                # 移除 searchresults
                html_str = re.sub(r'<ul[^>]*id=["\']searchresults["\'][^>]*>.*?</ul>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                
                # 再次清理：移除残留的不需要文本
                unwanted_patterns = [
                    r'Keyboard shortcuts[^<]*',
                    r'Press [←→S/?Esc][^<]*',
                    r'Auto Light Rust Coal Navy Ayu[^<]*',
                    r'openJiuwen Developer docs[^<]*'
                ]
                for pattern in unwanted_patterns:
                    html_str = re.sub(pattern, '', html_str, flags=re.IGNORECASE)
                
                # 移除包含 "openJiuwen Developer docs" 的整个标签及其内容
                html_str = re.sub(r'<[^>]*>.*?openJiuwen Developer docs.*?</[^>]*>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                # 移除包含 "openJiuwen Developer docs" 的标签（自闭合标签）
                html_str = re.sub(r'<[^>]*openJiuwen Developer docs[^>]*>', '', html_str, flags=re.IGNORECASE)
                # 移除纯文本中的 "openJiuwen Developer docs" 及其前面的内容（如果是在标题或链接中）
                html_str = re.sub(r'<[^>]*>.*?openJiuwen Developer docs.*?</[^>]*>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                
                return html_str
            else:
                # 如果没有找到 main 标签，尝试从 body-container 或 body 中提取
                # 优先从 body-container 中提取内容（不包含 body-container 本身）
                # 注意：这里 body_container 可能已经在上面查找过了，但为了代码清晰，重新查找
                if 'body_container' not in locals():
                    body_container = soup.find(id='body-container')
                else:
                    body_container = soup.find(id='body-container')
                if body_container:
                    # 从 body-container 内提取内容，但不包含 body-container 标签本身
                    # 查找 page-wrapper 或 content 区域
                    page_wrapper = body_container.find(id='page-wrapper') or body_container.find(class_='page-wrapper')
                    if page_wrapper:
                        content_div = page_wrapper.find(id='content') or page_wrapper.find(class_='content')
                        if content_div:
                            # 移除不需要的元素
                            for help_container in content_div.find_all(id='mdbook-help-container'):
                                help_container.decompose()
                            for menu_bar in content_div.find_all(class_='menu-bar'):
                                menu_bar.decompose()
                            for sidebar in content_div.find_all(id='sidebar'):
                                sidebar.decompose()
                            for search_wrapper in content_div.find_all(id='search-wrapper'):
                                search_wrapper.decompose()
                            for nav_wrapper in content_div.find_all(class_='nav-wrapper'):
                                nav_wrapper.decompose()
                            for nav_wide in content_div.find_all(class_='nav-wide-wrapper'):
                                nav_wide.decompose()
                            for script in content_div.find_all('script'):
                                script.decompose()
                            for style in content_div.find_all('style'):
                                style.decompose()
                            
                            # 移除包含不需要文本的元素
                            for element in content_div.find_all(text=True):
                                parent = element.parent
                                if parent and any(unwanted in element for unwanted in [
                                    "Keyboard shortcuts", "Press ←", "Press →", "Press S", "Press /",
                                    "Press ?", "Press Esc", "Auto Light Rust Coal Navy Ayu",
                                    "openJiuwen Developer docs"
                                ]):
                                    if parent.get_text(strip=True) == element.strip():
                                        parent.decompose()
                                    else:
                                        element.extract()
                            
                            # 移除 menu-title
                            for menu_title in content_div.find_all(class_='menu-title'):
                                menu_title.decompose()
                            for h1 in content_div.find_all('h1', class_='menu-title'):
                                h1.decompose()
                            
                            # 移除 sidebar-toggle-anchor
                            for sidebar_toggle in content_div.find_all(id='sidebar-toggle-anchor'):
                                sidebar_toggle.decompose()
                            
                            # 移除 page-wrapper
                            for page_wrapper in content_div.find_all(id='page-wrapper'):
                                page_wrapper.decompose()
                            for page_wrapper in content_div.find_all(class_='page-wrapper'):
                                page_wrapper.decompose()
                            
                            # 移除 page div
                            for page_div in content_div.find_all(class_='page'):
                                page_div.decompose()
                            
                            # 移除 body-container
                            for body_container in content_div.find_all(id='body-container'):
                                body_container.decompose()
                            
                            # 移除 menu-bar-hover-placeholder
                            for placeholder in content_div.find_all(id='menu-bar-hover-placeholder'):
                                placeholder.decompose()
                            
                            # 移除 right-buttons
                            for right_buttons in content_div.find_all(class_='right-buttons'):
                                right_buttons.decompose()
                            
                            # 移除 searchresults-outer
                            for searchresults in content_div.find_all(id='searchresults-outer'):
                                searchresults.decompose()
                            for searchresults in content_div.find_all(class_='searchresults-outer'):
                                searchresults.decompose()
                            
                            # 移除 searchresults-header
                            for searchresults_header in content_div.find_all(id='searchresults-header'):
                                searchresults_header.decompose()
                            for searchresults_header in content_div.find_all(class_='searchresults-header'):
                                searchresults_header.decompose()
                            
                            # 移除 searchresults
                            for searchresults in content_div.find_all(id='searchresults'):
                                searchresults.decompose()
                            
                            # 只提取 main 标签内的内容，不包含 content_div 本身
                            main_in_content = content_div.find('main')
                            if main_in_content:
                                html_str = str(main_in_content)
                            else:
                                html_str = str(content_div)
                            
                            # 使用正则表达式移除其他不需要的元素（双重保险）
                            # 移除 body-container
                            html_str = re.sub(r'<div[^>]*id=["\']body-container["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            html_str = re.sub(r'^.*?<div[^>]*id=["\']body-container["\'][^>]*>', '', html_str, flags=re.IGNORECASE | re.DOTALL)
                            # 移除 sidebar-toggle-anchor
                            html_str = re.sub(r'<input[^>]*id=["\']sidebar-toggle-anchor["\'][^>]*>', '', html_str, flags=re.IGNORECASE)
                            # 移除 page-wrapper
                            html_str = re.sub(r'<div[^>]*id=["\']page-wrapper["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            html_str = re.sub(r'<div[^>]*class=["\'][^"\']*page-wrapper[^"\']*["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            # 移除 page div
                            html_str = re.sub(r'<div[^>]*class=["\']page["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            # 移除 menu-title
                            html_str = re.sub(r'<h1[^>]*class=["\']menu-title["\'][^>]*>.*?</h1>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            html_str = re.sub(r'<[^>]*class=["\']menu-title["\'][^>]*>.*?</[^>]*>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            # 移除 menu-bar-hover-placeholder
                            html_str = re.sub(r'<div[^>]*id=["\']menu-bar-hover-placeholder["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            # 移除 right-buttons
                            html_str = re.sub(r'<div[^>]*class=["\']right-buttons["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            # 移除 searchresults-outer
                            html_str = re.sub(r'<div[^>]*id=["\']searchresults-outer["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            html_str = re.sub(r'<div[^>]*class=["\']searchresults-outer[^"\']*["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            # 移除 searchresults-header
                            html_str = re.sub(r'<div[^>]*id=["\']searchresults-header["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            html_str = re.sub(r'<div[^>]*class=["\']searchresults-header["\'][^>]*>.*?</div>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            # 移除 searchresults
                            html_str = re.sub(r'<ul[^>]*id=["\']searchresults["\'][^>]*>.*?</ul>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            
                            # 再次清理
                            unwanted_patterns = [
                                r'Keyboard shortcuts[^<]*',
                                r'Press [←→S/?Esc][^<]*',
                                r'Auto Light Rust Coal Navy Ayu[^<]*',
                                r'openJiuwen Developer docs[^<]*'
                            ]
                            for pattern in unwanted_patterns:
                                html_str = re.sub(pattern, '', html_str, flags=re.IGNORECASE)
                            
                            # 移除包含 "openJiuwen Developer docs" 的整个标签及其内容
                            html_str = re.sub(r'<[^>]*>.*?openJiuwen Developer docs.*?</[^>]*>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                            html_str = re.sub(r'<[^>]*openJiuwen Developer docs[^>]*>', '', html_str, flags=re.IGNORECASE)
                            
                            return html_str
                        else:
                            # 如果没有 content，直接使用 page-wrapper 的内容
                            for script in page_wrapper.find_all('script'):
                                script.decompose()
                            for style in page_wrapper.find_all('style'):
                                style.decompose()
                            html_str = str(page_wrapper)
                            # 确保不包含 body-container
                            html_str = re.sub(r'<div[^>]*id=["\']body-container["\'][^>]*>', '', html_str, flags=re.IGNORECASE)
                            html_str = re.sub(r'^.*?<div[^>]*id=["\']body-container["\'][^>]*>', '', html_str, flags=re.IGNORECASE | re.DOTALL)
                            return html_str
                    else:
                        # 如果没有 page-wrapper，直接使用 body-container 的内容（但不包含 body-container 标签）
                        for script in body_container.find_all('script'):
                            script.decompose()
                        for style in body_container.find_all('style'):
                            style.decompose()
                        # 查找 main 标签
                        main_in_body = body_container.find('main')
                        if main_in_body:
                            for script in main_in_body.find_all('script'):
                                script.decompose()
                            for style in main_in_body.find_all('style'):
                                style.decompose()
                            return str(main_in_body)
                        else:
                            # 获取 body-container 内的所有子元素（但不包含 body-container 标签本身）
                            inner_html = ''.join(str(child) for child in body_container.children)
                            # 确保不包含 body-container
                            inner_html = re.sub(r'<div[^>]*id=["\']body-container["\'][^>]*>', '', inner_html, flags=re.IGNORECASE)
                            return inner_html
                
                # 如果都没有，尝试从 body 中提取（最后备选）
                body = soup.find('body')
                if body:
                    # 移除 body-container 本身，查找 main 标签
                    for body_container in body.find_all(id='body-container'):
                        # 优先查找 main 标签
                        main_in_container = body_container.find('main')
                        if main_in_container:
                            for script in main_in_container.find_all('script'):
                                script.decompose()
                            for style in main_in_container.find_all('style'):
                                style.decompose()
                            return str(main_in_container)
                        # 如果没有 main，查找 content
                        inner_content = body_container.find(id='content') or body_container.find(class_='content')
                        if inner_content:
                            main_in_content = inner_content.find('main')
                            if main_in_content:
                                for script in main_in_content.find_all('script'):
                                    script.decompose()
                                for style in main_in_content.find_all('style'):
                                    style.decompose()
                                return str(main_in_content)
                            for script in inner_content.find_all('script'):
                                script.decompose()
                            for style in inner_content.find_all('style'):
                                style.decompose()
                            return str(inner_content)
                    
                    # 如果 body-container 内没有找到内容，移除不需要的元素
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
                    for body_container in body.find_all(id='body-container'):
                        body_container.decompose()  # 移除 body-container
                    for script in body.find_all('script'):
                        script.decompose()
                    for style in body.find_all('style'):
                        style.decompose()
                    
                    # 移除包含不需要文本的元素
                    for element in body.find_all(text=True):
                        parent = element.parent
                        if parent and any(unwanted in element for unwanted in [
                            "Keyboard shortcuts", "Press ←", "Press →", "Press S", "Press /",
                            "Press ?", "Press Esc", "Auto Light Rust Coal Navy Ayu",
                            "openJiuwen Developer docs"
                        ]):
                            if parent.get_text(strip=True) == element.strip():
                                parent.decompose()
                            else:
                                element.extract()
                    
                    html_str = str(body)
                    # 再次清理
                    unwanted_patterns = [
                        r'Keyboard shortcuts[^<]*',
                        r'Press [←→S/?Esc][^<]*',
                        r'Auto Light Rust Coal Navy Ayu[^<]*',
                        r'openJiuwen Developer docs[^<]*'
                    ]
                    for pattern in unwanted_patterns:
                        html_str = re.sub(pattern, '', html_str, flags=re.IGNORECASE)
                    
                    # 移除包含 "openJiuwen Developer docs" 的整个标签及其内容
                    html_str = re.sub(r'<[^>]*>.*?openJiuwen Developer docs.*?</[^>]*>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
                    html_str = re.sub(r'<[^>]*openJiuwen Developer docs[^>]*>', '', html_str, flags=re.IGNORECASE)
                    
                    return html_str
                
                return ""
        except ImportError:
            # 如果没有 BeautifulSoup，使用正则表达式提取
            # 提取 body 内容
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.IGNORECASE | re.DOTALL)
            if body_match:
                body_content = body_match.group(1)
                # 移除不需要的元素（使用正则表达式）
                body_content = re.sub(r'<div[^>]*id=["\']mdbook-help-container["\'][^>]*>.*?</div>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                body_content = re.sub(r'<div[^>]*class=["\'][^"\']*menu-bar[^"\']*["\'][^>]*>.*?</div>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                body_content = re.sub(r'<nav[^>]*id=["\']sidebar["\'][^>]*>.*?</nav>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                body_content = re.sub(r'<div[^>]*id=["\']search-wrapper["\'][^>]*>.*?</div>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                body_content = re.sub(r'<nav[^>]*class=["\'][^"\']*nav-wrapper[^"\']*["\'][^>]*>.*?</nav>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                body_content = re.sub(r'<nav[^>]*class=["\'][^"\']*nav-wide-wrapper[^"\']*["\'][^>]*>.*?</nav>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                # 移除 script 标签
                body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                # 移除 style 标签
                body_content = re.sub(r'<style[^>]*>.*?</style>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                return body_content
            return ""
    except Exception as e:
        print(f"  警告: 提取 HTML 内容失败 {html_file}: {e}")
        return ""


def extract_html_title(html_file: Path) -> str:
    """从 HTML 文件中提取标题"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 提取 title 标签
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
            # 移除 " - openJiuwen Developer docs" 等后缀
            title = re.sub(r'\s*-\s*openJiuwen.*$', '', title)
            return title
        
        # 如果没有 title 标签，尝试提取 h1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1))
            return unescape(h1_text).strip()
        
        return html_file.stem
    except Exception as e:
        print(f"  警告: 提取 HTML 标题失败 {html_file}: {e}")
        return html_file.stem


def parse_markdown_frontmatter(content: str) -> Tuple[Dict, str]:
    """解析 Markdown 文件的 frontmatter"""
    frontmatter = {}
    content_without_frontmatter = content
    
    # 检查是否有 frontmatter（以 --- 开头）
    if content.strip().startswith("---"):
        # 查找第二个 ---
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_str = parts[1].strip()
            content_without_frontmatter = parts[2].strip()
            
            try:
                frontmatter = yaml.safe_load(frontmatter_str) or {}
            except yaml.YAMLError as e:
                print(f"  警告: 解析 frontmatter 失败: {e}")
                frontmatter = {}
    
    return frontmatter, content_without_frontmatter


def extract_markdown_title(content: str, frontmatter: Dict, file_path: Path = None) -> str:
    """从 Markdown 内容中提取标题"""
    # 优先使用 frontmatter 中的 title
    if 'title' in frontmatter:
        return frontmatter['title']
    
    # 从内容中提取第一个 # 标题
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            title = line[2:].strip()
            # 如果标题是"节点说明"这种通用标题，尝试从文件名提取更具体的名称
            if title == "节点说明" and file_path:
                # 从文件名提取，例如 "代码节点V1.md" -> "代码节点"
                file_name = file_path.stem
                # 去掉末尾的 V1、v1 等版本后缀
                file_name = re.sub(r'[Vv]\d+$', '', file_name)
                if file_name and file_name != "节点说明":
                    return file_name
            return title
        elif line.startswith('## '):
            title = line[3:].strip()
            # 同样处理"节点说明"
            if title == "节点说明" and file_path:
                file_name = file_path.stem
                file_name = re.sub(r'[Vv]\d+$', '', file_name)
                if file_name and file_name != "节点说明":
                    return file_name
            return title
    
    # 如果都没有，尝试从文件名提取
    if file_path:
        file_name = file_path.stem
        # 去掉末尾的 V1、v1 等版本后缀
        file_name = re.sub(r'[Vv]\d+$', '', file_name)
        if file_name:
            return file_name
    
    return "未命名文档"


def copy_static_assets(source_dir: Path, target_dir: Path, file_extensions: List[str] = None):
    """复制静态资源文件"""
    if not source_dir.exists():
        return
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    if file_extensions is None:
        file_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.css', '.js', '.woff', '.woff2', '.ttf', '.eot']
    
    copied_count = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            if any(file_path.suffix.lower() in ext for ext in file_extensions):
                # 保持相对路径结构
                rel_path = file_path.relative_to(source_dir)
                target_path = target_dir / rel_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.copy2(file_path, target_path)
                    copied_count += 1
                except Exception as e:
                    print(f"  警告: 复制文件失败 {file_path} -> {target_path}: {e}")
    
    if copied_count > 0:
        print(f"  ✓ 复制了 {copied_count} 个静态资源文件到 {target_dir}")


def clear_all_data(db: Session):
    """清空所有文档相关数据"""
    print("清空所有文档数据...")
    
    # 删除所有节点（会级联删除关联的配置和资源）
    deleted_nodes = db.query(DocNode).delete()
    print(f"  删除 {deleted_nodes} 个文档节点")
    
    # 删除所有版本
    deleted_versions = db.query(DocVersion).delete()
    print(f"  删除 {deleted_versions} 个版本")
    
    db.commit()
    print("✓ 数据清空完成")


def create_version(db: Session) -> DocVersion:
    """创建或获取版本"""
    version = db.query(DocVersion).filter(DocVersion.version_name == VERSION_NAME).first()
    
    if not version:
        version = DocVersion(
            version_name=VERSION_NAME,
            label=VERSION_LABEL,
            is_current=True,
            is_latest=True,
            status="active"
        )
        db.add(version)
        db.commit()
        db.refresh(version)
        print(f"✓ 创建版本: {VERSION_NAME}")
    else:
        print(f"✓ 版本已存在: {VERSION_NAME}")
    
    return version


def create_category_node(db: Session, version: DocVersion, title: str, parent_id: Optional[int] = None, order: int = 0) -> DocNode:
    """创建目录节点"""
    node = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.node_type == "category",
        DocNode.title == title,
        DocNode.parent_id == parent_id
    ).first()
    
    if not node:
        node = DocNode(
            version_id=version.id,
            parent_id=parent_id,
            node_type="category",
            title=title,
            order=order
        )
        db.add(node)
        db.commit()
        db.refresh(node)
        print(f"  + 创建目录: {title}")
    
    return node


def import_markdown_file(
    db: Session,
    version: DocVersion,
    file_path: Path,
    base_dir: Path,
    parent_id: Optional[int] = None,
    order: int = 0
) -> Optional[DocNode]:
    """导入 Markdown 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, content_body = parse_markdown_frontmatter(content)
        title = extract_markdown_title(content_body, frontmatter, file_path)
        
        # 生成 slug
        rel_path = file_path.relative_to(base_dir)
        slug = str(rel_path).replace('.md', '').replace('.MD', '')
        if slug.endswith('/index'):
            slug = slug[:-6]
        
        # 创建或更新节点
        node = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.file_path == str(rel_path)
        ).first()
        
        if node:
            node.title = title
            node.slug = slug
            node.content = content_body
            node.frontmatter = frontmatter
            node.description = frontmatter.get('description', '')
            node.order = order
            node.parent_id = parent_id
            print(f"  更新文档: {rel_path}")
        else:
            node = DocNode(
                version_id=version.id,
                parent_id=parent_id,
                node_type="doc",
                title=title,
                slug=slug,
                file_path=str(rel_path),
                content=content_body,
                frontmatter=frontmatter,
                description=frontmatter.get('description', ''),
                order=order
            )
            db.add(node)
            print(f"  + 导入文档: {rel_path}")
        
        db.commit()
        db.refresh(node)
        return node
        
    except Exception as e:
        print(f"  ✗ 导入文档失败 {file_path}: {e}")
        db.rollback()
        return None


def import_html_file(
    db: Session,
    version: DocVersion,
    file_path: Path,
    base_dir: Path,
    parent_id: Optional[int] = None,
    order: int = 0
) -> Optional[DocNode]:
    """导入 HTML 文件"""
    try:
        title = extract_html_title(file_path)
        content = extract_html_content(file_path)
        
        # 生成 slug
        rel_path = file_path.relative_to(base_dir)
        slug = str(rel_path).replace('.html', '').replace('.HTML', '')
        if slug == 'index':
            slug = ''
        
        # 创建或更新节点
        node = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.file_path == str(rel_path)
        ).first()
        
        if node:
            node.title = title
            node.slug = slug
            node.content = content
            node.order = order
            node.parent_id = parent_id
            print(f"  更新文档: {rel_path}")
        else:
            node = DocNode(
                version_id=version.id,
                parent_id=parent_id,
                node_type="doc",
                title=title,
                slug=slug,
                file_path=str(rel_path),
                content=content,
                order=order
            )
            db.add(node)
            print(f"  + 导入文档: {rel_path}")
        
        db.commit()
        db.refresh(node)
        return node
        
    except Exception as e:
        print(f"  ✗ 导入文档失败 {file_path}: {e}")
        db.rollback()
        return None


def scan_markdown_directory(
    db: Session,
    version: DocVersion,
    directory: Path,
    base_dir: Path,
    parent_id: Optional[int] = None,
    only_docs_center: bool = False,
    skip_docs_center: bool = False
):
    """递归扫描 Markdown 目录"""
    if not directory.exists() or not directory.is_dir():
        return
    
    items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
    
    order = 0
    for item in items:
        if item.name.startswith('.'):
            continue
        
        # 如果只扫描文档中心，跳过其他目录
        if only_docs_center and item.name != "文档中心":
            continue
        
        # 如果跳过文档中心层，直接处理文档中心下的内容
        if skip_docs_center and item.name == "文档中心" and item.is_dir():
            # 不创建"文档中心"节点，直接递归处理其子目录和文件
            scan_markdown_directory(db, version, item, base_dir, parent_id, only_docs_center=False, skip_docs_center=False)
            continue
        
        if item.is_dir():
            # 创建目录节点
            category_node = create_category_node(db, version, item.name, parent_id, order)
            # 递归处理子目录
            scan_markdown_directory(db, version, item, base_dir, category_node.id, only_docs_center=False, skip_docs_center=False)
            order += 1
        elif item.suffix.lower() in ['.md', '.markdown']:
            # 处理 Markdown 文件
            import_markdown_file(db, version, item, base_dir, parent_id, order)
            order += 1


def scan_html_directory(
    db: Session,
    version: DocVersion,
    directory: Path,
    base_dir: Path,
    parent_id: Optional[int] = None,
    level: int = 0
):
    """递归扫描 HTML 目录"""
    if not directory.exists() or not directory.is_dir():
        return
    
    items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
    
    # 收集目录和文件，用于去重（同一层级下同名文件夹和文件，只保留文件夹）
    dirs_dict = {}
    files_dict = {}
    
    for item in items:
        # 跳过静态资源目录和文件
        if item.name in ['css', 'js', 'images', 'fonts', 'FontAwesome', 'highlight.js', 'highlight.css', 
                         'tomorrow-night.css', 'ayu-highlight.css', 'book.js', 'clipboard.min.js',
                         'elasticlunr.min.js', 'searcher.js', 'searchindex.js', 'toc.js', 'toc.html',
                         'favicon.png', 'favicon.svg', '404.html', 'print.html', 'SECURITY.html']:
            continue
        
        if item.is_dir():
            # 获取目录名（去掉扩展名）用于去重
            dir_name = item.stem if item.suffix else item.name
            dirs_dict[dir_name] = item
        elif item.suffix.lower() == '.html':
            # 获取文件名（去掉扩展名）用于去重
            file_name = item.stem
            files_dict[file_name] = item
    
    # 处理去重：如果同一层级下有同名的文件夹和文件，只保留文件夹
    items_to_process = []
    processed_names = set()
    
    # 先处理目录
    for dir_name, dir_item in dirs_dict.items():
        items_to_process.append(('dir', dir_item))
        processed_names.add(dir_name)
    
    # 再处理文件（跳过与目录同名的文件）
    for file_name, file_item in files_dict.items():
        if file_name not in processed_names:
            items_to_process.append(('file', file_item))
    
    # 按名称排序
    items_to_process.sort(key=lambda x: x[1].name)
    
    order = 0
    for item_type, item in items_to_process:
        if item_type == 'dir':
            # 创建目录节点
            category_node = create_category_node(db, version, item.name, parent_id, order)
            # 递归处理子目录
            scan_html_directory(db, version, item, base_dir, category_node.id, level + 1)
            order += 1
        else:
            # 处理 HTML 文件
            import_html_file(db, version, item, base_dir, parent_id, order)
            order += 1


def reorganize_agentstudio_order(db: Session, version: DocVersion):
    """重新组织 AgentStudio 文档的顺序（已去掉文档中心层）"""
    print("\n重新组织 AgentStudio 文档顺序...")
    
    # 找到 AgentStudio 目录
    agentstudio = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.title == "AgentStudio",
        DocNode.parent_id == None
    ).first()
    
    if not agentstudio:
        print("  ✗ 未找到 AgentStudio 目录")
        return
    
    # 获取 AgentStudio 下的所有节点（不再有文档中心层）
    nodes = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.parent_id == agentstudio.id
    ).all()
    
    # 定义顺序规则
    order_map = {
        "AgentStudio - 智能Agent开发平台": 1,
        "Test-AgentStudio 插件使用指南": 2,  # 放在 AgentStudio - 智能Agent开发平台 下面
        "开发智能体": 3,
        "模型介绍": 4,
    }
    
    # 找到"提示词"目录，放在最后
    prompt_category = None
    other_nodes = []
    ordered_nodes = []
    
    for node in nodes:
        if node.title == "提示词" and node.node_type == "category":
            prompt_category = node
        elif node.title in order_map:
            ordered_nodes.append((order_map[node.title], node))
        else:
            other_nodes.append(node)
    
    # 排序其他节点（按当前 order）
    other_nodes.sort(key=lambda x: (x.order, x.id))
    
    # 设置顺序
    current_order = 1
    
    # 1. 先设置固定顺序的节点
    ordered_nodes.sort(key=lambda x: x[0])
    for _, node in ordered_nodes:
        node.order = current_order
        db.commit()
        print(f"  ✓ {node.title} -> order={current_order}")
        current_order += 1
    
    # 2. 然后设置其他节点
    for node in other_nodes:
        if node.title != "提示词" or node.node_type != "category":
            node.order = current_order
            db.commit()
            print(f"  ✓ {node.title} -> order={current_order}")
            current_order += 1
    
    # 3. 最后设置"提示词"目录
    if prompt_category:
        prompt_category.order = current_order
        db.commit()
        print(f"  ✓ {prompt_category.title} -> order={current_order} (最后)")
        
        # 处理"提示词"目录下的文档顺序
        prompt_nodes = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.parent_id == prompt_category.id
        ).all()
        
        # 定义提示词目录下的顺序
        prompt_order_map = {
            "提示词管理快速入门": 1,
            "管理提示词版本": 2,  # 放在提示词管理快速入门下面
        }
        
        prompt_ordered = []
        prompt_others = []
        for node in prompt_nodes:
            if node.title in prompt_order_map:
                prompt_ordered.append((prompt_order_map[node.title], node))
            else:
                prompt_others.append(node)
        
        # 排序其他节点
        prompt_others.sort(key=lambda x: (x.order, x.id))
        
        prompt_current_order = 1
        # 设置固定顺序的节点
        prompt_ordered.sort(key=lambda x: x[0])
        for _, node in prompt_ordered:
            node.order = prompt_current_order
            db.commit()
            print(f"    ✓ 提示词/{node.title} -> order={prompt_current_order}")
            prompt_current_order += 1
        
        # 设置其他节点
        for node in prompt_others:
            node.order = prompt_current_order
            db.commit()
            print(f"    ✓ 提示词/{node.title} -> order={prompt_current_order}")
            prompt_current_order += 1
    
    print("  ✓ AgentStudio 文档顺序调整完成")


def reorganize_agentcore_order(db: Session, version: DocVersion):
    """重新组织 AgentCore 的顺序"""
    print("\n重新组织 AgentCore 文档顺序...")
    
    # 找到 AgentCore 目录
    agentcore = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.title == "AgentCore",
        DocNode.parent_id == None
    ).first()
    
    if not agentcore:
        print("  ✗ 未找到 AgentCore 目录")
        return
    
    # 获取 AgentCore 一级目录下的所有节点
    nodes = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.parent_id == agentcore.id
    ).all()
    
    # 处理重复的"产品简介"（只保留一个）
    product_intro_nodes = [n for n in nodes if n.title == "产品简介"]
    if len(product_intro_nodes) > 1:
        # 保留第一个，删除其他的
        for node in product_intro_nodes[1:]:
            print(f"  删除重复的节点: {node.title} (ID: {node.id}, file_path: {node.file_path})")
            db.delete(node)
        db.commit()
        # 重新查询节点
        nodes = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.parent_id == agentcore.id
        ).all()
    
    # 定义一级目录顺序
    top_level_order = {
        "产品简介": 1,
        "产品规格与约束": 2,
        "产品规格和约束": 2,  # 兼容不同的命名
        "开发指南": 3,
        "教程": 4,
    }
    
    # 设置一级目录顺序
    for node in nodes:
        title_key = node.title
        if title_key in top_level_order:
            node.order = top_level_order[title_key]
            db.commit()
            print(f"  ✓ {node.title} -> order={node.order}")
    
    # 处理开发指南内部的顺序
    dev_guide = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.title == "开发指南",
        DocNode.parent_id == agentcore.id
    ).first()
    
    if dev_guide:
        dev_guide_nodes = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.parent_id == dev_guide.id
        ).all()
        
        dev_guide_order = {
            "基础功能": 1,
            "高阶用法": 2,
            "工作流": 3,
            "Agent": 4,
            "agent": 4,  # 兼容小写
        }
        
        for node in dev_guide_nodes:
            title_key = node.title
            if title_key in dev_guide_order:
                node.order = dev_guide_order[title_key]
                db.commit()
                print(f"    ✓ 开发指南/{node.title} -> order={node.order}")
        
        # 处理"高阶用法/Runtime"目录下的顺序
        advanced_usage = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.title == "高阶用法",
            DocNode.parent_id == dev_guide.id
        ).first()
        
        if advanced_usage:
            runtime = db.query(DocNode).filter(
                DocNode.version_id == version.id,
                DocNode.title == "Runtime",
                DocNode.parent_id == advanced_usage.id
            ).first()
            
            if runtime:
                runtime_nodes = db.query(DocNode).filter(
                    DocNode.version_id == version.id,
                    DocNode.parent_id == runtime.id
                ).all()
                
                # 找到"概述"文档，放到第一个
                overview_node = None
                other_runtime_nodes = []
                for node in runtime_nodes:
                    if node.title == "概述":
                        overview_node = node
                    else:
                        other_runtime_nodes.append(node)
                
                # 排序其他节点（按当前 order）
                other_runtime_nodes.sort(key=lambda x: (x.order, x.id))
                
                runtime_order = 1
                if overview_node:
                    overview_node.order = runtime_order
                    db.commit()
                    print(f"      ✓ 开发指南/高阶用法/Runtime/{overview_node.title} -> order={runtime_order}")
                    runtime_order += 1
                
                for node in other_runtime_nodes:
                    node.order = runtime_order
                    db.commit()
                    print(f"      ✓ 开发指南/高阶用法/Runtime/{node.title} -> order={runtime_order}")
                    runtime_order += 1
        
        # 处理"工作流"目录下的顺序
        workflow = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.title == "工作流",
            DocNode.parent_id == dev_guide.id
        ).first()
        
        if workflow:
            workflow_nodes = db.query(DocNode).filter(
                DocNode.version_id == version.id,
                DocNode.parent_id == workflow.id
            ).all()
            
            # 定义工作流目录下的顺序
            workflow_order_map = {
                "概述": 1,
                "关键概念": 2,
                "构建工作流": 3,
                "组件": 4,
                "使用组件": 5,
            }
            
            workflow_ordered = []
            workflow_others = []
            for node in workflow_nodes:
                if node.title in workflow_order_map:
                    workflow_ordered.append((workflow_order_map[node.title], node))
                else:
                    workflow_others.append(node)
            
            # 排序其他节点
            workflow_others.sort(key=lambda x: (x.order, x.id))
            
            workflow_current_order = 1
            # 设置固定顺序的节点
            workflow_ordered.sort(key=lambda x: x[0])
            for _, node in workflow_ordered:
                node.order = workflow_current_order
                db.commit()
                print(f"      ✓ 开发指南/工作流/{node.title} -> order={workflow_current_order}")
                workflow_current_order += 1
            
            # 设置其他节点
            for node in workflow_others:
                node.order = workflow_current_order
                db.commit()
                print(f"      ✓ 开发指南/工作流/{node.title} -> order={workflow_current_order}")
                workflow_current_order += 1
        
        # 处理"Agent"目录下的顺序（逆序排列）
        agent = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.title.in_(["Agent", "agent"]),
            DocNode.parent_id == dev_guide.id
        ).first()
        
        if agent:
            agent_nodes = db.query(DocNode).filter(
                DocNode.version_id == version.id,
                DocNode.parent_id == agent.id
            ).all()
            
            # 按当前 order 排序，然后逆序
            agent_nodes.sort(key=lambda x: (x.order, x.id), reverse=True)
            
            agent_order = 1
            for node in agent_nodes:
                node.order = agent_order
                db.commit()
                print(f"      ✓ 开发指南/Agent/{node.title} -> order={agent_order} (逆序)")
                agent_order += 1
    
    # 处理"教程"目录下的顺序（逆序排列）
    tutorial = db.query(DocNode).filter(
        DocNode.version_id == version.id,
        DocNode.title == "教程",
        DocNode.parent_id == agentcore.id
    ).first()
    
    if tutorial:
        tutorial_nodes = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.parent_id == tutorial.id
        ).all()
        
        # 按当前 order 排序，然后逆序
        tutorial_nodes.sort(key=lambda x: (x.order, x.id), reverse=True)
        
        tutorial_order = 1
        for node in tutorial_nodes:
            node.order = tutorial_order
            db.commit()
            print(f"    ✓ 教程/{node.title} -> order={tutorial_order} (逆序)")
            tutorial_order += 1
    
    print("  ✓ AgentCore 文档顺序调整完成")


def main():
    """主函数"""
    print("=" * 60)
    print("openJiuwen V1 文档数据导入工具")
    print("=" * 60)
    
    # 确保表已创建
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 清空所有数据
        clear_all_data(db)
        
        # 创建版本
        version = create_version(db)
        
        # 1. 导入 AgentStudio MD 文档（只导入文档中心）
        print("\n" + "=" * 60)
        print("导入 AgentStudio 文档 (Markdown) - 仅文档中心")
        print("=" * 60)
        
        if AGENTSTUDIO_DOCS_DIR.exists():
            # 创建 AgentStudio 一级目录
            agentstudio_category = create_category_node(db, version, "AgentStudio", parent_id=None, order=0)
            
            # 复制静态资源
            print("\n复制 AgentStudio 静态资源...")
            copy_static_assets(AGENTSTUDIO_DOCS_DIR, AGENTSTUDIO_ASSETS_DIR)
            
            # 只扫描文档中心目录，但跳过"文档中心"这一层
            docs_center_dir = AGENTSTUDIO_DOCS_DIR / "文档中心"
            if docs_center_dir.exists():
                print("\n扫描并导入文档中心（跳过文档中心层）...")
                scan_markdown_directory(db, version, AGENTSTUDIO_DOCS_DIR, AGENTSTUDIO_DOCS_DIR, agentstudio_category.id, only_docs_center=True, skip_docs_center=True)
                
                # 重新组织顺序
                reorganize_agentstudio_order(db, version)
                print("✓ AgentStudio 文档导入完成")
            else:
                print(f"  ✗ 文档中心目录不存在: {docs_center_dir}")
        else:
            print(f"✗ AgentStudio 文档目录不存在: {AGENTSTUDIO_DOCS_DIR}")
        
        # 2. 导入 develop_docs HTML 文档
        print("\n" + "=" * 60)
        print("导入开发文档 (HTML)")
        print("=" * 60)
        
        if DEVELOP_DOCS_DIR.exists():
            # 创建 AgentCore 一级目录
            agentcore_category = create_category_node(db, version, "AgentCore", parent_id=None, order=1)
            
            # 复制静态资源
            print("\n复制开发文档静态资源...")
            copy_static_assets(DEVELOP_DOCS_DIR, DEVELOP_DOCS_ASSETS_DIR)
            
            # 扫描并导入文档（从根目录开始，不创建额外的目录）
            print("\n扫描并导入文档...")
            scan_html_directory(db, version, DEVELOP_DOCS_DIR, DEVELOP_DOCS_DIR, parent_id=agentcore_category.id)
            
            # 重新组织顺序
            reorganize_agentcore_order(db, version)
            print("✓ 开发文档导入完成")
        else:
            print(f"✗ 开发文档目录不存在: {DEVELOP_DOCS_DIR}")
        
        # 统计信息
        print("\n" + "=" * 60)
        print("导入统计")
        print("=" * 60)
        total_nodes = db.query(DocNode).filter(DocNode.version_id == version.id).count()
        doc_count = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.node_type == 'doc'
        ).count()
        category_count = db.query(DocNode).filter(
            DocNode.version_id == version.id,
            DocNode.node_type == 'category'
        ).count()
        print(f"总节点数: {total_nodes}")
        print(f"文档数: {doc_count}")
        print(f"目录数: {category_count}")
        
        print("\n" + "=" * 60)
        print("所有文档导入完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
