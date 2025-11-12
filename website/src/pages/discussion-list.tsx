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
import clsx from 'clsx';
import styles from './discussion.module.css';

// Mock 数据
const mockQuestions = [
  {
    id: '1',
    title: '如何快速开始使用九问平台？',
    category: 'usage',
    categoryLabel: '使用问题',
    author: '张三',
    createdAt: '2024-01-15',
    views: 128,
    replies: 5,
    status: 'solved',
  },
  {
    id: '2',
    title: 'API 调用时出现 401 错误',
    category: 'bug',
    categoryLabel: 'Bug 反馈',
    author: '李四',
    createdAt: '2024-01-14',
    views: 89,
    replies: 3,
    status: 'open',
  },
  {
    id: '3',
    title: '建议增加批量操作功能',
    category: 'feature',
    categoryLabel: '功能建议',
    author: '王五',
    createdAt: '2024-01-13',
    views: 156,
    replies: 8,
    status: 'open',
  },
  {
    id: '4',
    title: '文档中的示例代码无法运行',
    category: 'usage',
    categoryLabel: '使用问题',
    author: '赵六',
    createdAt: '2024-01-12',
    views: 67,
    replies: 2,
    status: 'solved',
  },
  {
    id: '5',
    title: '性能优化相关问题',
    category: 'other',
    categoryLabel: '其他',
    author: '钱七',
    createdAt: '2024-01-11',
    views: 94,
    replies: 4,
    status: 'open',
  },
];

const getCategoryBadgeClass = (category: string) => {
  const categoryMap: Record<string, string> = {
    usage: 'badge--success',
    bug: 'badge--danger',
    feature: 'badge--info',
    other: 'badge--secondary',
  };
  return categoryMap[category] || 'badge--secondary';
};

export default function DiscussionList(): ReactNode {
  return (
    <Layout
      title="讨论区"
      description="九问社区讨论区，查看问题、参与讨论">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '社区', to: '/community'}, {label: '讨论区'}]} />
        <div className={styles.listHeader}>
          <Heading as="h1">
            <Translate>讨论区</Translate>
          </Heading>
          <Link
            className="button button--primary button--lg"
            to="/discussion">
            <Translate>创建问题</Translate>
          </Link>
        </div>

        <div className="card margin-top--md">
          <div className="card__body">
            <div className={styles.filterBar}>
              <div className={styles.filterGroup}>
                <label className="margin-right--sm">
                  <strong>
                    <Translate>筛选：</Translate>
                  </strong>
                </label>
                <select className={styles.filterSelect}>
                  <option value="all">
                    <Translate>全部</Translate>
                  </option>
                  <option value="usage">
                    <Translate>使用问题</Translate>
                  </option>
                  <option value="bug">
                    <Translate>Bug 反馈</Translate>
                  </option>
                  <option value="feature">
                    <Translate>功能建议</Translate>
                  </option>
                  <option value="other">
                    <Translate>其他</Translate>
                  </option>
                </select>
              </div>
              <div className={styles.filterGroup}>
                <label className="margin-right--sm">
                  <strong>
                    <Translate>状态：</Translate>
                  </strong>
                </label>
                <select className={styles.filterSelect}>
                  <option value="all">
                    <Translate>全部</Translate>
                  </option>
                  <option value="open">
                    <Translate>待解决</Translate>
                  </option>
                  <option value="solved">
                    <Translate>已解决</Translate>
                  </option>
                </select>
              </div>
            </div>

            <div className={styles.questionsList}>
              {mockQuestions.map((question) => (
                <Link
                  key={question.id}
                  to={`/discussion-detail?id=${question.id}`}
                  className={styles.questionItem}>
                  <div className={styles.questionHeader}>
                    <span
                      className={clsx(
                        'badge',
                        getCategoryBadgeClass(question.category),
                        styles.categoryBadge,
                      )}>
                      {question.categoryLabel}
                    </span>
                    {question.status === 'solved' && (
                      <span className={clsx('badge', 'badge--success', styles.statusBadge)}>
                        <Translate>已解决</Translate>
                      </span>
                    )}
                    {question.status === 'open' && (
                      <span className={clsx('badge', 'badge--warning', styles.statusBadge)}>
                        <Translate>待解决</Translate>
                      </span>
                    )}
                  </div>
                  <h3 className={styles.questionTitle}>{question.title}</h3>
                  <div className={styles.questionMeta}>
                    <span>
                      <Translate
                        values={{
                          author: question.author,
                        }}>
                        {'提问者：{author}'}
                      </Translate>
                    </span>
                    <span>
                      <Translate
                        values={{
                          date: question.createdAt,
                        }}>
                        {'发布时间：{date}'}
                      </Translate>
                    </span>
                    <span>
                      <Translate
                        values={{
                          views: question.views,
                        }}>
                        {'浏览：{views}'}
                      </Translate>
                    </span>
                    <span>
                      <Translate
                        values={{
                          replies: question.replies,
                        }}>
                        {'回复：{replies}'}
                      </Translate>
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

