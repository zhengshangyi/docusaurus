/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import {useState, useEffect, useRef} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';
import clsx from 'clsx';
import styles from './versions-page.module.css';

// 版本信息接口
interface VersionInfo {
  name: string;
  label: string;
  release_date?: string;
  description?: string;
  downloads?: {
    name: string;
    url: string;
    size?: string;
  }[];
  changelog?: string;
}

export default function VersionsPage(): ReactNode {
  const [selectedVersion, setSelectedVersion] = useState<string | null>(null);
  const [versions, setVersions] = useState<VersionInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const sidebarRef = useRef<HTMLDivElement>(null);
  const mainRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [sidebarWidth, setSidebarWidth] = useState(260);
  const [isResizing, setIsResizing] = useState(false);

  // 获取版本列表
  useEffect(() => {
    const fetchVersions = async () => {
      setLoading(true);
      setError(null);
      try {
        // TODO: 从 API 获取版本列表
        // 目前使用 mock 数据
        const data: VersionInfo[] = [
          {
            name: 'agent-studio-v1',
            label: 'Agent Studio V1',
            release_date: '2025-11-19',
            description: 'AgentStudio 是一个专业的AI Agent开发与管理平台，旨在为开发者和企业用户提供完整的Agent构建、训练、部署和管理解决方案。AgentStudio提供了从Agent设计到商业化应用的全链路工具和服务。',
            downloads: [
              {
                name: 'Agent Studio V1',
                url: '',
                size: ''
              }
            ],
            changelog: `Agent Studio V1 (2025-11-19)

新增功能
- 多工作流控制
- 运行时中断与恢复
- 提示词自优化`
          }
        ];
        setVersions(data);
        if (data.length > 0 && !selectedVersion) {
          setSelectedVersion(data[0].name);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : '加载版本列表失败');
      } finally {
        setLoading(false);
      }
    };

    fetchVersions();
  }, []);

  // 获取选中版本的详细信息
  const selectedVersionInfo = versions.find(v => v.name === selectedVersion);

  // 处理侧边栏拖拽调整宽度
  useEffect(() => {
    if (!isResizing) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const containerRect = containerRef.current.getBoundingClientRect();
      const newWidth = e.clientX - containerRect.left;
      if (newWidth >= 200 && newWidth <= 400) {
        setSidebarWidth(newWidth);
      }
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';

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

  // 切换版本时，将右侧内容区域滚动到顶部
  useEffect(() => {
    if (selectedVersion && mainRef.current) {
      mainRef.current.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  }, [selectedVersion]);

  return (
    <Layout
      title="版本列表"
      description="openJiuwen项目版本列表">
      <div className={styles.versionsPage}>
        <main className="container margin-vert--lg">
          <Breadcrumbs items={[{label: '版本列表'}]} />
          <Heading as="h1" className="margin-bottom--lg">
            <Translate>版本列表</Translate>
          </Heading>

          {/* 主体内容：左右布局 */}
          <div className="container">
            <div className={styles.versionsContainer} ref={containerRef}>
              {/* 左侧版本目录 */}
              <aside 
                ref={sidebarRef}
                className={styles.versionsSidebar}
                style={{width: `${sidebarWidth}px`, minWidth: `${sidebarWidth}px`}}>
                <div className={styles.sidebarContent}>
                  {error && (
                    <div className="alert alert--danger margin-bottom--md">
                      {error}
                    </div>
                  )}

                  {loading ? (
                    <div className="text--center padding-vert--lg">
                      <p><Translate>加载中...</Translate></p>
                    </div>
                  ) : versions.length > 0 ? (
                    <div className={styles.versionsList}>
                      {versions.map((version) => (
                        <div
                          key={version.name}
                          className={clsx(
                            styles.versionItem,
                            selectedVersion === version.name && styles.versionItemActive
                          )}
                          onClick={() => setSelectedVersion(version.name)}>
                          <div className={styles.versionLabel}>
                            <strong>{version.label}</strong>
                          </div>
                          {version.release_date && (
                            <div className={styles.versionDate}>
                              {version.release_date}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="alert alert--info">
                      <Translate>暂无版本信息</Translate>
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

              {/* 右侧版本详情 */}
              <main ref={mainRef} className={styles.versionsMain}>
                <div className={styles.versionsContent}>
                  {loading && !selectedVersionInfo ? (
                    <div className="text--center padding-vert--xl">
                      <p><Translate>加载中...</Translate></p>
                    </div>
                  ) : error && !selectedVersionInfo ? (
                    <div className="alert alert--danger">
                      <h4><Translate>加载失败</Translate></h4>
                      <p>{error}</p>
                    </div>
                  ) : selectedVersionInfo ? (
                    <div className={styles.versionDetail}>
                      <Heading as="h2" className={styles.versionTitle}>
                        {selectedVersionInfo.label}
                      </Heading>
                      
                      {selectedVersionInfo.release_date && (
                        <p className={styles.versionMeta}>
                          <Translate>发布日期：</Translate> {selectedVersionInfo.release_date}
                        </p>
                      )}

                      {selectedVersionInfo.description && (
                        <div className={styles.versionDescription}>
                          <p>{selectedVersionInfo.description}</p>
                        </div>
                      )}

                      {selectedVersionInfo.downloads && selectedVersionInfo.downloads.length > 0 && (
                        <div className={styles.downloadsSection}>
                          <Heading as="h3" className={styles.sectionTitle}>
                            <Translate>下载</Translate>
                          </Heading>
                          <div className={styles.downloadsList}>
                            {selectedVersionInfo.downloads.map((download, index) => (
                              <div key={index} className={styles.downloadItem}>
                                <div className={styles.downloadInfo}>
                                  <span className={styles.downloadName}>{download.name}</span>
                                  {download.size && (
                                    <span className={styles.downloadSize}>{download.size}</span>
                                  )}
                                </div>
                                {download.url ? (
                                  <Link
                                    className="button button--primary button--sm"
                                    to={download.url}
                                    target="_blank"
                                    rel="noopener noreferrer">
                                    <Translate>下载</Translate>
                                  </Link>
                                ) : null}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {selectedVersionInfo.changelog && (
                        <div className={styles.changelogSection}>
                          <Heading as="h3" className={styles.sectionTitle}>
                            <Translate>更新日志</Translate>
                          </Heading>
                          <div className={styles.changelogContent}>
                            <pre className={styles.changelogText}>{selectedVersionInfo.changelog}</pre>
                          </div>
                        </div>
                      )}

                      {!selectedVersionInfo.downloads && !selectedVersionInfo.changelog && (
                        <div className="alert alert--info">
                          <Translate>该版本暂无详细信息</Translate>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="alert alert--info">
                      <Translate>请从左侧选择一个版本查看详情</Translate>
                    </div>
                  )}
                </div>
              </main>
            </div>
          </div>
        </main>
      </div>
    </Layout>
  );
}
