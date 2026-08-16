import { ArrowLeft, Loader2, RefreshCw, ShieldCheck } from 'lucide-react';
import { QRCodeSVG } from 'qrcode.react';
import { useNavigate } from 'react-router-dom';
import { useQRKiosk } from '../hooks/useQRKiosk';

export function KioskMode() {
  const navigate = useNavigate();
  const { token, isLoading, timeLeft, error, refetch } = useQRKiosk();

  // Calculate a color based on time left to create urgency
  const getTimerColor = () => {
    if (timeLeft > 20) return 'text-emerald-600';
    if (timeLeft > 10) return 'text-amber-500';
    return 'text-rose-600';
  };

  return (
    <div className="fixed inset-0 bg-slate-900 flex flex-col items-center justify-center z-50 animate-in fade-in duration-300">
      
      {/* Top Bar */}
      <div className="absolute top-0 left-0 right-0 p-6 flex justify-between items-center">
        <button 
          onClick={() => navigate(-1)}
          className="flex items-center space-x-2 text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span className="font-medium">Back to Dashboard</span>
        </button>
        <div className="flex items-center space-x-2 text-slate-400">
          <ShieldCheck className="w-5 h-5 text-emerald-500" />
          <span className="font-medium text-sm">Secure Kiosk Mode Active</span>
        </div>
      </div>

      {/* Main Content */}
      <div className="bg-white rounded-3xl shadow-2xl p-12 max-w-lg w-full flex flex-col items-center text-center">
        
        <div className="mb-8 space-y-2">
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Clock In</h1>
          <p className="text-slate-500">Scan this QR code using your NuruX mobile app to register your attendance.</p>
        </div>

        {/* QR Code Area */}
        <div className="relative bg-slate-50 p-8 rounded-2xl border-2 border-dashed border-slate-200 mb-8 w-full flex justify-center min-h-[300px] items-center">
          {isLoading && !token ? (
            <div className="flex flex-col items-center space-y-4 text-slate-400">
              <Loader2 className="w-12 h-12 animate-spin text-indigo-600" />
              <p className="font-medium">Generating secure token...</p>
            </div>
          ) : error ? (
            <div className="flex flex-col items-center space-y-4 text-rose-500">
              <p className="font-medium">{error}</p>
              <button 
                onClick={refetch}
                className="flex items-center space-x-2 bg-rose-100 px-4 py-2 rounded-lg hover:bg-rose-200 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Retry</span>
              </button>
            </div>
          ) : token ? (
            <div className="flex flex-col items-center animate-in zoom-in duration-500">
              <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-100">
                <QRCodeSVG 
                  value={token} 
                  size={240} 
                  level="H" 
                  includeMargin={false}
                  bgColor="#ffffff"
                  fgColor="#0f172a"
                />
              </div>
            </div>
          ) : null}
        </div>

        {/* Timer */}
        <div className="flex items-center justify-center space-x-3 w-full">
          <div className="h-1 flex-1 bg-slate-100 rounded-full overflow-hidden">
            <div 
              className={`h-full transition-all duration-1000 ease-linear ${timeLeft > 20 ? 'bg-emerald-500' : timeLeft > 10 ? 'bg-amber-400' : 'bg-rose-500'}`}
              style={{ width: `${(timeLeft / 60) * 100}%` }}
            />
          </div>
          <div className={`font-mono text-xl font-bold w-12 text-right ${getTimerColor()}`}>
            {timeLeft}s
          </div>
        </div>
        <p className="text-xs text-slate-400 mt-4 font-medium uppercase tracking-wider">
          Code refreshes automatically every minute
        </p>
      </div>

    </div>
  );
}
