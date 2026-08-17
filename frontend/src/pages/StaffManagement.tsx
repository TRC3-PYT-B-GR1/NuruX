import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { 
  Users, UserPlus, Building, ChevronDown, ChevronUp, 
  MapPin, CheckCircle2, XCircle, Search, Briefcase, Loader2
} from 'lucide-react';
import type { RootState } from '../store';
import { useEmployees } from '../hooks/useEmployees';
import { useDepartments } from '../hooks/useDepartments';
import { useRoles } from '../hooks/useRoles';
import { cn } from '../lib/utils';

export function StaffManagement() {
  const { user } = useSelector((state: RootState) => state.auth);
  const { employees, metrics, isLoading, addEmployee } = useEmployees();
  const { departments, addDepartment } = useDepartments();
  const { roles, addRole } = useRoles();

  const [showMetrics, setShowMetrics] = useState(false);
  const [showAddEmployee, setShowAddEmployee] = useState(false);
  const [showCreateDept, setShowCreateDept] = useState(false);
  const [showCreateRole, setShowCreateRole] = useState(false);
  const [isGettingLocation, setIsGettingLocation] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('All');

  // Add Employee Form State
  const [empForm, setEmpForm] = useState({
    first_name: '', last_name: '', email: '', password: '', phone: '', address: '', date_of_birth: '',
    gender: '', nationality: 'Nigerian', identification_number: '', employment_type: 'full_time', salary_grade: '',
    emergency_contact_name: '', emergency_contact_relationship: '', emergency_contact_phone: '', emergency_contact_address: '',
    next_of_kin_name: '', next_of_kin_relationship: '', next_of_kin_phone: '', next_of_kin_address: '',
    department: '', role: '', manager: '', rbac_role: 'employee'
  });

  // Create Department Form State
  const [deptForm, setDeptForm] = useState({
    name: '', description: '', latitude: '', longitude: '', geofence_radius_meters: '200'
  });

  // Create Role Form State
  const [roleForm, setRoleForm] = useState({
    title: '', department: ''
  });

  const canCreateDept = user?.role === 'super_admin' || user?.role === 'hr_officer';

  const handleAddEmployee = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await addEmployee(empForm);
      setShowAddEmployee(false);
      setEmpForm({ first_name: '', last_name: '', email: '', password: '', phone: '', address: '', date_of_birth: '', gender: '', nationality: 'Nigerian', identification_number: '', employment_type: 'full_time', salary_grade: '', emergency_contact_name: '', emergency_contact_relationship: '', emergency_contact_phone: '', emergency_contact_address: '', next_of_kin_name: '', next_of_kin_relationship: '', next_of_kin_phone: '', next_of_kin_address: '', department: '', role: '', manager: '', rbac_role: 'employee' });
    } catch (error: any) {
      const msg = error.response?.data?.detail || error.response?.data?.username?.[0] || error.message || 'Failed to add employee';
      alert(`Error: ${msg}`);
    }
  };

  const handleCreateDepartment = async (e: React.FormEvent) => {
    e.preventDefault();
    await addDepartment(deptForm);
    setShowCreateDept(false);
    setDeptForm({ name: '', description: '', latitude: '', longitude: '', geofence_radius_meters: '200' });
  };

  const handleCreateRole = async (e: React.FormEvent) => {
    e.preventDefault();
    await addRole({ title: roleForm.title, department: Number(roleForm.department) });
    setShowCreateRole(false);
    setRoleForm({ title: '', department: '' });
  };

  const handleGetLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser");
      return;
    }
    setIsGettingLocation(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setDeptForm(prev => ({
          ...prev,
          latitude: position.coords.latitude.toFixed(6),
          longitude: position.coords.longitude.toFixed(6)
        }));
        setIsGettingLocation(false);
      },
      (error) => {
        console.error("Error getting location:", error);
        alert("Failed to get location. Please check your browser permissions.");
        setIsGettingLocation(false);
      },
      { enableHighAccuracy: true }
    );
  };

  const filteredEmployees = employees.filter(emp => {
    const fullName = `${emp.first_name || ''} ${emp.last_name || ''}`.toLowerCase();
    const deptName = (emp.department_details?.name || '').toLowerCase();
    const search = (searchTerm || '').toLowerCase();
    
    const matchesSearch = fullName.includes(search) || deptName.includes(search);
    const matchesDept = selectedDepartment === 'All' || String(emp.department_details?.id) === selectedDepartment;
    
    return matchesSearch && matchesDept;
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Staff Management</h1>
          <p className="text-slate-600 mt-1">Manage your workforce, departments, and monitor key HR metrics.</p>
        </div>
        <div className="flex space-x-3">
          {canCreateDept && (
            <>
              <button
                onClick={() => setShowCreateDept(true)}
                className="flex items-center px-4 py-2 bg-slate-800 text-white rounded-lg hover:bg-slate-700 transition-colors border border-slate-700 shadow-lg"
              >
                <Building className="w-5 h-5 mr-2" />
                Create Department
              </button>
              <button
                onClick={() => setShowCreateRole(true)}
                className="flex items-center px-4 py-2 bg-slate-800 text-white rounded-lg hover:bg-slate-700 transition-colors border border-slate-700 shadow-lg"
              >
                <Briefcase className="w-5 h-5 mr-2" />
                Create Role
              </button>
            </>
          )}
          <button
            onClick={() => setShowAddEmployee(true)}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20"
          >
            <UserPlus className="w-5 h-5 mr-2" />
            Add Employee
          </button>
        </div>
      </div>

      {/* Metrics Accordion */}
      <div className="bg-slate-900/50 backdrop-blur-xl rounded-2xl border border-slate-800 shadow-xl overflow-hidden">
        <button 
          onClick={() => setShowMetrics(!showMetrics)}
          className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-800/50 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <Users className="w-5 h-5 text-blue-400" />
            </div>
            <h2 className="text-lg font-semibold text-white">Workforce Analytics</h2>
          </div>
          {showMetrics ? <ChevronUp className="text-slate-400" /> : <ChevronDown className="text-slate-400" />}
        </button>

        {showMetrics && metrics && (
          <div className="px-6 pb-6 pt-2 border-t border-slate-800 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
              <p className="text-sm text-slate-400 mb-1">Total Headcount</p>
              <p className="text-3xl font-bold text-white">{metrics.total_headcount}</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
              <p className="text-sm text-slate-400 mb-1">Total Departments</p>
              <p className="text-3xl font-bold text-white">{metrics.total_departments}</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
              <p className="text-sm text-slate-400 mb-1">Today's Clock Ins</p>
              <p className="text-3xl font-bold text-emerald-400">{metrics.total_clock_ins}</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
              <p className="text-sm text-slate-400 mb-1">Today's Clock Outs</p>
              <p className="text-3xl font-bold text-rose-400">{metrics.total_clock_outs}</p>
            </div>

            {/* Department Breakdowns */}
            <div className="col-span-full grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
              <div className="bg-slate-800/30 p-4 rounded-xl">
                <h3 className="text-sm font-medium text-slate-300 mb-3">Headcount by Department</h3>
                <div className="space-y-2">
                  {metrics.headcount_by_department.map(d => (
                    <div key={d.name} className="flex justify-between items-center text-sm">
                      <span className="text-slate-400">{d.name}</span>
                      <span className="text-white font-medium">{d.count}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-slate-800/30 p-4 rounded-xl">
                <h3 className="text-sm font-medium text-slate-300 mb-3">Clock Ins by Department (Today)</h3>
                <div className="space-y-2">
                  {metrics.clock_ins_by_department.map(d => (
                    <div key={d.name} className="flex justify-between items-center text-sm">
                      <span className="text-slate-400">{d.name}</span>
                      <span className="text-emerald-400 font-medium">{d.count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Directory Table */}
      <div className="bg-slate-900/50 backdrop-blur-xl rounded-2xl border border-slate-800 shadow-xl overflow-hidden flex flex-col h-[600px]">
        <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900">
          <h2 className="text-xl font-semibold text-white">Staff Directory</h2>
          <div className="flex items-center space-x-4">
            <select
              value={selectedDepartment}
              onChange={(e) => setSelectedDepartment(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg text-sm text-white px-3 py-2 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all cursor-pointer"
            >
              <option value="All">All Departments</option>
              {departments.map(d => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
            <div className="relative w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search employees..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
              />
            </div>
          </div>
        </div>
        
        <div className="flex-1 overflow-auto">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-900/80 sticky top-0 z-10 backdrop-blur-md">
              <tr>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Employee</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Department</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Role</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">Date Joined</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {isLoading ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-400">Loading directory...</td>
                </tr>
              ) : filteredEmployees.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-400">No employees found.</td>
                </tr>
              ) : (
                filteredEmployees.map(emp => (
                  <tr key={emp.id} className="hover:bg-slate-800/30 transition-colors group">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold shadow-lg">
                          {(emp.first_name?.[0] || '')}{(emp.last_name?.[0] || '')}
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-white group-hover:text-blue-400 transition-colors">
                            {emp.first_name} {emp.last_name}
                          </div>
                          <div className="text-sm text-slate-400">{emp.email}</div>
                          {emp.phone && <div className="text-xs text-slate-500">{emp.phone}</div>}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                      {emp.department_details?.name || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                      <div>{emp.role_details?.title || '-'}</div>
                      <div className="text-xs text-slate-500">{emp.employment_type?.replace('_', ' ') || 'Full time'} {emp.salary_grade ? `· ${emp.salary_grade}` : ''}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400">
                      {emp.date_joined ? new Date(emp.date_joined).toLocaleDateString() : '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <span className={cn(
                        "inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border",
                        emp.status === 'active' ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
                        emp.status === 'suspended' ? "bg-amber-500/10 text-amber-400 border-amber-500/20" :
                        "bg-rose-500/10 text-rose-400 border-rose-500/20"
                      )}>
                        {emp.status === 'active' && <CheckCircle2 className="w-3 h-3 mr-1" />}
                        {emp.status === 'exited' && <XCircle className="w-3 h-3 mr-1" />}
                        {emp.status ? emp.status.charAt(0).toUpperCase() + emp.status.slice(1) : ''}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Employee Modal / Slide-over */}
      {showAddEmployee && (
        <div className="fixed inset-0 z-50 flex items-center justify-end bg-black/60 backdrop-blur-sm">
          <div className="w-full max-w-md h-full bg-slate-900 border-l border-slate-800 shadow-2xl p-6 overflow-y-auto animate-in slide-in-from-right duration-300">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white">Add New Employee</h2>
              <button onClick={() => setShowAddEmployee(false)} className="text-slate-400 hover:text-white"><XCircle className="w-6 h-6" /></button>
            </div>
            
            <form onSubmit={handleAddEmployee} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">First Name</label>
                  <input required type="text" value={empForm.first_name} onChange={e => setEmpForm({...empForm, first_name: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Last Name</label>
                  <input required type="text" value={empForm.last_name} onChange={e => setEmpForm({...empForm, last_name: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <input placeholder="Gender" value={empForm.gender} onChange={e => setEmpForm({...empForm, gender: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                <input placeholder="Nationality" value={empForm.nationality} onChange={e => setEmpForm({...empForm, nationality: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                <input placeholder="ID / NIN" value={empForm.identification_number} onChange={e => setEmpForm({...empForm, identification_number: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Phone</label>
                  <input type="tel" value={empForm.phone} onChange={e => setEmpForm({...empForm, phone: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Date of Birth</label>
                  <input type="date" value={empForm.date_of_birth} onChange={e => setEmpForm({...empForm, date_of_birth: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Employment Type</label>
                  <select value={empForm.employment_type} onChange={e => setEmpForm({...empForm, employment_type: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white">
                    <option value="full_time">Full time</option><option value="part_time">Part time</option><option value="contract">Contract</option><option value="temporary">Temporary</option><option value="intern">Intern</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Salary Grade</label>
                  <input type="text" placeholder="e.g. GL 08" value={empForm.salary_grade} onChange={e => setEmpForm({...empForm, salary_grade: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Address</label>
                <textarea rows={2} value={empForm.address} onChange={e => setEmpForm({...empForm, address: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white resize-none" />
              </div>

              <div className="border-t border-slate-800 pt-4">
                <h3 className="mb-3 text-sm font-semibold text-slate-200">Emergency contact</h3>
                <div className="grid grid-cols-2 gap-4">
                  <input placeholder="Full name" value={empForm.emergency_contact_name} onChange={e => setEmpForm({...empForm, emergency_contact_name: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                  <input placeholder="Relationship" value={empForm.emergency_contact_relationship} onChange={e => setEmpForm({...empForm, emergency_contact_relationship: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                  <input placeholder="Phone" value={empForm.emergency_contact_phone} onChange={e => setEmpForm({...empForm, emergency_contact_phone: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                  <input placeholder="Address" value={empForm.emergency_contact_address} onChange={e => setEmpForm({...empForm, emergency_contact_address: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
              </div>

              <div className="border-t border-slate-800 pt-4">
                <h3 className="mb-3 text-sm font-semibold text-slate-200">Next of kin</h3>
                <div className="grid grid-cols-2 gap-4">
                  <input placeholder="Full name" value={empForm.next_of_kin_name} onChange={e => setEmpForm({...empForm, next_of_kin_name: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                  <input placeholder="Relationship" value={empForm.next_of_kin_relationship} onChange={e => setEmpForm({...empForm, next_of_kin_relationship: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                  <input placeholder="Phone" value={empForm.next_of_kin_phone} onChange={e => setEmpForm({...empForm, next_of_kin_phone: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                  <input placeholder="Address" value={empForm.next_of_kin_address} onChange={e => setEmpForm({...empForm, next_of_kin_address: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Email</label>
                  <input required type="email" value={empForm.email} onChange={e => setEmpForm({...empForm, email: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Password</label>
                  <input required type="text" placeholder="Set a temporary password" value={empForm.password} onChange={e => setEmpForm({...empForm, password: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Department</label>
                <select required value={empForm.department} onChange={e => setEmpForm({...empForm, department: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white">
                  <option value="">Select Department</option>
                  {departments.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Organization Role</label>
                <select required value={empForm.role} onChange={e => setEmpForm({...empForm, role: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white">
                  <option value="">Select Role</option>
                  {roles.map(r => <option key={r.id} value={r.id}>{r.title}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Line Manager</label>
                <select value={empForm.manager} onChange={e => setEmpForm({...empForm, manager: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white">
                  <option value="">No manager assigned</option>
                  {employees.filter(manager => manager.id !== 0).map(manager => <option key={manager.id} value={manager.id}>{manager.first_name} {manager.last_name}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">System Access Level (RBAC)</label>
                <select required value={empForm.rbac_role} onChange={e => setEmpForm({...empForm, rbac_role: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white">
                  <option value="employee">Standard Employee</option>
                  <option value="manager">Manager</option>
                  <option value="hr_officer">HR Officer</option>
                  <option value="payroll_officer">Payroll Officer</option>
                </select>
              </div>

              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowAddEmployee(false)} className="px-4 py-2 text-slate-300 hover:text-white">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-lg shadow-blue-500/20">Add Employee</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Department Modal */}
      {showCreateDept && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 animate-in zoom-in-95 duration-200">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white flex items-center">
                <Building className="w-6 h-6 mr-2 text-blue-400" />
                New Department
              </h2>
              <button onClick={() => setShowCreateDept(false)} className="text-slate-400 hover:text-white"><XCircle className="w-6 h-6" /></button>
            </div>

            <form onSubmit={handleCreateDepartment} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Department Name</label>
                <input required type="text" value={deptForm.name} onChange={e => setDeptForm({...deptForm, name: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Description</label>
                <textarea rows={2} value={deptForm.description} onChange={e => setDeptForm({...deptForm, description: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white resize-none" />
              </div>

              <div className="pt-2 border-t border-slate-800 mt-4">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-sm font-medium text-slate-300 flex items-center">
                    Geofencing Rules
                  </h3>
                  <button 
                    type="button" 
                    onClick={handleGetLocation}
                    disabled={isGettingLocation}
                    className="flex items-center text-xs text-emerald-400 hover:text-emerald-300 bg-emerald-500/10 hover:bg-emerald-500/20 px-2 py-1 rounded transition-colors disabled:opacity-50"
                    title="Get Current Location"
                  >
                    {isGettingLocation ? (
                      <Loader2 className="w-4 h-4 mr-1 animate-spin" />
                    ) : (
                      <MapPin className="w-4 h-4 mr-1" />
                    )}
                    Use Current Location
                  </button>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-400 mb-1">Latitude</label>
                    <input type="text" placeholder="e.g. 6.5244" value={deptForm.latitude} onChange={e => setDeptForm({...deptForm, latitude: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white text-sm" />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-400 mb-1">Longitude</label>
                    <input type="text" placeholder="e.g. 3.3792" value={deptForm.longitude} onChange={e => setDeptForm({...deptForm, longitude: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white text-sm" />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-xs font-medium text-slate-400 mb-1">Radius (meters)</label>
                    <input type="number" min="10" value={deptForm.geofence_radius_meters} onChange={e => setDeptForm({...deptForm, geofence_radius_meters: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white text-sm" />
                  </div>
                </div>
              </div>

              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowCreateDept(false)} className="px-4 py-2 text-slate-300 hover:text-white">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-lg shadow-blue-500/20">Create Department</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Role Modal */}
      {showCreateRole && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 animate-in zoom-in-95 duration-200">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white flex items-center">
                <Briefcase className="w-6 h-6 mr-2 text-blue-400" />
                New Role
              </h2>
              <button onClick={() => setShowCreateRole(false)} className="text-slate-400 hover:text-white"><XCircle className="w-6 h-6" /></button>
            </div>

            <form onSubmit={handleCreateRole} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Role Title</label>
                <input required type="text" placeholder="e.g. Senior Software Engineer" value={roleForm.title} onChange={e => setRoleForm({...roleForm, title: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white" />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Department</label>
                <select required value={roleForm.department} onChange={e => setRoleForm({...roleForm, department: e.target.value})} className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white">
                  <option value="">Select Department</option>
                  {departments.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                </select>
              </div>

              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowCreateRole(false)} className="px-4 py-2 text-slate-300 hover:text-white">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-lg shadow-blue-500/20">Create Role</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
