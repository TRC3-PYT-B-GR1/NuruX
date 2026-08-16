import 'package:flutter/material.dart';

class NotificationScreen extends StatelessWidget {
  const NotificationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Dummy notifications for UI demonstration
    final List<Map<String, dynamic>> notifications = [
      {
        'title': 'Leave Request Approved',
        'body': 'Your annual leave request from Aug 15 to Aug 20 has been approved by HR.',
        'time': '2 hours ago',
        'icon': Icons.check_circle_outline,
        'color': const Color(0xFF10B981),
        'isUnread': true,
      },
      {
        'title': 'Attendance Flag',
        'body': 'You arrived 14 minutes late yesterday. Please ensure you clock in before 9:00 AM.',
        'time': 'Yesterday',
        'icon': Icons.warning_amber_rounded,
        'color': const Color(0xFFF59E0B),
        'isUnread': true,
      },
      {
        'title': 'System Update',
        'body': 'The NuruX platform will be undergoing scheduled maintenance this weekend.',
        'time': 'Aug 8, 2026',
        'icon': Icons.info_outline,
        'color': const Color(0xFF3B82F6),
        'isUnread': false,
      },
      {
        'title': 'Welcome to NuruX',
        'body': 'Your employee profile has been successfully set up. Welcome aboard!',
        'time': 'Aug 1, 2026',
        'icon': Icons.celebration_outlined,
        'color': const Color(0xFF8B5CF6),
        'isUnread': false,
      },
    ];

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF0F172A)),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text('Notifications', style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: notifications.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.notifications_off_outlined, size: 64, color: Colors.grey.shade300),
                  const SizedBox(height: 16),
                  const Text("No notifications yet", style: TextStyle(color: Colors.grey, fontSize: 16)),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(24.0),
              itemCount: notifications.length,
              itemBuilder: (context, index) {
                final notif = notifications[index];
                return _buildNotificationItem(notif);
              },
            ),
    );
  }

  Widget _buildNotificationItem(Map<String, dynamic> notif) {
    final bool isUnread = notif['isUnread'] ?? false;
    
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isUnread ? const Color(0xFFF8FAFC) : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isUnread ? const Color(0xFFE2E8F0) : Colors.grey.shade200,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: notif['color'].withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(notif['icon'], color: notif['color'], size: 24),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        notif['title'],
                        style: TextStyle(
                          fontWeight: isUnread ? FontWeight.bold : FontWeight.w600,
                          fontSize: 16,
                          color: const Color(0xFF0F172A),
                        ),
                      ),
                    ),
                    if (isUnread)
                      Container(
                        width: 8,
                        height: 8,
                        decoration: const BoxDecoration(
                          color: Color(0xFF3B82F6),
                          shape: BoxShape.circle,
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  notif['body'],
                  style: TextStyle(
                    color: Colors.grey.shade600,
                    fontSize: 14,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  notif['time'],
                  style: TextStyle(
                    color: Colors.grey.shade400,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
