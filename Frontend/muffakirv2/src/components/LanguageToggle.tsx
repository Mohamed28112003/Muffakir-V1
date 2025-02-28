'use client';

import React from 'react';
import { FaGlobe } from 'react-icons/fa';

function LanguageToggle({ lang, onToggle }: { lang: string; onToggle: () => void }) {
  return (
    <button 
      className="language-toggle"
      onClick={onToggle}
      aria-label="Toggle language"
    >
      <FaGlobe size={20} />
      <span>{lang === 'en' ? 'AR' : 'EN'}</span>
    </button>
  );
}

export default LanguageToggle;