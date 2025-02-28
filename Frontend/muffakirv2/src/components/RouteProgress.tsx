'use client';

import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
import Loading from '../components/Loading'; // adjust the path if needed
import React from 'react';

export function RouteProgress() {
  const pathname = usePathname();
  const [isRouting, setIsRouting] = useState(false);

  const startLoading = () => {
    NProgress.start();
    setIsRouting(true);
  };

  const stopLoading = () => {
    NProgress.done();
    setIsRouting(false);
  };

  // Listen for normal route changes (link clicks, etc.)
  useEffect(() => {
    console.log(pathname)
    startLoading();
    const timer = setTimeout(() => {
      stopLoading();
    }, 500);
    return () => {
      clearTimeout(timer);
      stopLoading();
    };
  }, [pathname]);

  // Also listen for back/forward navigation events
  useEffect(() => {
    const handlePopState = () => {
      startLoading();
      const timer = setTimeout(() => {
        stopLoading();
      }, 500);
      // Clear timer on next popstate or unmount
      return () => clearTimeout(timer);
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  return <Loading isRouting={isRouting} />;
}
