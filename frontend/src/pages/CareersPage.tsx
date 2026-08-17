import { useEffect, useState } from 'react';
import { ArrowRight, BriefcaseBusiness, Loader2, LogIn, MapPin, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../lib/api';

interface Job { id: number; title: string; description: string; department: string; date_posted: string; }

export default function CareersPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/recruitment/careers/jobs/')
      .then(({ data }) => setJobs(Array.isArray(data) ? data : data.results || []))
      .catch(() => setError('We could not load open positions right now. Please try again later.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-dvh bg-slate-950 text-white">
      <header className="flex items-center justify-between border-b border-white/10 px-6 py-5 sm:px-12">
        <Link to="/careers" className="flex items-center gap-3"><span className="grid h-10 w-10 place-items-center rounded-xl bg-amber-400 text-slate-950"><Sparkles size={21} /></span><span className="text-xl font-black">NuruX Careers</span></Link>
        <Link to="/login" className="flex items-center gap-2 rounded-lg border border-white/15 px-3 py-2 text-sm font-semibold text-slate-200 hover:bg-white/10"><LogIn size={16} /> Staff login</Link>
      </header>
      <section className="mx-auto max-w-6xl px-6 py-16 sm:px-12">
        <div className="max-w-2xl"><p className="mb-3 text-sm font-bold uppercase tracking-[0.2em] text-emerald-400">Build the future of work</p><h1 className="text-4xl font-black tracking-tight sm:text-6xl">Do meaningful work with NuruX.</h1><p className="mt-5 text-lg leading-8 text-slate-400">Explore open positions and join a team building smarter workforce operations for African organizations.</p></div>
        <div className="mt-14 flex items-center justify-between"><h2 className="text-2xl font-bold">Open positions</h2><span className="text-sm text-slate-400">{jobs.length} role{jobs.length === 1 ? '' : 's'}</span></div>
        {loading && <div className="flex min-h-48 items-center justify-center"><Loader2 className="h-7 w-7 animate-spin text-emerald-400" /></div>}
        {error && <div className="mt-6 rounded-xl border border-rose-400/20 bg-rose-400/10 p-4 text-rose-200">{error}</div>}
        {!loading && !error && jobs.length === 0 && <div className="mt-6 rounded-2xl border border-white/10 bg-white/[0.04] p-10 text-center text-slate-400">No open positions at the moment. Please check back soon.</div>}
        <div className="mt-6 grid gap-5 md:grid-cols-2">{jobs.map((job) => <article key={job.id} className="group rounded-2xl border border-white/10 bg-white/[0.05] p-6 transition hover:-translate-y-1 hover:border-emerald-400/40 hover:bg-white/[0.08]"><div className="flex items-start justify-between gap-4"><span className="grid h-11 w-11 place-items-center rounded-xl bg-indigo-400/15 text-indigo-300"><BriefcaseBusiness size={22} /></span><span className="rounded-full bg-emerald-400/10 px-3 py-1 text-xs font-semibold text-emerald-300">Open</span></div><h3 className="mt-6 text-xl font-bold">{job.title}</h3><div className="mt-2 flex items-center gap-2 text-sm text-slate-400"><MapPin size={14} /> {job.department || 'NuruX'} · Nigeria</div><p className="mt-4 line-clamp-3 text-sm leading-6 text-slate-400">{job.description || 'Join the team and help us build the next generation of workforce technology.'}</p><Link to={`/careers/${job.id}`} className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-emerald-300 group-hover:text-emerald-200">View position <ArrowRight size={16} /></Link></article>)}</div>
      </section>
    </main>
  );
}
