-- Initial PostgreSQL database setup script for ForecastIQ
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Initialize roles
INSERT INTO roles (id, name, description, permissions_json)
VALUES 
  ('role-admin-id-00000000000000000001', 'ADMIN', 'System Administrator with full permissions', '{"all": true}'),
  ('role-manager-id-000000000000000002', 'MANAGER', 'Organization Manager with read/write & model training access', '{"manage_models": true, "manage_datasets": true}'),
  ('role-analyst-id-000000000000000003', 'SALES_ANALYST', 'Sales Analyst with forecast view & export access', '{"view_forecasts": true, "export_reports": true}')
ON CONFLICT (name) DO NOTHING;
