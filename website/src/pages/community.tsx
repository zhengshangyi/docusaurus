/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Breadcrumbs from '@site/src/components/Breadcrumbs';
import styles from './styles.module.css';

// Jiuwen开发者日历区块
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
      title: 'openJiuwen 技术分享会', 
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
    <div className={clsx('jiuwen-calendar-section')} style={{padding: '0'}}>
      <div className="container">
        <div className="row">
          <div className="col">
            <Heading as="h2" className="margin-bottom--lg">
              <Translate>openJiuwen社区日历</Translate>
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
                          [styles.calendarDayOtherMonth]: !day.isCurrentMonth,
                          [styles.calendarDayToday]: isToday,
                          [styles.calendarDayHasEvent]: dayEvents.length > 0,
                          [styles.calendarDaySelected]: isSelected,
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
                    className={clsx(styles.calendarTab, {[styles.calendarTabActive]: activeTab === 'all'})}
                    onClick={() => setActiveTab('all')}
                    type="button">
                    <img src={allIconUrl} alt="全部" className={styles.calendarTabIcon} />
                    <Translate>全部</Translate>
                  </button>
                  <button
                    className={clsx(styles.calendarTab, {[styles.calendarTabActive]: activeTab === 'meeting'})}
                    onClick={() => setActiveTab('meeting')}
                    type="button">
                    <img src={meetingIconUrl} alt="会议" className={styles.calendarTabIcon} />
                    <Translate>会议</Translate>
                  </button>
                  <button
                    className={clsx(styles.calendarTab, {[styles.calendarTabActive]: activeTab === 'activity'})}
                    onClick={() => setActiveTab('activity')}
                    type="button">
                    <img src={activityIconUrl} alt="活动" className={styles.calendarTabIcon} />
                    <Translate>活动</Translate>
                  </button>
                  <button
                    className={clsx(styles.calendarTab, {[styles.calendarTabActive]: activeTab === 'peak'})}
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
                            [styles.calendarEventExpandIconExpanded]: isExpanded
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
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Community(): ReactNode {
  return (
    <Layout
      title="社区"
      description="加入openJiuwen社区，参与讨论、分享经验、查看社区日历">
      <main className="container margin-vert--lg">
        <Breadcrumbs items={[{label: '社区'}]} />
        <Heading as="h1">
          <Translate>openJiuwen社区</Translate>
        </Heading>
        
        <div className="margin-top--md">
          <div className="card">
            <div className="card__header">
              <Heading as="h2" className="margin-bottom--none">
                <Translate>社区介绍</Translate>
              </Heading>
            </div>
            <div className="card__body">
              <p className="text--lg margin-bottom--md">
                <Translate>
                  openJiuwen社区是一个活跃的开发者社区，致力于大模型应用开发的交流与分享。
                  在这里，你可以：
                </Translate>
              </p>
              <ul className="margin-bottom--none">
                <li><Translate>与其他开发者交流经验和最佳实践</Translate></li>
                <li><Translate>获取最新的技术资讯和平台更新</Translate></li>
                <li><Translate>参与社区活动和线上/线下会议</Translate></li>
                <li><Translate>贡献代码、文档和示例</Translate></li>
                <li><Translate>获得技术支持和帮助</Translate></li>
              </ul>
            </div>
          </div>
        </div>

        <div className="margin-top--lg">
          <DeveloperCalendarSection />
        </div>

        <div className="margin-top--lg">
          <Heading as="h2">
            <Translate>互动与交流</Translate>
          </Heading>
          <div className="row margin-top--md">
            <div className="col col--4">
              <div className="card">
                <div className="card__header">
                  <h3><Translate>Gitee</Translate></h3>
                </div>
                <div className="card__body">
                  <p><Translate>在 Gitee 上查看源代码、提交 Issue 和 Pull Request</Translate></p>
                  <Link className="button button--primary button--lg jiuwen-btn-primary" to="https://gitee.com/testmyai/test-agentcore" target="_blank" rel="noopener noreferrer">
                    <Translate>访问 Gitee</Translate>
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
                  <Link 
                    className="button button--primary button--lg jiuwen-btn-primary" 
                    to="https://gitee.com/testmyai/test-agentcore" 
                    target="_blank"
                    rel="noopener noreferrer">
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
                  <Link className="button button--primary button--lg jiuwen-btn-primary" to="/contribute">
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

