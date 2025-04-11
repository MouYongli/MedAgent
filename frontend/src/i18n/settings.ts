import { getAvailableLanguages } from './utils';

export const fallbackLng = 'en'
export const languages = ['en', 'zh', 'de']
export const defaultNS = 'common'

export const languageLabels: { [key: string]: string } = {
  'en': 'English',
  'zh': '中文',
  'de': 'Deutsch'
}

export function getOptions(lng = fallbackLng, ns = defaultNS) {
  return {
    supportedLngs: languages,
    fallbackLng,
    lng,
    fallbackNS: defaultNS,
    defaultNS,
    ns,
    interpolation: {
      escapeValue: false
    }
  }
}