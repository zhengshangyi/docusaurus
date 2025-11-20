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
import blogBox from '@site/src/css/blog.module.css'

export default function BlogPage(): ReactNode {
  const BLOG_ITEMS = [
    {
      id: '1',
      title: 'openJiuwen v1.13 重磅发布！大模型训练与推理等调度能力全面增强',
      author: 'openJiuwen官方',
      description: '新增特性：支持LeaderWorkerSet用于大模型推理场景、新增Cron VolcanoJob、支持基于标签的HyperNode自动发现、新增原生Ray框架支持、新增HCCL插件支持、增强NodeGroup功能、引入ResourceStrategyFit插件、混部能力优化等。',
      view_count: 1000,
      created_at: '2023-12-15',
      updated_at: '2023-12-15',
    },
    {
      id: '2',
      title: 'Kubernetes 集群管理最佳实践指南',
      author: 'NickFuryX 个人分享',
      description: '本文介绍了Kubernetes集群管理的最佳实践，包括资源调度优化、安全配置、监控告警设置、备份恢复策略等关键内容，帮助用户构建稳定高效的容器平台。',
      view_count: 1000,
      created_at: '2023-12-10',
      updated_at: '2023-12-10',
    },
    {
      id: '3',
      title: 'openJiuwen v1.12 重磅发布！新增大模型训练与推理等调度能力',
      author: 'openJiuwen官方',
      description: '新增特性：支持LeaderWorkerSet用于大模型推理场景、新增Cron VolcanoJob、支持基于标签的HyperNode自动发现、新增原生Ray框架支持、新增HCCL插件支持、增强NodeGroup功能、引入ResourceStrategyFit插件、混部能力优化等。',
      view_count: 1000,
      created_at: '2023-11-20',
      updated_at: '2023-11-20',
    },
  ];

  const monthName = { '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug', 
    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec' };

  return (
    <Layout
      title="博客"
      description="九问平台博客">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '博客'}]} />
        <Heading as="h1" className={blogBox.blogTitle}>
          <Translate>博客</Translate>
        </Heading>
        <p className={blogBox.blogDescription}>
          <Translate>
            这里提供九问平台的最新动态、技术文章和最佳实践，帮助您快速上手和深入理解平台功能。
          </Translate>
        </p>

        <div className={blogBox.blogContainer}>
          <div className={blogBox.blogItems}>
            {/* 遍历BLOG_ITEMS */}
            {BLOG_ITEMS.map((item: { id: string; title: string; author: string; description: string; 
                          view_count: number; created_at: string; updated_at: string }, index: number) => {
              // 格式化日期，确保日期有前导零
              const dateParts = item.updated_at ? item.updated_at.split('-') : item.created_at.split('-');
              if (dateParts.length !== 3) {
                return null; // 无效日期格式时跳过
              }
              const [year, month = '', day = ''] = dateParts;
              const formattedDay = day.padStart(2, '0');
              const formattedMonth = month.padStart(2, '0');
              
              return (
                <div className={blogBox.blogItem} key={item.id}>
                  <div className={blogBox.blogItemMeta}>
                    <div className={blogBox.blogItemMetaBlock}>
                      <span className={blogBox.blogItemDate}>
                        <div className={blogBox.blogItemDateNumber}>{formattedDay}</div>
                        <div className={blogBox.blogItemDateSeparator}>/</div>
                        <div className={blogBox.blogItemDateYearBlock}>
                          <div className={blogBox.blogItemDateMonth}>{monthName[formattedMonth as keyof typeof monthName]}</div>
                          <div className={blogBox.blogItemDateYear}>{year}</div>
                        </div>
                      </span>
                    </div>
                  </div>
                  <div className={blogBox.blogItemContentBlock}>
                    <div className={blogBox.blogItemContent}>
                      <h3 className={blogBox.blogItemTitleWrapper}>
                        <div className={blogBox.blogItemTitleText}>
                          <a href={`/blogs/blog-artical-${item.id}`}>{item.title}</a>
                        </div>
                        <div className={blogBox.blogItemSubWrapper}>
                          <div className={blogBox.blogItemAuthor}>
                            <img src="/img/blog/author.png" alt="user" className={blogBox.blogItemAuthorIcon} />
                            <span>{item.author}</span>
                          </div>
                          <div className={blogBox.blogItemView}>
                            <img src="/img/blog/watched.png" alt="view" className={blogBox.blogItemViewIcon} />
                            <span className={blogBox.blogItemViewCount}>{item.view_count}</span>
                          </div>
                        </div>
                      </h3>
                      <div className={blogBox.blogItemStyle}>
                        <Translate>
                          {item.description}
                        </Translate>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className={blogBox.blogCheckMore}>
          <span> 查看更多博客 </span>
          <i className="el-icon" style={{width: '24px', height: '24px', marginBottom: '2px'}}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" transform="translate(0, 1)">
              <path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path>
            </svg>
          </i>
        </div>
      </main>
    </Layout>
  );
}

