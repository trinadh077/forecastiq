import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { AppLayout } from '../layouts/AppLayout';
import { HomePage } from '../pages/HomePage';
import { LoginPage } from '../pages/LoginPage';
import { RegisterPage } from '../pages/RegisterPage';
import { DataStudioPage } from '../pages/DataStudioPage';
import { MLEnginePage } from '../pages/MLEnginePage';
import { ForecastStudioPage } from '../pages/ForecastStudioPage';
import { NotFoundPage } from '../pages/NotFoundPage';

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route path="/" element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route path="datasets" element={<DataStudioPage />} />
        <Route path="models" element={<MLEnginePage />} />
        <Route path="forecasts" element={<ForecastStudioPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
};
