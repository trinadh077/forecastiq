import React, { useState, useEffect } from 'react';
import { Card } from '../components/ui/Card';
import { TrendingUp, Database, ArrowRight, Activity, BarChart3, Cpu } from 'lucide-react';
import apiClient from '../services/api';

interface KPICard {
  label: string;
  value: string;
  change?: string;
  color: string;
  icon: React.ReactNode;
}

export const HomePage: React.FC = () => {
  const [kpis, setKpis] = useState<KPICard[]>([]);


  useEffect(() => {
    fetchKPIs();
  }, []);

  const fetchKPIs = async () => {
    try {
      const [datasetsRes, modelsRes, forecastsRes] = await Promise.allSettled([
        apiClient.get('/datasets'),
        apiClient.get('/ml-models'),
        apiClient.get('/forecasts'),
      ]);

      const datasetCount = datasetsRes.status === 'fulfilled' ? (datasetsRes.value.data?.data?.length || 0) : 0;
      const modelCount = modelsRes.status === 'fulfilled' ? (modelsRes.value.data?.data?.length || 0) : 0;
      const forecastCount = forecastsRes.status === 'fulfilled' ? (forecastsRes.value.data?.data?.length || 0) : 0;



      // Build KPI cards from real data
      const kpiList: KPICard[] = [
        {
          label: 'Total Datasets',
          value: datasetCount.toString(),
          color: 'text-emerald-400',
          icon: <Database className="h-5 w-5" />,
        },
        {
          label: 'Trained Models',
          value: modelCount.toString(),
          color: 'text-amber-400',
          icon: <Cpu className="h-5 w-5" />,
        },
        {
          label: 'Active Forecasts',
          value: forecastCount.toString(),
          color: 'text-indigo-400',
          icon: <TrendingUp className="h-5 w-5" />,
        },
        {
          label: 'Platform Status',
          value: 'Live',
          change: 'All systems operational',
          color: 'text-emerald-400',
          icon: <Activity className="h-5 w-5" />,
        },
      ];

      // Add model metrics if available
      if (modelsRes.status === 'fulfilled' && modelsRes.value.data?.data?.length > 0) {
        const bestModel = modelsRes.value.data.data.reduce((best: any, m: any) => {
          const r2 = m.metrics?.r2_score || 0;
          const bestR2 = best?.metrics?.r2_score || 0;
          return r2 > bestR2 ? m : best;
        }, modelsRes.value.data.data[0]);

        if (bestModel?.metrics) {
          kpiList[2] = {
            label: 'Best Model R² Score',
            value: bestModel.metrics.r2_score?.toFixed(4) || 'N/A',
            change: `${bestModel.algorithm} — MAPE: ${bestModel.metrics.mape?.toFixed(2)}%`,
            color: 'text-indigo-400',
            icon: <BarChart3 className="h-5 w-5" />,
          };
        }
      }

      setKpis(kpiList);
    } catch (e) {
      // Show default KPIs
      setKpis([
        { label: 'Platform Status', value: 'Live', color: 'text-emerald-400', icon: <Activity className="h-5 w-5" /> },
      ]);
    }
  };

  return (
    <div className="space-y-8 max-w-6xl">
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight mb-2">
          ForecastIQ Dashboard
        </h1>
        <p className="text-slate-400 text-sm max-w-2xl">
          Enterprise AI Sales Forecasting platform. Upload datasets, train ML models, and generate revenue projections.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {kpis.map((kpi, idx) => (
          <Card key={idx} className="p-4 border-slate-800 bg-slate-900/60 hover:border-slate-700 transition-all">
            <div className="flex items-center gap-3 mb-3">
              <div className={`p-2 bg-slate-800 rounded-lg ${kpi.color}`}>
                {kpi.icon}
              </div>
              <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">
                {kpi.label}
              </span>
            </div>
            <div className="flex items-baseline gap-2">
              <span className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</span>
              {kpi.change && (
                <span className="text-[10px] text-slate-500">{kpi.change}</span>
              )}
            </div>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="hover:border-indigo-500/50 transition-all group cursor-pointer" onClick={() => window.location.href = '/forecasts'}>
          <div className="p-3 bg-indigo-500/10 rounded-lg w-fit mb-4 text-indigo-400 group-hover:bg-indigo-500 group-hover:text-white transition-colors">
            <TrendingUp className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-1">Forecast Studio</h3>
          <p className="text-xs text-slate-400 leading-relaxed mb-4">
            Generate revenue projections from your uploaded data with AI confidence bands and trend analysis.
          </p>
          <span className="text-xs text-indigo-400 font-medium flex items-center gap-1">
            Open Forecast Studio <ArrowRight className="h-3 w-3" />
          </span>
        </Card>

        <Card className="hover:border-emerald-500/50 transition-all group cursor-pointer" onClick={() => window.location.href = '/datasets'}>
          <div className="p-3 bg-emerald-500/10 rounded-lg w-fit mb-4 text-emerald-400 group-hover:bg-emerald-500 group-hover:text-white transition-colors">
            <Database className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-1">Data Studio</h3>
          <p className="text-xs text-slate-400 leading-relaxed mb-4">
            Upload CSV/Excel datasets with automatic column type detection, null analysis, and outlier flagging.
          </p>
          <span className="text-xs text-emerald-400 font-medium flex items-center gap-1">
            Open Data Studio <ArrowRight className="h-3 w-3" />
          </span>
        </Card>

        <Card className="hover:border-amber-500/50 transition-all group cursor-pointer" onClick={() => window.location.href = '/models'}>
          <div className="p-3 bg-amber-500/10 rounded-lg w-fit mb-4 text-amber-400 group-hover:bg-amber-500 group-hover:text-white transition-colors">
            <Cpu className="h-6 w-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-1">ML Engine</h3>
          <p className="text-xs text-slate-400 leading-relaxed mb-4">
            Train XGBoost, Random Forest, or Ridge models on your data with real accuracy metrics.
          </p>
          <span className="text-xs text-amber-400 font-medium flex items-center gap-1">
            Open ML Engine <ArrowRight className="h-3 w-3" />
          </span>
        </Card>
      </div>

      {/* System Status */}
      <Card className="border-slate-800 bg-slate-900/40">
        <h3 className="text-sm font-semibold text-slate-200 mb-3">System Status</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div className="flex items-center gap-2 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            FastAPI Backend
          </div>
          <div className="flex items-center gap-2 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            React 19 Frontend
          </div>
          <div className="flex items-center gap-2 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            JWT Authentication
          </div>
          <div className="flex items-center gap-2 text-emerald-400">
            <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
            ML Training Pipeline
          </div>
        </div>
      </Card>
    </div>
  );
};
