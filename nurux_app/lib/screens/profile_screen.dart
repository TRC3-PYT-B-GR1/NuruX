import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import 'login_screen.dart';
import 'notification_screen.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final AuthService _authService = AuthService();
  final ApiService _apiService = ApiService();
  
  String _employeeName = "Employee";
  String _employeeRole = "employee";

  @override
  void initState() {
    super.initState();
    _loadUserInfo();
  }

  Future<void> _loadUserInfo() async {
    final name = await _authService.getEmployeeName();
    final role = await _authService.getEmployeeRole();
    if (!mounted) return;
    setState(() {
      if (name != null && name.isNotEmpty) _employeeName = name;
      if (role != null && role.isNotEmpty) _employeeRole = role;
    });
  }

  Future<void> _handleLogout() async {
    await _apiService.logout();
    if (!mounted) return;
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (context) => const LoginScreen()),
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: const Text('My Profile', style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            const SizedBox(height: 16),
            // Profile Header
            Center(
              child: Container(
                width: 100,
                height: 100,
                decoration: BoxDecoration(
                  color: const Color(0xFF0F172A),
                  shape: BoxShape.circle,
                ),
                child: Center(
                  child: Text(
                    _employeeName.substring(0, 1).toUpperCase(),
                    style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: Colors.white),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 24),
            Text(
              _employeeName,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF0F172A)),
            ),
            const SizedBox(height: 4),
            Text(
              _employeeRole.replaceAll('_', ' '),
              style: const TextStyle(fontSize: 14, color: Colors.grey),
            ),
            
            const SizedBox(height: 48),
            
            // Menu Items
            _buildMenuItem(Icons.person_outline, 'Personal Information'),
            _buildMenuItem(Icons.notifications_outlined, 'Notifications'),
            _buildMenuItem(Icons.help_outline, 'Support & FAQ'),
            
            const SizedBox(height: 48),
            
            // Logout Button
            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton.icon(
                onPressed: _handleLogout,
                icon: const Icon(Icons.logout, color: Colors.white),
                label: const Text('Log Out', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red.shade400,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  elevation: 0,
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildMenuItem(IconData icon, String title) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: const Color(0xFFF8FAFC),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: ListTile(
        leading: Icon(icon, color: const Color(0xFF0F172A)),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600, color: Color(0xFF0F172A))),
        trailing: const Icon(Icons.chevron_right, color: Colors.grey),
        onTap: () {
          if (title == 'Notifications') {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const NotificationScreen()),
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text("Coming soon")),
            );
          }
        },
      ),
    );
  }
}
