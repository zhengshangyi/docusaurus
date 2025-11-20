import type {ReactNode} from 'react';
import {useState, useEffect} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Translate from '@docusaurus/Translate';
import Breadcrumbs from '@site/src/components/Breadcrumbs';
import articalBox from '@site/src/css/artical.module.css';

export default function BlogArticlePage(): ReactNode {
  // 相关文章数据
  const relatedArticles = [
    { title: 'Volcano v1.12.0正式发布', href: '/zh/blog/volcano-1.12.0-release/' },
    { title: 'Volcano v1.11.0正式发布', href: '/zh/blog/volcano-1.11.0-release/' },
    { title: 'Volcano v1.10.0正式发布', href: '/zh/blog/volcano-1.10.0-release/' },
    { title: 'Volcano v1.9.0正式发布', href: '/zh/blog/volcano-1.9.0-release/' },
    { title: 'Volcano v1.8.2正式发布', href: '/zh/blog/volcano-1.8.2-release/' },
  ];

  const Artical_1 = {
    id: "1",
    title: 'openJiuwen v1.13 重磅发布',
    author: "openJiuwen官方",
    view_count: 1000,
    updated_at: "2023-12-12",
    created_at: "2023-12-12",
  };

  // 使用useState和useEffect来管理内容
  const [markdownContent, setMarkdownContent] = useState<ReactNode>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // 在组件挂载时设置内容
  useEffect(() => {
    // 避免使用动态导入，直接使用静态内容
    setLoading(true);
    try {
      // 在Docusaurus中，通常不会直接从外部路径导入文件
      // 而是应该将内容放在docs目录下或直接在组件中定义
      setMarkdownContent(
        <div>
          <h2>openJiuwen v1.13 重磅发布！</h2>
          <p>大模型训练与推理等调度能力全面增强</p>
          <p>本次更新带来了多项重要功能改进和性能优化，包括：</p>
          <ul>
            <li>增强的大模型训练调度能力</li>
            <li>优化的推理性能</li>
            <li>更好的资源利用效率</li>
          </ul>
        </div>
      );
    } catch (error) {
      console.error('Error setting content:', error);
      setMarkdownContent(
        <div>
          <p>无法显示文章内容。</p>
        </div>
      );
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <Layout
      title="博客"
      description="九问平台博客">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '博客', to: '/blog-page'}, {label: 'openJiuwen v1.13 重磅发布', to: '/blogs/blog-artical-1'}]} />
        <div className={articalBox.articalContainer}>
            <div className={articalBox.leftRow}>
                {/* 左侧边栏 */}
                {/* 作者信息 */}
                <div className={articalBox.authorPic}>
                    {/* 根据作者名称选择不同的图片 */}
                    {Artical_1.author === "openJiuwen官方" ? (
                        <img src="/img/blog/artical/jiuwen_logo.png" alt="作者" />
                    ) : (
                        <img src="/img/blog/artical/default_author.png" alt="作者" />
                    )}
                </div>
                <div className={articalBox.authorMedia}>
                    <img src="/img/blog/artical/mail.png" alt="邮件" className={articalBox.Icon} />
                    <img src="/img/blog/artical/gitee.svg" alt="Gitee" className={articalBox.Icon} />
                    <img src="/img/blog/artical/wechat.png" alt="微信" className={articalBox.Icon} />
                </div>
                <div className={articalBox.relatedArticles}>
                    <Heading as="h3" className={articalBox.relatedArticlesTitle}>相关文章</Heading>
                    <ul className={articalBox.relatedArticlesList}>
                        {relatedArticles.map((article, index) => (
                            <li key={index}>
                                <a href={article.href}>{article.title}</a>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
            <div className={articalBox.rightRow}>
                {/* 右侧边栏 */}
                <div className={articalBox.articalContent}>
                    <h1 className={articalBox.articalTitle}>{Artical_1.title}</h1>
                    <p className={articalBox.articalMeta}>
                        作者：{Artical_1.author} &nbsp;&nbsp;
                        查看次数：{Artical_1.view_count} &nbsp;&nbsp;
                        更新时间：{Artical_1.updated_at} &nbsp;&nbsp;
                        创建时间：{Artical_1.created_at}
                    </p>
                    <div className={articalBox.articalBody}>
                        {loading ? (
                          <div className={articalBox.loading}>加载中...</div>
                        ) : (
                          <div>{markdownContent}</div>
                        )}
                    </div>
                </div>
            </div>
        </div>
        {/* 回到顶部 */}
        <div className={articalBox.backToTop}>
            <a href="#top" className={articalBox.backToTopText}> 回到顶部 </a>
            <img src="/img/blog/artical/up.png" alt="向上" className={articalBox.backToTopIcon} />
        </div>
      </main>
    </Layout>
  );
}
