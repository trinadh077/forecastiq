import React from 'react';
import { Spinner } from './ui/Spinner';

export const LoadingScreen: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 text-slate-100">
      <Spinner className="h-10 w-10 text-indigo-500 mb-4" />
      <p className="text-sm font-medium text-slate-400">Loading ForecastIQ...</p>
    </div>
  );
};
