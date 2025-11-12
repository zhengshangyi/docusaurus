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
import clsx from 'clsx';
import styles from './resources.module.css';

export default function BlogPage(): ReactNode {
  return (
    <Layout
      title="博客"
      description="九问平台博客">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '博客'}]} />
        <Heading as="h1" className="margin-bottom--lg">
          <Translate>博客</Translate>
        </Heading>

        <div className="card margin-top--md">
          <div className="card__body">
            <p className="margin-bottom--md">
              <Translate>
                这里提供九问平台的最新动态、技术文章和最佳实践，帮助您快速上手和深入理解平台功能。
              </Translate>
            </p>

            {/* Wiki 风格的内容区域 */}
            <div className={styles.wikiContent}>
              <div className={styles.wikiSection}>
                <Heading as="h3" className="margin-bottom--sm">
                  <Translate>快速入门</Translate>
                </Heading>
                <div className={styles.wikiPlaceholder}>
                  <p className="text--muted">
                    <Translate>
                      快速入门教程内容将在此处显示...
                    </Translate>
                  </p>
                </div>
              </div>

              <div className={clsx(styles.wikiSection, 'margin-top--lg')}>
                <Heading as="h3" className="margin-bottom--sm">
                  <Translate>教程指南</Translate>
                </Heading>
                <div className={styles.wikiPlaceholder}>
                  <p className="text--muted">
                    <Translate>
                      详细教程内容将在此处显示...
                    </Translate>
                  </p>
                </div>
              </div>

              <div className={clsx(styles.wikiSection, 'margin-top--lg')}>
                <Heading as="h3" className="margin-bottom--sm">
                  <Translate>最佳实践</Translate>
                </Heading>
                <div className={styles.wikiPlaceholder}>
                  <p className="text--muted">
                    <Translate>
                      最佳实践内容将在此处显示...
                    </Translate>
                  </p>
                </div>
              </div>

              <div className={clsx(styles.wikiSection, 'margin-top--lg')}>
                <Heading as="h3" className="margin-bottom--sm">
                  <Translate>常见问题</Translate>
                </Heading>
                <div className={styles.wikiPlaceholder}>
                  <p className="text--muted">
                    <Translate>
                      常见问题解答将在此处显示...
                    </Translate>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

