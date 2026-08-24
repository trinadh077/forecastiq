import React from 'react';
import { Card } from '../components/ui/Card';
import { TrendingUp, Database, ShieldCheck, ArrowRight } from 'lucide-react';

export const HomePage: React.FC = () => {
  return (
    <div className="space-y-8 max-w-6xl">
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight mb-2">
          ForecastIQ Platform Foundation
        </h1>
        <p className="text-slate-400 text-sm max-w-2xl">
          Enterprise AI Sales Forecasting platform core architecture initialized. Production-grade FastAPI backend, Async PostgreSQL models, OAuth2/JWT auth, and React 19 single-page architecture ready.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="hover:border-indigo-500/50 transition-all group">
          <div className="p-3 bg-indigo-500/10 rounded-lg w-fit mb-4 text-indigo-400 group-hover:bg-indigo-500 group-hover:text-white transition-colors">
            <TrendingUp className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-1">Multi-Model Forecasting</h3>
          <p className="text-xs text-slate-400 leading-relaxed mb-4">
            Architecture configured for Facebook Prophet, XGBoost, ARIMA, LSTM, and Ensemble models with 30-365 day horizons.
          </p>
          <span className="text-xs text-indigo-400 font-medium flex items-center gap-1">
            Core Engine Ready <ArrowRight className="h-3 w-3" />
          </span>
        </Card>

        <Card className="hover:border-emerald-500/50 transition-all group">
          <div className="p-3 bg-emerald-500/10 rounded-lg w-fit mb-4 text-emerald-400 group-hover:bg-emerald-500 group-hover:text-white transition-colors">
            <Database className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-1">Data Studio Pipeline</h3>
          <p className="text-xs text-slate-400 leading-relaxed mb-4">
            Supports CSV/Excel upload validation, null detection, IQR outlier handling, auto-date parsing, and schemas.
          </p>
          <span className="text-xs text-emerald-400 font-medium flex items-center gap-1">
            Data Models Ready <ArrowRight className="h-3 w-3" />
          </span>
        </Card>

        <Card className="hover:border-amber-500/50 transition-all group">
          <div className="p-3 bg-amber-500/10 rounded-lg w-fit mb-4 text-amber-400 group-hover:bg-amber-500 group-hover:text-white transition-colors">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-1">Multi-Tenant RBAC</h3>
          <p className="text-xs text-slate-400 leading-relaxed mb-4">
            Enterprise role-based security (Admin, Manager, Sales Analyst) with organization boundaries and audit logs.
          </p>
          <span className="text-xs text-amber-400 font-medium flex items-center gap-1">
            RBAC Core Ready <ArrowRight className="h-3 w-3" />
          </span>
        </Card>
      </div>

      <Card className="border-slate-800 bg-slate-900/40">
        <h3 className="text-sm font-semibold text-slate-200 mb-3">Phase 1 Architectural Verification Checklist</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div className="flex items-center gap-2 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            FastAPI 0.111 / Python 3.12
          </div>
          <div className="flex items-center gap-2 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            SQLAlchemy 2.0 Async PostgreSQL
          </div>
          <div className="flex items-center gap-2 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            Alembic Database Migrations
          </div>
          <div className="flex items-center gap-2 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            Docker & Compose NGINX Setup
          </div>
        </div>
      </Card>
    </div>
  );
};
