/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import React from 'react';
import clsx from 'clsx';
import LiteYouTubeEmbed from 'react-lite-youtube-embed';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl, {useBaseUrlUtils} from '@docusaurus/useBaseUrl';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

import Image from '@theme/IdealImage';
import Layout from '@theme/Layout';
import {useAuth} from '@site/src/contexts/AuthContext';

import Tweet from '@site/src/components/Tweet';
import Tweets, {type TweetItem} from '@site/src/data/tweets';
import Features, {type FeatureItem} from '@site/src/data/features';
import Heading from '@theme/Heading';

import styles from './styles.module.css';
import VideoBox from '@site/src/css/videobox.module.css'
import CommunityBox from '@site/src/css/community.module.css'
import SolutionsBox from '@site/src/css/solutions.module.css'
import JoinBox from '@site/src/css/join.module.css'
import PartnersBox from '@site/src/css/partner.module.css'
import ContactBox from '@site/src/css/contact.module.css'
import 'react-lite-youtube-embed/dist/LiteYouTubeEmbed.css';

function HeroBanner() {
  return (
    <div className={styles.hero}>
      <div className={styles.heroInner}>
        <Heading as="h1" className={styles.heroProjectTagline}>
          <img
            alt={translate({message: 'openJiuwen Logo'})}
            className={styles.heroLogo}
            src={useBaseUrl('/img/jiuwen-logo.svg')}
            width="120"
            height="120"
          />
          <span
            className={styles.heroTitleTextHtml}
            // eslint-disable-next-line react/no-danger
            dangerouslySetInnerHTML={{
              __html: translate({
                id: 'homepage.hero.title',
                message:
                  '九问大模型应用开发平台',
                description:
                  'Home page hero title, can contain simple html tags',
              }),
            }}
          />
        </Heading>
        <p className={styles.heroSubtitle}>
          <Translate>
            打造开发、运行、调优一站式Agent平台
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

// openJiuwen项目介绍区块
function ProjectIntroSection() {
  const videoUrl = 'https://openharmony-official-website.obs.cn-north-4.myhuaweicloud.com/testing/oh_webiste/video/%E5%BC%80%E6%BA%90%E9%B8%BF%E8%92%99%E5%AE%A3%E4%BC%A0%E7%89%872025_0616final.mp4';
  
  return (
    <div className={clsx(VideoBox.openjiuwenIntroSection, 'openjiuwen-intro-section')}>
      {/* 主内容区域 */}
      <div className="container">
        {/* 开启openJiuwen之旅 */}
        <div className={VideoBox.introTitle}>
          <Heading as="h2" className={VideoBox.title}> 
            <Translate>开启openJiuwen之旅</Translate>
          </Heading>
        </div>

        <div className={VideoBox.mainBox}>
          <div className={VideoBox.contentWrapper}>
            {/* 上方内容 */}
            <div className={VideoBox.topContent}>
              <Heading as="h1" className={VideoBox.title}> 
                <Translate>openJiuwen项目简介</Translate>
              </Heading>
              <div className={VideoBox.description}>
                <Translate>
                openJiuwen作为开源大语言模型应用开发框架，致力于提供灵活、强大且易用的
                AI Agent开发与运行能力。基于该框架，开发者可以快速构建处理各类简单或复杂任务
                的AI Agent，实现多Agent协同交互，高效开发生产级可靠AI Agent；并助力企业
                与个人快速搭建AI Agent系统或平台，推动商用级Agentic AI技术广泛应用与落地。
                </Translate>
              </div>
              <button type="button" className={VideoBox.moreBtn}>
                <span><Translate>了解更多</Translate></span>
              </button>
            </div>
            
            {/* 下方视频区域 */}
            <div className={VideoBox.videoContainer}>
              <div className={VideoBox.videoPlaceholder}>
                <div className={VideoBox.videoThumbnail} style={{ backgroundColor: 'black', height: '450px' }}></div>
                <div className={VideoBox.playIcon} />
              </div>
              <video src={videoUrl} className={VideoBox.videoPlayer} controls>
                <track kind="captions" srcLang="zh-CN" label="中文字幕" />
              </video>
            </div>
          </div>
        </div>
        
        {/* 功能盒子区域 */}
        <div className={VideoBox.boxesContainer}>
          {/* 下载盒子 */}
          <div className={VideoBox.box}>
            <div className={VideoBox.boxContent}>
              <div className={VideoBox.imageWrapper}>
                <img 
                  src="/img/svgs/downloading.svg" 
                  alt="下载" 
                  className="box-image"
                />
              </div>
              <Heading as="h3" className={VideoBox.boxTitle}>
                <Translate>下载</Translate>
              </Heading>
              <p className={VideoBox.boxDescription}>
                <Translate>开启openJiuwen开发之旅</Translate>
              </p>
            </div>
          </div>
          
          {/* 体验盒子 */}
          <div className={VideoBox.box}>
            <div className={VideoBox.boxContent}>
              <div className={VideoBox.imageWrapper}>
                <img 
                  src="/img/svgs/experience.svg" 
                  alt="体验" 
                  className="box-image"
                />
              </div>
              <Heading as="h3" className={VideoBox.boxTitle}>
                <Translate>体验</Translate>
              </Heading>
              <p className={VideoBox.boxDescription}>
                <Translate>体验openJiuwen开发乐趣</Translate>
              </p>
            </div>
          </div>

          {/* 文档盒子 */}
          <div className={VideoBox.box}>
            <div className={VideoBox.boxContent}>
              <div className={VideoBox.imageWrapper}>
                <img 
                  src="/img/svgs/documents.svg" 
                  alt="文档" 
                  className="box-image"
                />
              </div>
              <Heading as="h3" className={VideoBox.boxTitle}>
                <Translate>文档</Translate>
              </Heading>
              <p className={VideoBox.boxDescription}>
                <Translate>查看openJiuwen文档</Translate>
              </p>
            </div>
          </div>
          
          {/* 社区盒子 */}
          <div className={VideoBox.box}>
            <div className={VideoBox.boxContent}>
              <div className={VideoBox.imageWrapper}>
                <img 
                  src="/img/svgs/community.svg" 
                  alt="社区" 
                  className="box-image"
                />
              </div>
              <Heading as="h3" className={VideoBox.boxTitle}>
                <Translate>社区</Translate>
              </Heading>
              <p className={VideoBox.boxDescription}>
                <Translate>加入openJiuwen开发者社区</Translate>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// 社区活力数据展示组件
function CommunityVitalitySection(): ReactNode {
  const communityStats = [
    { number: '722,861', text: '合并请求', englishText: 'PR' },
    { number: '9,517', text: '代码贡献者', englishText: 'Contributor' },
    { number: '31,405', text: '项目点赞', englishText: 'Star' },
    { number: '126,694', text: '仓库克隆', englishText: 'Fork' },
    { number: '70', text: '特别兴趣小组', englishText: 'Sig' },
  ];

  return (
    <section className={CommunityBox.communityVitalitySection}>
      <div className={CommunityBox.communityContainer}>
        <div className={CommunityBox.communityTitle}>
          <Heading as="h2" className={CommunityBox.title}>  
            <Translate>社区活力</Translate>
          </Heading>
        </div>

        <div className={CommunityBox.communityMainBox}>
          <div className={CommunityBox.communityContentWrapper}>
            {communityStats.map((stat, index) => (
              <div key={index} className={CommunityBox.communityContentItem}>
                <div className={CommunityBox.communityNumber}>{stat.number}</div>
                <div className={CommunityBox.communityText}>
                  <div>{stat.text}</div>
                  <div>{stat.englishText}</div>
                </div>
              </div>
            ))}
          </div>
          <div className={CommunityBox.communityViewMoreResults}>
            <span> 查看贡献详情 </span>
            <i className="el-icon" style={{width: '24px', height: '24px', marginBottom: '2px'}}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" transform="translate(0, 1)">
                <path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path>
              </svg>
            </i>
          </div>
        </div>
        <div className={CommunityBox.communityCheckMore}>
          <button className={CommunityBox.communityMoreBtn}>
            <span> 前往SIG中心 </span>
          </button>
        </div>
      </div>
    </section>
  );
}

// 解决方案展示组件
function SolutionsSection(): ReactNode {
  const [activeIndex, setActiveIndex] = React.useState(0);
  const [solutions] = React.useState([
    {
      id: 1,
      title: '物联解决方案',
      description: '基于openJiuwen的Agent平台技术，变电站设备实现自发现、自组网并构建边缘计算能力。',
      imageUrl: '/img/pngs/ICBC.png',
      logoUrl: '/img/pngs/ICBC_logo.png'
    },
    {
      id: 2,
      title: '交通解决方案',
      description: '基于openJiuwen的智能交通监控系统，实现交通流量分析、智能信号灯控制和车辆识别。',
      imageUrl: '/img/pngs/ICBC.png',
      logoUrl: '/img/pngs/ICBC_logo.png'
    },
    {
      id: 3,
      title: '教育解决方案',
      description: '基于openJiuwen的智慧教育平台，提供在线教学、智能管理和个性化学习体验。',
      imageUrl: '/img/pngs/ICBC.png',
      logoUrl: '/img/pngs/ICBC_logo.png'
    },
    {
      id: 4,
      title: '金融解决方案',
      description: '基于openJiuwen的AI金融安全系统，实现支付安全、身份认证和风险控制。',
      imageUrl: '/img/pngs/ICBC.png',
      logoUrl: '/img/pngs/ICBC_logo.png'
    }
  ]);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % solutions.length);
    }, 8000);
    return () => clearInterval(interval);
  }, [solutions.length]);

  const handleIndicatorClick = (index: number) => {
    setActiveIndex(index);
  };

  const currentSolution = solutions[activeIndex];

  return (
    <section className={SolutionsBox.solutionsSection}>
      <div className={SolutionsBox.backgroundBox}>
        {solutions.map((solution, index) => (
          <img
            key={solution.id}
            src={solution.imageUrl}
            alt={`${solution.title} background`}
            className={`${SolutionsBox.backgroundImage} ${index === activeIndex ? SolutionsBox.active : ''}`}
          />
        ))}
        
        <div className={SolutionsBox.contentOverlay}>
          <h1 className={SolutionsBox.mainTitle}>解决方案</h1>
          
          <div className={SolutionsBox.contentContainer}>
            <div className={SolutionsBox.solutionContent}>
              <img 
                src={currentSolution?.logoUrl || ''}
                alt="solution logo" 
                className={SolutionsBox.solutionLogo} 
              />
              <h2 className={SolutionsBox.solutionTitle}>{currentSolution?.title ?? ''}</h2>
              <p className={SolutionsBox.solutionDesc}>
                {currentSolution?.description?.split('\n').map((line, i) => (
                  <React.Fragment key={i}>
                    {line}
                    <br />
                  </React.Fragment>
                ))}
              </p>
              <button 
                aria-disabled="false" 
                type="button" 
                className={SolutionsBox.solutionMoreBtn}>
                <span> 查看案例 </span>
              </button>
            </div>
          </div>
          
          <div className={SolutionsBox.indicatorContainer}>
            {solutions.map((_, index) => (
              <div
                key={index}
                className={`${SolutionsBox.indicatorDot} ${index === activeIndex ? SolutionsBox.active : ''}`}
                onClick={() => handleIndicatorClick(index)}
                aria-label={`Go to slide ${index + 1}`}
              />
            ))}
          </div>
          
          <div className={SolutionsBox.solutionCheckMore}>
            <span> 查看更多解决方案 </span>
            <i className="el-icon" style={{width: '24px', height: '24px', marginBottom: '2px'}}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" transform="translate(0, 1)">
                <path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path>
              </svg>
            </i>
          </div>
        </div>
      </div>
    </section>
  );
}

// 加入社区组件
function JoinCommunitySection() {
  return (
    <section className={JoinBox.joinSection}>
      <div className="container">
        <div className={JoinBox.joinTitle}>
          <Heading as="h2" className={JoinBox.title}>  
            <Translate> 加入openJiuwen开发者社区 </Translate>
          </Heading>
        </div>

        <div className={JoinBox.joinSubtitle}>
          <p>
            期待更多伙伴加入，携手共建AI Agent开发新时代。
          </p>
        </div>

        {/* 功能盒子区域 */}
        <div className={JoinBox.boxesContainer}>
          {/* 成为社区贡献者 */}
          <div className={JoinBox.box}>
            <div className={JoinBox.boxContent}>
              <div className={JoinBox.imageWrapper}>
                <img 
                  src="/img/jpgs/join_coder.jpg" 
                  alt="贡献者" 
                  className={JoinBox.boxImage}
                />
              </div>
              <Heading as="h3" className={JoinBox.boxTitle}>
                <Translate> 成为社区贡献者 </Translate>
              </Heading>
              <p className={JoinBox.boxDescription}>
                <Translate> 加入openJiuwen开发者社区，与其他开发者互动，分享知识、交换经验 </Translate>
              </p>
              <div className={JoinBox.joinBtnWrapper}>
                <button className={JoinBox.joinBtn}>
                  <Translate> 贡献攻略 </Translate>
                </button>
                <div className={JoinBox.joinViewMoreResults}>
                  <span> 查看贡献详情 </span>
                  <i className="el-icon" style={{width: '24px', height: '24px', marginBottom: '2px'}}>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" transform="translate(0, 1)">
                      <path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path>
                    </svg>
                  </i>
                </div>
              </div>
            </div>
          </div>

          {/* 成为项目群捐赠人 */}
          <div className={JoinBox.box}>
            <div className={JoinBox.boxContent}>
              <div className={JoinBox.imageWrapper}>
                <img 
                  src="/img/jpgs/join_donate.jpg" 
                  alt="捐赠" 
                  className={JoinBox.boxImage}
                />
              </div>
              <Heading as="h3" className={JoinBox.boxTitle}>
                <Translate> 成为项目群捐赠人 </Translate>
              </Heading>
              <p className={JoinBox.boxDescription}>
                <Translate> 加入openJiuwen项目群，为项目贡献代码、分享经验、获得项目支持 </Translate>
              </p>
              <div className={JoinBox.joinBtnWrapper}>
                <button className={JoinBox.joinBtn}>
                  <Translate> 成员单位 </Translate>
                </button>
                <div className={JoinBox.joinViewMoreResults}>
                  <span> 查看捐赠权益 </span>
                  <i className="el-icon" style={{width: '24px', height: '24px', marginBottom: '2px'}}>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" transform="translate(0, 1)">
                      <path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path>
                    </svg>
                  </i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// Jiuwen开发者日历区块 - 参考 MindSpore 设计
function DeveloperCalendarSection() {
  const [currentDate, setCurrentDate] = React.useState(new Date());
  const [selectedDate, setSelectedDate] = React.useState<Date | null>(null);
  const [activeTab, setActiveTab] = React.useState<'all' | 'meeting' | 'activity' | 'peak'>('all');
  const [expandedEventIndex, setExpandedEventIndex] = React.useState<number | null>(null);
  
  // 在组件顶层调用 hook
  const allIconUrl = useBaseUrl('/img/all.svg');
  const meetingIconUrl = useBaseUrl('/img/metting.svg');
  const activityIconUrl = useBaseUrl('/img/activity.svg');
  const peakIconUrl = useBaseUrl('/img/peak.svg');

  // 示例活动数据 - 分散到2025年11月~12月
  const events = [
    { 
      date: '2025-11-05', 
      title: 'Jiuwen 技术分享会', 
      type: 'meeting',
      organizer: '张工程师',
      platform: '腾讯会议',
      meetingId: '123 456 789',
      joinLink: 'https://meeting.tencent.com/dm/xxx',
      description: '分享最新的AI智能体开发技术和实践经验'
    },
    { 
      date: '2025-11-12', 
      title: '开发者社区活动', 
      type: 'activity',
      organizer: '李开发者',
      platform: '线下活动',
      meetingId: '-',
      joinLink: 'https://community.openjiuwen.com/activity/xxx',
      description: '社区开发者线下交流活动，探讨技术难题'
    },
    { 
      date: '2025-11-18', 
      title: 'AI 技术峰会', 
      type: 'peak',
      organizer: '王技术总监',
      platform: 'Zoom',
      meetingId: '987 654 321',
      joinLink: 'https://zoom.us/j/xxx',
      description: '年度AI技术峰会，汇聚行业专家和开发者'
    },
    { 
      date: '2025-11-25', 
      title: 'SIG 月度会议', 
      type: 'meeting',
      organizer: '赵架构师',
      platform: '钉钉会议',
      meetingId: '456 789 012',
      joinLink: 'https://meeting.dingtalk.com/j/xxx',
      description: 'SIG小组月度例会，讨论项目进展和规划'
    },
    { 
      date: '2025-12-03', 
      title: '社区线下聚会', 
      type: 'activity',
      organizer: '陈社区经理',
      platform: '线下活动',
      meetingId: '-',
      joinLink: 'https://community.openjiuwen.com/meetup/xxx',
      description: '社区成员线下聚会，增进交流与友谊'
    },
    { 
      date: '2025-12-10', 
      title: '开发者大会', 
      type: 'peak',
      organizer: '刘大会主席',
      platform: '飞书会议',
      meetingId: '789 012 345',
      joinLink: 'https://vc.feishu.cn/j/xxx',
      description: '年度开发者大会，展示最新成果和技术趋势'
    },
    { 
      date: '2025-12-15', 
      title: '技术培训课程', 
      type: 'meeting',
      organizer: '周培训师',
      platform: '腾讯会议',
      meetingId: '234 567 890',
      joinLink: 'https://meeting.tencent.com/dm/yyy',
      description: '深入讲解openJiuwen平台的高级功能和使用技巧'
    },
    { 
      date: '2025-12-20', 
      title: '开源贡献者聚会', 
      type: 'activity',
      organizer: '吴开源负责人',
      platform: '线下活动',
      meetingId: '-',
      joinLink: 'https://community.openjiuwen.com/contributor/xxx',
      description: '感谢开源贡献者，分享贡献经验和心得'
    },
    { 
      date: '2025-12-28', 
      title: '年终技术总结会', 
      type: 'meeting',
      organizer: '郑技术负责人',
      platform: '腾讯会议',
      meetingId: '345 678 901',
      joinLink: 'https://meeting.tencent.com/dm/zzz',
      description: '回顾2025年技术发展，展望2026年规划'
    },
  ];

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    const days = [];
    // 填充上个月的日期
    const prevMonth = new Date(year, month - 1, 0);
    const prevMonthDays = prevMonth.getDate();
    for (let i = startingDayOfWeek - 1; i >= 0; i--) {
      days.push({ date: prevMonthDays - i, isCurrentMonth: false });
    }
    // 当前月的日期
    for (let i = 1; i <= daysInMonth; i++) {
      days.push({ date: i, isCurrentMonth: true });
    }
    // 填充下个月的日期
    const remainingDays = 42 - days.length;
    for (let i = 1; i <= remainingDays; i++) {
      days.push({ date: i, isCurrentMonth: false });
    }
    return days;
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' });
  };

  const getEventsForDate = (day: number, isCurrentMonth: boolean) => {
    if (!isCurrentMonth) return [];
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return events.filter(event => event.date === dateStr);
  };

  // 获取未来30天内的活动
  const getUpcomingEvents = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const thirtyDaysLater = new Date(today);
    thirtyDaysLater.setDate(today.getDate() + 30);
    
    return events.filter(event => {
      const eventDate = new Date(event.date);
      eventDate.setHours(0, 0, 0, 0);
      return eventDate >= today && eventDate <= thirtyDaysLater;
    });
  };

  // 获取选中日期的活动
  const getSelectedDateEvents = () => {
    if (!selectedDate) return [];
    const year = selectedDate.getFullYear();
    const month = selectedDate.getMonth() + 1;
    const day = selectedDate.getDate();
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return events.filter(event => event.date === dateStr);
  };

  const getFilteredEvents = () => {
    // 如果有选中日期，显示该日期的活动
    if (selectedDate) {
      const selectedEvents = getSelectedDateEvents();
      if (activeTab === 'all') return selectedEvents;
      return selectedEvents.filter(event => event.type === activeTab);
    }
    
    // 否则显示未来30天的活动
    const upcomingEvents = getUpcomingEvents();
    if (activeTab === 'all') return upcomingEvents;
    return upcomingEvents.filter(event => event.type === activeTab);
  };

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case 'meeting':
        return meetingIconUrl;
      case 'activity':
        return activityIconUrl;
      case 'peak':
        return peakIconUrl;
      default:
        return allIconUrl;
    }
  };

  const prevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const days = getDaysInMonth(currentDate);
  const weekDays = ['日', '一', '二', '三', '四', '五', '六'];

  return (
    <div className={clsx(styles.section, 'jiuwen-calendar-section')}>
      <div className="container">
        <div className="row">
          <div className="col">
            <Heading as="h2" className={clsx('margin-bottom--lg', 'text--center')}>
              <Translate>Jiuwen开发者日历</Translate>
            </Heading>
            <div className={styles.calendarContainer}>
              <div className={styles.calendarWrapper}>
                <div className={styles.calendarHeader}>
                  <button className={styles.calendarNavButton} onClick={prevMonth} type="button">
                    ‹
                  </button>
                  <h3 className={styles.calendarMonth}>{formatDate(currentDate)}</h3>
                  <button className={styles.calendarNavButton} onClick={nextMonth} type="button">
                    ›
                  </button>
                </div>
                <div className={styles.calendarGrid}>
                  {weekDays.map(day => (
                    <div key={day} className={styles.calendarWeekday}>
                      {day}
                    </div>
                  ))}
                  {days.map((day, index) => {
                    const dayEvents = getEventsForDate(day.date, day.isCurrentMonth);
                    const isToday = day.isCurrentMonth &&
                      day.date === new Date().getDate() &&
                      currentDate.getMonth() === new Date().getMonth() &&
                      currentDate.getFullYear() === new Date().getFullYear();
                    
                    // 判断是否被选中
                    const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day.date);
                    const isSelected = selectedDate && 
                      day.isCurrentMonth &&
                      dayDate.getDate() === selectedDate.getDate() &&
                      dayDate.getMonth() === selectedDate.getMonth() &&
                      dayDate.getFullYear() === selectedDate.getFullYear();
                    
                    // 获取该日期所有事件的类型图标
                    const eventTypes = Array.from(new Set(dayEvents.map(e => e.type)));
                    
                    return (
                      <div
                        key={index}
                        className={clsx(styles.calendarDay, {
                          [`${styles.calendarDayOtherMonth}`]: !day.isCurrentMonth,
                          [`${styles.calendarDayToday}`]: isToday,
                          ...(dayEvents.length > 0 ? { [`${styles.calendarDayHasEvent}`]: true } : {}),
                          [`${styles.calendarDaySelected}`]: isSelected,
                        })}
                        onClick={() => {
                          if (day.isCurrentMonth) {
                            const clickedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day.date);
                            // 如果点击的是已选中的日期，则取消选中
                            if (isSelected) {
                              setSelectedDate(null);
                            } else {
                              setSelectedDate(clickedDate);
                            }
                            // 切换日期时重置展开状态
                            setExpandedEventIndex(null);
                          }
                        }}>
                        <span className={styles.calendarDayNumber}>{day.date}</span>
                        {dayEvents.length > 0 && (
                          <div className={styles.calendarDayEvents}>
                            {eventTypes.map((type, idx) => (
                              <img
                                key={idx}
                                src={getEventTypeIcon(type)}
                                alt={type}
                                className={styles.calendarDayEventIcon}
                              />
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
              <div className={styles.calendarEvents}>
                <div className={styles.calendarEventsHeader}>
                  <h3 className={styles.calendarEventsTitle}>
                    {selectedDate ? (
                      <Translate
                        id="calendar.selectedDate"
                        values={{
                          date: selectedDate.toLocaleDateString('zh-CN', { 
                            year: 'numeric', 
                            month: 'long', 
                            day: 'numeric' 
                          })
                        }}>
                        {'{date} 的活动'}
                      </Translate>
                    ) : (
                      <Translate>近期活动</Translate>
                    )}
                  </h3>
                  {selectedDate && (
                    <button
                      className={styles.calendarClearSelection}
                      onClick={() => {
                        setSelectedDate(null);
                        setExpandedEventIndex(null);
                      }}
                      type="button"
                      title="清除选择">
                      ✕
                    </button>
                  )}
                </div>
                <div className={styles.calendarTabs}>
                  <button
                    className={clsx(styles.calendarTab, {[styles.calendarTabActive as string]: activeTab === 'all'})}
                    onClick={() => setActiveTab('all')}
                    type="button">
                    <img src={allIconUrl} alt="全部" className={styles.calendarTabIcon} />
                    <Translate>全部</Translate>
                  </button>
                  <button
                    className={clsx(styles.calendarTab, activeTab === 'meeting' && styles.calendarTabActive)}
                    onClick={() => setActiveTab('meeting')}
                    type="button">
                    <img src={meetingIconUrl} alt="会议" className={styles.calendarTabIcon} />
                    <Translate>会议</Translate>
                  </button>
                  <button
                    className={clsx(styles.calendarTab, {[styles.calendarTabActive as string]: activeTab === 'activity'})}
                    onClick={() => setActiveTab('activity')}
                    type="button">
                    <img src={activityIconUrl} alt="活动" className={styles.calendarTabIcon} />
                    <Translate>活动</Translate>
                  </button>
                  <button
                    className={clsx(styles.calendarTab, {[styles.calendarTabActive as string]: activeTab === 'peak'})}
                    onClick={() => setActiveTab('peak')}
                    type="button">
                    <img src={peakIconUrl} alt="峰会" className={styles.calendarTabIcon} />
                    <Translate>峰会</Translate>
                  </button>
                </div>
                <div className={styles.calendarEventsList}>
                  {getFilteredEvents().length === 0 ? (
                    <div className={styles.calendarNoEvents}>
                      {selectedDate ? (
                        <Translate>该日期暂无活动</Translate>
                      ) : (
                        <Translate>暂无近期活动</Translate>
                      )}
                    </div>
                  ) : (
                    (selectedDate ? getFilteredEvents() : getFilteredEvents().slice(0, 5)).map((event, index) => {
                      const isExpanded = expandedEventIndex === index;
                      return (
                        <div key={index} className={styles.calendarEventItem}>
                        <div 
                          className={styles.calendarEventHeader}
                          onClick={() => setExpandedEventIndex(isExpanded ? null : index)}
                        >
                          <img
                            src={getEventTypeIcon(event.type)}
                            alt={event.type}
                            className={styles.calendarEventIcon}
                          />
                          <div className={styles.calendarEventContent}>
                            <div className={styles.calendarEventDate}>{event.date}</div>
                            <div className={styles.calendarEventTitle}>{event.title}</div>
                          </div>
                          <span className={clsx(styles.calendarEventExpandIcon, {
                          ...(isExpanded ? { [`${styles.calendarEventExpandIconExpanded}`]: true } : {})
                          })}>
                            ▼
                          </span>
                        </div>
                        {isExpanded && (
                          <div className={styles.calendarEventDetails}>
                            <div className={styles.calendarEventDetailRow}>
                              <span className={styles.calendarEventDetailLabel}>会议名称：</span>
                              <span className={styles.calendarEventDetailValue}>{event.title}</span>
                            </div>
                            <div className={styles.calendarEventDetailRow}>
                              <span className={styles.calendarEventDetailLabel}>发起人：</span>
                              <span className={styles.calendarEventDetailValue}>{event.organizer}</span>
                            </div>
                            <div className={styles.calendarEventDetailRow}>
                              <span className={styles.calendarEventDetailLabel}>平台：</span>
                              <span className={styles.calendarEventDetailValue}>{event.platform}</span>
                            </div>
                            <div className={styles.calendarEventDetailRow}>
                              <span className={styles.calendarEventDetailLabel}>会议ID：</span>
                              <span className={styles.calendarEventDetailValue}>{event.meetingId}</span>
                            </div>
                            <div className={styles.calendarEventDetailRow}>
                              <span className={styles.calendarEventDetailLabel}>参会链接：</span>
                              <a 
                                href={event.joinLink} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className={styles.calendarEventDetailLink}
                              >
                                {event.joinLink}
                              </a>
                            </div>
                            {event.description && (
                              <div className={styles.calendarEventDetailRow}>
                                <span className={styles.calendarEventDetailLabel}>活动描述：</span>
                                <span className={styles.calendarEventDetailValue}>{event.description}</span>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    );
                    })
                  )}
                </div>
                <div className={styles.calendarEventsFooter}>
                  <Link className="button button--outline" to="/community">
                    <Translate>查看完整日历</Translate>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// 合作伙伴区块
function PartnersSection() {
  {/* 合作伙伴区块 */}
  return (
    <section className={PartnersBox.partnersSection}>
      <div className={PartnersBox.partnersTitle}>
        <Heading as="h2" className={PartnersBox.title}>  
          <Translate> openJiuwen合作伙伴 </Translate>
        </Heading>
      </div>
      <div className={PartnersBox.partnersSubtitle}>
        <Translate> 我们的合作伙伴，帮助我们实现了更广泛的影响力和更强大的功能。 </Translate>
      </div>
      <div className={PartnersBox.partnersContainer}>
        <div className={PartnersBox.partnerBox}>
          <img src="/img/partners/ICBC.png" alt="工商银行" />
          <div className={PartnersBox.partnerTag}>
            <Translate> 工商银行 </Translate>
          </div>
        </div>
        <div className={PartnersBox.partnerBox}>
          <img src="/img/partners/zju.png" alt="浙江大学" />
          <div className={PartnersBox.partnerTag}>
            <Translate> 浙江大学 </Translate>
          </div>
        </div>
        <div className={PartnersBox.partnerBox}>
          <img src="/img/partners/rmu.png" alt="中国人民大学" />
          <div className={PartnersBox.partnerTag}>
            <Translate> 中国人民大学 </Translate>
          </div>
        </div>
      </div>
    </section>
  )
}

// 联系方式区块
function ContactSection() {
  return (
    <section className={ContactBox.contactSection}>
      <div className={ContactBox.contactTitle}>
        <Heading as="h2" className={ContactBox.title}>  
          <Translate> 欢迎关注我们 </Translate>
        </Heading>
      </div>
      <div className={ContactBox.contactSubtitle}>
        <Translate> 关注openJiuwen及时获取最新资讯。 </Translate>
      </div>
      <div className={ContactBox.contactContainer}>
        <div className={ContactBox.contactBox}>
          <img src="/img/qrcodes/qrcode_1.png" alt="二维码" />
          <div className={ContactBox.contactText}>
            <Translate> 微信公众号 </Translate>
          </div>
        </div>
        <div className={ContactBox.contactBox}>
          <img src="/img/qrcodes/qrcode_1.png" alt="二维码" />
          <div className={ContactBox.contactText}>
            <Translate> 微信视频号 </Translate>
          </div>
        </div>
        <div className={ContactBox.contactBox}>
          <img src="/img/qrcodes/qrcode_1.png" alt="二维码" />
          <div className={ContactBox.contactText}>
            <Translate> 哔哩哔哩 </Translate>
          </div>
        </div>
      </div>
    </section>
  )
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
            {'openJiuwen\xa0{newVersion} is\xa0out!️'}
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

// 管理导航栏（仅管理员和 root 用户可见）
function AdminNavigation(): ReactNode {
  // 只在客户端检查
  if (!ExecutionEnvironment.canUseDOM) {
    return <></>;
  }

  const {isAdmin, isRoot, loading} = useAuth();

  // 如果正在加载或不是管理员，不显示
  if (loading || !isAdmin) {
    return <></>;
  }

  return (
    <div style={{
      backgroundColor: 'var(--ifm-color-primary)',
      color: 'white',
      padding: '0.75rem 1rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '1.5rem',
      flexWrap: 'wrap',
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
        flexWrap: 'wrap',
      }}>
        <span style={{fontWeight: 600, fontSize: '0.95rem'}}>管理功能：</span>
        <Link
          to="/admin/"
          style={{
            color: 'white',
            textDecoration: 'none',
            padding: '0.4rem 0.8rem',
            borderRadius: '4px',
            backgroundColor: 'rgba(255, 255, 255, 0.2)',
            transition: 'background-color 0.2s',
            fontSize: '0.9rem',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
          }}>
          管理台
        </Link>
        {isRoot && (
          <Link
            to="/admin/users/"
            style={{
              color: 'white',
              textDecoration: 'none',
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              backgroundColor: 'rgba(255, 255, 255, 0.2)',
              transition: 'background-color 0.2s',
              fontSize: '0.9rem',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
            }}>
            用户管理
          </Link>
        )}
      </div>
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
        {/* 管理台功能已暂时隐藏 */}
        {/* <AdminNavigation /> */}
        <HeroBanner />
        <ProjectIntroSection />
        <CommunityVitalitySection />
        <SolutionsSection />
        <JoinCommunitySection />
        <DeveloperCalendarSection />
        <PartnersSection />
        <ContactSection />
      </main>
    </Layout>
  );
}
