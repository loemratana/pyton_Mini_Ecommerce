import React, { useState, useEffect } from 'react';
import { Globe } from 'lucide-react';

export const LanguageSwitcher = () => {
  const [currentLang, setCurrentLang] = useState('en');

  // Check initial language from cookies when component mounts
  useEffect(() => {
    const match = document.cookie.match(/googtrans=\/en\/(.*?)(;|$)/);
    if (match && match[1]) {
      setCurrentLang(match[1]);
    } else {
      setCurrentLang('en');
    }
  }, []);

  const changeLanguage = (langCode) => {
    const selectElement = document.querySelector('.goog-te-combo');
    if (selectElement) {
      selectElement.value = langCode;
      selectElement.dispatchEvent(new Event('change'));
      setCurrentLang(langCode);
    } else {
      console.error('Google Translate script not loaded yet.');
    }
  };

  const toggleLanguage = () => {
    const nextLang = currentLang === 'en' ? 'km' : 'en';
    changeLanguage(nextLang);
  };

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 transition-colors text-gray-700 font-medium text-sm"
      title="Translate (English / Khmer)"
    >
      <Globe size={18} className={currentLang === 'km' ? 'text-blue-600' : 'text-gray-500'} />
      <span className="uppercase">{currentLang === 'en' ? 'EN' : 'KH'}</span>
    </button>
  );
};
