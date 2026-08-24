import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { TrendingUp, BarChart3, Database, Cpu, Sun, Moon, LogOut } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';
import { useAuth } from '../hooks/useAuth';

export const AppLayout: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();

  const navItems = [
    { label: 'Overview', path: '/', icon: BarChart3, color: 'text-indigo-400' },
    { label: 'Forecast Studio', path: '/forecasts', icon: TrendingUp, color: 'text-indigo-400' },
    { label: 'Data Studio', path: '/datasets', icon: Database, color: 'text-emerald-400' },
    { label: 'ML Engine', path: '/models', icon: Cpu, color: 'text-amber-400' },
  ];

  return (
    <div className="min-h-screen flex bg-slate-950 text-slate-100 font-sans">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-slate-900/60 border-r border-slate-800 flex flex-col justify-between p-4 shrink-0">
        <div>
          <Link to="/" className="flex items-center gap-3 px-3 py-4 mb-6">
            <div className="p-2 bg-indigo-600 rounded-xl shadow-lg shadow-indigo-600/30">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-white leading-tight">ForecastIQ</h1>
              <span className="text-[10px] uppercase tracking-wider text-indigo-400 font-semibold">AI Sales SaaS</span>
            </div>
          </Link>

          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-indigo-600/20 text-white border border-indigo-500/30 font-semibold'
                      : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                  }`}
                >
                  <Icon className={`h-4 w-4 ${item.color}`} />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="pt-4 border-t border-slate-800 flex items-center justify-between px-3">
          <span className="text-[10px] text-slate-500 font-mono">ForecastIQ v1.0.0</span>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white transition-colors"
            title="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-16 border-b border-slate-800 px-8 flex items-center justify-between bg-slate-900/30 backdrop-blur-md sticky top-0 z-10">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Enterprise AI Sales Revenue Intelligence Platform
          </h2>

          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              FastAPI + React 19 Active
            </span>

            {isAuthenticated ? (
              <div className="flex items-center gap-3 pl-4 border-l border-slate-800">
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-7 h-7 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-indigo-400 font-bold">
                    {user?.full_name?.charAt(0) || 'U'}
                  </div>
                  <span className="font-medium text-white">{user?.full_name || 'Executive User'}</span>
                </div>
                <button
                  onClick={logout}
                  className="p-1.5 text-slate-400 hover:text-rose-400 transition-colors"
                  title="Sign out"
                >
                  <LogOut className="h-4 w-4" />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg shadow-sm"
              >
                Sign In
              </Link>
            )}
          </div>
        </header>

        <main className="flex-1 p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
