'use client';

import React from 'react';

export default function Loading({isRouting} : {isRouting: boolean}) {
  return (
    <main>
      {isRouting && (
    <div className="loading-container">
      <p className="loading-text"></p>
    </div>
      )}
    </main>
  );
}
