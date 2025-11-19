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

export default function Contribute(): ReactNode {
  return (
    <Layout
      title="贡献"
      description="了解如何为openJiuwen平台做出贡献">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '贡献'}]} />
        <Heading as="h1">
          <Translate>贡献指南</Translate>
        </Heading>
        
        <div className="margin-top--lg">
          <p className="text--lg">
            <Translate>
              感谢您对openJiuwen平台的关注！我们欢迎各种形式的贡献，包括但不限于：
            </Translate>
          </p>
        </div>

        <div className="margin-top--xl">
          <div className="row">
            <div className="col col--4">
              <div className="card margin-bottom--md">
                <div className="card__header">
                  <h3>💻 <Translate>代码贡献</Translate></h3>
                </div>
                <div className="card__body">
                  <p>
                    <Translate>
                      提交 Bug 修复、新功能或性能优化。请先 Fork 项目，创建分支，提交 Pull Request。
                    </Translate>
                  </p>
                  <Link className="button button--primary button--lg jiuwen-btn-primary" to="https://gitee.com/testmyai/test-agentcore" target="_blank" rel="noopener noreferrer">
                    <Translate>查看 Gitee</Translate>
                  </Link>
                </div>
              </div>
            </div>
            <div className="col col--4">
              <div className="card margin-bottom--md">
                <div className="card__header">
                  <h3>🐛 <Translate>报告问题</Translate></h3>
                </div>
                <div className="card__body">
                  <p>
                    <Translate>
                      发现 Bug 或有改进建议？请在 Gitee Issues 中报告，帮助我们改进项目。
                    </Translate>
                  </p>
                  <Link className="button button--primary button--lg jiuwen-btn-primary" to="https://gitee.com/testmyai/test-agentcore/issues" target="_blank" rel="noopener noreferrer">
                    <Translate>提交 Issue</Translate>
                  </Link>
                </div>
              </div>
            </div>
            <div className="col col--4">
              <div className="card margin-bottom--md">
                <div className="card__header">
                  <h3>💬 <Translate>社区支持</Translate></h3>
                </div>
                <div className="card__body">
                  <p>
                    <Translate>
                      在社区中回答问题、分享经验、帮助其他开发者，让社区更加活跃。
                    </Translate>
                  </p>
                  <Link className="button button--primary button--lg jiuwen-btn-primary" to="/community">
                    <Translate>加入社区</Translate>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="margin-top--xl">
          <Heading as="h2">
            <Translate>贡献流程</Translate>
          </Heading>
          <ol>
            <li><Translate>Fork 项目仓库</Translate></li>
            <li><Translate>创建功能分支（git checkout -b feature/AmazingFeature）</Translate></li>
            <li><Translate>提交更改（git commit -m 'Add some AmazingFeature'）</Translate></li>
            <li><Translate>推送到分支（git push origin feature/AmazingFeature）</Translate></li>
            <li><Translate>开启 Pull Request</Translate></li>
          </ol>
        </div>
      </main>
    </Layout>
  );
}

