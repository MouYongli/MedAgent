// components/common/Navigation.tsx

import React from 'react';
import { Menu } from 'antd';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import { HomeOutlined, MessageOutlined, EditOutlined, DashboardOutlined, DatabaseOutlined } from '@ant-design/icons';
import { usePathname } from 'next/navigation';

const AppNav: React.FC = () => {
  const { t } = useTranslation();

  const pathname = usePathname();
  
  let selectedKey = 'home';
  if (pathname.startsWith('/chat')) {
    selectedKey = 'chat';
  } else if (pathname.startsWith('/knowledge')) {
    selectedKey = 'knowledge';
  } else if (pathname.startsWith('/studio')) {
    selectedKey = 'studio';
  } else if (pathname.startsWith('/dashboard')) {
    selectedKey = 'dashboard';
  }

  const menuItems = [
    { key: 'home', icon: <HomeOutlined />, label: <Link href="/">{t('nav.home')}</Link> },
    { key: 'chat', icon: <MessageOutlined />, label: <Link href="/chat">{t('nav.chat')}</Link> },
    { key: 'knowledge', icon: <DatabaseOutlined />, label: <Link href="/knowledge">{t('nav.knowledge')}</Link> },
    { key: 'studio', icon: <EditOutlined />, label: <Link href="/studio">{t('nav.studio')}</Link> },
    { key: 'dashboard', icon: <DashboardOutlined />, label: <Link href="/dashboard">{t('nav.dashboard')}</Link> },
  ];

  return (
    <Menu
      mode="horizontal"
      selectedKeys={[selectedKey]}  // now controlled by the current route
      theme="dark"
      style={{ flex: 1, overflow: 'hidden', display: 'flex', justifyContent: 'center' }}
      items={menuItems}
    />
  );
};

export default AppNav;