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

export default function Community(): ReactNode {
  return (
    <Layout
      title="社区"
      description="加入九问社区，参与讨论、分享经验、查看社区日历">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '社区'}]} />
        <Heading as="h1">
          <Translate>九问社区</Translate>
        </Heading>
        
        <div className="margin-top--lg">
          <Heading as="h2">
            <Translate>社区介绍</Translate>
          </Heading>
          <p className="text--lg">
            <Translate>
              九问社区是一个活跃的开发者社区，致力于大模型应用开发的交流与分享。
              在这里，你可以：
            </Translate>
          </p>
          <ul>
            <li><Translate>与其他开发者交流经验和最佳实践</Translate></li>
            <li><Translate>获取最新的技术资讯和平台更新</Translate></li>
            <li><Translate>参与社区活动和线上/线下会议</Translate></li>
            <li><Translate>贡献代码、文档和示例</Translate></li>
            <li><Translate>获得技术支持和帮助</Translate></li>
          </ul>
        </div>

        <div className="margin-top--xl">
          <Heading as="h2">
            <Translate>社区日历</Translate>
          </Heading>
          <div className="card margin-top--md">
            <div className="card__header">
              <h3><Translate>即将举行的活动</Translate></h3>
            </div>
            <div className="card__body">
              <p>
                <Translate>
                  社区活动日历正在准备中。我们将定期举办线上技术分享、开发者聚会等活动。
                  敬请关注！
                </Translate>
              </p>
            </div>
          </div>
        </div>

        <div className="margin-top--xl">
          <Heading as="h2">
            <Translate>互动与交流</Translate>
          </Heading>
          <div className="row margin-top--md">
            <div className="col col--4">
              <div className="card">
                <div className="card__header">
                  <h3><Translate>GitHub</Translate></h3>
                </div>
                <div className="card__body">
                  <p><Translate>在 GitHub 上查看源代码、提交 Issue 和 Pull Request</Translate></p>
                  <Link className="button button--primary" to="https://github.com/jiuwen" target="_blank">
                    <Translate>访问 GitHub</Translate>
                  </Link>
                </div>
              </div>
            </div>
            <div className="col col--4">
              <div className="card">
                <div className="card__header">
                  <h3><Translate>讨论区</Translate></h3>
                </div>
                <div className="card__body">
                  <p><Translate>参与社区讨论，提问和回答问题</Translate></p>
                  <Link className="button button--primary" to="/discussion-list">
                    <Translate>进入讨论区</Translate>
                  </Link>
                </div>
              </div>
            </div>
            <div className="col col--4">
              <div className="card">
                <div className="card__header">
                  <h3><Translate>贡献</Translate></h3>
                </div>
                <div className="card__body">
                  <p><Translate>贡献代码、文档或帮助改进项目</Translate></p>
                  <Link className="button button--primary" to="/contribute">
                    <Translate>了解如何贡献</Translate>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

