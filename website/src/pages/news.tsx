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

export default function News(): ReactNode {
  return (
    <Layout
      title="新闻资讯"
      description="九问平台最新动态、版本更新、社区活动和技术博客">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '新闻'}]} />
        <Heading as="h1">
          <Translate>新闻资讯</Translate>
        </Heading>
        <div className="margin-top--lg">
          <p className="text--lg">
            <Translate>
              这里将展示九问平台的最新动态，包括版本更新、社区活动、技术博客等内容。
              内容正在准备中，敬请期待。
            </Translate>
          </p>
          <div className="margin-top--lg">
            <Link className="button button--primary" to="/blog-page">
              <Translate>查看技术博客</Translate>
            </Link>
            <Link className="button button--secondary margin-left--sm" to="/community">
              <Translate>加入社区</Translate>
            </Link>
          </div>
        </div>
      </main>
    </Layout>
  );
}

