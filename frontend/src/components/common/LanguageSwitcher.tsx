'use client';

import React from 'react';
import { Select, MenuItem } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { languages, languageLabels } from '@/i18n/settings';

const LanguageSwitcher: React.FC = () => {
    const { i18n } = useTranslation();

    const handleChange = (value: string) => {
        if (i18n.changeLanguage) {
            i18n.changeLanguage(value);
        }
    };

    return (
        <Select
            defaultValue={i18n.language || 'en'}
            style={{ width: 100 }}
            onChange={(event) => handleChange(event.target.value)}
        >
            {languages.map((lang) => (
                <MenuItem key={lang} value={lang}>
                    {languageLabels[lang]}
                </MenuItem>
            ))}
        </Select>
    );
};

export default LanguageSwitcher;
