/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';

export default function DocsContent(): ReactNode {
  return (
    <Layout
      title="文档"
      description="九问项目文档">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '文档', to: '/docs-page'}, {label: '文档内容'}]} />
        <Heading as="h1" className="margin-bottom--lg">
          <Translate>文档</Translate>
        </Heading>

        <div className="card margin-top--md">
          <div className="card__body">
            <Heading as="h2" className="margin-bottom--md">
              <Translate>欢迎使用九问文档</Translate>
            </Heading>
            
            <p className="margin-bottom--md">
              <Translate>
                这里是九问项目的文档中心，您可以在这里找到详细的文档说明。
              </Translate>
            </p>

            <div className="margin-top--lg">
              <Heading as="h3" className="margin-bottom--sm">
                <Translate>快速开始</Translate>
              </Heading>
              <p className="text--muted">
                <Translate>
                  快速开始内容将在此处显示...
                </Translate>
              </p>
            </div>

            <div className="margin-top--lg">
              <Heading as="h3" className="margin-bottom--sm">
                <Translate>API 参考</Translate>
              </Heading>
              <p className="text--muted">
                <Translate>
                  API 参考文档将在此处显示...
                </Translate>
              </p>
            </div>

            <div className="margin-top--lg">
              <Heading as="h3" className="margin-bottom--sm">
                <Translate>使用指南</Translate>
              </Heading>
              <p className="text--muted">
                <Translate>
                  使用指南内容将在此处显示...
                </Translate>
              </p>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

