/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import {useState, useEffect, useRef} from 'react';
import {useLocation, useHistory} from '@docusaurus/router';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';
import clsx from 'clsx';
import styles from './docs-page.module.css';
import {docsVersionsApi, type DocVersion, type DocItem, type DocVersionDetailResponse, type DocContentResponse} from '@site/src/utils/api';

// API 基础地址（与 api.ts 保持一致）
const API_BASE_URL = '';

export default function DocsPage(): ReactNode {
  const location = useLocation();
  const history = useHistory();
  
  const [version, setVersion] = useState<DocVersion | null>(null);
  const [versionDetail, setVersionDetail] = useState<DocVersionDetailResponse | null>(null);
  const [selectedDocPath, setSelectedDocPath] = useState<string>('');
  const [docContent, setDocContent] = useState<DocContentResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedDirs, setExpandedDirs] = useState<Set<string>>(new Set());
  const [sidebarWidth, setSidebarWidth] = useState(260);
  const [isResizing, setIsResizing] = useState(false);
  const [filterText, setFilterText] = useState<string>('');
  const containerRef = useRef<HTMLDivElement>(null);
  const sidebarRef = useRef<HTMLElement>(null);
  const mainRef = useRef<HTMLElement>(null);

  // 从URL参数获取选中的文档路径
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const path = params.get('path') || '';
    if (path) {
      setSelectedDocPath(path);
    }
  }, [location.search]);

  // 加载版本列表
  useEffect(() => {
    const loadVersions = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await docsVersionsApi.getVersions();
        
        if (response.versions.length > 0) {
          const currentVersion = response.versions.find(v => v.name === response.current) || response.versions[0];
          setVersion(currentVersion);
        }
      } catch (err) {
        console.error('加载版本列表失败:', err);
        setError('加载版本列表失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    loadVersions();
  }, []);

  // 加载选中版本的文档详情
  useEffect(() => {
    if (!version) return;

    const loadVersionDetail = async () => {
      try {
        setLoading(true);
        setError(null);
        const detail = await docsVersionsApi.getVersionDetail(version.name);
        setVersionDetail(detail);
        
        // 默认展开所有目录
        const allDirs = new Set<string>();
        const collectDirs = (items: DocItem[]) => {
          items.forEach(item => {
            if (item.type === 'directory') {
              allDirs.add(item.path);
              if (item.children) {
                collectDirs(item.children);
              }
            }
          });
        };
        collectDirs(detail.docs);
        setExpandedDirs(allDirs);
        
        // 如果没有选中文档且有文档，选中第一个文档
        if (!selectedDocPath && detail.docs.length > 0) {
          const firstDoc = findFirstDoc(detail.docs);
          if (firstDoc) {
            setSelectedDocPath(firstDoc.path);
            updateUrl(firstDoc.path);
          }
        }
      } catch (err) {
        console.error('加载文档详情失败:', err);
        setError('加载文档详情失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    loadVersionDetail();
  }, [version]);

  // 加载文档内容
  useEffect(() => {
    if (!version || !selectedDocPath) return;

    const loadDocContent = async () => {
      try {
        setLoading(true);
        setError(null);
        const content = await docsVersionsApi.getDocContent(version.name, selectedDocPath);
        setDocContent(content);
      } catch (err) {
        console.error('加载文档内容失败:', err);
        setError('加载文档内容失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    loadDocContent();
  }, [version, selectedDocPath]);

  // 切换文档时，将右侧内容区域滚动到顶部
  useEffect(() => {
    if (selectedDocPath && mainRef.current) {
      mainRef.current.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  }, [selectedDocPath]);

  // 处理 HTML 内容中的图片加载错误
  useEffect(() => {
    if (docContent && docContent.file_type === 'html' && mainRef.current) {
      const images = mainRef.current.querySelectorAll('img');
      images.forEach((img) => {
        img.onerror = () => {
          console.error('图片加载失败:', img.src);
        };
      });
    }
  }, [docContent]);

  const findFirstDoc = (items: DocItem[]): DocItem | null => {
    for (const item of items) {
      if (item.type === 'file') {
        return item;
      }
      if (item.type === 'directory' && item.children) {
        const found = findFirstDoc(item.children);
        if (found) return found;
      }
    }
    return null;
  };

  // 生成面包屑路径
  const generateBreadcrumbs = (): Array<{label: string, path?: string}> => {
    if (!selectedDocPath || !versionDetail) {
      return [{label: '文档'}];
    }

    const breadcrumbs: Array<{label: string, path?: string}> = [{label: '文档'}];
    
    // 查找当前文档在文档树中的路径
    const findPath = (items: DocItem[], targetPath: string, currentPath: Array<{label: string, path: string}> = []): Array<{label: string, path: string}> | null => {
      for (const item of items) {
        // 确定要使用的路径（优先使用 file_path，如果没有则使用 path）
        const itemPath = item.file_path || item.path;
        const newPath = [...currentPath, {label: item.title, path: itemPath}];
        
        // 检查是否是目标路径（可能是文件路径或目录路径）
        if (item.path === targetPath || item.file_path === targetPath || itemPath === targetPath) {
          return newPath;
        }
        
        // 如果是目录，递归查找
        if (item.type === 'directory' && item.children) {
          const found = findPath(item.children, targetPath, newPath);
          if (found) return found;
        }
      }
      return null;
    };

    const path = findPath(versionDetail.docs, selectedDocPath);
    if (path) {
      // 将路径添加到面包屑中
      path.forEach((item, index) => {
        if (index < path.length - 1) {
          // 中间路径项，可以点击
          breadcrumbs.push({label: item.label, path: item.path});
        } else {
          // 最后一项，当前文档，不添加路径（不可点击）
          breadcrumbs.push({label: item.label});
        }
      });
    } else {
      // 如果找不到路径，至少显示当前文档名称
      const pathParts = selectedDocPath.split('/');
      pathParts.forEach((part, index) => {
        if (index < pathParts.length - 1) {
          breadcrumbs.push({label: part});
        } else {
          breadcrumbs.push({label: part.replace(/\.(md|html)$/, '')});
        }
      });
    }

    return breadcrumbs;
  };

  const updateUrl = (path: string) => {
    const params = new URLSearchParams(location.search);
    params.set('path', path);
    history.replace({
      ...location,
      search: params.toString(),
    });
  };

  const toggleDirectory = (path: string) => {
    const newExpanded = new Set(expandedDirs);
    if (newExpanded.has(path)) {
      newExpanded.delete(path);
    } else {
      newExpanded.add(path);
    }
    setExpandedDirs(newExpanded);
  };

  const handleDocClick = (path: string) => {
    setSelectedDocPath(path);
    updateUrl(path);
  };

  // 拖动分割线的处理函数
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing || !containerRef.current) return;
      
      const containerRect = containerRef.current.getBoundingClientRect();
      const newWidth = e.clientX - containerRect.left;
      
      // 限制最小和最大宽度
      const minWidth = 200;
      const maxWidth = 400;
      
      if (newWidth >= minWidth && newWidth <= maxWidth) {
        setSidebarWidth(newWidth);
      }
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
  }, [isResizing]);

  // 阻止目录和内容区域的滚动传播到整个页面
  useEffect(() => {
    const preventScrollPropagation = (e: WheelEvent) => {
      const target = e.target as HTMLElement;
      const sidebar = sidebarRef.current;
      const main = mainRef.current;

      if (!sidebar || !main) return;

      // 检查是否在目录或内容区域
      const isInSidebar = sidebar.contains(target);
      const isInMain = main.contains(target);

      if (isInSidebar || isInMain) {
        const element = isInSidebar ? sidebar : main;
        
        // 检查是否已经滚动到底部或顶部
        const isAtTop = element.scrollTop <= 0;
        const isAtBottom = element.scrollTop >= element.scrollHeight - element.clientHeight - 1;

        // 如果向上滚动且已经在顶部，或向下滚动且已经在底部，阻止滚动传播
        if ((e.deltaY < 0 && isAtTop) || (e.deltaY > 0 && isAtBottom)) {
          e.preventDefault();
          e.stopPropagation();
        }
      }
    };

    document.addEventListener('wheel', preventScrollPropagation, { passive: false });

    return () => {
      document.removeEventListener('wheel', preventScrollPropagation);
    };
  }, []);

  // 筛选文档树
  const filterDocItems = (items: DocItem[], filter: string): DocItem[] => {
    if (!filter.trim()) {
      return items;
    }

    const filterLower = filter.toLowerCase();
    const filtered: DocItem[] = [];

    for (const item of items) {
      const titleMatch = item.title.toLowerCase().includes(filterLower);
      
      if (item.type === 'directory' && item.children) {
        // 递归筛选子项
        const filteredChildren = filterDocItems(item.children, filter);
        // 如果标题匹配或有匹配的子项，则包含此项
        if (titleMatch || filteredChildren.length > 0) {
          filtered.push({
            ...item,
            children: filteredChildren
          });
        }
      } else if (titleMatch) {
        // 文件项标题匹配
        filtered.push(item);
      }
    }

    return filtered;
  };

  // 当筛选时自动展开匹配的目录
  useEffect(() => {
    if (filterText.trim() && versionDetail) {
      const expandMatchingDirs = (items: DocItem[]) => {
        const newExpanded = new Set<string>();
        const filterLower = filterText.toLowerCase();
        
        const checkItem = (item: DocItem) => {
          const titleMatch = item.title.toLowerCase().includes(filterLower);
          
          if (item.type === 'directory' && item.children) {
            const hasMatchingChildren = item.children.some(child => 
              child.title.toLowerCase().includes(filterLower) ||
              (child.type === 'directory' && checkItem(child))
            );
            
            if (titleMatch || hasMatchingChildren) {
              newExpanded.add(item.path);
              item.children.forEach(checkItem);
            }
          }
        };
        
        items.forEach(checkItem);
        setExpandedDirs(newExpanded);
      };
      
      expandMatchingDirs(versionDetail.docs);
    } else if (!filterText.trim() && versionDetail) {
      // 清除筛选时，恢复默认展开状态（可选）
      // setExpandedDirs(new Set());
    }
  }, [filterText, versionDetail]);

  const renderDocItem = (item: DocItem, level: number = 0): ReactNode => {
    const isDirectory = item.type === 'directory';
    const isExpanded = expandedDirs.has(item.path);
    const isSelected = item.path === selectedDocPath || (item.file_path && item.file_path === selectedDocPath);
    const indentStyle = {paddingLeft: `${level * 1.2}rem`};

    if (isDirectory) {
      // 点击图标展开/收起目录，如果有同名文件则同时打开
      const handleIconClick = (e: React.MouseEvent) => {
        e.stopPropagation(); // 阻止事件冒泡
        toggleDirectory(item.path);
        // 如果有同名文件，同时打开该文件
        if (item.file_path) {
          handleDocClick(item.file_path);
        }
      };

      const handleTitleClick = (e: React.MouseEvent) => {
        if (item.file_path) {
          // 如果目录有同名文件，点击标题打开文件
          e.stopPropagation();
          handleDocClick(item.file_path);
        } else {
          // 否则展开/收起目录
          toggleDirectory(item.path);
        }
      };

      return (
        <div key={item.path}>
          <div
            className={clsx(styles.docItem, styles.docDirectory, {
              [styles.docItemSelected]: isSelected
            })}
            style={indentStyle}>
            <img
              src={isExpanded ? "/img/document_icon/folder-open.svg" : "/img/document_icon/folder-close.svg"}
              alt={isExpanded ? "展开" : "收起"}
              className={styles.folderIcon}
              onClick={handleIconClick}
            />
            <span 
              className={styles.docTitle}
              onClick={handleTitleClick}
              style={{ cursor: item.file_path ? 'pointer' : 'default' }}>
              {item.title}
            </span>
          </div>
          {isExpanded && item.children && (
            <div className={styles.docChildren}>
              {item.children.map(child => renderDocItem(child, level + 1))}
            </div>
          )}
        </div>
      );
    } else {
      return (
        <div
          key={item.path}
          className={clsx(styles.docItem, styles.docFile, {
            [styles.docItemSelected]: isSelected
          })}
          style={indentStyle}
          onClick={() => handleDocClick(item.path)}>
          <img
            src={isSelected ? "/img/document_icon/book-open.svg" : "/img/document_icon/book.svg"}
            alt="文档"
            className={styles.bookIcon}
          />
          <span className={styles.docTitle}>{item.title}</span>
        </div>
      );
    }
  };

  return (
    <Layout
      title="文档"
      description="九问项目文档中心">
      <div className={styles.docsPage}>
        {/* 顶部版本选择器 */}
        <div className={styles.docsHeader}>
          <div className="container">
            <Breadcrumbs items={[{label: '文档'}]} />
            <div className={styles.versionSelector}>
              <label htmlFor="version-select" className={styles.versionLabel}>
                <strong><Translate>版本：</Translate></strong>
              </label>
              <select
                id="version-select"
                className={styles.select}
                value={version?.name || ''}
                disabled={loading || !version}>
                {version && (
                  <option value={version.name}>
                    {version.label} {version.release_date ? `(${version.release_date})` : ''}
                  </option>
                )}
              </select>
              {version?.release_date && (
                <span className={styles.versionDate}>
                  <Translate>发布日期：</Translate> {version.release_date}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* 主体内容：左右布局 */}
        <div className="container">
          <div className={styles.docsContainer} ref={containerRef}>
            {/* 左侧文档目录 */}
            <aside 
              ref={sidebarRef}
              className={styles.docsSidebar}
              style={{width: `${sidebarWidth}px`, minWidth: `${sidebarWidth}px`}}>
            <div className={styles.sidebarContent}>
              {/* 筛选框 */}
              {!loading && versionDetail && versionDetail.docs.length > 0 && (
                <div className={styles.filterBox}>
                  <img 
                    src="/img/document_icon/doc-search-two.svg" 
                    alt="搜索" 
                    className={styles.searchIcon}
                  />
                  <input
                    type="text"
                    className={styles.filterInput}
                    placeholder="搜索文档..."
                    value={filterText}
                    onChange={(e) => setFilterText(e.target.value)}
                  />
                </div>
              )}

              {error && (
                <div className="alert alert--danger margin-bottom--md">
                  {error}
                </div>
              )}

              {loading && !versionDetail ? (
                <div className="text--center padding-vert--lg">
                  <p><Translate>加载中...</Translate></p>
                </div>
              ) : versionDetail && versionDetail.docs.length > 0 ? (
                <div className={styles.docsTree}>
                  {filterDocItems(versionDetail.docs, filterText).map(item => renderDocItem(item))}
                  {filterText.trim() && filterDocItems(versionDetail.docs, filterText).length === 0 && (
                    <div className={styles.noResults}>
                      <Translate>未找到匹配的文档</Translate>
                    </div>
                  )}
                </div>
              ) : (
                <div className="alert alert--info">
                  <Translate>该版本暂无文档</Translate>
                </div>
              )}
            </div>
            </aside>

            {/* 可拖动的分割线 */}
            <div
              className={styles.splitter}
              onMouseDown={(e) => {
                e.preventDefault();
                setIsResizing(true);
              }}
            />

            {/* 右侧文档内容 */}
          <main ref={mainRef} className={styles.docsMain}>
            <div className={styles.docsContent}>
              {loading && !docContent ? (
                <div className="text--center padding-vert--xl">
                  <p><Translate>加载中...</Translate></p>
                </div>
              ) : error && !docContent ? (
                <div className="alert alert--danger">
                  <h4><Translate>加载失败</Translate></h4>
                  <p>{error}</p>
                </div>
              ) : docContent ? (
                <>
                  {/* 面包屑导航 */}
                  <div className={styles.docBreadcrumbs}>
                    {generateBreadcrumbs().map((crumb, index, array) => (
                      <span key={index} className={styles.breadcrumbItem}>
                        <span className={index === array.length - 1 ? styles.breadcrumbCurrent : styles.breadcrumbText}>
                          {crumb.label}
                        </span>
                        {index < array.length - 1 && (
                          <span className={styles.breadcrumbSeparator}> / </span>
                        )}
                      </span>
                    ))}
                  </div>
                  <div className={styles.docBody}>
                    {docContent.file_type === 'html' ? (
                      // HTML 内容：直接渲染 HTML
                      <div 
                        dangerouslySetInnerHTML={{ __html: docContent.content }}
                        className={styles.htmlContent}
                      />
                    ) : (
                      // Markdown 内容：使用 ReactMarkdown 渲染
                      <ReactMarkdown 
                        remarkPlugins={[remarkGfm]}
                        components={{
                          h1: ({node, ...props}) => <h1 className={styles.markdownH1} {...props} />,
                          h2: ({node, ...props}) => <h2 className={styles.markdownH2} {...props} />,
                          h3: ({node, ...props}) => <h3 className={styles.markdownH3} {...props} />,
                          h4: ({node, ...props}) => <h4 className={styles.markdownH4} {...props} />,
                          p: ({node, ...props}) => <p className={styles.markdownP} {...props} />,
                          ul: ({node, ...props}) => <ul className={styles.markdownUl} {...props} />,
                          ol: ({node, ...props}) => <ol className={styles.markdownOl} {...props} />,
                          li: ({node, ...props}) => <li className={styles.markdownLi} {...props} />,
                          code: ({node, inline, ...props}: any) => 
                            inline ? (
                              <code className={styles.markdownCodeInline} {...props} />
                            ) : (
                              <code className={styles.markdownCodeBlock} {...props} />
                            ),
                          pre: ({node, ...props}) => <pre className={styles.markdownPre} {...props} />,
                          a: ({node, ...props}) => <a className={styles.markdownA} {...props} />,
                          blockquote: ({node, ...props}) => <blockquote className={styles.markdownBlockquote} {...props} />,
                          table: ({node, ...props}) => <div className={styles.markdownTableWrapper}><table className={styles.markdownTable} {...props} /></div>,
                          th: ({node, ...props}) => <th className={styles.markdownTh} {...props} />,
                          td: ({node, ...props}) => <td className={styles.markdownTd} {...props} />,
                          hr: ({node, ...props}) => <hr className={styles.markdownHr} {...props} />,
                          img: ({node, src, alt, ...props}: any) => {
                            // 处理图片路径：API 路径已经是正确的相对路径，直接使用
                            // 如果需要绝对路径，可以拼接 API_BASE_URL
                            const imageSrc = src ? `${API_BASE_URL}${src}` : '';
                            return <img src={imageSrc} alt={alt || ''} className={styles.markdownImg} {...props} />;
                          },
                        }}
                      >
                        {docContent.content}
                      </ReactMarkdown>
                    )}
                  </div>
                </>
              ) : (
                <div className="alert alert--info">
                  <p><Translate>请从左侧选择文档</Translate></p>
                </div>
              )}
            </div>
          </main>
          </div>
        </div>
      </div>
    </Layout>
  );
}
