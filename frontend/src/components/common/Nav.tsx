'use client';
import React from 'react';
import { Menu, MenuItem } from '@mui/material';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import HomeOutlined from '@mui/icons-material/HomeOutlined';
import MessageOutlined from '@mui/icons-material/MessageOutlined';
import EditOutlined from '@mui/icons-material/EditOutlined';
import DashboardOutlined from '@mui/icons-material/DashboardOutlined';
import { usePathname } from 'next/navigation';

export default function AppNav() {
  const { t } = useTranslation();

  const pathname = usePathname();
  
  let selectedKey = 'home';
  if (pathname.startsWith('/chat')) {
    selectedKey = 'chat';
  } else if (pathname.startsWith('/studio')) {
    selectedKey = 'studio';
  } else if (pathname.startsWith('/dashboard')) {
    selectedKey = 'dashboard';
  }

  const menuItems = [
    { key: 'home', icon: <HomeOutlined />, label: <Link href="/">{t('nav.home')}</Link> },
    { key: 'chat', icon: <MessageOutlined />, label: <Link href="/chat">{t('nav.chat')}</Link> },
    { key: 'studio', icon: <EditOutlined />, label: <Link href="/studio">{t('nav.studio')}</Link> },
    { key: 'dashboard', icon: <DashboardOutlined />, label: <Link href="/dashboard">{t('nav.dashboard')}</Link> },
  ];

  return (
    <Menu
      mode="horizontal"
      selectedKeys={[selectedKey]}  // now controlled by the current route
      theme="dark"
      style={{ flex: 1, overflow: 'hidden', display: 'flex', justifyContent: 'center' }}
    >
      {menuItems.map((item) => (
        <MenuItem key={item.key} icon={item.icon}>
          {item.label}
        </MenuItem>
      ))}
    </Menu>
  );
}