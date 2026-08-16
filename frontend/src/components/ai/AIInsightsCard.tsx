import { useEffect, useState } from 'react';
import { Sparkles, TrendingUp, AlertCircle, Loader2 } from 'lucide-react';
import { api } from '../../lib/api';

export function AIInsightsCard() {
  const [insight, setInsight] = useState<string>('');
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const fetchInsight = async () => {
      try {
        const response = await api.get('/ai/insights/');
        setInsight(response.data.summary);
      } catch {
        setInsight("Unable to generate AI insights at the moment.");
      } finally {
        setLoading(false);
      }
    };
    fetchInsight();
  }, []);

  return (
    <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg p-6 text-white relative overflow-hidden mb-6">
      {/* Decorative background elements */}
      <div className="absolute -top-10 -right-10 w-40 h-40 bg-white opacity-10 rounded-full blur-2xl"></div>
      <div className="absolute -bottom-10 -left-10 w-40 h-40 bg-white opacity-10 rounded-full blur-2xl"></div>
      
      <div className="relative z-10">
        <div className="flex items-center space-x-2 mb-4">
          <div className="p-2 bg-white/20 rounded-lg">
            <Sparkles className="h-5 w-5 text-yellow-300" />
          </div>
          <h2 className="text-lg font-semibold tracking-wide">NuruX AI Daily Insights</h2>
        </div>
        
        {loading ? (
          <div className="flex items-center space-x-3 text-indigo-100 py-2">
            <Loader2 className="h-5 w-5 animate-spin" />
            <p className="text-sm">Analyzing company data...</p>
          </div>
        ) : (
          <div className="bg-white/10 backdrop-blur-md rounded-lg p-4 border border-white/20">
            <p className="text-sm md:text-base leading-relaxed text-indigo-50">
              {insight}
            </p>
          </div>
        )}
        
        <div className="mt-4 flex space-x-4">
          <div className="flex items-center space-x-1 text-xs text-indigo-200">
            <TrendingUp className="h-3 w-3" />
            <span>Real-time analysis</span>
          </div>
          <div className="flex items-center space-x-1 text-xs text-indigo-200">
            <AlertCircle className="h-3 w-3" />
            <span>Updated hourly</span>
          </div>
        </div>
      </div>
    </div>
  );
}
