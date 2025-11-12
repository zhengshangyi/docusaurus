/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import {useState} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';
import clsx from 'clsx';
import styles from './resources.module.css';

// 预设的版本列表
const presetVersions = [
  {name: 'v1.0', label: 'V1.0', path: '/docs-content'},
  {name: 'v1.1', label: 'V1.1', path: '/docs-content'},
  {name: 'v1.2', label: 'V1.2', path: '/docs-content'},
  {name: 'v2.0', label: 'V2.0', path: '/docs-content'},
];

export default function DocsPage(): ReactNode {
  const [selectedVersion, setSelectedVersion] = useState(presetVersions[0]);

  return (
    <Layout
      title="项目文档"
      description="九问项目文档中心">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '文档'}]} />
        <Heading as="h1" className="margin-bottom--lg">
          <Translate>项目文档</Translate>
        </Heading>

        <div className="card margin-top--md">
          <div className="card__body">
            <p className="margin-bottom--md">
              <Translate>
                选择文档版本，查看对应版本的详细文档和 API 参考。
              </Translate>
            </p>
            
            {/* 版本选择器 */}
            <div className={clsx('margin-bottom--md', styles.versionSelector)}>
              <label htmlFor="version-select" className="margin-right--sm">
                <strong>
                  <Translate>选择版本：</Translate>
                </strong>
              </label>
              <select
                id="version-select"
                className={styles.select}
                value={selectedVersion.name}
                onChange={(e) => {
                  const version = presetVersions.find(
                    (v) => v.name === e.target.value,
                  );
                  if (version) {
                    setSelectedVersion(version);
                  }
                }}>
                {presetVersions.map((version) => (
                  <option key={version.name} value={version.name}>
                    {version.label}
                  </option>
                ))}
              </select>
            </div>

            {/* 文档链接 */}
            <div className={styles.docsActions}>
              <Link
                className="button button--primary button--lg"
                to={selectedVersion.path}>
                <Translate>查看文档</Translate>
              </Link>
              <Link
                className="button button--outline button--lg margin-left--sm"
                to="/versions-page">
                <Translate>所有版本</Translate>
              </Link>
            </div>

            {/* 版本信息 */}
            <div className={clsx('margin-top--md', styles.versionInfo)}>
              <p className="text--sm text--muted">
                <Translate
                  values={{
                    versionName: selectedVersion.label,
                  }}>
                  {'当前选择：{versionName}'}
                </Translate>
              </p>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

