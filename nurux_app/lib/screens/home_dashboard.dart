import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import 'qr_scanner_screen.dart';
import 'login_screen.dart';
import 'leave_screen.dart';

class HomeDashboard extends StatefulWidget {
  const HomeDashboard({super.key});

  @override
  State<HomeDashboard> createState() => _HomeDashboardState();
}

class _HomeDashboardState extends State<HomeDashboard> {
  final AuthService _authService = AuthService();
  final ApiService _apiService = ApiService();
  
  String _employeeName = "";
  String _employeeRole = "";
  bool _isCheckedIn = false;
  bool _hasCheckedOut = false;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadDashboard();
  }

  Future<void> _loadDashboard() async {
    final name = await _authService.getEmployeeName();
    final role = await _authService.getEmployeeRole();
    Map<String, dynamic>? today;
    try {
      today = await _apiService.getTodayAttendanceStatus();
    } catch (_) {}
    if (!mounted) return;
    setState(() {
      if (name != null) _employeeName = name;
      if (role != null) _employeeRole = role;
      _isCheckedIn = today?['is_checked_in'] == true;
      _hasCheckedOut = today?['is_checked_out'] == true;
      _isLoading = false;
    });
  }

  Future<void> _handleLogout() async {
    await _apiService.logout();
    if (!mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const LoginScreen()),
    );
  }

  // _handleClockOut is now handled via QRScannerScreen

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        children: [
          // Header Section
          Container(
            width: double.infinity,
            color: const Color(0xFF0F172A),
            padding: EdgeInsets.only(
              top: MediaQuery.of(context).padding.top + 24,
              left: 24,
              right: 24,
              bottom: 32,
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Good morning,',
                      style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 14),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      _employeeName,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      _employeeRole.replaceAll('_', ' '),
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.7),
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
                IconButton(
                  icon: const Icon(Icons.logout, color: Colors.white70),
                  onPressed: _handleLogout,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(),
                )
              ],
            ),
          ),
          
          // Main Content Section
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Today\'s Status', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 8),
                  Text(
                    _isCheckedIn ? 'Checked In' : (_hasCheckedOut ? 'Checked Out' : 'Not Checked In'),
                    style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF0F172A)),
                  ),
                  const SizedBox(height: 24),
                  
                  // Primary Action Button
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: _isLoading || _hasCheckedOut ? null : () async {
                        await Navigator.push(
                          context, 
                          MaterialPageRoute(
                            builder: (context) => QRScannerScreen(isClockOut: _isCheckedIn)
                          )
                        );
                        await _loadDashboard();
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: _isCheckedIn ? const Color(0xFFEF4444) : const Color(0xFF10B981),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      child: _isLoading
                          ? const CircularProgressIndicator(color: Colors.white)
                          : Text(
                              _hasCheckedOut
                                  ? 'Attendance Complete for Today'
                                  : (_isCheckedIn ? 'Scan QR to Clock Out' : 'Scan QR to Check In'),
                              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                            ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  
                  // Secondary Action Button (Leave)
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: OutlinedButton(
                      onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const LeaveScreen())),
                      style: OutlinedButton.styleFrom(
                        side: const BorderSide(color: Color(0xFF10B981), width: 2),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      child: const Text(
                        'Request for Leave',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF10B981)),
                      ),
                    ),
                  ),
                  const SizedBox(height: 32),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
