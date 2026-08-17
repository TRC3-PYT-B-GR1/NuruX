import { useEffect, useState } from 'react';
import { Loader2, Plus, Target, TrendingUp } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { api } from '../lib/api';

interface KPI {
  id: number;
  name: string;
  description: string;
  target: string | number;
  created_at?: string;
}

function rows<T>(payload: { results?: T[] } | T[]): T[] {
  return Array.isArray(payload) ? payload : payload.results || [];
}

export default function PerformancePage() {
  const [kpis, setKpis] = useState<KPI[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({ name: '', description: '', target: '' });

  const loadKpis = async () => {
    setLoading(true);
    try {
      const response = await api.get('/performance/kpis/');
      setKpis(rows<KPI>(response.data));
      setError('');
    } catch {
      setError('KPI data could not be loaded. Check that the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void loadKpis(); }, []);

  const createKpi = async () => {
    if (!form.name.trim() || form.target === '') return;
    setSaving(true);
    try {
      const response = await api.post('/performance/kpis/', {
        name: form.name.trim(),
        description: form.description.trim(),
        target: Number(form.target),
      });
      setKpis((current) => [response.data, ...current]);
      setForm({ name: '', description: '', target: '' });
      setShowForm(false);
      setError('');
    } catch {
      setError('The KPI could not be saved.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="rounded-2xl bg-gradient-to-r from-violet-700 via-indigo-700 to-blue-700 p-6 text-white shadow-lg">
        <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2 text-indigo-100"><TrendingUp className="h-4 w-4" /> Performance workspace</div>
            <h1 className="text-3xl font-bold">KPIs & Targets</h1>
            <p className="mt-1 max-w-2xl text-sm text-indigo-100">Define the measures your teams use to track progress and performance.</p>
          </div>
          <Button onClick={() => setShowForm((value) => !value)} className="bg-white text-indigo-700 hover:bg-indigo-50"><Plus className="mr-2 h-4 w-4" /> Add KPI</Button>
        </div>
        {showForm && <div className="mt-5 grid gap-2 rounded-xl bg-white/10 p-3 md:grid-cols-[1fr_1.5fr_150px_auto]">
          <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} placeholder="KPI name" className="rounded-lg border-0 px-3 py-2 text-sm text-slate-900 outline-none" />
          <input value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} placeholder="Description" className="rounded-lg border-0 px-3 py-2 text-sm text-slate-900 outline-none" />
          <input type="number" min="0" step="1" value={form.target} onChange={(event) => setForm({ ...form, target: event.target.value })} placeholder="Target" className="rounded-lg border-0 px-3 py-2 text-sm text-slate-900 outline-none" />
          <Button onClick={() => void createKpi()} disabled={saving} className="bg-slate-900 hover:bg-slate-800">{saving ? 'Saving…' : 'Save'}</Button>
        </div>}
      </div>

      {error && <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">{error}</div>}
      {loading ? <div className="flex min-h-60 items-center justify-center"><Loader2 className="h-7 w-7 animate-spin text-indigo-600" /></div> : kpis.length === 0 ? <div className="rounded-xl border border-dashed border-slate-300 bg-white p-12 text-center text-sm text-slate-500">No KPIs yet. Add the first target for your team.</div> : <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{kpis.map((kpi) => <div key={kpi.id} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><div className="mb-4 flex items-start justify-between gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600"><Target className="h-5 w-5" /></div><span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700">Target {kpi.target}</span></div><h2 className="font-semibold text-slate-900">{kpi.name}</h2><p className="mt-2 text-sm text-slate-500">{kpi.description || 'No description provided.'}</p></div>)}</div>}
    </div>
  );
}
