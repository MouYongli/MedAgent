'use client';

import React, { useEffect, useState } from 'react';
import { I18nextProvider } from 'react-i18next';
import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import AppHeader from '@/components/common/Header';
import AppFooter from '@/components/common/Footer';
import { getOptions, languages } from '@/i18n/settings';
import { Box, Grid } from '@mui/material';

const i18n = i18next.createInstance();

i18n.use(initReactI18next);

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    const initI18n = async () => {
      try {
        // 动态导入所有配置的语言翻译
        const translations = await Promise.all(
          languages.map(async (lang) => {
            const module = await import(`@/i18n/${lang}/common.json`);
            return { lang, translation: module.default };
          })
        );

        // 构建 resources 对象
        const resources = translations.reduce((acc, { lang, translation }) => ({
          ...acc,
          [lang]: {
            common: translation
          }
        }), {});

        await i18n.init({
          ...getOptions(),
          resources
        });

        setInitialized(true);
      } catch (error) {
        console.error('Failed to initialize i18n:', error);
      }
    };

    initI18n();
  }, []);

  if (!initialized) {
    return (
      <html>
        <body>
          <div>Loading...</div>
        </body>
      </html>
    );
  }

  return (
    <html lang={i18n.language}>
      <head>
        <title>MedAgent</title>
        <meta charSet="utf-8" />        
        <meta name="description" content="MedAgent - AI-powered medical assistant" />
        <link rel="stylesheet" href="/styles/globals.css" />
        <link rel="icon" href="/images/logo.svg" />
      </head>
      <body>
        <I18nextProvider i18n={i18n}>
          <AppHeader />
          <main style={{ minHeight: '80vh', padding: '20px' }}>{children}</main>
          <AppFooter />
        </I18nextProvider>
      </body>
    </html>
  );
}
