import React, { useState, useEffect } from 'react';
import { Upload, Database, FileText, CheckCircle2, Table, AlertTriangle, BarChart3, Shield, Info } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';
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

interface QualityReport {
  overall_score: number;
  scores: { completeness: number; outlier_free: number; uniqueness: number; consistency: number };
  null_analysis: { column: string; total_missing: number; missing_pct: number }[];
  outlier_analysis: { column: string; outlier_count: number; outlier_pct: number }[];
  duplicates: { count: number; pct: number };
  type_distribution: Record<string, number>;
  consistency_issues: { column: string; issue: string; severity: string }[];
  recommendations: { priority: string; message: string }[];
}

export const DataStudioPage: React.FC = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<Dataset | null>(null);
  const [preview, setPreview] = useState<DatasetPreview | null>(null);
  const [qualityReport, setQualityReport] = useState<QualityReport | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [isLoadingQuality, setIsLoadingQuality] = useState(false);

  useEffect(() => {
    fetchDatasets();
  }, []);

  useEffect(() => {
    if (selectedDataset) {
      fetchPreview(selectedDataset.id);
      setQualityReport(null);
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

  const fetchQualityReport = async (datasetId: string) => {
    setIsLoadingQuality(true);
    try {
      const res = await apiClient.get(`/datasets/${datasetId}/quality`);
      if (res.data?.data) {
        setQualityReport(res.data.data);
      }
    } catch (e) {
      setQualityReport(null);
    } finally {
      setIsLoadingQuality(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await apiClient.post('/datasets/upload', formData);
      if (res.data?.data) {
        setUploadSuccess(true);
        setTimeout(() => setUploadSuccess(false), 4000);
        fetchDatasets();
        setSelectedDataset(res.data.data);
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.response?.data?.error?.message || e?.message || 'Upload failed';
      alert(`Upload failed: ${msg}`);
    } finally {
      setIsUploading(false);
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

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-emerald-400';
    if (score >= 70) return 'text-amber-400';
    return 'text-rose-400';
  };

  const getPriorityColor = (p: string) => {
    if (p === 'high') return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
    if (p === 'medium') return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
    return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
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
              <button
                onClick={() => fetchQualityReport(selectedDataset.id)}
                disabled={isLoadingQuality}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-[11px] font-medium rounded-lg transition-all"
              >
                <Shield className="h-3.5 w-3.5" />
                {isLoadingQuality ? 'Analyzing...' : 'Data Quality Report'}
              </button>
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

          {/* DATA QUALITY REPORT */}
          {qualityReport && (
            <div className="space-y-6 border-t border-slate-800 pt-6">
              <h4 className="text-sm font-semibold text-white flex items-center gap-2">
                <Shield className="h-4 w-4 text-indigo-400" />
                Data Quality Report
              </h4>

              {/* Overall Score + Dimension Scores */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <Card className="p-4 border-slate-800 bg-slate-900/60 text-center">
                  <span className="text-[10px] text-slate-400 uppercase tracking-wider block mb-1">Overall</span>
                  <span className={`text-3xl font-bold ${getScoreColor(qualityReport.overall_score)}`}>
                    {qualityReport.overall_score}
                  </span>
                  <span className="text-[10px] text-slate-500 block">/100</span>
                </Card>
                {Object.entries(qualityReport.scores).map(([key, val]) => (
                  <Card key={key} className="p-4 border-slate-800 bg-slate-900/60 text-center">
                    <span className="text-[10px] text-slate-400 uppercase tracking-wider block mb-1">
                      {key.replace('_', ' ')}
                    </span>
                    <span className={`text-2xl font-bold ${getScoreColor(val)}`}>{val}</span>
                    <span className="text-[10px] text-slate-500 block">%</span>
                  </Card>
                ))}
              </div>

              {/* Charts Row */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Null Analysis Bar Chart */}
                <div>
                  <h5 className="text-[10px] font-semibold text-slate-300 uppercase tracking-wider mb-3">Missing Values by Column</h5>
                  <div className="h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={qualityReport.null_analysis.map((n) => ({
                          column: n.column.length > 12 ? n.column.slice(0, 12) + '...' : n.column,
                          Missing: n.total_missing,
                          Present: Math.max(0, (preview?.sample_rows?.length || 20) - n.total_missing),
                        }))}
                        margin={{ top: 5, right: 10, left: -10, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis dataKey="column" stroke="#64748b" tick={{ fontSize: 9 }} />
                        <YAxis stroke="#64748b" tick={{ fontSize: 9 }} />
                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '11px' }} />
                        <Legend wrapperStyle={{ fontSize: '10px' }} />
                        <Bar dataKey="Present" stackId="a" fill="#10b981" radius={[0, 0, 0, 0]} />
                        <Bar dataKey="Missing" stackId="a" fill="#ef4444" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Type Distribution Radar */}
                <div>
                  <h5 className="text-[10px] font-semibold text-slate-300 uppercase tracking-wider mb-3">Column Type Distribution</h5>
                  <div className="h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart
                        data={Object.entries(qualityReport.type_distribution).map(([type, count]) => ({
                          type,
                          count,
                        }))}
                        margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
                      >
                        <PolarGrid stroke="#1e293b" />
                        <PolarAngleAxis dataKey="type" tick={{ fontSize: 10, fill: '#94a3b8' }} />
                        <PolarRadiusAxis tick={{ fontSize: 8, fill: '#64748b' }} />
                        <Radar name="Columns" dataKey="count" stroke="#6366f1" fill="#6366f1" fillOpacity={0.3} />
                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '11px' }} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* Duplicates + Consistency */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="p-4 border-slate-800 bg-slate-900/60">
                  <h5 className="text-[10px] font-semibold text-slate-300 uppercase tracking-wider mb-2">Duplicate Rows</h5>
                  <span className="text-2xl font-bold text-white">{qualityReport.duplicates.count}</span>
                  <span className="text-xs text-slate-400 ml-2">({qualityReport.duplicates.pct}%)</span>
                </Card>
                <Card className="p-4 border-slate-800 bg-slate-900/60">
                  <h5 className="text-[10px] font-semibold text-slate-300 uppercase tracking-wider mb-2">Consistency Issues</h5>
                  {qualityReport.consistency_issues.length === 0 ? (
                    <span className="text-xs text-emerald-400">No issues found</span>
                  ) : (
                    <div className="space-y-1">
                      {qualityReport.consistency_issues.map((ci, i) => (
                        <span key={i} className="text-[10px] text-amber-400 block">{ci.column}: {ci.issue}</span>
                      ))}
                    </div>
                  )}
                </Card>
              </div>

              {/* Recommendations */}
              <Card className="p-4 border-slate-800 bg-slate-900/60">
                <h5 className="text-[10px] font-semibold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-1">
                  <Info className="h-3 w-3" /> Recommendations
                </h5>
                <div className="space-y-2">
                  {qualityReport.recommendations.map((rec, i) => (
                    <div key={i} className={`p-2 rounded-lg text-[11px] flex items-start gap-2 border ${getPriorityColor(rec.priority)}`}>
                      <span className="font-semibold uppercase text-[9px] shrink-0 mt-0.5">{rec.priority}</span>
                      <span>{rec.message}</span>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}

          {/* Sample Data Preview Table */}
          {preview && preview.sample_rows.length > 0 && !qualityReport && (
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
