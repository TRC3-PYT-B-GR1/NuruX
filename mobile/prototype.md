import 'package:flutter/material.dart';
import 'dart:async';

void main() {
  runApp(const SmartAttendanceApp());
}

/// Defines the core color palette used throughout the application.
/// Centralizing colors makes theming and future updates easier.
class AppColors {
  static const Color primaryBlue = Color(0xFF101D38);
  static const Color primaryTeal = Color(0xFF23B59A);
  static const Color background = Color(0xFFF7F9FC);
  static const Color cardBg = Colors.white;
  
  // Text colors
  static const Color textMain = Color(0xFF1E293B);
  static const Color textSecondary = Color(0xFF64748B);
  
  // Status indicator colors
  static const Color statusOnTimeBg = Color(0xFFE8F7F0);
  static const Color statusOnTimeText = Color(0xFF10B981);
  static const Color statusLateBg = Color(0xFFFFF7ED);
  static const Color statusLateText = Color(0xFFF59E0B);
  static const Color statusAbsentBg = Color(0xFFFEF2F2);
  static const Color statusAbsentText = Color(0xFFEF4444);
}

/// The root widget of the application.
/// Configures the global theme, fonts, and default routing.
class SmartAttendanceApp extends StatelessWidget {
  const SmartAttendanceApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Attendance',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        scaffoldBackgroundColor: AppColors.background,
        primaryColor: AppColors.primaryBlue,
        fontFamily: 'Roboto', // Uses a clean sans-serif font
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.primaryBlue,
          primary: AppColors.primaryBlue,
          secondary: AppColors.primaryTeal,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: AppColors.background,
          elevation: 0,
          iconTheme: IconThemeData(color: AppColors.textMain),
          titleTextStyle: TextStyle(
            color: AppColors.primaryBlue,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      home: const LoginScreen(),
    );
  }
}

/// The initial authentication screen.
/// Includes standard credentials login and a biometric alternative.
class LoginScreen extends StatelessWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 40),
              _buildLogo(),
              const SizedBox(height: 32),
              _buildWelcomeText(),
              const SizedBox(height: 40),
              _buildLoginForm(context),
              const SizedBox(height: 32),
              _buildDivider(),
              const SizedBox(height: 32),
              _buildBiometricLogin(),
              const SizedBox(height: 40),
              const Text(
                'Having trouble signing in? Contact HR support',
                style: TextStyle(color: AppColors.textSecondary, fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // Extracted UI builder for the app logo
  Widget _buildLogo() {
    return Container(
      width: 80,
      height: 80,
      decoration: BoxDecoration(
        color: AppColors.primaryBlue,
        borderRadius: BorderRadius.circular(20),
      ),
      alignment: Alignment.center,
      child: const Text(
        'NuruX',
        style: TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
          fontSize: 20,
        ),
      ),
    );
  }

  // Extracted UI builder for the welcome messaging
  Widget _buildWelcomeText() {
    return Column(
      children: const [
        Text(
          'Smart Attendance',
          style: TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
            color: AppColors.primaryBlue,
          ),
        ),
        SizedBox(height: 8),
        Text(
          'Sign in with your company account',
          style: TextStyle(
            color: AppColors.textSecondary,
            fontSize: 14,
          ),
        ),
      ],
    );
  }

  // Extracted UI builder for the input fields and login button
  Widget _buildLoginForm(BuildContext context) {
    return Column(
      children: [
        const CustomTextField(hint: 'Employee ID or email'),
        const SizedBox(height: 16),
        const CustomTextField(hint: 'Password', obscureText: true),
        const SizedBox(height: 16),
        Align(
          alignment: Alignment.centerLeft,
          child: TextButton(
            onPressed: () {
              // TODO: Implement forgot password logic
            },
            child: const Text(
              'Forgot password?',
              style: TextStyle(color: AppColors.primaryTeal),
            ),
          ),
        ),
        const SizedBox(height: 24),
        SizedBox(
          width: double.infinity,
          height: 56,
          child: ElevatedButton(
            onPressed: () {
              // Navigate to main dashboard upon successful login
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (_) => const MainNavigationScreen()),
              );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primaryBlue,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: const Text(
              'Log In',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: Colors.white),
            ),
          ),
        ),
      ],
    );
  }

  // Extracted UI builder for the "or sign in with" divider
  Widget _buildDivider() {
    return Row(
      children: [
        Expanded(child: Divider(color: Colors.grey.shade300)),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 16),
          child: Text('or sign in with', style: TextStyle(color: AppColors.textSecondary, fontSize: 12)),
        ),
        Expanded(child: Divider(color: Colors.grey.shade300)),
      ],
    );
  }

  // Extracted UI builder for Face ID / Touch ID prompt
  Widget _buildBiometricLogin() {
    return Column(
      children: [
        Container(
          width: 60,
          height: 60,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: AppColors.primaryTeal, width: 2),
          ),
          child: const Icon(Icons.fingerprint, color: AppColors.primaryTeal, size: 32),
        ),
        const SizedBox(height: 16),
        const Text(
          'Sign in with Face ID / Touch ID',
          style: TextStyle(fontWeight: FontWeight.w500, color: AppColors.textMain),
        ),
      ],
    );
  }
}

/// A reusable, stylized text field for forms.
class CustomTextField extends StatelessWidget {
  final String hint;
  final bool obscureText;

  const CustomTextField({
    Key? key, 
    required this.hint, 
    this.obscureText = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextField(
      obscureText: obscureText,
      decoration: InputDecoration(
        hintText: hint,
        hintStyle: const TextStyle(color: Colors.black38),
        filled: true,
        fillColor: const Color(0xFFF1F5F9),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 18),
      ),
    );
  }
}

/// Manages the bottom navigation bar and swaps between the main application views.
class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({Key? key}) : super(key: key);

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;
  
  // List of root screens corresponding to navigation tabs
  final List<Widget> _screens = [
    const HomeScreen(),
    const HistoryScreen(),
    const ReportsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        selectedItemColor: AppColors.primaryBlue,
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home_filled), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: 'History'),
          BottomNavigationBarItem(icon: Icon(Icons.bar_chart), label: 'Reports'),
        ],
      ),
    );
  }
}

/// The primary dashboard displaying user status, quick stats, and recent activity.
class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // State variables intended to be populated by an API response
  String userName = '';
  String userRole = '';
  String currentStatus = 'Not Checked In';
  int onTimeDays = 0;
  int lateDays = 0;
  
  // Empty list for recent activities representing a state before data is fetched
  List<Map<String, dynamic>> recentActivities = [];

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(),
          Transform.translate(
            offset: const Offset(0, -20),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildStatusCard(context),
                  const SizedBox(height: 24),
                  _buildStatsRow(),
                  const SizedBox(height: 32),
                  const Text(
                    'Recent Activity', 
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.primaryBlue)
                  ),
                  const SizedBox(height: 16),
                  _buildRecentActivityList(),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Top colored header containing user info
  Widget _buildHeader() {
    return Container(
      width: double.infinity,
      color: AppColors.primaryBlue,
      padding: const EdgeInsets.only(top: 60, left: 24, right: 24, bottom: 40),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Good morning,', style: TextStyle(color: Colors.white70, fontSize: 14)),
          const SizedBox(height: 4),
          Text(
            userName.isEmpty ? 'Employee Name' : userName, 
            style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)
          ),
          const SizedBox(height: 4),
          Text(
            userRole.isEmpty ? 'Role • Location' : userRole, 
            style: const TextStyle(color: Colors.white70, fontSize: 14)
          ),
        ],
      ),
    );
  }

  // Floating card showing current check-in status and scan button
  Widget _buildStatusCard(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Today\'s Status', style: TextStyle(color: AppColors.textSecondary, fontSize: 12)),
          const SizedBox(height: 8),
          Text(
            currentStatus, 
            style: const TextStyle(color: AppColors.primaryBlue, fontSize: 18, fontWeight: FontWeight.bold)
          ),
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            height: 50,
            child: ElevatedButton(
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const QRScanScreen()));
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primaryTeal,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              child: const Text('Scan QR to Check In', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: Colors.white)),
            ),
          ),
        ],
      ),
    );
  }

  // Row displaying summarized monthly stats
  Widget _buildStatsRow() {
    return Row(
      children: [
        Expanded(
          child: SummaryStatCard(
            title: '$onTimeDays days', 
            subtitle: 'On-time this month', 
            bgColor: AppColors.statusOnTimeBg, 
            textColor: AppColors.statusOnTimeText
          )
        ),
        const SizedBox(width: 16),
        Expanded(
          child: SummaryStatCard(
            title: '$lateDays days', 
            subtitle: 'Late arrivals', 
            bgColor: AppColors.statusLateBg, 
            textColor: AppColors.statusLateText
          )
        ),
      ],
    );
  }

  // Handles rendering the empty state or the list of recent activities
  Widget _buildRecentActivityList() {
    if (recentActivities.isEmpty) {
      return const Padding(
        padding: EdgeInsets.symmetric(vertical: 24),
        child: Center(
          child: Text('No recent activity available.', style: TextStyle(color: AppColors.textSecondary)),
        ),
      );
    }
    
    return Column(
      children: recentActivities.map((activity) => ActivityListItem(
        date: activity['date'] ?? '',
        description: activity['description'] ?? '',
        statusText: activity['statusText'],
        statusColor: activity['statusColor'],
      )).toList(),
    );
  }
}

/// Reusable widget for displaying summary statistics in a rounded box
class SummaryStatCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final Color bgColor;
  final Color textColor;

  const SummaryStatCard({
    Key? key,
    required this.title,
    required this.subtitle,
    required this.bgColor,
    required this.textColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: bgColor, borderRadius: BorderRadius.circular(12)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: textColor)),
          const SizedBox(height: 4),
          Text(subtitle, style: TextStyle(fontSize: 12, color: textColor.withOpacity(0.8))),
        ],
      ),
    );
  }
}

/// Reusable widget for individual activity rows
class ActivityListItem extends StatelessWidget {
  final String date;
  final String description;
  final String? statusText;
  final Color? statusColor;

  const ActivityListItem({
    Key? key,
    required this.date,
    required this.description,
    this.statusText,
    this.statusColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 24),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(date, style: const TextStyle(fontWeight: FontWeight.w600, color: AppColors.textMain, fontSize: 14)),
              const SizedBox(height: 4),
              Row(
                children: [
                  Text(description, style: const TextStyle(color: AppColors.textSecondary, fontSize: 12)),
                  if (statusText != null) ...[
                    const Text(' • ', style: TextStyle(color: AppColors.textSecondary, fontSize: 12)),
                    Text(statusText!, style: TextStyle(color: statusColor, fontSize: 12, fontWeight: FontWeight.w500)),
                  ]
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}

/// Simulates a camera viewfinder for scanning an office QR code.
class QRScanScreen extends StatefulWidget {
  const QRScanScreen({Key? key}) : super(key: key);

  @override
  State<QRScanScreen> createState() => _QRScanScreenState();
}

class _QRScanScreenState extends State<QRScanScreen> {
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF11151E),
      body: SafeArea(
        child: GestureDetector(
          // Simulating a successful scan on tap anywhere for demo purposes
          onTap: () {
            Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => SuccessScreen(
              locationName: 'Verified Location',
              checkInTime: DateTime.now(),
              statusMessage: 'Checked In Successfully',
              isLate: false,
            )));
          },
          child: Column(
            children: [
              const SizedBox(height: 40),
              const Text('Scan Office QR Code', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              const Text('Align the QR code within the frame', style: TextStyle(color: Colors.white70, fontSize: 14)),
              
              Expanded(
                child: Center(
                  child: _buildScannerFrame(),
                ),
              ),
              
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 40),
                child: Text(
                  'Point your camera at the QR code posted at your office entrance',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white54, fontSize: 12),
                ),
              ),
              const SizedBox(height: 40),
              
              _buildCancelButton(context),
            ],
          ),
        ),
      ),
    );
  }

  // Builds the animated-looking bounding box for the QR code
  Widget _buildScannerFrame() {
    return Container(
      width: 250,
      height: 250,
      decoration: BoxDecoration(
        border: Border.all(color: Colors.transparent),
      ),
      child: Stack(
        children: [
          _buildScannerCorner(Alignment.topLeft, borderLeft: true, borderTop: true),
          _buildScannerCorner(Alignment.topRight, borderRight: true, borderTop: true),
          _buildScannerCorner(Alignment.bottomLeft, borderLeft: true, borderBottom: true),
          _buildScannerCorner(Alignment.bottomRight, borderRight: true, borderBottom: true),
          
          // Simulated scanning laser line
          Center(
            child: Container(
              height: 2,
              width: double.infinity,
              color: AppColors.primaryTeal,
              margin: const EdgeInsets.symmetric(horizontal: 10),
            ),
          )
        ],
      ),
    );
  }

  // Helper to draw the corners of the scanner frame
  Widget _buildScannerCorner(Alignment alignment, {bool borderLeft = false, bool borderTop = false, bool borderRight = false, bool borderBottom = false}) {
    return Align(
      alignment: alignment,
      child: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
          border: Border(
            left: borderLeft ? const BorderSide(color: AppColors.primaryTeal, width: 4) : BorderSide.none,
            top: borderTop ? const BorderSide(color: AppColors.primaryTeal, width: 4) : BorderSide.none,
            right: borderRight ? const BorderSide(color: AppColors.primaryTeal, width: 4) : BorderSide.none,
            bottom: borderBottom ? const BorderSide(color: AppColors.primaryTeal, width: 4) : BorderSide.none,
          ),
        ),
      ),
    );
  }

  // Cancel button for the scanner
  Widget _buildCancelButton(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: SizedBox(
        width: double.infinity,
        height: 56,
        child: TextButton(
          onPressed: () => Navigator.pop(context),
          style: TextButton.styleFrom(
            backgroundColor: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
          child: const Text('Cancel', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.primaryBlue)),
        ),
      ),
    );
  }
}

/// Displays the result of a successful scan, confirming location and time.
class SuccessScreen extends StatelessWidget {
  final String locationName;
  final DateTime checkInTime;
  final bool isLate;
  final String statusMessage;
  final String? lateDurationMessage;

  const SuccessScreen({
    Key? key,
    required this.locationName,
    required this.checkInTime,
    this.isLate = false,
    required this.statusMessage,
    this.lateDurationMessage,
  }) : super(key: key);

  /// Helper to format DateTime into a readable string (e.g., 9:02 AM • 5 Aug)
  String _formatTime(DateTime time) {
    String hour = time.hour > 12 ? (time.hour - 12).toString() : (time.hour == 0 ? '12' : time.hour.toString());
    String minute = time.minute.toString().padLeft(2, '0');
    String amPm = time.hour >= 12 ? 'PM' : 'AM';
    List<String> months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    String month = months[time.month - 1];
    return '$hour:$minute $amPm • ${time.day} $month';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          _buildMapBackground(context),
          _buildConfirmationSheet(context),
        ],
      ),
    );
  }

  // Simulates a stylized map background showing the user's pinned location
  Widget _buildMapBackground(BuildContext context) {
    return Positioned(
      top: 0, left: 0, right: 0, bottom: MediaQuery.of(context).size.height * 0.4,
      child: Container(
        color: const Color(0xFFE2EBE5),
        child: Stack(
          alignment: Alignment.center,
          children: [
            // Decorative line representing a road or path
            Container(height: 10, width: double.infinity, color: const Color(0xFFC8D6CE)),
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Location label tag
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.white, 
                    borderRadius: BorderRadius.circular(20), 
                    boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 4)]
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.location_on, color: AppColors.statusAbsentText, size: 16),
                      const SizedBox(width: 4),
                      Text(locationName, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
                const SizedBox(height: 30),
                // Pulsing dot indicator
                Container(
                  width: 80, height: 80,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: AppColors.primaryTeal, width: 2, style: BorderStyle.solid),
                    color: AppColors.primaryTeal.withOpacity(0.1),
                  ),
                  child: Center(
                    child: Container(
                      width: 12, height: 12,
                      decoration: const BoxDecoration(color: AppColors.primaryBlue, shape: BoxShape.circle),
                    ),
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }

  // White bottom sheet containing the status summary and action button
  Widget _buildConfirmationSheet(BuildContext context) {
    return Positioned(
      left: 0, right: 0, bottom: 0,
      child: Container(
        padding: const EdgeInsets.all(32),
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.vertical(top: Radius.circular(32)),
          boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 20, offset: Offset(0, -5))],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Success Chip
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(color: AppColors.statusOnTimeBg, borderRadius: BorderRadius.circular(20)),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: const [
                  Icon(Icons.check, color: AppColors.statusOnTimeText, size: 16),
                  SizedBox(width: 4),
                  Text('Location Verified', style: TextStyle(color: AppColors.statusOnTimeText, fontSize: 12, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Text(statusMessage, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.primaryBlue)),
            const SizedBox(height: 8),
            Text(_formatTime(checkInTime), style: const TextStyle(color: AppColors.textSecondary, fontSize: 14)),
            
            // Conditional UI if the employee arrived late
            if (isLate && lateDurationMessage != null) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(color: AppColors.statusLateBg, borderRadius: BorderRadius.circular(20)),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.access_alarm, color: AppColors.statusLateText, size: 16),
                    const SizedBox(width: 4),
                    Text(lateDurationMessage!, style: const TextStyle(color: AppColors.statusLateText, fontSize: 12, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            ],
            
            const SizedBox(height: 32),
            // Done Button
            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryBlue,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Done', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: Colors.white)),
              ),
            ),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}

/// Shows a historical log of the user's attendance records for a selected period.
class HistoryScreen extends StatefulWidget {
  const HistoryScreen({Key? key}) : super(key: key);

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  String currentPeriod = 'Current Period';
  int onTimeCount = 0;
  int lateCount = 0;
  int absentCount = 0;
  
  // Empty list prepared for fetched history logs
  List<Map<String, dynamic>> historyRecords = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Attendance History'),
        centerTitle: false,
      ),
      body: Column(
        children: [
          _buildPeriodSelector(),
          _buildSummaryStatsRow(),
          const SizedBox(height: 24),
          _buildHistoryList(),
        ],
      ),
    );
  }

  // Header allowing user to switch months/periods
  Widget _buildPeriodSelector() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Icon(Icons.chevron_left, color: AppColors.textSecondary),
          Text(currentPeriod, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.primaryBlue)),
          const Icon(Icons.chevron_right, color: AppColors.textSecondary),
        ],
      ),
    );
  }

  // Three-column row showing aggregated counts for the period
  Widget _buildSummaryStatsRow() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Row(
        children: [
          Expanded(child: MiniStatBox(count: '$onTimeCount', label: 'On time', bg: AppColors.statusOnTimeBg, textCol: AppColors.statusOnTimeText)),
          const SizedBox(width: 12),
          Expanded(child: MiniStatBox(count: '$lateCount', label: 'Late', bg: AppColors.statusLateBg, textCol: AppColors.statusLateText)),
          const SizedBox(width: 12),
          Expanded(child: MiniStatBox(count: '$absentCount', label: 'Absent', bg: AppColors.statusAbsentBg, textCol: AppColors.statusAbsentText)),
        ],
      ),
    );
  }

  // Scrollable list of past attendance records
  Widget _buildHistoryList() {
    return Expanded(
      child: historyRecords.isEmpty 
        ? const Center(child: Text('No attendance records found.', style: TextStyle(color: AppColors.textSecondary)))
        : ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            itemCount: historyRecords.length,
            itemBuilder: (context, index) {
              final record = historyRecords[index];
              return HistoryItemRow(
                date: record['date'] ?? '', 
                time: record['time'] ?? '', 
                status: record['status'] ?? '', 
                statusBg: record['statusBg'] ?? AppColors.background, 
                statusText: record['statusText'] ?? AppColors.textMain,
              );
            }
          ),
    );
  }
}

/// Helper widget for the three-column stats on the history screen
class MiniStatBox extends StatelessWidget {
  final String count;
  final String label;
  final Color bg;
  final Color textCol;

  const MiniStatBox({
    Key? key,
    required this.count,
    required this.label,
    required this.bg,
    required this.textCol,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 16),
      decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(12)),
      child: Column(
        children: [
          Text(count, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: textCol)),
          Text(label, style: TextStyle(fontSize: 12, color: textCol)),
        ],
      ),
    );
  }
}

/// Helper widget displaying an individual log row in the history list
class HistoryItemRow extends StatelessWidget {
  final String date;
  final String time;
  final String status;
  final Color statusBg;
  final Color statusText;

  const HistoryItemRow({
    Key? key,
    required this.date,
    required this.time,
    required this.status,
    required this.statusBg,
    required this.statusText,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 24),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(date, style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.primaryBlue, fontSize: 14)),
              const SizedBox(height: 4),
              Text(time, style: const TextStyle(color: AppColors.textSecondary, fontSize: 12)),
            ],
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(color: statusBg, borderRadius: BorderRadius.circular(12)),
            child: Text(status, style: TextStyle(color: statusText, fontSize: 12, fontWeight: FontWeight.bold)),
          )
        ],
      ),
    );
  }
}

/// Shows macro-level company attendance statistics (typically for HR admins).
class ReportsScreen extends StatefulWidget {
  const ReportsScreen({Key? key}) : super(key: key);

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  String reportTitle = 'Company-wide • Current Period';
  double avgAttendance = 0.0;
  int lateArrivals = 0;
  
  // Empty data arrays awaiting API population
  List<Map<String, dynamic>> chartData = [];
  List<Map<String, dynamic>> frequentLateEmployees = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Attendance Reports'),
        centerTitle: false,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(reportTitle, style: const TextStyle(color: AppColors.textSecondary)),
            const SizedBox(height: 24),
            _buildTopStatsRow(),
            const SizedBox(height: 32),
            const Text('On-time Rate by Day', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.primaryBlue)),
            const SizedBox(height: 24),
            _buildBarChart(),
            const SizedBox(height: 40),
            const Text('Frequent Late Arrivals', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.primaryBlue)),
            const SizedBox(height: 16),
            _buildFrequentLateList(),
            const SizedBox(height: 40),
            _buildExportButton(),
          ],
        ),
      ),
    );
  }

  // Row showing average attendance percentage and total late arrivals
  Widget _buildTopStatsRow() {
    return Row(
      children: [
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white, 
              borderRadius: BorderRadius.circular(12), 
              border: Border.all(color: Colors.grey.shade200)
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('${avgAttendance.toStringAsFixed(1)}%', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.primaryBlue)),
                const Text('Avg. attendance', style: TextStyle(fontSize: 12, color: AppColors.textSecondary)),
              ],
            ),
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: AppColors.statusLateBg, borderRadius: BorderRadius.circular(12)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('$lateArrivals', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.statusLateText)),
                const Text('Late arrivals', style: TextStyle(fontSize: 12, color: AppColors.statusLateText)),
              ],
            ),
          ),
        ),
      ],
    );
  }

  // Renders a custom bar chart layout mapping over dynamic data
  Widget _buildBarChart() {
    return SizedBox(
      height: 150,
      child: chartData.isEmpty 
        ? const Center(child: Text('Not enough data for chart.', style: TextStyle(color: AppColors.textSecondary)))
        : Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            crossAxisAlignment: CrossAxisAlignment.end,
            children: chartData.map((data) => ChartBarColumn(
              label: data['label'] ?? '', 
              fillPercentage: data['value'] ?? 0.0
            )).toList(),
          ),
    );
  }

  // Renders the list of employees who frequently arrive late
  Widget _buildFrequentLateList() {
    if (frequentLateEmployees.isEmpty) {
      return const Padding(
        padding: EdgeInsets.symmetric(vertical: 16),
        child: Text('No frequent late arrivals recorded.', style: TextStyle(color: AppColors.textSecondary)),
      );
    }
    
    return Column(
      children: frequentLateEmployees.map((emp) => Padding(
        padding: const EdgeInsets.only(bottom: 16),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(emp['name'] ?? '', style: const TextStyle(fontWeight: FontWeight.w500, color: AppColors.primaryBlue)),
            Text(emp['detail'] ?? '', style: const TextStyle(color: AppColors.statusLateText, fontSize: 12, fontWeight: FontWeight.w500)),
          ],
        ),
      )).toList(),
    );
  }

  // Bottom action button for exporting data
  Widget _buildExportButton() {
    return SizedBox(
      width: double.infinity,
      height: 56,
      child: OutlinedButton(
        onPressed: () {
          // TODO: Implement CSV generation and download
        },
        style: OutlinedButton.styleFrom(
          side: const BorderSide(color: AppColors.primaryBlue),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
        child: const Text('Export CSV Report', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: AppColors.primaryBlue)),
      ),
    );
  }
}

/// Custom drawn bar component used in the Reports Screen charts
class ChartBarColumn extends StatelessWidget {
  final String label;
  final double fillPercentage;

  const ChartBarColumn({
    Key? key,
    required this.label,
    required this.fillPercentage,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        Container(
          width: 32,
          height: 120,
          decoration: BoxDecoration(
            color: const Color(0xFFE2E8F0),
            borderRadius: BorderRadius.circular(6),
          ),
          alignment: Alignment.bottomCenter,
          child: FractionallySizedBox(
            heightFactor: fillPercentage,
            child: Container(
              decoration: BoxDecoration(
                color: AppColors.primaryTeal,
                borderRadius: BorderRadius.circular(6),
              ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Text(label, style: const TextStyle(color: AppColors.textSecondary, fontSize: 12)),
      ],
    );
  }
}