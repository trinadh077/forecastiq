import React from 'react';
import { cn } from '../../utils/cn';

export const Spinner: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div
      className={cn(
        'animate-spin rounded-full h-6 w-6 border-2 border-indigo-500 border-t-transparent',
        className
      )}
    />
  );
};
