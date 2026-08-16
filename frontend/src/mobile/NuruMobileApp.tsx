import {
  ArrowLeft,
  Bell,
  CalendarDays,
  Check,
  ChevronLeft,
  ChevronRight,
  Download,
  HelpCircle,
  History,
  Home,
  LoaderCircle,
  LogOut,
  MapPin,
  Plus,
  ScanLine,
  Smartphone,
  SunMedium,
  UserRound,
  X,
} from 'lucide-react';
import { useCallback, useEffect, useMemo, useRef, useState, type FormEvent } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { useLatestAppVersion } from '../hooks/useLatestAppVersion';
import { api } from '../lib/api';
import type { RootState } from '../store';
import { logout } from '../store/authSlice';

type AppTab = 'home' | 'history' | 'profile';
type AppView = 'main' | 'leave' | 'scanner';

interface AttendanceRecord {
  id: number;
  date: string;
  clock_in: string | null;
  clock_out: string | null;
  status: string;
}

interface TodayStatus {
  attendance: AttendanceRecord | null;
  is_checked_in: boolean;
  is_checked_out: boolean;
}

interface LeaveBalance {
  id: number;
  leave_type: string;
  year: number;
  total_allocated: number;
  used_days: number;
  remaining_days: number;
}

interface LeaveRequest {
  id: number;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: string;
  duration_days: number;
}

interface LeaveFormState {
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
}

const initialLeaveForm: LeaveFormState = {
  leave_type: 'ANNUAL',
  start_date: '',
  end_date: '',
  reason: '',
};

function listFrom<T>(data: T[] | { results?: T[] }) {
  return Array.isArray(data) ? data : data.results || [];
}

function apiErrorMessage(error: unknown, fallback: string) {
  if (typeof error === 'object' && error && 'response' in error) {
    const data = (error as { response?: { data?: Record<string, unknown> } }).response?.data;
    if (data) {
      if (typeof data.detail === 'string') return data.detail;
      if (typeof data.error === 'string') return data.error;
      const first = Object.values(data)[0];
      if (Array.isArray(first)) return String(first[0]);
      if (typeof first === 'string') return first;
    }
  }
  return fallback;
}

function titleCase(value: string) {
  return value.toLowerCase().replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function friendlyTime(value: string | null | undefined) {
  if (!value) return '—';
  return new Intl.DateTimeFormat(undefined, { hour: 'numeric', minute: '2-digit' }).format(new Date(value));
}

function friendlyDate(value: string) {
  return new Intl.DateTimeFormat(undefined, { weekday: 'short', day: 'numeric', month: 'short' }).format(
    new Date(`${value}T00:00:00`),
  );
}

function greeting() {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning,';
  if (hour < 17) return 'Good afternoon,';
  return 'Good evening,';
}

function SplashScreen() {
  return (
    <div className="flex min-h-dvh flex-col items-center justify-center bg-slate-950 px-8 text-center text-white sm:min-h-[calc(100dvh-2rem)]">
      <div className="grid h-24 w-24 place-items-center rounded-[30px] bg-amber-400 text-slate-950 shadow-[0_24px_70px_rgba(251,191,36,0.28)]">
        <SunMedium size={52} strokeWidth={1.9} />
      </div>
      <h1 className="mt-7 text-4xl font-black tracking-[-0.05em]">NuruX</h1>
      <p className="mt-3 max-w-xs text-sm leading-6 text-slate-400">Next generation intelligent workforce</p>
      <LoaderCircle className="mt-12 animate-spin text-emerald-400" size={25} />
    </div>
  );
}

function PageHeader({ title, onBack }: { title: string; onBack: () => void }) {
  return (
    <header className="sticky top-0 z-20 flex h-18 items-center border-b border-slate-100 bg-white/95 px-5 backdrop-blur">
      <button
        type="button"
        onClick={onBack}
        aria-label="Go back"
        className="grid h-10 w-10 place-items-center rounded-xl text-slate-800 transition hover:bg-slate-100"
      >
        <ArrowLeft size={21} />
      </button>
      <h1 className="absolute left-1/2 -translate-x-1/2 text-lg font-extrabold text-slate-950">{title}</h1>
    </header>
  );
}

function StatusPill({ status }: { status: string }) {
  const normalized = status.toUpperCase();
  const style = normalized === 'PRESENT' || normalized === 'ON_TIME'
    ? 'bg-emerald-50 text-emerald-600'
    : normalized === 'LATE' || normalized === 'PENDING' || normalized === 'APPROVED_BY_MANAGER'
      ? 'bg-amber-50 text-amber-700'
      : normalized === 'APPROVED_BY_HR'
        ? 'bg-emerald-50 text-emerald-600'
        : 'bg-red-50 text-red-500';
  const label = normalized === 'PRESENT' || normalized === 'ON_TIME'
    ? 'On Time'
    : normalized === 'APPROVED_BY_MANAGER'
      ? 'Manager Approved'
      : normalized === 'APPROVED_BY_HR'
        ? 'Approved'
        : titleCase(normalized);

  return <span className={`rounded-full px-3.5 py-1.5 text-[11px] font-extrabold ${style}`}>{label}</span>;
}

function HomeScreen({
  name,
  role,
  today,
  isLoading,
  onScan,
  onLeave,
  onLogout,
}: {
  name: string;
  role: string;
  today: TodayStatus | null;
  isLoading: boolean;
  onScan: () => void;
  onLeave: () => void;
  onLogout: () => void;
}) {
  const isCheckedIn = today?.is_checked_in === true;
  const hasCheckedOut = today?.is_checked_out === true;
  const statusLabel = hasCheckedOut ? 'Checked Out' : isCheckedIn ? 'Checked In' : 'Not Checked In';

  return (
    <div className="min-h-full bg-white">
      <header className="relative overflow-hidden bg-slate-950 px-6 pb-9 pt-10 text-white">
        <div className="absolute -right-12 -top-16 h-48 w-48 rounded-full bg-emerald-500/15 blur-3xl" />
        <div className="relative flex items-start justify-between">
          <div>
            <p className="text-sm text-slate-400">{greeting()}</p>
            <h1 className="mt-1 max-w-[320px] truncate text-2xl font-black tracking-[-0.035em]">{name}</h1>
            <p className="mt-1 text-xs font-medium capitalize text-slate-400">{titleCase(role)}</p>
          </div>
          <button type="button" onClick={onLogout} aria-label="Log out" className="grid h-10 w-10 place-items-center rounded-xl text-slate-300 transition hover:bg-white/10 hover:text-white">
            <LogOut size={20} />
          </button>
        </div>
      </header>

      <section className="px-6 py-7">
        <div className="flex items-end justify-between">
          <div>
            <p className="text-sm font-bold text-slate-400">Today's Status</p>
            <h2 className="mt-1 text-[1.75rem] font-black tracking-[-0.04em] text-slate-950">{statusLabel}</h2>
          </div>
          <span className={`mb-1 h-3 w-3 rounded-full ${hasCheckedOut ? 'bg-slate-400' : isCheckedIn ? 'bg-emerald-500' : 'bg-amber-400'} shadow-[0_0_0_6px_rgba(16,185,129,0.08)]`} />
        </div>

        {today?.attendance && (
          <div className="mt-5 grid grid-cols-2 gap-3 rounded-2xl border border-slate-100 bg-slate-50 p-4">
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.12em] text-slate-400">Clock in</p>
              <p className="mt-1 text-lg font-black text-slate-900">{friendlyTime(today.attendance.clock_in)}</p>
            </div>
            <div className="border-l border-slate-200 pl-4">
              <p className="text-[11px] font-bold uppercase tracking-[0.12em] text-slate-400">Clock out</p>
              <p className="mt-1 text-lg font-black text-slate-900">{friendlyTime(today.attendance.clock_out)}</p>
            </div>
          </div>
        )}

        <button
          type="button"
          onClick={onScan}
          disabled={isLoading || hasCheckedOut}
          className={`mt-7 flex h-15 w-full items-center justify-center gap-2.5 rounded-xl text-base font-extrabold text-white shadow-lg transition active:scale-[0.99] disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none ${isCheckedIn ? 'bg-red-500 shadow-red-500/20 hover:bg-red-600' : 'bg-emerald-500 shadow-emerald-500/20 hover:bg-emerald-600'}`}
        >
          {isLoading ? <LoaderCircle className="animate-spin" size={20} /> : <ScanLine size={21} />}
          {hasCheckedOut ? 'Attendance Complete for Today' : isCheckedIn ? 'Scan QR to Clock Out' : 'Scan QR to Check In'}
        </button>

        <button
          type="button"
          onClick={onLeave}
          className="mt-4 flex h-15 w-full items-center justify-center gap-2.5 rounded-xl border-2 border-emerald-500 bg-white text-base font-extrabold text-emerald-600 transition hover:bg-emerald-50 active:scale-[0.99]"
        >
          <CalendarDays size={21} /> Request for Leave
        </button>

        <div className="mt-8 rounded-2xl bg-slate-950 p-5 text-white">
          <div className="flex items-start gap-4">
            <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-emerald-400/15 text-emerald-400">
              <MapPin size={21} />
            </span>
            <div>
              <p className="font-extrabold">Ready when you arrive</p>
              <p className="mt-1 text-sm leading-6 text-slate-400">Allow camera and location access when scanning your workplace QR code.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function HistoryScreen({ records, isLoading }: { records: AttendanceRecord[]; isLoading: boolean }) {
  const [month, setMonth] = useState(() => {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), 1);
  });

  const monthRecords = useMemo(() => records.filter((record) => {
    const date = new Date(`${record.date}T00:00:00`);
    return date.getMonth() === month.getMonth() && date.getFullYear() === month.getFullYear();
  }), [month, records]);

  const stats = useMemo(() => monthRecords.reduce((counts, record) => {
    if (record.status === 'PRESENT' || record.status === 'ON_TIME') counts.onTime += 1;
    else if (record.status === 'LATE') counts.late += 1;
    else counts.absent += 1;
    return counts;
  }, { onTime: 0, late: 0, absent: 0 }), [monthRecords]);

  const shiftMonth = (amount: number) => setMonth((current) => new Date(current.getFullYear(), current.getMonth() + amount, 1));

  return (
    <section className="px-6 pb-8 pt-8">
      <h1 className="text-[1.75rem] font-black tracking-[-0.04em] text-slate-950">Attendance History</h1>

      <div className="mt-6 flex items-center justify-between">
        <button type="button" onClick={() => shiftMonth(-1)} aria-label="Previous month" className="grid h-10 w-10 place-items-center rounded-xl hover:bg-slate-100">
          <ChevronLeft size={20} />
        </button>
        <p className="font-extrabold text-slate-900">
          {new Intl.DateTimeFormat(undefined, { month: 'long', year: 'numeric' }).format(month)}
        </p>
        <button type="button" onClick={() => shiftMonth(1)} aria-label="Next month" className="grid h-10 w-10 place-items-center rounded-xl hover:bg-slate-100">
          <ChevronRight size={20} />
        </button>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2.5">
        <div className="rounded-xl bg-emerald-50 p-3.5 text-emerald-600">
          <p className="text-2xl font-black">{stats.onTime}</p><p className="mt-1 text-[11px] font-semibold">On time</p>
        </div>
        <div className="rounded-xl bg-amber-50 p-3.5 text-amber-700">
          <p className="text-2xl font-black">{stats.late}</p><p className="mt-1 text-[11px] font-semibold">Late</p>
        </div>
        <div className="rounded-xl bg-red-50 p-3.5 text-red-500">
          <p className="text-2xl font-black">{stats.absent}</p><p className="mt-1 text-[11px] font-semibold">Absent</p>
        </div>
      </div>

      <div className="mt-8">
        {isLoading ? (
          <div className="grid min-h-52 place-items-center"><LoaderCircle className="animate-spin text-slate-700" /></div>
        ) : monthRecords.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-200 px-5 py-12 text-center">
            <History className="mx-auto text-slate-300" size={34} />
            <p className="mt-3 font-bold text-slate-700">No attendance yet</p>
            <p className="mt-1 text-sm text-slate-400">Records for this month will appear here.</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {monthRecords.map((record) => (
              <div key={record.id} className="flex items-center justify-between py-4">
                <div>
                  <p className="font-extrabold text-slate-900">{friendlyDate(record.date)}</p>
                  <p className="mt-1 text-sm text-slate-400">{friendlyTime(record.clock_in)}</p>
                </div>
                <StatusPill status={record.status} />
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

function LeaveScreen({
  balances,
  requests,
  isLoading,
  onBack,
  onRefresh,
  notify,
}: {
  balances: LeaveBalance[];
  requests: LeaveRequest[];
  isLoading: boolean;
  onBack: () => void;
  onRefresh: () => Promise<void>;
  notify: (message: string, tone?: 'success' | 'error') => void;
}) {
  const [showForm, setShowForm] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [form, setForm] = useState(initialLeaveForm);

  const submitRequest = async (event: FormEvent) => {
    event.preventDefault();
    if (!form.start_date || !form.end_date || !form.reason.trim()) {
      notify('Please complete every leave field.', 'error');
      return;
    }
    setIsSubmitting(true);
    try {
      await api.post('/leave/leave-requests/', { ...form, reason: form.reason.trim() });
      await onRefresh();
      setForm(initialLeaveForm);
      setShowForm(false);
      notify('Leave request submitted.');
    } catch (error) {
      notify(apiErrorMessage(error, 'Unable to submit your leave request.'), 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const cancelRequest = async (id: number) => {
    try {
      await api.post(`/leave/leave-requests/${id}/cancel/`);
      await onRefresh();
      notify('Leave request cancelled.');
    } catch (error) {
      notify(apiErrorMessage(error, 'Unable to cancel this request.'), 'error');
    }
  };

  return (
    <div className="relative min-h-full bg-white pb-24">
      <PageHeader title="Leave" onBack={onBack} />
      <section className="px-6 py-7">
        <h2 className="text-[1.65rem] font-black tracking-[-0.04em] text-slate-950">Your leave balance</h2>
        <p className="mt-2 text-sm leading-6 text-slate-500">Plan time away and follow each request from one place.</p>

        {isLoading ? (
          <div className="grid h-40 place-items-center"><LoaderCircle className="animate-spin" /></div>
        ) : balances.length === 0 ? (
          <div className="mt-6 rounded-2xl border border-dashed border-slate-200 p-6 text-center text-sm text-slate-400">No leave balance has been allocated yet.</div>
        ) : (
          <div className="mt-6 grid grid-cols-2 gap-3">
            {balances.map((balance, index) => (
              <div key={balance.id} className={`rounded-2xl p-4 ${index % 2 ? 'bg-amber-50 text-amber-800' : 'bg-emerald-50 text-emerald-700'}`}>
                <p className="text-3xl font-black">{balance.remaining_days}</p>
                <p className="mt-1 text-xs font-bold">{titleCase(balance.leave_type)}</p>
                <p className="mt-3 text-[10px] font-semibold opacity-65">of {balance.total_allocated} days · {balance.year}</p>
              </div>
            ))}
          </div>
        )}

        <h2 className="mt-9 text-lg font-black text-slate-950">Request history</h2>
        <div className="mt-3 space-y-3">
          {requests.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-slate-200 px-5 py-9 text-center text-sm text-slate-400">Your leave requests will appear here.</div>
          ) : requests.map((request) => (
            <article key={request.id} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-extrabold text-slate-900">{titleCase(request.leave_type)}</p>
                  <p className="mt-1 text-xs font-medium text-slate-400">
                    {friendlyDate(request.start_date)} – {friendlyDate(request.end_date)} · {request.duration_days} day{request.duration_days === 1 ? '' : 's'}
                  </p>
                </div>
                <StatusPill status={request.status} />
              </div>
              <p className="mt-3 line-clamp-2 text-sm leading-6 text-slate-600">{request.reason}</p>
              {request.status === 'PENDING' && (
                <button type="button" onClick={() => void cancelRequest(request.id)} className="mt-3 text-xs font-extrabold text-red-500 hover:text-red-600">Cancel request</button>
              )}
            </article>
          ))}
        </div>
      </section>

      <button
        type="button"
        onClick={() => setShowForm(true)}
        className="fixed bottom-7 right-[max(1.5rem,calc((100vw-592px)/2))] z-30 flex h-14 items-center gap-2 rounded-full bg-slate-950 px-5 font-extrabold text-white shadow-xl shadow-slate-950/20 transition hover:bg-slate-800"
      >
        <Plus size={20} /> Request leave
      </button>

      {showForm && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-slate-950/55 p-0 backdrop-blur-sm sm:p-4" onMouseDown={(event) => {
          if (event.target === event.currentTarget) setShowForm(false);
        }}>
          <form onSubmit={submitRequest} className="w-full max-w-[608px] rounded-t-[28px] bg-white px-6 pb-8 pt-5 shadow-2xl sm:rounded-[28px]">
            <div className="mx-auto mb-4 h-1 w-10 rounded-full bg-slate-200 sm:hidden" />
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-black text-slate-950">Request Leave</h3>
              <button type="button" onClick={() => setShowForm(false)} aria-label="Close leave request" className="grid h-10 w-10 place-items-center rounded-xl hover:bg-slate-100"><X size={20} /></button>
            </div>

            <label className="mt-5 block text-sm font-bold text-slate-700">
              Leave Type
              <select value={form.leave_type} onChange={(event) => setForm({ ...form, leave_type: event.target.value })} className="mt-2 h-13 w-full rounded-xl border border-slate-200 bg-white px-3 outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10">
                {['ANNUAL', 'CASUAL', 'MEDICAL', 'STUDY', 'COMPASSIONATE', 'MATERNITY', 'PATERNITY'].map((type) => <option key={type} value={type}>{titleCase(type)}</option>)}
              </select>
            </label>

            <div className="mt-4 grid grid-cols-2 gap-3">
              <label className="text-sm font-bold text-slate-700">Start Date
                <input type="date" required min={new Date().toISOString().slice(0, 10)} value={form.start_date} onChange={(event) => setForm({ ...form, start_date: event.target.value })} className="mt-2 h-13 w-full min-w-0 rounded-xl border border-slate-200 px-3 text-sm outline-none focus:border-emerald-500" />
              </label>
              <label className="text-sm font-bold text-slate-700">End Date
                <input type="date" required min={form.start_date || new Date().toISOString().slice(0, 10)} value={form.end_date} onChange={(event) => setForm({ ...form, end_date: event.target.value })} className="mt-2 h-13 w-full min-w-0 rounded-xl border border-slate-200 px-3 text-sm outline-none focus:border-emerald-500" />
              </label>
            </div>

            <label className="mt-4 block text-sm font-bold text-slate-700">Reason
              <textarea required rows={3} value={form.reason} onChange={(event) => setForm({ ...form, reason: event.target.value })} placeholder="Why are you requesting leave?" className="mt-2 w-full resize-none rounded-xl border border-slate-200 p-3 outline-none focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10" />
            </label>

            <button type="submit" disabled={isSubmitting} className="mt-5 flex h-13 w-full items-center justify-center rounded-xl bg-slate-950 font-extrabold text-white disabled:opacity-60">
              {isSubmitting ? <LoaderCircle className="animate-spin" size={20} /> : 'Submit Request'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

function getBrowserPosition() {
  return new Promise<string>((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Location is not available in this browser.'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => resolve(`${coords.latitude.toFixed(6)},${coords.longitude.toFixed(6)}`),
      () => reject(new Error('Location access is required to record attendance.')),
      { enableHighAccuracy: true, timeout: 12000, maximumAge: 15000 },
    );
  });
}

interface BarcodeResult { rawValue: string }
interface BarcodeDetectorInstance { detect(source: HTMLVideoElement): Promise<BarcodeResult[]> }
type BarcodeDetectorConstructor = new (options: { formats: string[] }) => BarcodeDetectorInstance;

function ScannerScreen({ isClockOut, onBack, onFinished }: { isClockOut: boolean; onBack: () => void; onFinished: () => Promise<void> }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const frameRef = useRef<number | null>(null);
  const isReadingRef = useRef(false);
  const [token, setToken] = useState('');
  const [cameraError, setCameraError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<AttendanceRecord | null>(null);
  const [submitError, setSubmitError] = useState('');

  const stopCamera = useCallback(() => {
    if (frameRef.current !== null) cancelAnimationFrame(frameRef.current);
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
  }, []);

  const submitToken = useCallback(async (qrToken: string) => {
    const cleaned = qrToken.trim();
    if (!cleaned || isReadingRef.current) return;
    isReadingRef.current = true;
    setIsSubmitting(true);
    setSubmitError('');
    try {
      const gpsLocation = await getBrowserPosition();
      const endpoint = isClockOut ? '/attendance/attendance/clock_out/' : '/attendance/attendance/clock_in/';
      const { data } = await api.post<AttendanceRecord>(endpoint, { gps_location: gpsLocation, qr_token: cleaned });
      stopCamera();
      setResult(data);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : apiErrorMessage(error, 'Unable to record attendance.'));
      isReadingRef.current = false;
    } finally {
      setIsSubmitting(false);
    }
  }, [isClockOut, stopCamera]);

  useEffect(() => {
    let isMounted = true;

    const start = async () => {
      if (!navigator.mediaDevices?.getUserMedia) {
        setCameraError('Camera scanning is not supported here. Paste the QR token below.');
        return;
      }

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' } }, audio: false });
        if (!isMounted) {
          stream.getTracks().forEach((track) => track.stop());
          return;
        }
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          await videoRef.current.play();
        }

        const Detector = (window as unknown as { BarcodeDetector?: BarcodeDetectorConstructor }).BarcodeDetector;
        if (!Detector) {
          setCameraError('Automatic QR reading is not available in this browser. You can paste the QR token below.');
          return;
        }

        const detector = new Detector({ formats: ['qr_code'] });
        const readFrame = async () => {
          if (!isMounted || !videoRef.current || isReadingRef.current) return;
          try {
            const codes = await detector.detect(videoRef.current);
            if (codes[0]?.rawValue) {
              setToken(codes[0].rawValue);
              await submitToken(codes[0].rawValue);
              if (isMounted && !isReadingRef.current) frameRef.current = requestAnimationFrame(readFrame);
              return;
            }
          } catch {
            // The video can be between frames while the camera is starting.
          }
          frameRef.current = requestAnimationFrame(readFrame);
        };
        frameRef.current = requestAnimationFrame(readFrame);
      } catch {
        setCameraError('Camera access was blocked. Allow it in your browser or paste the QR token below.');
      }
    };

    void start();
    return () => {
      isMounted = false;
      stopCamera();
    };
  }, [stopCamera, submitToken]);

  if (result) {
    return (
      <div className="flex min-h-full flex-col bg-white">
        <div className="flex flex-1 flex-col items-center justify-center px-7 py-12 text-center">
          <div className="grid h-28 w-28 place-items-center rounded-full bg-emerald-50 text-emerald-500">
            <Check size={58} strokeWidth={2.4} />
          </div>
          <h1 className="mt-8 text-3xl font-black tracking-[-0.04em] text-slate-950">{isClockOut ? 'Clocked Out' : 'Checked In'} Successfully!</h1>
          <p className="mt-3 text-sm leading-6 text-slate-500">Your attendance has been recorded securely.</p>
          <div className="mt-8 w-full max-w-sm rounded-2xl bg-slate-50 p-5">
            <div className="flex justify-between border-b border-slate-200 pb-3 text-sm"><span className="text-slate-400">Time</span><strong>{friendlyTime(isClockOut ? result.clock_out : result.clock_in)}</strong></div>
            <div className="flex justify-between pt-3 text-sm"><span className="text-slate-400">Status</span><StatusPill status={result.status} /></div>
          </div>
        </div>
        <div className="p-6">
          <button type="button" onClick={() => void onFinished()} className="h-14 w-full rounded-xl bg-slate-950 font-extrabold text-white">Back to Home</button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-full bg-slate-950 text-white">
      <header className="flex h-18 items-center px-5">
        <button type="button" onClick={onBack} aria-label="Close scanner" className="grid h-10 w-10 place-items-center rounded-xl hover:bg-white/10"><ArrowLeft size={21} /></button>
        <h1 className="absolute left-1/2 -translate-x-1/2 font-extrabold">{isClockOut ? 'Clock Out' : 'Check In'}</h1>
      </header>

      <section className="px-6 pb-8 pt-4 text-center">
        <h2 className="text-2xl font-black tracking-[-0.035em]">Scan workplace QR</h2>
        <p className="mt-2 text-sm leading-6 text-slate-400">Keep the code inside the frame. Your location will be requested after it is read.</p>

        <div className="relative mx-auto mt-7 aspect-square max-w-sm overflow-hidden rounded-[28px] bg-slate-900 ring-1 ring-white/10">
          <video ref={videoRef} muted playsInline className="h-full w-full object-cover" />
          <div className="pointer-events-none absolute inset-[14%] rounded-2xl border-2 border-emerald-400 shadow-[0_0_0_999px_rgba(2,6,23,0.46)]">
            <span className="absolute -left-0.5 -top-0.5 h-8 w-8 rounded-tl-2xl border-l-4 border-t-4 border-amber-400" />
            <span className="absolute -right-0.5 -top-0.5 h-8 w-8 rounded-tr-2xl border-r-4 border-t-4 border-amber-400" />
            <span className="absolute -bottom-0.5 -left-0.5 h-8 w-8 rounded-bl-2xl border-b-4 border-l-4 border-amber-400" />
            <span className="absolute -bottom-0.5 -right-0.5 h-8 w-8 rounded-br-2xl border-b-4 border-r-4 border-amber-400" />
          </div>
          {isSubmitting && <div className="absolute inset-0 grid place-items-center bg-slate-950/65"><LoaderCircle className="animate-spin text-emerald-400" size={36} /></div>}
        </div>

        {cameraError && <p className="mx-auto mt-4 max-w-sm text-xs leading-5 text-amber-300">{cameraError}</p>}
        {submitError && <p role="alert" className="mx-auto mt-4 max-w-sm rounded-xl bg-red-500/10 px-4 py-3 text-sm text-red-300">{submitError}</p>}

        <div className="mx-auto mt-6 max-w-sm text-left">
          <label className="text-xs font-bold uppercase tracking-[0.12em] text-slate-400">Manual QR token</label>
          <textarea value={token} onChange={(event) => setToken(event.target.value)} rows={2} placeholder="Paste the QR token if your browser cannot scan it" className="mt-2 w-full resize-none rounded-xl border border-white/10 bg-white/[0.06] p-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-emerald-400" />
          <button type="button" onClick={() => void submitToken(token)} disabled={!token.trim() || isSubmitting} className="mt-3 flex h-13 w-full items-center justify-center rounded-xl bg-emerald-500 font-extrabold text-white disabled:opacity-40">
            {isSubmitting ? <LoaderCircle className="animate-spin" size={20} /> : 'Use this code'}
          </button>
        </div>
      </section>
    </div>
  );
}

function ProfileScreen({ name, role, downloadUrl, versionName, onLogout, notify }: { name: string; role: string; downloadUrl: string | null; versionName?: string; onLogout: () => void; notify: (message: string) => void }) {
  const menu = [
    { icon: UserRound, label: 'Personal Information', message: 'Your profile is managed by HR.' },
    { icon: Bell, label: 'Notifications', message: 'You are all caught up.' },
    { icon: HelpCircle, label: 'Support & FAQ', message: 'Contact HR support for account assistance.' },
  ];

  return (
    <section className="px-6 pb-9 pt-7">
      <h1 className="text-center text-lg font-black text-slate-950">My Profile</h1>
      <div className="mt-9 text-center">
        <div className="mx-auto grid h-25 w-25 place-items-center rounded-full bg-slate-950 text-4xl font-black text-white shadow-xl shadow-slate-950/15">
          {name.charAt(0).toUpperCase() || 'E'}
        </div>
        <h2 className="mt-5 text-2xl font-black tracking-[-0.035em] text-slate-950">{name}</h2>
        <p className="mt-1 text-sm text-slate-400">{titleCase(role)}</p>
      </div>

      <div className="mt-10 space-y-3">
        {menu.map(({ icon: Icon, label, message }) => (
          <button key={label} type="button" onClick={() => notify(message)} className="flex min-h-15 w-full items-center rounded-xl border border-slate-200 bg-slate-50 px-4 text-left transition hover:border-slate-300 hover:bg-white">
            <Icon size={20} className="text-slate-800" />
            <span className="ml-3 flex-1 text-sm font-bold text-slate-800">{label}</span>
            <ChevronRight size={18} className="text-slate-400" />
          </button>
        ))}
      </div>

      {downloadUrl ? (
        <a href={downloadUrl} download className="mt-7 flex min-h-15 w-full items-center rounded-xl border-2 border-emerald-500 px-4 text-emerald-600 transition hover:bg-emerald-50">
          <span className="grid h-9 w-9 place-items-center rounded-lg bg-emerald-50"><Smartphone size={19} /></span>
          <span className="ml-3 flex-1"><strong className="block text-sm">Download Android app</strong><span className="text-xs text-emerald-600/70">{versionName ? `Version ${versionName}` : 'Latest APK'}</span></span>
          <Download size={19} />
        </a>
      ) : (
        <div className="mt-7 flex min-h-15 items-center rounded-xl border border-slate-200 bg-slate-50 px-4 text-slate-400">
          <Smartphone size={20} /><span className="ml-3 text-sm font-semibold">Android download coming soon</span>
        </div>
      )}

      <button type="button" onClick={onLogout} className="mt-8 flex h-14 w-full items-center justify-center gap-2 rounded-xl bg-red-500 font-extrabold text-white transition hover:bg-red-600">
        <LogOut size={19} /> Log Out
      </button>
    </section>
  );
}

function BottomNavigation({ active, onChange }: { active: AppTab; onChange: (tab: AppTab) => void }) {
  const items = [
    { value: 'home' as const, icon: Home, label: 'Home' },
    { value: 'history' as const, icon: History, label: 'History' },
    { value: 'profile' as const, icon: UserRound, label: 'Profile' },
  ];

  return (
    <nav className="sticky bottom-0 z-30 grid h-20 grid-cols-3 border-t border-slate-100 bg-white/95 px-4 pb-[env(safe-area-inset-bottom)] shadow-[0_-12px_30px_rgba(15,23,42,0.05)] backdrop-blur">
      {items.map(({ value, icon: Icon, label }) => {
        const isActive = active === value;
        return (
          <button key={value} type="button" onClick={() => onChange(value)} aria-current={isActive ? 'page' : undefined} className={`flex flex-col items-center justify-center gap-1 text-[11px] font-bold transition ${isActive ? 'text-emerald-500' : 'text-slate-400 hover:text-slate-600'}`}>
            <Icon size={22} fill={isActive ? 'currentColor' : 'none'} strokeWidth={isActive ? 2.4 : 2} />
            {label}
          </button>
        );
      })}
    </nav>
  );
}

export function NuruMobileApp() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((state: RootState) => state.auth.user);
  const [activeTab, setActiveTab] = useState<AppTab>('home');
  const [view, setView] = useState<AppView>('main');
  const [today, setToday] = useState<TodayStatus | null>(null);
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [balances, setBalances] = useState<LeaveBalance[]>([]);
  const [requests, setRequests] = useState<LeaveRequest[]>([]);
  const [isBooting, setIsBooting] = useState(true);
  const [isRefreshingToday, setIsRefreshingToday] = useState(true);
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);
  const [isLeaveLoading, setIsLeaveLoading] = useState(true);
  const [toast, setToast] = useState<{ message: string; tone: 'success' | 'error' } | null>(null);
  const { version, downloadUrl } = useLatestAppVersion();

  const notify = useCallback((message: string, tone: 'success' | 'error' = 'success') => {
    setToast({ message, tone });
  }, []);

  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(null), 3300);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const loadToday = useCallback(async () => {
    setIsRefreshingToday(true);
    try {
      const { data } = await api.get<TodayStatus>('/attendance/attendance/today/');
      setToday(data);
    } catch (error) {
      notify(apiErrorMessage(error, 'Unable to load today’s attendance.'), 'error');
    } finally {
      setIsRefreshingToday(false);
    }
  }, [notify]);

  const loadHistory = useCallback(async () => {
    setIsHistoryLoading(true);
    try {
      const { data } = await api.get<AttendanceRecord[] | { results?: AttendanceRecord[] }>('/attendance/attendance/');
      setRecords(listFrom(data));
    } catch (error) {
      notify(apiErrorMessage(error, 'Unable to load attendance history.'), 'error');
    } finally {
      setIsHistoryLoading(false);
    }
  }, [notify]);

  const loadLeave = useCallback(async () => {
    setIsLeaveLoading(true);
    try {
      const [balanceResponse, requestResponse] = await Promise.all([
        api.get<LeaveBalance[] | { results?: LeaveBalance[] }>('/leave/leave-balances/'),
        api.get<LeaveRequest[] | { results?: LeaveRequest[] }>('/leave/leave-requests/'),
      ]);
      setBalances(listFrom(balanceResponse.data));
      setRequests(listFrom(requestResponse.data));
    } catch (error) {
      notify(apiErrorMessage(error, 'Unable to load leave details.'), 'error');
    } finally {
      setIsLeaveLoading(false);
    }
  }, [notify]);

  useEffect(() => {
    const startedAt = Date.now();
    Promise.allSettled([loadToday(), loadHistory(), loadLeave()]).finally(() => {
      const remaining = Math.max(0, 650 - (Date.now() - startedAt));
      window.setTimeout(() => setIsBooting(false), remaining);
    });
  }, [loadHistory, loadLeave, loadToday]);

  const handleLogout = async () => {
    const refresh = localStorage.getItem('nuru_refresh_token');
    try {
      if (refresh) await api.post('/accounts/logout/', { refresh });
    } catch {
      // Local logout still completes if the server session is already gone.
    } finally {
      dispatch(logout());
      navigate('/login', { replace: true });
    }
  };

  const finishScan = async () => {
    await Promise.all([loadToday(), loadHistory()]);
    setView('main');
    setActiveTab('home');
  };

  const employeeName = user?.full_name?.trim() || user?.username || 'Employee';
  const employeeRole = user?.role || 'employee';

  if (isBooting) {
    return <div className="min-h-dvh bg-slate-100 sm:py-4"><div className="mx-auto max-w-[640px] overflow-hidden bg-white sm:rounded-[30px] sm:shadow-2xl"><SplashScreen /></div></div>;
  }

  const mainContent = activeTab === 'history'
    ? <HistoryScreen records={records} isLoading={isHistoryLoading} />
    : activeTab === 'profile'
      ? <ProfileScreen name={employeeName} role={employeeRole} downloadUrl={downloadUrl} versionName={version?.version_name} onLogout={() => void handleLogout()} notify={notify} />
      : <HomeScreen name={employeeName} role={employeeRole} today={today} isLoading={isRefreshingToday} onScan={() => setView('scanner')} onLeave={() => setView('leave')} onLogout={() => void handleLogout()} />;

  return (
    <main className="min-h-dvh bg-slate-100 sm:py-4">
      <div className="relative mx-auto flex min-h-dvh max-w-[640px] flex-col overflow-hidden bg-white sm:min-h-[calc(100dvh-2rem)] sm:rounded-[30px] sm:shadow-2xl">
        <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain">
          {view === 'leave' ? (
            <LeaveScreen balances={balances} requests={requests} isLoading={isLeaveLoading} onBack={() => setView('main')} onRefresh={loadLeave} notify={notify} />
          ) : view === 'scanner' ? (
            <ScannerScreen isClockOut={today?.is_checked_in === true} onBack={() => setView('main')} onFinished={finishScan} />
          ) : mainContent}
        </div>

        {view === 'main' && <BottomNavigation active={activeTab} onChange={setActiveTab} />}

        {toast && (
          <div role="status" className={`absolute bottom-24 left-1/2 z-50 flex w-[calc(100%-3rem)] -translate-x-1/2 items-center gap-3 rounded-xl px-4 py-3 text-sm font-bold text-white shadow-xl ${toast.tone === 'error' ? 'bg-red-500' : 'bg-slate-950'}`}>
            <span className={`grid h-6 w-6 shrink-0 place-items-center rounded-full ${toast.tone === 'error' ? 'bg-white/15' : 'bg-emerald-500'}`}>
              {toast.tone === 'error' ? <X size={14} /> : <Check size={14} />}
            </span>
            {toast.message}
          </div>
        )}
      </div>
    </main>
  );
}

export default NuruMobileApp;
