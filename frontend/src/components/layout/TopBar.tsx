import { Search, Bell, ChevronDown } from 'lucide-react';

export function TopBar() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-slate-400" />
          </div>
          <input
            type="text"
            className="block w-full pl-10 pr-3 py-2 border border-slate-200 rounded-md leading-5 bg-slate-50 placeholder-slate-400 focus:outline-none focus:bg-white focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
            placeholder="Search..."
          />
        </div>
      </div>

      {/* Right section */}
      <div className="ml-4 flex items-center space-x-6">
        <button className="text-slate-400 hover:text-slate-500 transition-colors relative">
          <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
          <Bell className="h-5 w-5" />
        </button>

        <div className="flex items-center space-x-3 cursor-pointer group">
          <div className="h-8 w-8 rounded-full bg-slate-200 overflow-hidden border border-slate-300">
            <img 
              src="https://i.pravatar.cc/150?u=evan" 
              alt="Evan" 
              className="h-full w-full object-cover"
            />
          </div>
          <div className="flex items-center text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">
            <span>Evan</span>
            <ChevronDown className="ml-1 h-4 w-4 text-slate-400" />
          </div>
        </div>
      </div>
    </header>
  );
}
