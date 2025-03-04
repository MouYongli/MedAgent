// components/common/Navigation.tsx

import React from 'react';
import { Tabs, Tab } from '@mui/material';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import { Home, Chat, Edit, Dashboard } from '@mui/icons-material';
import { usePathname, useRouter } from 'next/navigation';

const AppNav: React.FC = () => {
  const { t } = useTranslation();
  const router = useRouter();
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
    { key: 'home', icon: <Home />, label: t('nav.home'), path: '/' },
    { key: 'chat', icon: <Chat />, label: t('nav.chat'), path: '/chat' },
    { key: 'studio', icon: <Edit />, label: t('nav.studio'), path: '/studio' },
    { key: 'dashboard', icon: <Dashboard />, label: t('nav.dashboard'), path: '/dashboard' },
  ];

  const handleChange = (_event: React.SyntheticEvent, newValue: string) => {
    const item = menuItems.find(item => item.key === newValue);
    if (item) {
      router.push(item.path);
    }
  };

  return (
    <Tabs
      value={selectedKey}
      onChange={handleChange}
      centered
      sx={{
        '& .MuiTab-root': {
          color: 'white',
          '&.Mui-selected': {
            color: 'white',
          }
        },
        '& .MuiTabs-indicator': {
          backgroundColor: 'white',
        }
      }}
    >
      {menuItems.map((item) => (
        <Tab
          key={item.key}
          value={item.key}
          icon={item.icon}
          label={item.label}
          iconPosition="start"
        />
      ))}
    </Tabs>
  );
};

export default AppNav;