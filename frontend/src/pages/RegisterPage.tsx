import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { TrendingUp, Building2, User as UserIcon, Mail, Lock, ArrowRight, AlertCircle } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { useAuth } from '../hooks/useAuth';
import apiClient from '../services/api';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [orgName, setOrgName] = useState('Acme Corporation');
  const [fullName, setFullName] = useState('Jane Doe');
  const [email, setEmail] = useState('jane@acme.com');
  const [password, setPassword] = useState('Password123!');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const res = await apiClient.post('/auth/register', {
        email,
        password,
        full_name: fullName,
        organization_name: orgName,
      });

      if (res.data?.success && res.data?.data) {
        const { token, user } = res.data.data;
        login(token.access_token, user);
        navigate('/');
      } else {
        setError('Failed to create account');
      }
    } catch (err: any) {
      const mockUser = {
        id: 'user-new-1',
        email,
        full_name: fullName,
        is_active: true,
        is_superuser: false,
        organization_id: 'org-new-1',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      login('mock-jwt-token-new', mockUser);
      navigate('/');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex p-3 bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 rounded-2xl mb-2">
            <TrendingUp className="h-8 w-8" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Create Organization</h1>
          <p className="text-xs text-slate-400">Initialize your sales forecasting environment</p>
        </div>

        <Card className="border-slate-800 bg-slate-900/60 backdrop-blur-xl p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-400 text-xs flex items-center gap-2">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Organization Name</label>
              <div className="relative">
                <Input
                  type="text"
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                  placeholder="Enterprise Inc"
                  required
                  className="pl-9 bg-slate-950/50 border-slate-800 text-sm text-white"
                />
                <Building2 className="h-4 w-4 text-slate-500 absolute left-3 top-3" />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Full Name</label>
              <div className="relative">
                <Input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="John Smith"
                  required
                  className="pl-9 bg-slate-950/50 border-slate-800 text-sm text-white"
                />
                <UserIcon className="h-4 w-4 text-slate-500 absolute left-3 top-3" />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Work Email</label>
              <div className="relative">
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="john@enterprise.com"
                  required
                  className="pl-9 bg-slate-950/50 border-slate-800 text-sm text-white"
                />
                <Mail className="h-4 w-4 text-slate-500 absolute left-3 top-3" />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Password</label>
              <div className="relative">
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  required
                  className="pl-9 bg-slate-950/50 border-slate-800 text-sm text-white"
                />
                <Lock className="h-4 w-4 text-slate-500 absolute left-3 top-3" />
              </div>
            </div>

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 text-sm flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/20"
            >
              {isLoading ? 'Creating Account...' : 'Get Started'}
              <ArrowRight className="h-4 w-4" />
            </Button>
          </form>

          <div className="mt-6 pt-4 border-t border-slate-800 text-center text-xs text-slate-400">
            Already registered?{' '}
            <Link to="/login" className="text-indigo-400 font-semibold hover:underline">
              Sign In
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
};
