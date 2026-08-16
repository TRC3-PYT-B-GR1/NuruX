import { useState, type FormEvent } from 'react';
import { Download, LockKeyhole, Mail, ShieldCheck, Smartphone, SunMedium } from 'lucide-react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { useLatestAppVersion } from '../hooks/useLatestAppVersion';
import { api } from '../lib/api';
import type { RootState } from '../store';
import { setCredentials, setLoading } from '../store/authSlice';

function loginErrorMessage(error: unknown) {
  if (typeof error === 'object' && error && 'response' in error) {
    const response = (error as { response?: { data?: { detail?: string; non_field_errors?: string[] } } }).response;
    return response?.data?.detail || response?.data?.non_field_errors?.[0] || 'Invalid email or password.';
  }
  return 'Unable to sign in right now. Please try again.';
}

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isLoading } = useSelector((state: RootState) => state.auth);
  const { version, downloadUrl, isLoading: isVersionLoading } = useLatestAppVersion();

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault();
    setError('');
    dispatch(setLoading(true));

    try {
      const { data } = await api.post('/accounts/login/', { username: email.trim(), password });
      const userResponse = await api.get('/accounts/me/', {
        headers: { Authorization: `Bearer ${data.access}` },
      });

      dispatch(setCredentials({
        user: userResponse.data,
        access: data.access,
        refresh: data.refresh,
      }));
      navigate('/');
    } catch (loginError) {
      setError(loginErrorMessage(loginError));
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <main className="min-h-dvh bg-white text-slate-900 lg:grid lg:grid-cols-[minmax(0,1fr)_minmax(360px,0.82fr)]">
      <section className="relative flex min-h-dvh flex-col px-6 pb-10 pt-8 sm:px-10 lg:px-16 lg:py-12 xl:px-24">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3" aria-label="NuruX">
            <span className="grid h-11 w-11 place-items-center rounded-[14px] bg-amber-400 text-slate-950 shadow-[0_10px_30px_rgba(251,191,36,0.24)]">
              <SunMedium size={25} strokeWidth={2.4} />
            </span>
            <div>
              <p className="text-xl font-black tracking-[-0.04em]">NuruX</p>
              <p className="text-[10px] font-semibold uppercase tracking-[0.19em] text-slate-400">Smart workforce</p>
            </div>
          </div>

          {downloadUrl && (
            <a
              href={downloadUrl}
              className="hidden items-center gap-2 rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-bold text-slate-700 transition hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-700 sm:flex"
              download
            >
              <Download size={17} />
              Get the APK
            </a>
          )}
        </div>

        <div className="mx-auto flex w-full max-w-[440px] flex-1 flex-col justify-center py-14 lg:mx-0">
          <div className="mb-10">
            <p className="mb-3 text-sm font-bold text-emerald-600">Welcome back</p>
            <h1 className="text-[2.4rem] font-black leading-[1.07] tracking-[-0.045em] text-slate-950 sm:text-5xl">
              Your workday,<br />right on time.
            </h1>
            <p className="mt-5 max-w-sm text-base leading-7 text-slate-500">
              Sign in with your company account to record attendance, review history, and request leave.
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            {error && (
              <div role="alert" className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
                {error}
              </div>
            )}

            <label className="block">
              <span className="mb-2 block text-sm font-bold text-slate-700">Email or employee ID</span>
              <span className="relative block">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={19} />
                <input
                  type="text"
                  required
                  autoComplete="username"
                  placeholder="you@company.com"
                  className="h-14 w-full rounded-xl border border-slate-200 bg-slate-50 pl-12 pr-4 text-[15px] outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  disabled={isLoading}
                />
              </span>
            </label>

            <label className="block">
              <span className="mb-2 block text-sm font-bold text-slate-700">Password</span>
              <span className="relative block">
                <LockKeyhole className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={19} />
                <input
                  type="password"
                  required
                  autoComplete="current-password"
                  placeholder="Enter your password"
                  className="h-14 w-full rounded-xl border border-slate-200 bg-slate-50 pl-12 pr-4 text-[15px] outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  disabled={isLoading}
                />
              </span>
            </label>

            <button
              type="button"
              onClick={() => window.alert('Contact HR support to reset your password.')}
              className="text-sm font-semibold text-emerald-600 hover:text-emerald-700"
            >
              Forgot password?
            </button>

            <button
              type="submit"
              disabled={isLoading}
              className="flex h-14 w-full items-center justify-center rounded-xl bg-slate-950 text-base font-bold text-white shadow-[0_14px_30px_rgba(15,23,42,0.18)] transition hover:bg-slate-800 focus:outline-none focus:ring-4 focus:ring-slate-950/15 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isLoading ? <span className="h-5 w-5 animate-spin rounded-full border-2 border-white/35 border-t-white" /> : 'Log In'}
            </button>
          </form>

          <div className="mt-7 sm:hidden">
            {downloadUrl ? (
              <a
                href={downloadUrl}
                download
                className="flex h-14 w-full items-center justify-center gap-2 rounded-xl border-2 border-emerald-500 font-bold text-emerald-600"
              >
                <Download size={19} /> Download Android app{version?.version_name ? ` · v${version.version_name}` : ''}
              </a>
            ) : (
              <div className="flex h-14 items-center justify-center gap-2 rounded-xl border border-slate-200 bg-slate-50 text-sm font-semibold text-slate-400">
                <Smartphone size={18} /> {isVersionLoading ? 'Checking Android version…' : 'Android download coming soon'}
              </div>
            )}
          </div>
        </div>

        <p className="text-center text-xs leading-5 text-slate-400 lg:text-left">
          Having trouble signing in? <span className="font-semibold text-slate-600">Contact HR support.</span>
        </p>
      </section>

      <aside className="relative hidden overflow-hidden bg-slate-950 p-12 text-white lg:flex lg:flex-col lg:justify-between xl:p-16">
        <div className="absolute -right-32 -top-36 h-96 w-96 rounded-full bg-emerald-500/20 blur-3xl" />
        <div className="absolute -bottom-40 -left-32 h-96 w-96 rounded-full bg-amber-400/10 blur-3xl" />

        <div className="relative z-10 flex items-center gap-2 text-sm font-semibold text-slate-300">
          <ShieldCheck size={18} className="text-emerald-400" /> Secure employee access
        </div>

        <div className="relative z-10">
          <div className="mb-9 grid h-24 w-24 place-items-center rounded-[30px] bg-amber-400 text-slate-950 shadow-[0_22px_60px_rgba(251,191,36,0.24)]">
            <SunMedium size={52} strokeWidth={1.8} />
          </div>
          <h2 className="max-w-lg text-4xl font-black leading-tight tracking-[-0.04em] xl:text-5xl">
            Next generation intelligent workforce.
          </h2>
          <p className="mt-6 max-w-md text-base leading-7 text-slate-400">
            One clear place for attendance, leave, and the moments that keep every team moving.
          </p>
        </div>

        <div className="relative z-10 rounded-2xl border border-white/10 bg-white/[0.06] p-5 backdrop-blur">
          <div className="flex items-center gap-4">
            <span className="grid h-12 w-12 place-items-center rounded-xl bg-emerald-400/15 text-emerald-400">
              <Smartphone size={23} />
            </span>
            <div className="min-w-0 flex-1">
              <p className="font-bold">Prefer the Android app?</p>
              <p className="mt-1 text-sm text-slate-400">
                {version?.version_name ? `Version ${version.version_name} is ready to install.` : 'Take NuruX with you on Android.'}
              </p>
            </div>
            {downloadUrl ? (
              <a href={downloadUrl} download aria-label="Download the NuruX Android APK" className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-emerald-500 text-white transition hover:bg-emerald-400">
                <Download size={20} />
              </a>
            ) : (
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-white/10 text-slate-500">
                <Download size={20} />
              </span>
            )}
          </div>
        </div>
      </aside>
    </main>
  );
}
