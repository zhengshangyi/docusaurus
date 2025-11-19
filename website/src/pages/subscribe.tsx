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
import styles from './subscribe.module.css';

// Mock 数据
const emailLists = [
  {
    email: 'contact@openjiuwen.osinfra.cn',
    brief: '公共邮箱',
    description: '社区公共邮箱，日常交流使用',
    subscribeUrl: null // 不涉及订阅
  },
  {
    email: 'cla@openjiuwen.osinfra.cn',
    brief: 'CLA相关',
    description: '用于发送CLA签署邮件',
    subscribeUrl: null // 不涉及订阅
  },
  {
    email: 'legal@openjiuwen.osinfra.cn',
    brief: '法务工作小组邮件列表',
    description: '任何社区开发者可反馈合规等法务相关问题到此邮箱',
    subscribeUrl: null // 不涉及订阅
  }
];

export default function Subscribe(): ReactNode {
  return (
    <Layout
      title="邮件订阅"
      description="订阅九问平台邮件列表，获取最新资讯和技术动态">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '社区', to: '/community'}, {label: '邮件订阅'}]} />
        <Heading as="h1">
          <Translate>邮件订阅</Translate>
        </Heading>
        
        {/* 订阅指导步骤 */}
        <div className="margin-top--lg">
          <div className="card">
            <div className="card__header">
              <Heading as="h2" className="margin-bottom--none">
                <Translate>如何订阅邮件列表</Translate>
              </Heading>
            </div>
            <div className="card__body">
              <p className="text--lg margin-bottom--md">
                <Translate>
                  订阅九问平台邮件列表非常简单，只需按照以下6个步骤操作：
                </Translate>
              </p>
              <ul className={styles.stepsList}>
                <li>
                  <strong><Translate>第一步：</Translate></strong>
                  <Translate>点击下方表格中需要订阅的邮件名称或订阅按钮</Translate>
                </li>
                <li>
                  <strong><Translate>第二步：</Translate></strong>
                  <Translate>浏览器会跳转到订阅页面，页面会提供详细的订阅说明和邮件列表介绍</Translate>
                </li>
                <li>
                  <strong><Translate>第三步：</Translate></strong>
                  <Translate>在订阅页面填写个人用于接收消息的邮箱地址、姓名等必要信息</Translate>
                </li>
                <li>
                  <strong><Translate>第四步：</Translate></strong>
                  <Translate>点击订阅按钮后，系统会向您填写的邮箱发送一封确认邮件</Translate>
                </li>
                <li>
                  <strong><Translate>第五步：</Translate></strong>
                  <Translate>打开邮箱，找到确认邮件并按照邮件中的提示回复确认订阅</Translate>
                </li>
                <li>
                  <strong><Translate>第六步：</Translate></strong>
                  <Translate>确认后，您会收到一封来自邮件列表的欢迎邮件，表示订阅成功</Translate>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* 邮件列表表格 */}
        <div className="margin-top--xl">
          <Heading as="h2">
            <Translate>openJiuwen 邮件列表</Translate>
          </Heading>
          <div className="card margin-top--md">
            <div className="card__body">
              <div className={styles.tableWrapper}>
                <table className={styles.emailTable}>
                  <thead>
                    <tr>
                      <th><Translate>邮箱</Translate></th>
                      <th><Translate>简述</Translate></th>
                      <th><Translate>说明</Translate></th>
                      <th><Translate>订阅</Translate></th>
                    </tr>
                  </thead>
                  <tbody>
                    {emailLists.map((list, index) => (
                      <tr key={index}>
                        <td className={styles.emailCell}>
                          <code className={styles.emailCode}>{list.email}</code>
                        </td>
                        <td className={styles.briefCell}>
                          <strong>{list.brief}</strong>
                        </td>
                        <td className={styles.descriptionCell}>
                          {list.description}
                        </td>
                        <td className={styles.actionCell}>
                          {list.subscribeUrl ? (
                            <Link
                              className="button button--primary button--sm"
                              to={list.subscribeUrl}
                              target="_blank"
                              rel="noopener noreferrer">
                              <Translate>订阅</Translate>
                            </Link>
                          ) : null}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

