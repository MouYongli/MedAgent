'use client';

import React from 'react';
import { Select, MenuItem, FormControl, SelectChangeEvent } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { languages, languageLabels } from '@/i18n/settings';

const LanguageSwitcher: React.FC = () => {
    const { i18n } = useTranslation();

    const handleChange = (event: SelectChangeEvent) => {
        if (i18n.changeLanguage) {
            i18n.changeLanguage(event.target.value);
        }
    };

    return (
        <FormControl size="small">
            <Select
                value={i18n.language || 'en'}
                onChange={handleChange}
                sx={{ width: 100 }}
                variant="standard"
            >
                {languages.map((lang) => (
                    <MenuItem key={lang} value={lang}>
                        {languageLabels[lang]}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
};

export default LanguageSwitcher;