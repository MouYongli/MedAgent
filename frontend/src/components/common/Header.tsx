// components/common/Header.tsx
'use client';

import React from 'react';
import { AppBar, Toolbar, Button, Box } from '@mui/material';
import { Person as PersonIcon } from '@mui/icons-material';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import AppNav from '@/components/common/Nav';
import LanguageSwitcher from '@/components/common/LanguageSwitcher';

const AppHeader: React.FC = () => {
  const { t } = useTranslation();

  return (
    <AppBar position="static">
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        {/* Left side: Logo */}
        <Box sx={{ typography: 'h6', fontWeight: 'bold' }}>
          MedAgent
        </Box>

        {/* Center: Navigation */}
        <Box sx={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
          <AppNav />
        </Box>

        {/* Right side: Language switcher and sign-in button */}
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
