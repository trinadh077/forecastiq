import React, { useState, useEffect } from 'react';
import { Cpu, Activity, CheckCircle2, Sliders, Play, Award, AlertCircle, BarChart3 } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import apiClient from '../services/api';
import { MLModel, Dataset } from '../types';

export const MLEnginePage: React.FC = () => {
  const [models, setModels] = useState<MLModel[]>([]);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [algorithm, setAlgorithm] = useState<string>('XGBOOST');
  const [modelName, setModelName] = useState('XGBoost Sales Engine v2');
  const [selectedDatasetId, setSelectedDatasetId] = useState('');
  const [targetColumn, setTargetColumn] = useState('');
  const [datasetColumns, setDatasetColumns] = useState<string[]>([]);
  const [isTraining, setIsTraining] = useState(false);
  const [trainingSuccess, setTrainingSuccess] = useState(false);
  const [trainingError, setTrainingError] = useState<string | null>(null);

  useEffect(() => {
    fetchModels();
    fetchDatasets();
  }, []);

  const fetchModels = async () => {
    try {
      const res = await apiClient.get('/ml-models');
      if (res.data?.data) {
        setModels(res.data.data);
      }
    } catch (e) {
      setModels([]);
    }
  };

  const fetchDatasets = async () => {
    try {
      const res = await apiClient.get('/datasets');
      if (res.data?.data) {
        setDatasets(res.data.data);
        if (res.data.data.length > 0) {
          setSelectedDatasetId(res.data.data[0].id);
          loadDatasetColumns(res.data.data[0].id);
        }
      }
    } catch (e) {
      setDatasets([]);
    }
  };

  const loadDatasetColumns = async (datasetId: string) => {
    try {
      const res = await apiClient.get(`/datasets/${datasetId}/preview`);
      if (res.data?.data?.columns) {
        setDatasetColumns(res.data.data.columns);
        // Auto-select first numeric column as target
        const types = res.data.data.types || {};
        const numericCol = res.data.data.columns.find((c: string) =>
          types[c] === 'float' || types[c] === 'int'
        );
        if (numericCol) {
          setTargetColumn(numericCol);
        }
      }
    } catch (e) {
      setDatasetColumns([]);
    }
  };

  const handleTrainModel = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsTraining(true);
    setTrainingError(null);
    setTrainingSuccess(false);

    try {
      const res = await apiClient.post('/ml-models/train', {
        name: modelName,
        algorithm,
        dataset_id: selectedDatasetId,
        target_column: targetColumn || undefined,
      });
      if (res.data?.data) {
        setTrainingSuccess(true);
        setTimeout(() => setTrainingSuccess(false), 5000);
        fetchModels();
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.response?.data?.error?.message || e?.message || 'Training failed';
      setTrainingError(msg);
    } finally {
      setIsTraining(false);
    }
  };

  return (
    <div className="space-y-8 max-w-6xl">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Cpu className="h-6 w-6 text-amber-400" />
          ML Forecasting Engine & Algorithm Tuning
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Train real ML algorithms on your uploaded datasets and evaluate accuracy metrics (MAPE, RMSE, R²).
        </p>
      </div>

      {trainingSuccess && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 className="h-5 w-5 shrink-0" />
          <span>Model trained successfully! Real accuracy metrics computed on your data.</span>
        </div>
      )}

      {trainingError && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-xs flex items-center gap-2">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <span>{trainingError}</span>
        </div>
      )}

      {/* No datasets warning */}
      {datasets.length === 0 && (
        <Card className="border-amber-500/30 bg-amber-500/5 p-6">
          <div className="flex items-center gap-3">
            <AlertCircle className="h-5 w-5 text-amber-400 shrink-0" />
            <div>
              <h3 className="text-sm font-semibold text-amber-400">No Datasets Found</h3>
              <p className="text-xs text-slate-400 mt-1">
                Upload a CSV dataset in Data Studio first, then come back to train models on it.
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* Model Training Form */}
      {datasets.length > 0 && (
        <Card className="border-slate-800 bg-slate-900/60 p-6">
          <form onSubmit={handleTrainModel} className="space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                <Sliders className="h-4 w-4 text-indigo-400" />
                Train New Model on Your Data
              </h3>
              <span className="text-[10px] text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded-full border border-indigo-500/20 font-mono">
                Real Training Active
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-2">Model Name</label>
                <input
                  type="text"
                  value={modelName}
                  onChange={(e) => setModelName(e.target.value)}
                  required
                  className="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-2">Algorithm</label>
                <select
                  value={algorithm}
                  onChange={(e) => setAlgorithm(e.target.value)}
                  className="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                >
                  <option value="XGBOOST">XGBoost Gradient Boosting (Recommended)</option>
                  <option value="RANDOM_FOREST">Random Forest</option>
                  <option value="LINEAR_REGRESSION">Ridge Linear Regression</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-2">Dataset</label>
                <select
                  value={selectedDatasetId}
                  onChange={(e) => {
                    setSelectedDatasetId(e.target.value);
                    loadDatasetColumns(e.target.value);
                  }}
                  className="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                >
                  {datasets.map((ds) => (
                    <option key={ds.id} value={ds.id}>{ds.name} ({ds.row_count} rows)</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-2">Target Column (what to predict)</label>
                <select
                  value={targetColumn}
                  onChange={(e) => setTargetColumn(e.target.value)}
                  className="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                >
                  {datasetColumns.map((col) => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
              </div>

              <div className="flex items-end">
                <Button
                  type="submit"
                  disabled={isTraining || !selectedDatasetId}
                  className="w-full bg-amber-600 hover:bg-amber-500 text-white text-xs py-2.5 font-medium rounded-xl shadow-lg shadow-amber-600/20 flex items-center justify-center gap-2"
                >
                  <Play className={`h-4 w-4 ${isTraining ? 'animate-spin' : ''}`} />
                  {isTraining ? 'Training on Real Data...' : 'Train ML Model'}
                </Button>
              </div>
            </div>
          </form>
        </Card>
      )}

      {/* Trained Models Metric Cards */}
      {models.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-white tracking-tight flex items-center gap-2">
            <Award className="h-4 w-4 text-emerald-400" />
            Trained Model Registry ({models.length} models)
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {models.map((m) => (
              <Card key={m.id} className="border-slate-800 bg-slate-900/60 p-5 space-y-4 hover:border-slate-700 transition-all">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                      {m.algorithm}
                    </span>
                    <h4 className="font-bold text-sm text-white mt-2">{m.name}</h4>
                  </div>
                  <Activity className="h-5 w-5 text-emerald-400" />
                </div>

                <div className="grid grid-cols-2 gap-3 pt-2 border-t border-slate-800">
                  <div className="p-2.5 bg-slate-950/60 rounded-xl">
                    <span className="text-[10px] text-slate-400 block">MAPE Error</span>
                    <span className="text-sm font-bold text-emerald-400">{m.metrics?.mape?.toFixed(2)}%</span>
                  </div>
                  <div className="p-2.5 bg-slate-950/60 rounded-xl">
                    <span className="text-[10px] text-slate-400 block">R² Score</span>
                    <span className="text-sm font-bold text-indigo-400">{m.metrics?.r2_score?.toFixed(4)}</span>
                  </div>
                  <div className="p-2.5 bg-slate-950/60 rounded-xl">
                    <span className="text-[10px] text-slate-400 block">RMSE ($)</span>
                    <span className="text-xs font-semibold text-slate-200">${m.metrics?.rmse?.toLocaleString()}</span>
                  </div>
                  <div className="p-2.5 bg-slate-950/60 rounded-xl">
                    <span className="text-[10px] text-slate-400 block">MAE ($)</span>
                    <span className="text-xs font-semibold text-slate-200">${m.metrics?.mae?.toLocaleString()}</span>
                  </div>
                </div>

                {/* Feature Importance */}
                {(m.metrics as any)?.feature_importance && (
                  <div className="pt-2 border-t border-slate-800">
                    <span className="text-[10px] text-slate-400 block mb-2 flex items-center gap-1">
                      <BarChart3 className="h-3 w-3" /> Top Feature Importance
                    </span>
                    <div className="space-y-1">
                      {Object.entries((m.metrics as any).feature_importance as Record<string, number>)
                        .sort(([, a], [, b]) => b - a)
                        .slice(0, 3)
                        .map(([feature, imp]) => {
                          const importance = Number(imp);
                          const maxVal = Math.max(...Object.values((m.metrics as any).feature_importance as Record<string, number>).map(Number));
                          return (
                          <div key={feature} className="flex items-center gap-2">
                            <span className="text-[10px] text-slate-400 truncate w-24">{feature}</span>
                            <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-indigo-500 rounded-full"
                                style={{ width: `${Math.min(100, (importance / maxVal) * 100)}%` }}
                              />
                            </div>
                            <span className="text-[10px] text-slate-500 w-10 text-right">{(importance * 100).toFixed(1)}%</span>
                          </div>
                          );
                        })}
                    </div>
                  </div>
                )}
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
