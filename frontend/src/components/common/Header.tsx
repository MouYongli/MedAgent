// components/common/Header.tsx
'use client';

import React from 'react';
import { Layout, Button, Space } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import AppNav from '@/components/common/Nav';
import LanguageSwitcher from '@/components/common/LanguageSwitcher';

const { Header } = Layout;

const AppHeader: React.FC = () => {
  const { t } = useTranslation();

  return (
    <Header
      style={{
        display: 'flex',
        alignItems: 'center',
        backgroundColor: '#001529', // Dark background
        justifyContent: 'space-between',
        padding: '0 20px',
      }}
    >
      {/* Left side: Logo */}
      <div style={{ flex: 'none', color: '#fff', fontSize: '1.2rem', fontWeight: 'bold' }}>
        MedAgent
      </div>

      {/* Center: Navigation */}
      <div style={{ flex: 1, overflow: 'hidden', display: 'flex', justifyContent: 'center' }}>
        <AppNav />
      </div>

      {/* Right side: Language switcher and sign-in button */}
      <Space>
        <LanguageSwitcher />
        <Link href="/sign-in">
          <Button type="primary" shape="round" icon={<UserOutlined />}>
            {t('nav.sign_in')}
          </Button>
        </Link>
      </Space>
    </Header>
  );
};

export default AppHeader;
