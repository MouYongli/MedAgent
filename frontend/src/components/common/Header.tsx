// components/common/Header.tsx
'use client';

import React from 'react';
import { AppBar, Toolbar, Button, Box } from '@mui/material';
import { Person as PersonIcon } from '@mui/icons-material';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import AppNav from '@/components/common/Nav';
import LanguageSwitcher from '@/components/common/LanguageSwitcher';

const menuItems = [
  { key: 'nav1', label: 'nav 1' },
  { key: 'nav2', label: 'nav 2' },
  { key: 'nav3', label: 'nav 3' },
];

const AppHeader: React.FC = () => {
  const { t } = useTranslation();

  return (
    <AppBar position="static">
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        {/* 左侧 Logo */}
        <Box sx={{ typography: 'h6', fontWeight: 'bold' }}>
          MedAgent
        </Box>

        {/* 中间导航 */}  
        <Box sx={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
          <AppNav />
        </Box>

        {/* 右侧语言切换器和登录按钮 */}
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <LanguageSwitcher />
          <Link href="/sign-in" style={{ textDecoration: 'none' }}>
            <Button
              variant="contained"
              startIcon={<PersonIcon />}
              sx={{ borderRadius: 28 }}
            >
              {t('nav.sign_in')}
            </Button>
          </Link>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default AppHeader;
