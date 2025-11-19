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
      description="openJiuwen最新动态、版本更新、社区活动">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '新闻'}]} />
        <Heading as="h1">
          <Translate>新闻资讯</Translate>
        </Heading>
        <div className="margin-top--lg">
          <p className="text--lg">
            <Translate>
              这里将展示openJiuwen的最新动态，包括版本更新、社区活动等内容。 内容正在准备中，敬请期待。
            </Translate>
          </p>
        </div>
      </main>
    </Layout>
  );
}

