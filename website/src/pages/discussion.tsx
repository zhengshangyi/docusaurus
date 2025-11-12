/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import {useState} from 'react';
import {useHistory} from '@docusaurus/router';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';
import clsx from 'clsx';
import styles from './discussion.module.css';

export default function Discussion(): ReactNode {
  const history = useHistory();
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    content: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // 这里可以添加提交逻辑
    // 提交成功后跳转到列表页
    history.push('/discussion-list');
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => {
    const {name, value} = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <Layout
      title="讨论区"
      description="九问社区讨论区，发布问题、参与讨论">
      <main className="container margin-vert--lg">
        <Breadcrumbs
          items={[
            {label: '社区', to: '/community'},
            {label: '讨论区', to: '/discussion-list'},
            {label: '发布问题'},
          ]}
        />
        <div className={styles.detailHeader}>
          <Link className="button button--outline" to="/discussion-list">
            <Translate>← 返回列表</Translate>
          </Link>
        </div>
        <Heading as="h1" className="margin-top--lg margin-bottom--lg">
          <Translate>发布问题</Translate>
        </Heading>

        <div className="row">
          <div className="col col--8">
            <div className="card margin-bottom--lg">
              <div className="card__header">
                <Heading as="h2">
                  <Translate>问题信息</Translate>
                </Heading>
              </div>
              <div className="card__body">
                <form onSubmit={handleSubmit}>
                  <div className="margin-bottom--md">
                    <label htmlFor="title" className="margin-bottom--sm">
                      <strong>
                        <Translate>问题标题</Translate>
                      </strong>
                    </label>
                    <input
                      type="text"
                      id="title"
                      name="title"
                      className={clsx('input', styles.input)}
                      placeholder="请输入问题标题"
                      value={formData.title}
                      onChange={handleChange}
                      required
                    />
                  </div>

                  <div className="margin-bottom--md">
                    <label htmlFor="category" className="margin-bottom--sm">
                      <strong>
                        <Translate>问题分类</Translate>
                      </strong>
                    </label>
                    <select
                      id="category"
                      name="category"
                      className={clsx('input', styles.select)}
                      value={formData.category}
                      onChange={handleChange}
                      required>
                      <option value="">
                        <Translate>请选择分类</Translate>
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

                  <div className="margin-bottom--md">
                    <label htmlFor="content" className="margin-bottom--sm">
                      <strong>
                        <Translate>问题描述</Translate>
                      </strong>
                    </label>
                    <textarea
                      id="content"
                      name="content"
                      className={clsx('textarea', styles.textarea)}
                      rows={8}
                      placeholder="请详细描述您的问题..."
                      value={formData.content}
                      onChange={handleChange}
                      required
                    />
                  </div>

                  <div className={styles.formActions}>
                    <button
                      type="submit"
                      className="button button--primary button--lg">
                      <Translate>发布问题</Translate>
                    </button>
                    <button
                      type="button"
                      className="button button--secondary button--lg margin-left--sm"
                      onClick={() => {
                        setFormData({title: '', category: '', content: ''});
                      }}>
                      <Translate>重置</Translate>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <div className="col col--4">
            <div className="card">
              <div className="card__header">
                <Heading as="h3">
                  <Translate>帮助提示</Translate>
                </Heading>
              </div>
              <div className="card__body">
                <ul>
                  <li>
                    <Translate>
                      在发布问题前，请先搜索是否已有类似问题
                    </Translate>
                  </li>
                  <li>
                    <Translate>
                      问题标题要简洁明了，能够准确描述问题
                    </Translate>
                  </li>
                  <li>
                    <Translate>
                      问题描述要详细，包括复现步骤、预期结果和实际结果
                    </Translate>
                  </li>
                  <li>
                    <Translate>
                      如果是 Bug，请提供环境信息和错误日志
                    </Translate>
                  </li>
                </ul>
              </div>
            </div>

            <div className="card margin-top--md">
              <div className="card__header">
                <Heading as="h3">
                  <Translate>常见问题</Translate>
                </Heading>
              </div>
              <div className="card__body">
                <p className="text--sm text--muted">
                  <Translate>
                    常见问题列表将在此处显示...
                  </Translate>
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

