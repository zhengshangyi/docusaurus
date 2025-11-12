/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import React, {type ReactNode} from 'react';
import Translate, {translate} from '@docusaurus/Translate';

export type FeatureItem = {
  title: string;
  image: {
    src: string;
    width: number;
    height: number;
  };
  text: ReactNode;
};

const FEATURES: FeatureItem[] = [
  {
    title: translate({
      message: '极简开发',
      id: 'homepage.features.simple-development.title',
    }),
    image: {
      src: '/img/undraw_workflow.svg',
      width: 1009.54,
      height: 717.96,
    },
    text: (
      <Translate
        id="homepage.features.simple-development.text"
        values={{
          workflow: <strong>Workflow高效编排</strong>,
          prompt: <strong>Prompt模板智能生成</strong>,
          analysis: <strong>应用Top-down观测分析</strong>,
        }}>
        {'{workflow}、{prompt}、{analysis}，让开发更简单高效。'}
      </Translate>
    ),
  },
  {
    title: translate({
      message: '高成功率',
      id: 'homepage.features.high-success-rate.title',
    }),
    image: {
      src: '/img/undraw_success.svg',
      width: 1108,
      height: 731.18,
    },
    text: (
      <Translate
        id="homepage.features.high-success-rate.text"
        values={{
          fill: <strong>Prompt智能填充</strong>,
          correct: <strong>插件调用参数修正</strong>,
          mine: <strong>插件关系智能挖掘与层次检索</strong>,
        }}>
        {'{fill}、{correct}、{mine}，提升应用成功率。'}
      </Translate>
    ),
  },
  {
    title: translate({
      message: '高性能',
      id: 'homepage.features.high-performance.title',
    }),
    image: {
      src: '/img/undraw_performance.svg',
      width: 1038.23,
      height: 693.31,
    },
    text: (
      <Translate
        id="homepage.features.high-performance.text"
        values={{
          engine: <strong>实时计算图引擎</strong>,
          sandbox: <strong>高性能隔离执行沙箱</strong>,
        }}>
        {'{engine}、{sandbox}，确保应用运行流畅稳定。'}
      </Translate>
    ),
  },
  {
    title: translate({
      message: '活跃的社区',
      id: 'homepage.features.active-community.title',
    }),
    image: {
      src: '/img/undraw_community.svg',
      width: 1137.97,
      height: 736.21,
    },
    text: (
      <Translate id="homepage.features.active-community.text">
        活跃的开发者社区，提供技术支持、经验分享和最佳实践，帮助开发者共同成长。
      </Translate>
    ),
  },
  {
    title: translate({
      message: '安全可靠',
      id: 'homepage.features.secure-reliable.title',
    }),
    image: {
      src: '/img/undraw_security.svg',
      width: 1137,
      height: 776.59,
    },
    text: (
      <Translate id="homepage.features.secure-reliable.text">
        完善的安全机制和可靠性保障，确保应用和数据的安全稳定运行。
      </Translate>
    ),
  },
];

export default FEATURES;
