/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import clsx from 'clsx';
import styles from './styles.module.css';

type BreadcrumbItem = {
  label: string;
  to?: string;
};

type BreadcrumbsProps = {
  items: BreadcrumbItem[];
};

export default function Breadcrumbs({items}: BreadcrumbsProps): ReactNode {
  if (items.length === 0) {
    return null;
  }

  return (
    <nav className={clsx('breadcrumbs', styles.breadcrumbs)} aria-label="面包屑导航">
      <ul className={styles.breadcrumbList}>
        <li className={styles.breadcrumbItem}>
          <Link to="/" className={styles.breadcrumbLink}>
            <Translate>首页</Translate>
          </Link>
        </li>
        {items.map((item, index) => (
          <li key={index} className={styles.breadcrumbItem}>
            <span className={styles.breadcrumbSeparator}>/</span>
            {item.to && index < items.length - 1 ? (
              <Link to={item.to} className={styles.breadcrumbLink}>
                {item.label}
              </Link>
            ) : (
              <span className={styles.breadcrumbCurrent}>{item.label}</span>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}

