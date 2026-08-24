export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  organization_id?: string;
  role_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  domain?: string;
  settings_json?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface Dataset {
  id: string;
  name: string;
  file_path: string;
  file_size_bytes: number;
  row_count?: number;
  column_schema?: {
    columns: string[];
    types: Record<string, string>;
  };
  status: string;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export interface MLModel {
  id: string;
  name: string;
  algorithm: string;
  hyperparameters?: Record<string, any>;
  metrics?: {
    mape: number;
    rmse: number;
    r2_score: number;
    mae?: number;
  };
  status: string;
  dataset_id: string;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export interface ForecastPoint {
  date: string;
  revenue?: number;
  predicted?: number;
  lower_bound?: number;
  upper_bound?: number;
  type: 'historical' | 'projected';
}

export interface ForecastData {
  summary: {
    total_projected_revenue: number;
    projected_arr: number;
    growth_rate_pct: number;
    horizon_days: number;
    confidence_interval: number;
    avg_daily_revenue: number;
  };
  historical: ForecastPoint[];
  projected: ForecastPoint[];
}

export interface Forecast {
  id: string;
  title: string;
  horizon_days: number;
  confidence_interval: number;
  forecast_data: ForecastData;
  organization_id: string;
  model_id: string;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}
