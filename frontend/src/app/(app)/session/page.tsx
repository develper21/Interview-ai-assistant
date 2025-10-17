'use client';
import React from 'react';
import InterviewWidget from '@/components/features/interview/InterviewWidget';

const SessionPage = () => {
  return (
    <div className="flex flex-col h-full">
      <h1 className="text-4xl font-bold mb-8">Live Interview Session</h1>

      <div className="flex-1">
        <InterviewWidget />
      </div>
    </div>
  );
};

export default SessionPage;
