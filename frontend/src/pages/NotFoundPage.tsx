import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center">
      <h1 className="text-6xl font-extrabold text-indigo-500 mb-2">404</h1>
      <h2 className="text-xl font-bold text-slate-100 mb-2">Page Not Found</h2>
      <p className="text-slate-400 text-sm max-w-md mb-6">
        The requested module or workspace page could not be located on the ForecastIQ network.
      </p>
      <Link to="/">
        <Button variant="primary">Return to Dashboard</Button>
      </Link>
    </div>
  );
};
