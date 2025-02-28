'use client';

import React from 'react';
import { useEffect, useState } from 'react';
import { FaMoon, FaSun } from 'react-icons/fa';
function ThemeToggle() {

  const [darkMode, setDarkMode] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('theme') === 'dark';
    }
    return false;
  });

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    setDarkMode(savedTheme === 'dark');
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.setAttribute('theme', 'dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.setAttribute('theme', 'light');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);
  

  return (
    <button 
      className="theme-toggle"
      onClick={() => setDarkMode(!darkMode)}
      aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {darkMode ? <FaSun size={20} /> : <FaMoon size={20} />}
    </button>
  );
}

export default ThemeToggle;