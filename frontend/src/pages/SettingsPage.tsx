import { useSelector } from 'react-redux';
import { useState, type FormEvent } from 'react';
import type { RootState } from '../store';
import { Button } from '../components/ui/Button';
import { api } from '../lib/api';

export function SettingsPage() {
  const { user } = useSelector((state: RootState) => state.auth);
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [feedback, setFeedback] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const handlePasswordChange = async (event: FormEvent) => {
    event.preventDefault();
    setFeedback('');
    if (newPassword !== confirmPassword) {
      setFeedback('New passwords do not match.');
      return;
    }
    setIsSaving(true);
    try {
      await api.post('/accounts/change-password/', {
        current_password: currentPassword,
        new_password: newPassword,
      });
      setFeedback('Password changed successfully.');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setShowPasswordForm(false);
    } catch (error: any) {
      const data = error.response?.data;
      setFeedback(data?.current_password?.[0] || data?.new_password?.[0] || data?.detail || 'Unable to change password.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-500 p-6">
      <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center gap-6">
        <div className="h-24 w-24 rounded-full bg-slate-200 overflow-hidden border-4 border-white shadow-lg">
          <img 
            src={`https://ui-avatars.com/api/?name=${user?.username}&background=random&size=200`} 
            alt={user?.username} 
            className="h-full w-full object-cover"
          />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-slate-900">{user?.username}</h1>
          <p className="text-sm font-medium text-slate-500 uppercase tracking-widest mt-1">
            {user?.role?.replace('_', ' ')}
          </p>
          <p className="text-slate-600 mt-2">Manage your account settings and preferences here.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-100">
          <h2 className="text-lg font-bold text-slate-800">Profile Settings</h2>
        </div>
        <div className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
            <input 
              type="email" 
              disabled 
              value={user?.email || ''} 
              className="w-full md:w-1/2 p-2 border border-slate-200 rounded-md bg-slate-50 text-slate-500 cursor-not-allowed" 
            />
            <p className="text-xs text-slate-400 mt-1">Please contact HR to change your registered email.</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Username</label>
            <input 
              type="text" 
              disabled 
              value={user?.username || ''} 
              className="w-full md:w-1/2 p-2 border border-slate-200 rounded-md bg-slate-50 text-slate-500 cursor-not-allowed" 
            />
          </div>
          <div className="pt-4 border-t border-slate-100">
            <Button
              type="button"
              variant="outline"
              onClick={() => setShowPasswordForm((visible) => !visible)}
              className="text-rose-600 border-rose-200 hover:bg-rose-50 hover:border-rose-300"
            >
              Change Password
            </Button>
            {showPasswordForm && (
              <form onSubmit={handlePasswordChange} className="mt-4 max-w-md space-y-3">
                <input
                  type="password"
                  required
                  autoComplete="current-password"
                  value={currentPassword}
                  onChange={(event) => setCurrentPassword(event.target.value)}
                  placeholder="Current password"
                  className="w-full rounded-md border border-slate-300 p-2"
                />
                <input
                  type="password"
                  required
                  autoComplete="new-password"
                  value={newPassword}
                  onChange={(event) => setNewPassword(event.target.value)}
                  placeholder="New password"
                  className="w-full rounded-md border border-slate-300 p-2"
                />
                <input
                  type="password"
                  required
                  autoComplete="new-password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  placeholder="Confirm new password"
                  className="w-full rounded-md border border-slate-300 p-2"
                />
                <Button type="submit" disabled={isSaving}>
                  {isSaving ? 'Saving…' : 'Save password'}
                </Button>
              </form>
            )}
            {feedback && <p className="mt-3 text-sm text-slate-600">{feedback}</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
