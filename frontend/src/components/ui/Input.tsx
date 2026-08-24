import React from 'react';
import { cn } from '../../utils/cn';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && <label className="block text-xs font-medium text-slate-400 mb-1.5">{label}</label>}
        <input
          ref={ref}
          className={cn(
            'w-full h-10 px-3 py-2 bg-slate-900 border border-slate-800 rounded-lg text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all',
            error && 'border-rose-500 focus:ring-rose-500',
            className
          )}
          {...props}
        />
        {error && <p className="mt-1 text-xs text-rose-500">{error}</p>}
      </div>
    );
  }
);
Input.displayName = 'Input';
