import 'package:flutter/material.dart';
import '../services/api_service.dart';

class HistoryScreen extends StatefulWidget {
  final bool showBackButton;
  const HistoryScreen({super.key, this.showBackButton = true});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  final ApiService _apiService = ApiService();
  bool _isLoading = true;
  List<dynamic> _history = [];
  String? _errorMessage;
  
  DateTime _currentMonth = DateTime.now();

  @override
  void initState() {
    super.initState();
    _fetchHistory();
  }

  Future<void> _fetchHistory() async {
    try {
      final data = await _apiService.getAttendanceHistory();
      if (!mounted) return;
      setState(() {
        _history = data;
        _isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  String _getMonthName(int month) {
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    return months[month - 1];
  }

  String _formatDate(DateTime date) {
    const weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return "${weekdays[date.weekday - 1]}, ${date.day} ${months[date.month - 1]}";
  }

  Widget _buildStatusTag(String? status) {
    Color bgColor;
    Color textColor;
    String text;

    if (status == 'ON_TIME' || status == 'PRESENT') {
      bgColor = const Color(0xFFE6F7F1);
      textColor = const Color(0xFF10B981);
      text = 'On Time';
    } else if (status == 'LATE') {
      bgColor = const Color(0xFFFEF3C7);
      textColor = const Color(0xFFD97706);
      text = 'Late';
    } else {
      bgColor = Colors.red.shade50;
      textColor = Colors.red.shade400;
      text = 'Absent';
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        text,
        style: TextStyle(color: textColor, fontWeight: FontWeight.bold, fontSize: 12),
      ),
    );
  }

  Widget _buildStatCard(String count, String label, Color bgColor, Color textColor) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
        decoration: BoxDecoration(
          color: bgColor,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(count, style: TextStyle(color: textColor, fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(label, style: TextStyle(color: textColor, fontSize: 12)),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Calculate stats based on _history data for the current month
    // We will just do a simple filter for this example
    final currentMonthRecords = _history.where((record) {
      final date = DateTime.parse(record['date']).toLocal();
      return date.month == _currentMonth.month && date.year == _currentMonth.year;
    }).toList();

    int onTimeCount = 0;
    int lateCount = 0;
    int absentCount = 0;

    for (var record in currentMonthRecords) {
      if (record['status'] == 'ON_TIME' || record['status'] == 'PRESENT') {
        onTimeCount++;
      } else if (record['status'] == 'LATE') {
        lateCount++;
      } else {
        absentCount++;
      }
    }

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: widget.showBackButton 
            ? IconButton(
                icon: const Icon(Icons.arrow_back, color: Color(0xFF0F172A)),
                onPressed: () => Navigator.pop(context),
              )
            : null,
      ),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator(color: Color(0xFF0F172A)))
        : _errorMessage != null
          ? Center(child: Text(_errorMessage!, style: const TextStyle(color: Colors.red)))
          : Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Attendance History',
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF0F172A),
                    ),
                  ),
                  const SizedBox(height: 24),
                  
                  // Month Selector
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.chevron_left, size: 20),
                        onPressed: () {
                          setState(() {
                            _currentMonth = DateTime(_currentMonth.year, _currentMonth.month - 1);
                          });
                        },
                      ),
                      Text(
                        "${_getMonthName(_currentMonth.month)} ${_currentMonth.year}",
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF0F172A),
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.chevron_right, size: 20),
                        onPressed: () {
                          setState(() {
                            _currentMonth = DateTime(_currentMonth.year, _currentMonth.month + 1);
                          });
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // Stat Cards
                  Row(
                    children: [
                      _buildStatCard(
                        onTimeCount.toString(), 
                        'On time', 
                        const Color(0xFFE6F7F1), 
                        const Color(0xFF10B981)
                      ),
                      const SizedBox(width: 12),
                      _buildStatCard(
                        lateCount.toString(), 
                        'Late', 
                        const Color(0xFFFEF3C7), 
                        const Color(0xFFD97706)
                      ),
                      const SizedBox(width: 12),
                      _buildStatCard(
                        absentCount.toString(), 
                        'Absent', 
                        Colors.red.shade50, 
                        Colors.red.shade400
                      ),
                    ],
                  ),
                  const SizedBox(height: 32),
                  
                  // List
                  Expanded(
                    child: ListView.builder(
                      itemCount: currentMonthRecords.length,
                      itemBuilder: (context, index) {
                        final record = currentMonthRecords[index];
                        final DateTime date = DateTime.parse(record['date']).toLocal();
                        final String dateStr = _formatDate(date);
                        
                        String timeStr = "—";
                        if (record['clock_in'] != null && record['status'] != 'ABSENT') {
                          final clockIn = DateTime.parse(record['clock_in']).toLocal();
                          final int hour = clockIn.hour;
                          final int minute = clockIn.minute;
                          final String period = hour >= 12 ? 'PM' : 'AM';
                          final int displayHour = hour > 12 ? hour - 12 : (hour == 0 ? 12 : hour);
                          timeStr = "$displayHour:${minute.toString().padLeft(2, '0')} $period";
                        }

                        return Padding(
                          padding: const EdgeInsets.only(bottom: 24.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    dateStr, 
                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF0F172A))
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    timeStr,
                                    style: const TextStyle(color: Colors.grey, fontSize: 14),
                                  ),
                                ],
                              ),
                              _buildStatusTag(record['status']),
                            ],
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
