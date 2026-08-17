import { useEffect, useMemo, useState } from 'react';
import { BriefcaseBusiness, CalendarDays, ChevronRight, Loader2, Plus, Search, Sparkles, Users } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { api } from '../lib/api';

type Stage = 'Applied' | 'Screening' | 'Interview' | 'Offer';
interface Candidate { id: number; name: string; role: string; stage: Stage; score: number; applied: string; }
interface Job { id: number; title: string; }
const stages: Stage[] = ['Applied', 'Screening', 'Interview', 'Offer'];
const stageApiValues: Record<Stage, string> = { Applied: 'applied', Screening: 'screening', Interview: 'interview', Offer: 'offer' };

function results<T>(payload: { results?: T[] } | T[]): T[] { return Array.isArray(payload) ? payload : payload.results || []; }

export default function RecruitmentPage() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [query, setQuery] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [newRole, setNewRole] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const [jobsResponse, candidatesResponse] = await Promise.all([api.get('/recruitment/jobs/'), api.get('/recruitment/candidates/')]);
      const jobRows = results<{ id: number; title: string }>(jobsResponse.data);
      const candidateRows = results<{ id: number; full_name: string; job_title: string; stage: string; score: number; applied: string }>(candidatesResponse.data);
      setJobs(jobRows);
      setCandidates(candidateRows.filter((row) => row.stage !== 'rejected' && row.stage !== 'hired').map((row) => ({
        id: row.id, name: row.full_name, role: row.job_title, stage: (row.stage.charAt(0).toUpperCase() + row.stage.slice(1)) as Stage, score: row.score, applied: row.applied ? new Date(row.applied).toLocaleDateString() : '',
      })));
      setError('');
    } catch { setError('Recruitment data could not be loaded. Check that the backend migrations have been applied.'); }
    finally { setLoading(false); }
  };

  useEffect(() => { void loadData(); }, []);
  const visibleCandidates = useMemo(() => candidates.filter((candidate) => `${candidate.name} ${candidate.role}`.toLowerCase().includes(query.toLowerCase())), [candidates, query]);

  const moveCandidate = async (candidate: Candidate, direction: number) => {
    const index = stages.indexOf(candidate.stage);
    const next = stages[Math.max(0, Math.min(stages.length - 1, index + direction))];
    if (next === candidate.stage) return;
    setCandidates((current) => current.map((item) => item.id === candidate.id ? { ...item, stage: next } : item));
    try { await api.patch(`/recruitment/candidates/${candidate.id}/`, { stage: stageApiValues[next] }); }
    catch { setError('Candidate stage could not be saved.'); void loadData(); }
  };

  const createRole = async () => {
    const role = newRole.trim();
    if (!role) return;
    setSaving(true);
    try {
      const response = await api.post('/recruitment/jobs/', { title: role, department: 'General', description: `${role} opportunity at NuruX`, status: 'open' });
      setJobs((current) => [response.data, ...current]); setNewRole(''); setShowForm(false); setError('');
    } catch { setError('The new role could not be saved.'); }
    finally { setSaving(false); }
  };

  const statCards = [
    { label: 'Open roles', value: jobs.length, icon: BriefcaseBusiness, colors: 'text-indigo-600 bg-indigo-50' },
    { label: 'Candidates', value: candidates.length, icon: Users, colors: 'text-blue-600 bg-blue-50' },
    { label: 'Interviews', value: candidates.filter((candidate) => candidate.stage === 'Interview').length, icon: CalendarDays, colors: 'text-amber-600 bg-amber-50' },
    { label: 'Offers ready', value: candidates.filter((candidate) => candidate.stage === 'Offer').length, icon: Sparkles, colors: 'text-emerald-600 bg-emerald-50' },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="rounded-2xl bg-gradient-to-r from-indigo-700 via-blue-700 to-cyan-600 p-6 text-white shadow-lg">
        <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between"><div><div className="mb-2 flex items-center gap-2 text-blue-100"><Sparkles className="h-4 w-4" /> Talent workspace</div><h1 className="text-3xl font-bold">Recruitment Pipeline</h1><p className="mt-1 max-w-2xl text-sm text-blue-100">Move candidates from application to offer with a clear, collaborative hiring view.</p></div><Button onClick={() => setShowForm((value) => !value)} className="bg-white text-indigo-700 hover:bg-blue-50"><Plus className="mr-2 h-4 w-4" /> Open position</Button></div>
        {showForm && <div className="mt-5 flex flex-col gap-2 rounded-xl bg-white/10 p-3 sm:flex-row"><input value={newRole} onChange={(event) => setNewRole(event.target.value)} placeholder="Position title" className="flex-1 rounded-lg border-0 px-3 py-2 text-sm text-slate-900 outline-none" onKeyDown={(event) => event.key === 'Enter' && void createRole()} /><Button onClick={() => void createRole()} disabled={saving} className="bg-slate-900 hover:bg-slate-800">{saving ? 'Saving…' : 'Create role'}</Button></div>}
      </div>

      {error && <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">{error}</div>}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">{statCards.map(({ label, value, icon: Icon, colors }) => <div key={label} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><div className={`mb-3 flex h-10 w-10 items-center justify-center rounded-lg ${colors}`}><Icon className="h-5 w-5" /></div><p className="text-sm text-slate-500">{label}</p><p className="mt-1 text-2xl font-bold text-slate-900">{value}</p></div>)}</div>

      <div className="rounded-xl border border-slate-200 bg-white shadow-sm"><div className="flex flex-col gap-4 border-b border-slate-100 p-5 sm:flex-row sm:items-center sm:justify-between"><div><h2 className="text-lg font-bold text-slate-900">Candidate pipeline</h2><p className="text-sm text-slate-500">Stages and shortlist scores are saved to the database.</p></div><div className="relative w-full sm:w-64"><Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search candidates" className="w-full rounded-lg border border-slate-200 py-2 pl-9 pr-3 text-sm outline-none focus:border-indigo-400" /></div></div>
        {loading ? <div className="flex min-h-60 items-center justify-center"><Loader2 className="h-7 w-7 animate-spin text-indigo-600" /></div> : <div className="grid gap-4 p-5 lg:grid-cols-4">{stages.map((stage) => <div key={stage} className="min-h-52 rounded-xl bg-slate-50 p-3"><div className="mb-3 flex items-center justify-between"><h3 className="text-sm font-semibold text-slate-700">{stage}</h3><span className="rounded-full bg-white px-2 py-0.5 text-xs text-slate-500">{visibleCandidates.filter((candidate) => candidate.stage === stage).length}</span></div><div className="space-y-3">{visibleCandidates.filter((candidate) => candidate.stage === stage).map((candidate) => <div key={candidate.id} className="rounded-lg border border-slate-200 bg-white p-3 shadow-sm"><div className="flex items-start justify-between gap-2"><div><p className="text-sm font-semibold text-slate-900">{candidate.name}</p><p className="text-xs text-slate-500">{candidate.role}</p></div><span className="rounded bg-emerald-50 px-1.5 py-0.5 text-xs font-semibold text-emerald-700">{candidate.score}%</span></div><p className="mt-2 text-[11px] text-slate-400">Applied {candidate.applied}</p><div className="mt-3 flex items-center justify-between"><button disabled={stage === stages[0]} onClick={() => void moveCandidate(candidate, -1)} className="text-xs text-slate-500 disabled:opacity-30">Back</button><button disabled={stage === stages[stages.length - 1]} onClick={() => void moveCandidate(candidate, 1)} className="flex items-center text-xs font-medium text-indigo-600 disabled:opacity-30">Advance <ChevronRight className="ml-0.5 h-3 w-3" /></button></div></div>)}{visibleCandidates.filter((candidate) => candidate.stage === stage).length === 0 && <p className="py-5 text-center text-xs text-slate-400">No candidates yet</p>}</div></div>)}</div>}
      </div>
      {candidates.length === 0 && !loading && <div className="text-center text-xs text-slate-400">Recruitment is connected. Add a role or run the demo seed command to populate candidates.</div>}
    </div>
  );
}
