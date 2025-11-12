/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';

// 预设的版本列表
const presetVersions = [
  {name: 'v1.0', label: 'V1.0', path: '/docs-content'},
  {name: 'v1.1', label: 'V1.1', path: '/docs-content'},
  {name: 'v1.2', label: 'V1.2', path: '/docs-content'},
  {name: 'v2.0', label: 'V2.0', path: '/docs-content'},
];

export default function VersionsPage(): ReactNode {
  return (
    <Layout
      title="所有版本"
      description="九问项目所有版本列表">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '文档', to: '/docs-page'}, {label: '所有版本'}]} />
        <Heading as="h1" className="margin-bottom--lg">
          <Translate>所有版本</Translate>
        </Heading>

        <div className="card margin-top--md">
          <div className="card__body">
            <p className="margin-bottom--md">
              <Translate>
                以下是九问项目的所有版本列表，您可以选择查看不同版本的文档。
              </Translate>
            </p>

            <div className="margin-top--lg">
              <Heading as="h3" className="margin-bottom--md">
                <Translate>当前版本</Translate>
              </Heading>
              <table className="table">
                <thead>
                  <tr>
                    <th><Translate>版本</Translate></th>
                    <th><Translate>文档</Translate></th>
                  </tr>
                </thead>
                <tbody>
                  {presetVersions.map((version) => (
                    <tr key={version.name}>
                      <td><strong>{version.label}</strong></td>
                      <td>
                        <Link to={version.path}>
                          <Translate>查看文档</Translate>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="margin-top--xl">
              <Heading as="h3" className="margin-bottom--md">
                <Translate>历史版本</Translate>
              </Heading>
              <p className="text--muted">
                <Translate>
                  历史版本信息将在此处显示...
                </Translate>
              </p>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

