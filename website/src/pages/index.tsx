/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import clsx from 'clsx';
import LiteYouTubeEmbed from 'react-lite-youtube-embed';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl, {useBaseUrlUtils} from '@docusaurus/useBaseUrl';

import Image from '@theme/IdealImage';
import Layout from '@theme/Layout';

import Tweet from '@site/src/components/Tweet';
import Tweets, {type TweetItem} from '@site/src/data/tweets';
import Features, {type FeatureItem} from '@site/src/data/features';
import Heading from '@theme/Heading';

import styles from './styles.module.css';
import 'react-lite-youtube-embed/dist/LiteYouTubeEmbed.css';

function HeroBanner() {
  return (
    <div className={styles.hero}>
      <div className={styles.heroInner}>
        <Heading as="h1" className={styles.heroProjectTagline}>
          <img
            alt={translate({message: 'Jiuwen Logo'})}
            className={styles.heroLogo}
            src={useBaseUrl('/img/jiuwen-logo.svg')}
            width="160"
            height="160"
          />
          <span
            className={styles.heroTitleTextHtml}
            // eslint-disable-next-line react/no-danger
            dangerouslySetInnerHTML={{
              __html: translate({
                id: 'homepage.hero.title',
                message:
                  '下一代AI智能体开发平台 <b>九问</b>',
                description:
                  'Home page hero title, can contain simple html tags',
              }),
            }}
          />
        </Heading>
        <p className={styles.heroSubtitle}>
          <Translate>
            为开发者提供强大、易用、高效的AI应用开发工具和解决方案
          </Translate>
        </p>
        <div className={clsx(styles.indexCtas, 'jiuwen-hero-buttons')}>
          <Link className="button button--primary button--lg jiuwen-btn-primary" to="/docs-page">
            <Translate>开始使用</Translate>
          </Link>
          <Link className="button button--outline button--lg jiuwen-btn-outline" to="/news">
            <Translate>最新动态</Translate>
          </Link>
          <Link className="button button--outline button--lg jiuwen-btn-outline" to="/community">
            <Translate>加入社区</Translate>
          </Link>
        </div>
      </div>
    </div>
  );
}

// 项目介绍区块 - 简洁风格
function ProjectIntroSection() {
  return (
    <div className={clsx(styles.section, 'jiuwen-intro-section')}>
      <div className="container">
        <div className="row">
          <div className="col col--10 col--offset-1">
            <Heading as="h2" className={clsx('margin-bottom--lg', 'text--center')}>
              <Translate>关于九问</Translate>
            </Heading>
            <div className="text--center padding-horiz--md">
              <p className={styles.introText}>
                <Translate>
                  九问（Jiuwen）致力于打造下一代AI智能体开发平台，为开发者提供强大、易用、高效的AI应用开发工具和解决方案。
                  我们提供完整的开发框架、丰富的API接口、完善的文档和活跃的社区支持，帮助开发者快速构建和部署大模型应用。
                </Translate>
              </p>
              <div className="margin-top--xl">
                <Link className="button button--primary button--lg" to="/docs-page">
                  <Translate>查看文档</Translate>
                </Link>
                <Link className="button button--secondary button--lg margin-left--sm" to="/community">
                  <Translate>加入社区</Translate>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// 新闻资讯区块
function NewsSection() {
  return (
    <div className={clsx(styles.section, styles.sectionAlt, 'jiuwen-news-section')}>
      <div className="container">
        <div className="row">
          <div className="col">
            <Heading as="h2" className={clsx('margin-bottom--lg', 'text--center')}>
              <Translate>最新动态</Translate>
            </Heading>
            <div className="row">
              <div className="col col--4">
                <div className="card margin-bottom--md">
                  <div className="card__header">
                    <h3><Translate>平台更新</Translate></h3>
                  </div>
                  <div className="card__body">
                    <p><Translate>最新版本发布，带来更多功能和性能优化...</Translate></p>
                    <Link to="/news" className="button button--link">
                      <Translate>了解更多 →</Translate>
                    </Link>
                  </div>
                </div>
              </div>
              <div className="col col--4">
                <div className="card margin-bottom--md">
                  <div className="card__header">
                    <h3><Translate>社区活动</Translate></h3>
                  </div>
                  <div className="card__body">
                    <p><Translate>参与我们的社区活动，与开发者交流分享...</Translate></p>
                    <Link to="/community" className="button button--link">
                      <Translate>查看日历 →</Translate>
                    </Link>
                  </div>
                </div>
              </div>
              <div className="col col--4">
                <div className="card margin-bottom--md">
                  <div className="card__header">
                    <h3><Translate>技术博客</Translate></h3>
                  </div>
                  <div className="card__body">
                    <p><Translate>阅读最新的技术文章和最佳实践...</Translate></p>
                    <Link to="/blog-page" className="button button--link">
                      <Translate>阅读更多 →</Translate>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
            <div className="text--center margin-top--lg">
              <Link className="button button--primary" to="/news">
                <Translate>查看所有动态</Translate>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


function VideoContainer() {
  return (
    <div className="container text--center margin-top--xl">
      <div className="row">
        <div className="col">
          <Heading as="h2">
            <Translate>Check it out in the intro video</Translate>
          </Heading>
          <div className="video-container">
            <LiteYouTubeEmbed
              id="_An9EsKPhp0"
              params="autoplay=1&autohide=1&showinfo=0&rel=0"
              title="Explain Like I'm 5: Jiuwen"
              poster="maxresdefault"
              webp
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function Feature({
  feature,
  className,
}: {
  feature: FeatureItem;
  className?: string;
}) {
  const {withBaseUrl} = useBaseUrlUtils();

  return (
    <div className={clsx('col', className)}>
      <img
        className={styles.featureImage}
        alt={feature.title}
        width={Math.floor(feature.image.width)}
        height={Math.floor(feature.image.height)}
        src={withBaseUrl(feature.image.src)}
        loading="lazy"
      />
      <Heading as="h3" className={clsx(styles.featureHeading)}>
        {feature.title}
      </Heading>
      <p className="padding-horiz--md">{feature.text}</p>
    </div>
  );
}

function FeaturesContainer() {
  const firstRow = Features.slice(0, 3);
  const secondRow = Features.slice(3);

  return (
    <div className="container text--center">
      <Heading as="h2" className={clsx('margin-bottom--xl', 'text--center')}>
        <Translate>为什么选择九问</Translate>
      </Heading>
      <div className="row margin-top--lg margin-bottom--lg">
        {firstRow.map((feature, idx) => (
          <Feature feature={feature} key={idx} />
        ))}
      </div>
      <div className="row">
        {secondRow.map((feature, idx) => (
          <Feature
            feature={feature}
            key={idx}
            className={clsx('col--4', idx === 0 && 'col--offset-2')}
          />
        ))}
      </div>
    </div>
  );
}

function TopBanner() {
  // TODO We should be able to strongly type customFields
  //  Refactor to use a CustomFields interface + TS declaration merging
  const announcedVersion = useDocusaurusContext().siteConfig.customFields
    ?.announcedVersion as string;

  return (
    <div className={styles.topBanner}>
      <div className={styles.topBannerTitle}>
        {'🎉\xa0'}
        <Link
          to={`/blog/releases/${announcedVersion}`}
          className={styles.topBannerTitleText}>
          <Translate
            id="homepage.banner.launch.newVersion"
            values={{newVersion: announcedVersion}}>
            {'Jiuwen\xa0{newVersion} is\xa0out!️'}
          </Translate>
        </Link>
        {'\xa0🥳'}
      </div>
      {/*
      <div style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap'}}>
        <div style={{flex: 1, whiteSpace: 'nowrap'}}>
          <div className={styles.topBannerDescription}>
            We are on{' '}
            <b>
              <Link to="https://www.producthunt.com/posts/docusaurus-2-0">
                ProductHunt
              </Link>{' '}
              and{' '}
              <Link to="https://news.ycombinator.com/item?id=32303052">
                Hacker News
              </Link>{' '}
              today!
            </b>
          </div>
        </div>
        <div
          style={{
            flexGrow: 1,
            flexShrink: 0,
            padding: '0.5rem',
            display: 'flex',
            justifyContent: 'center',
          }}>
          <ProductHuntCard />
          <HackerNewsIcon />
        </div>
      </div>
      */}
    </div>
  );
}

export default function Home(): ReactNode {
  const {
    siteConfig: {customFields, tagline},
  } = useDocusaurusContext();
  const {description} = customFields as {description: string};
  return (
    <Layout title={tagline} description={description}>
      <main>
        <HeroBanner />
        <ProjectIntroSection />
        <div className={styles.section}>
          <FeaturesContainer />
        </div>
        <NewsSection />
      </main>
    </Layout>
  );
}
