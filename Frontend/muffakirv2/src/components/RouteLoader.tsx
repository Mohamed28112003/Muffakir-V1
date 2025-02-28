'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { usePathname } from 'next/navigation';
import React from 'react';
export function RouteLoader() {
  const pathname = usePathname();
  const [isLoading, setIsLoading] = useState(false);
  const [currentPath, setCurrentPath] = useState(pathname);

  useEffect(() => {
    if (pathname !== currentPath) {
      setIsLoading(true);
      setCurrentPath(pathname);
    }
  }, [pathname, currentPath]);

  useEffect(() => {
    if (isLoading) {
      const timer = setTimeout(() => setIsLoading(false), 500); // Simulate loading delay
      return () => clearTimeout(timer);
    }
  }, [isLoading]);

  return (
    <AnimatePresence>
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center"
        >
          <div className="space-y-4 flex flex-col items-center">
            <motion.div
              animate={{
                scale: [1, 1.2, 1],
                rotate: [0, 180, 360],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: 'anticipate',
              }}
              className="w-16 h-16 bg-foreground rounded-full"
            />
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-foreground font-medium"
            >
              Loading...
            </motion.span>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}