import { useEffect, useState, type FormEvent } from 'react';
import { ArrowLeft, BriefcaseBusiness, CheckCircle2, Loader2, Upload } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../lib/api';

interface Job { id: number; title: string; description: string; department: string; }

export default function CareerApplicationPage() {
  const { jobId } = useParams();
  const [job, setJob] = useState<Job | null>(null);
  const [form, setForm] = useState({ full_name: '', email: '', phone: '' });
  const [resume, setResume] = useState<File | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [submittedId, setSubmittedId] = useState<number | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get(`/recruitment/careers/jobs/${jobId}/`).then(({ data }) => setJob(data)).catch(() => setError('This position is no longer available.')).finally(() => setLoading(false));
  }, [jobId]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!jobId) return;
    setSubmitting(true); setError('');
    const payload = new FormData();
    payload.append('full_name', form.full_name); payload.append('email', form.email); payload.append('phone', form.phone);
    if (resume) payload.append('resume', resume);
    try {
      const { data } = await api.post(`/recruitment/careers/jobs/${jobId}/apply/`, payload, { headers: { 'Content-Type': 'multipart/form-data' } });
      setSubmittedId(data.id);
    } catch (requestError: any) {
      const detail = requestError.response?.data?.detail || requestError.response?.data?.non_field_errors?.[0] || requestError.response?.data?.email?.[0] || 'We could not submit your application. Please check the form and try again.';
      setError(detail);
    } finally { setSubmitting(false); }
  };

  if (loading) return <div className="flex min-h-dvh items-center justify-center bg-slate-950 text-emerald-400"><Loader2 className="h-8 w-8 animate-spin" /></div>;
  if (submittedId) return <main className="flex min-h-dvh items-center justify-center bg-slate-950 px-6 text-white"><div className="w-full max-w-lg rounded-3xl border border-white/10 bg-white/[0.06] p-10 text-center"><CheckCircle2 className="mx-auto h-14 w-14 text-emerald-400" /><h1 className="mt-6 text-3xl font-black">Application received</h1><p className="mt-3 leading-7 text-slate-400">Thank you for applying for <span className="font-semibold text-white">{job?.title}</span>. Our hiring team will review your application.</p><p className="mt-5 text-xs text-slate-500">Application reference: #{submittedId}</p><Link to="/careers" className="mt-8 inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-5 py-3 font-bold text-slate-950 hover:bg-emerald-400"><ArrowLeft size={17} /> Back to careers</Link></div></main>;
  if (!job) return <div className="flex min-h-dvh items-center justify-center bg-slate-950 px-6 text-rose-200">{error || 'Position not found.'}</div>;

  return <main className="min-h-dvh bg-slate-950 px-6 py-10 text-white sm:px-12"><div className="mx-auto max-w-3xl"><Link to="/careers" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white"><ArrowLeft size={16} /> All positions</Link><div className="mt-10 grid gap-10 lg:grid-cols-[1fr_0.9fr]"><section><span className="grid h-12 w-12 place-items-center rounded-xl bg-indigo-400/15 text-indigo-300"><BriefcaseBusiness size={23} /></span><h1 className="mt-6 text-4xl font-black">{job.title}</h1><p className="mt-2 text-emerald-300">{job.department || 'NuruX'} · Nigeria</p><div className="mt-8 whitespace-pre-wrap text-base leading-8 text-slate-400">{job.description}</div></section><form onSubmit={submit} className="rounded-2xl border border-white/10 bg-white/[0.06] p-6 shadow-2xl"><h2 className="text-xl font-bold">Apply for this role</h2>{error && <div className="mt-4 rounded-lg border border-rose-400/20 bg-rose-400/10 p-3 text-sm text-rose-200">{error}</div>}<label className="mt-5 block text-sm font-semibold text-slate-300">Full name<input required value={form.full_name} onChange={(event) => setForm({ ...form, full_name: event.target.value })} className="mt-2 h-12 w-full rounded-lg border border-white/10 bg-slate-900 px-3 text-white outline-none focus:border-emerald-400" placeholder="Jane Doe" /></label><label className="mt-4 block text-sm font-semibold text-slate-300">Email<input required type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} className="mt-2 h-12 w-full rounded-lg border border-white/10 bg-slate-900 px-3 text-white outline-none focus:border-emerald-400" placeholder="jane@example.com" /></label><label className="mt-4 block text-sm font-semibold text-slate-300">Phone<input required value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} className="mt-2 h-12 w-full rounded-lg border border-white/10 bg-slate-900 px-3 text-white outline-none focus:border-emerald-400" placeholder="080 0000 0000" /></label><label className="mt-4 block text-sm font-semibold text-slate-300">Resume <span className="font-normal text-slate-500">(PDF, DOC, DOCX)</span><span className="mt-2 flex cursor-pointer items-center gap-2 rounded-lg border border-dashed border-white/20 bg-slate-900 px-3 py-3 text-sm text-slate-400 hover:border-emerald-400"><Upload size={17} /> {resume?.name || 'Choose a file'}<input type="file" accept=".pdf,.doc,.docx" onChange={(event) => setResume(event.target.files?.[0] || null)} className="sr-only" /></span></label><button disabled={submitting} className="mt-6 flex h-12 w-full items-center justify-center gap-2 rounded-lg bg-emerald-500 font-bold text-slate-950 hover:bg-emerald-400 disabled:opacity-60">{submitting ? <Loader2 className="h-5 w-5 animate-spin" /> : 'Submit application'}</button><p className="mt-3 text-center text-[11px] text-slate-500">By applying, you consent to NuruX using your information for recruitment.</p></form></div></div></main>;
}
