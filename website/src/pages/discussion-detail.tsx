/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import {useState, useEffect} from 'react';
import {useLocation} from '@docusaurus/router';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';
import clsx from 'clsx';
import styles from './discussion.module.css';

// Mock 数据
const mockQuestions: Record<
  string,
  {
    id: string;
    title: string;
    category: string;
    categoryLabel: string;
    author: string;
    createdAt: string;
    views: number;
    replies: number;
    status: string;
    content: string;
    repliesList: Array<{
      id: string;
      author: string;
      createdAt: string;
      content: string;
    }>;
  }
> = {
  '1': {
    id: '1',
    title: '如何快速开始使用九问平台？',
    category: 'usage',
    categoryLabel: '使用问题',
    author: '张三',
    createdAt: '2024-01-15',
    views: 128,
    replies: 5,
    status: 'solved',
    content: `我想了解如何快速开始使用九问平台，需要哪些步骤？

我已经完成了账号注册，但是不知道接下来应该做什么。希望能得到详细的指导。

谢谢！`,
    repliesList: [
      {
        id: 'r1',
        author: '管理员',
        createdAt: '2024-01-15',
        content: `欢迎使用九问平台！快速开始步骤如下：

1. 完成账号注册和认证
2. 查看文档了解基本概念
3. 尝试创建第一个项目
4. 参考示例代码进行开发

详细文档请参考：/docs-page`,
      },
      {
        id: 'r2',
        author: '李四',
        createdAt: '2024-01-16',
        content: '我也刚入门，一起学习！',
      },
    ],
  },
  '2': {
    id: '2',
    title: 'API 调用时出现 401 错误',
    category: 'bug',
    categoryLabel: 'Bug 反馈',
    author: '李四',
    createdAt: '2024-01-14',
    views: 89,
    replies: 3,
    status: 'open',
    content: `我在调用 API 时遇到了 401 未授权错误。

错误信息：
\`\`\`
{
  "error": "Unauthorized",
  "code": 401
}
\`\`\`

我已经检查了 API Key 的配置，看起来是正确的。请问可能是什么原因？`,
    repliesList: [
      {
        id: 'r1',
        author: '技术支持',
        createdAt: '2024-01-14',
        content: `401 错误通常是由于认证信息不正确导致的。请检查：

1. API Key 是否正确配置
2. 请求头中是否包含正确的 Authorization 字段
3. API Key 是否已过期

如果问题仍然存在，请提供更多详细信息。`,
      },
    ],
  },
  '3': {
    id: '3',
    title: '建议增加批量操作功能',
    category: 'feature',
    categoryLabel: '功能建议',
    author: '王五',
    createdAt: '2024-01-13',
    views: 156,
    replies: 8,
    status: 'open',
    content: `在使用过程中，我发现需要频繁进行单个操作，效率较低。

建议增加批量操作功能，比如：
- 批量删除
- 批量修改
- 批量导出

这样可以大大提高工作效率。`,
    repliesList: [
      {
        id: 'r1',
        author: '产品经理',
        createdAt: '2024-01-13',
        content: '感谢您的建议！我们已经在规划这个功能，预计在下个版本中发布。',
      },
    ],
  },
  '4': {
    id: '4',
    title: '文档中的示例代码无法运行',
    category: 'usage',
    categoryLabel: '使用问题',
    author: '赵六',
    createdAt: '2024-01-12',
    views: 67,
    replies: 2,
    status: 'solved',
    content: `我在按照文档中的示例代码进行操作时，发现代码无法正常运行。

示例代码：
\`\`\`javascript
// 示例代码
\`\`\`

报错信息：xxx

请问是什么原因？`,
    repliesList: [
      {
        id: 'r1',
        author: '开发者',
        createdAt: '2024-01-12',
        content: '这个问题已经修复，请更新到最新版本的文档。',
      },
    ],
  },
  '5': {
    id: '5',
    title: '性能优化相关问题',
    category: 'other',
    categoryLabel: '其他',
    author: '钱七',
    createdAt: '2024-01-11',
    views: 94,
    replies: 4,
    status: 'open',
    content: `想了解如何进行性能优化，有什么最佳实践吗？`,
    repliesList: [
      {
        id: 'r1',
        author: '技术专家',
        createdAt: '2024-01-11',
        content: '性能优化是一个复杂的话题，建议参考我们的性能优化文档。',
      },
    ],
  },
};

const getCategoryBadgeClass = (category: string) => {
  const categoryMap: Record<string, string> = {
    usage: 'badge--success',
    bug: 'badge--danger',
    feature: 'badge--info',
    other: 'badge--secondary',
  };
  return categoryMap[category] || 'badge--secondary';
};

export default function DiscussionDetail(): ReactNode {
  const location = useLocation();
  const [question, setQuestion] = useState<typeof mockQuestions[string] | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const id = params.get('id');
    if (id && mockQuestions[id]) {
      setQuestion(mockQuestions[id]);
    }
  }, [location.search]);

  if (!question) {
    return (
      <Layout title="问题详情" description="查看问题详情">
        <main className="container margin-vert--lg">
          <Breadcrumbs
            items={[
              {label: '社区', to: '/community'},
              {label: '讨论区', to: '/discussion-list'},
              {label: '问题详情'},
            ]}
          />
          <div className="card">
            <div className="card__body">
              <p>
                <Translate>问题不存在或已被删除</Translate>
              </p>
              <Link className="button button--primary margin-top--md" to="/discussion-list">
                <Translate>返回列表</Translate>
              </Link>
            </div>
          </div>
        </main>
      </Layout>
    );
  }

  return (
    <Layout
      title={question.title}
      description="查看问题详情">
      <main className="container margin-vert--lg">
        <Breadcrumbs
          items={[
            {label: '社区', to: '/community'},
            {label: '讨论区', to: '/discussion-list'},
            {label: question ? question.title : '问题详情'},
          ]}
        />
        <div className={styles.detailHeader}>
          <Link className="button button--outline" to="/discussion-list">
            <Translate>← 返回列表</Translate>
          </Link>
        </div>

        <div className="card margin-top--md">
          <div className="card__header">
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
            <Heading as="h1" className={styles.detailTitle}>
              {question.title}
            </Heading>
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
          </div>
          <div className="card__body">
            <div className={styles.questionContent}>
              <pre className={styles.contentText}>{question.content}</pre>
            </div>
          </div>
        </div>

        <div className="margin-top--lg">
          <Heading as="h2" className="margin-bottom--md">
            <Translate
              values={{
                count: question.repliesList.length,
              }}>
              {'回复 ({count})'}
            </Translate>
          </Heading>
          {question.repliesList.map((reply) => (
            <div key={reply.id} className="card margin-bottom--md">
              <div className="card__header">
                <div className={styles.replyHeader}>
                  <strong>{reply.author}</strong>
                  <span className="text--sm text--muted">{reply.createdAt}</span>
                </div>
              </div>
              <div className="card__body">
                <p className={styles.replyContent}>{reply.content}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="card margin-top--lg">
          <div className="card__header">
            <Heading as="h3">
              <Translate>发表回复</Translate>
            </Heading>
          </div>
          <div className="card__body">
            <textarea
              className={clsx('textarea', styles.textarea)}
              rows={5}
              placeholder="请输入您的回复..."
            />
            <div className={styles.formActions}>
              <button className="button button--primary">
                <Translate>提交回复</Translate>
              </button>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

