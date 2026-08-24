import React, { useState, useEffect } from 'react';
import { Upload, Database, FileText, CheckCircle2, Table, AlertTriangle, BarChart3 } from 'lucide-react';
import { Card } from '../components/ui/Card';
import apiClient from '../services/api';
import { Dataset } from '../types';

interface ColumnStat {
  null_count: number;
  null_pct: number;
  unique_count: number;
  min?: number;
  max?: number;
  mean?: number;
  std?: number;
  outlier_count?: number;
}

interface DatasetPreview {
  id: string;
  name: string;
  row_count: number;
  columns: string[];
  types: Record<string, string>;
  stats: Record<string, ColumnStat>;
  sample_rows: Record<string, any>[];
}

export const DataStudioPage: React.FC = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<Dataset | null>(null);
  const [preview, setPreview] = useState<DatasetPreview | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);

  useEffect(() => {
    fetchDatasets();
  }, []);

  useEffect(() => {
    if (selectedDataset) {
      fetchPreview(selectedDataset.id);
    }
  }, [selectedDataset]);

  const fetchDatasets = async () => {
    try {
      const res = await apiClient.get('/datasets');
      if (res.data?.data) {
        setDatasets(res.data.data);
        if (res.data.data.length > 0) {
          setSelectedDataset(res.data.data[0]);
        }
      }
    } catch (e) {
      // Backend offline — show empty state
      setDatasets([]);
    }
  };

  const fetchPreview = async (datasetId: string) => {
    setIsLoadingPreview(true);
    try {
      const res = await apiClient.get(`/datasets/${datasetId}/preview`);
      if (res.data?.data) {
        setPreview(res.data.data);
      }
    } catch (e) {
      setPreview(null);
    } finally {
      setIsLoadingPreview(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await apiClient.post('/datasets/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (res.data?.data) {
        setUploadSuccess(true);
        setTimeout(() => setUploadSuccess(false), 4000);
        fetchDatasets();
        // Select the newly uploaded dataset
        setSelectedDataset(res.data.data);
      }
    } catch (e: any) {
      let msg = 'Upload failed.';
      if (e?.response?.data?.detail) {
        msg = e.response.data.detail;
      } else if (e?.response?.data?.error?.message) {
        msg = e.response.data.error.message;
      } else if (e?.message?.includes('Network Error')) {
        msg = 'Network error — the backend may be unreachable.';
      } else if (e?.message) {
        msg = e.message;
      }
      alert(`Upload failed: ${msg}`);
    } finally {
      setIsUploading(false);
      // Reset file input
      e.target.value = '';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const getTypeBadge = (type: string) => {
    const colors: Record<string, string> = {
      datetime: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
      float: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
      int: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20',
      string: 'text-slate-300 bg-slate-500/10 border-slate-500/20',
      category: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
      bool: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
    };
    return colors[type] || 'text-slate-300 bg-slate-500/10 border-slate-500/20';
  };

  return (
    <div className="space-y-8 max-w-6xl">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Database className="h-6 w-6 text-emerald-400" />
            Data Studio & Pipeline Management
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Upload sales history, validate column data types, detect outliers, and inspect datasets for AI model training.
          </p>
        </div>

        <label className="cursor-pointer">
          <input type="file" accept=".csv,.xlsx,.xls,.json" onChange={handleFileUpload} className="hidden" />
          <span className="inline-flex items-center gap-2 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs rounded-xl shadow-lg shadow-emerald-600/20 transition-all">
            <Upload className="h-4 w-4" />
            {isUploading ? 'Analyzing File...' : 'Upload CSV / Excel Dataset'}
          </span>
        </label>
      </div>

      {uploadSuccess && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 className="h-5 w-5 shrink-0" />
          <span>Dataset uploaded, parsed, and schema validated successfully. Ready for ML training.</span>
        </div>
      )}

      {/* Dataset Selection Cards */}
      {datasets.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {datasets.map((ds) => {
            const isSelected = selectedDataset?.id === ds.id;
            return (
              <Card
                key={ds.id}
                onClick={() => setSelectedDataset(ds)}
                className={`cursor-pointer transition-all p-4 border ${
                  isSelected
                    ? 'border-emerald-500/80 bg-slate-900/90 shadow-lg shadow-emerald-500/10'
                    : 'border-slate-800 bg-slate-900/40 hover:border-slate-700'
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-400">
                    <FileText className="h-5 w-5" />
                  </div>
                  <span className="inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    {ds.status}
                  </span>
                </div>
                <h4 className="font-semibold text-sm text-white truncate mb-1">{ds.name}</h4>
                <div className="text-[11px] text-slate-400 flex items-center justify-between">
                  <span>{ds.row_count?.toLocaleString() || 0} rows</span>
                  <span>{formatFileSize(ds.file_size_bytes || 0)}</span>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {datasets.length === 0 && !isUploading && (
        <Card className="border-slate-800 bg-slate-900/60 p-12 text-center">
          <Database className="h-12 w-12 text-slate-600 mx-auto mb-4" />
          <h3 className="text-sm font-semibold text-slate-300 mb-2">No Datasets Yet</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Upload a CSV, Excel, or JSON file to get started. The system will automatically detect column types, null values, and outliers.
          </p>
        </Card>
      )}

      {/* Active Dataset Inspection Detail */}
      {selectedDataset && (
        <Card className="border-slate-800 bg-slate-900/60 p-6 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div>
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Table className="h-5 w-5 text-indigo-400" />
                {selectedDataset.name}
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                {selectedDataset.row_count?.toLocaleString()} rows &middot;{' '}
                {preview?.columns?.length || selectedDataset.column_schema?.columns?.length || 0} columns
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs px-3 py-1 bg-slate-800 rounded-lg text-slate-300">
                Uploaded: {new Date(selectedDataset.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>

          {isLoadingPreview && (
            <div className="text-center py-8 text-slate-400 text-xs">Loading dataset preview...</div>
          )}

          {/* Column Schema with Stats */}
          {preview && (
            <div>
              <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                <BarChart3 className="h-3.5 w-3.5" />
                Detected Feature Schema & Statistics
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {preview.columns.map((col) => {
                  const typeName = preview.types[col] || 'string';
                  const stat = preview.stats[col];
                  return (
                    <div key={col} className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-white truncate">{col}</span>
                        <span className={`text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded border ${getTypeBadge(typeName)}`}>
                          {typeName}
                        </span>
                      </div>
                      {stat && (
                        <div className="text-[10px] text-slate-400 space-y-1">
                          <div className="flex justify-between">
                            <span>Unique:</span>
                            <span className="text-slate-300">{stat.unique_count.toLocaleString()}</span>
                          </div>
                          {stat.null_count > 0 && (
                            <div className="flex justify-between text-amber-400">
                              <span className="flex items-center gap-1">
                                <AlertTriangle className="h-2.5 w-2.5" />
                                Nulls:
                              </span>
                              <span>{stat.null_count} ({stat.null_pct}%)</span>
                            </div>
                          )}
                          {stat.min !== undefined && stat.min !== null && (
                            <div className="flex justify-between">
                              <span>Range:</span>
                              <span className="text-slate-300">
                                {stat.min.toLocaleString()} — {stat.max?.toLocaleString()}
                              </span>
                            </div>
                          )}
                          {stat.mean !== undefined && stat.mean !== null && (
                            <div className="flex justify-between">
                              <span>Mean ± Std:</span>
                              <span className="text-slate-300">
                                {stat.mean.toLocaleString()} ± {stat.std?.toLocaleString()}
                              </span>
                            </div>
                          )}
                          {stat.outlier_count !== undefined && stat.outlier_count > 0 && (
                            <div className="flex justify-between text-rose-400">
                              <span className="flex items-center gap-1">
                                <AlertTriangle className="h-2.5 w-2.5" />
                                Outliers:
                              </span>
                              <span>{stat.outlier_count}</span>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Sample Data Preview Table */}
          {preview && preview.sample_rows.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3">
                Sample Rows Preview (First {Math.min(preview.sample_rows.length, 20)} Rows)
              </h4>
              <div className="overflow-x-auto border border-slate-800 rounded-xl">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="bg-slate-950/80 text-slate-400 uppercase font-semibold text-[10px] border-b border-slate-800">
                    <tr>
                      {preview.columns.slice(0, 8).map((col) => (
                        <th key={col} className="p-3 whitespace-nowrap">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {preview.sample_rows.slice(0, 10).map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-800/30">
                        {preview.columns.slice(0, 8).map((col) => (
                          <td key={col} className="p-3 whitespace-nowrap max-w-[150px] truncate">
                            {row[col] !== null && row[col] !== undefined && row[col] !== ''
                              ? String(row[col])
                              : <span className="text-slate-600 italic">null</span>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
};
