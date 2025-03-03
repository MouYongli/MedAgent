'use client';

import React from 'react';
import { AppBar, Toolbar, Button, IconButton, Box } from '@mui/material';
import PersonOutlineOutlined from '@mui/icons-material/PersonOutlineOutlined';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import AppNav from './Nav';
import LanguageSwitcher from '@/components/common/LanguageSwitcher';

const AppHeader: React.FC = () => {
  const { t } = useTranslation();

  return (
    <AppBar position="static" style={{ backgroundColor: '#001529' }}>
      <Toolbar style={{ display: 'flex', justifyContent: 'space-between' }}>
        <Box style={{ flex: 'none', color: '#fff', fontSize: '1.2rem', fontWeight: 'bold' }}>
          MedAgent
        </Box>
        <Box style={{ flex: 1, overflow: 'hidden', display: 'flex', justifyContent: 'center' }}>
          <AppNav />
        </Box>
        <Box>
          <LanguageSwitcher />
          <Link href="/sign-in">
            <Button variant="contained" color="primary" startIcon={<PersonOutlineOutlined />}>
              {t('nav.sign_in')}
            </Button>
          </Link>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default AppHeader;
