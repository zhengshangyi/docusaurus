/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import {useState, useEffect} from 'react';
import {useLocation} from '@docusaurus/router';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';
import Link from '@docusaurus/Link';
import {docsVersionsApi, type DocContentResponse} from '@site/src/utils/api';

export default function DocsContent(): ReactNode {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const version = params.get('version') || '';
  const path = params.get('path') || '';
  
  const [docContent, setDocContent] = useState<DocContentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!version || !path) {
      setError('缺少版本或路径参数');
      return;
    }

    const loadDocContent = async () => {
      try {
        setLoading(true);
        setError(null);
        const content = await docsVersionsApi.getDocContent(version, path);
        setDocContent(content);
      } catch (err) {
        console.error('加载文档内容失败:', err);
        setError(err instanceof Error ? err.message : '加载文档内容失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    loadDocContent();
  }, [version, path]);

  return (
    <Layout
      title={docContent?.title || '文档'}
      description="九问项目文档">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[
          {label: '文档', to: '/docs-page'}, 
          {label: docContent?.title || '文档内容'}
        ]} />
        
        {loading ? (
          <div className="text--center padding-vert--xl">
            <p><Translate>加载中...</Translate></p>
          </div>
        ) : error ? (
          <div className="alert alert--danger">
            <h4><Translate>加载失败</Translate></h4>
            <p>{error}</p>
            <Link to="/docs-page" className="button button--primary">
              <Translate>返回文档列表</Translate>
            </Link>
          </div>
        ) : docContent ? (
          <div className="card margin-top--md">
            <div className="card__body">
              <div className="margin-bottom--lg">
                <Link to="/docs-page" className="button button--outline button--sm">
                  ← <Translate>返回文档列表</Translate>
                </Link>
              </div>
              
              <Heading as="h1" className="margin-bottom--lg">
                {docContent.title}
              </Heading>
              
              <div className="margin-bottom--md text--sm text--muted">
                <span><Translate>版本：</Translate> {docContent.version}</span>
                <span className="margin-left--md"><Translate>路径：</Translate> {docContent.path}</span>
              </div>
              
              <div 
                className="markdown margin-top--lg"
                // eslint-disable-next-line react/no-danger
                dangerouslySetInnerHTML={{__html: docContent.content}}
              />
            </div>
          </div>
        ) : (
          <div className="alert alert--warning">
            <p><Translate>未找到文档内容</Translate></p>
            <Link to="/docs-page" className="button button--primary">
              <Translate>返回文档列表</Translate>
            </Link>
          </div>
        )}
      </main>
    </Layout>
  );
}
