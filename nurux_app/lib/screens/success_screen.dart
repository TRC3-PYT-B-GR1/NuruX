import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/location_service.dart';
import 'main_layout.dart';

class SuccessScreen extends StatefulWidget {
  final String qrToken;
  final bool isClockOut;
  const SuccessScreen({super.key, required this.qrToken, this.isClockOut = false});

  @override
  State<SuccessScreen> createState() => _SuccessScreenState();
}

class _SuccessScreenState extends State<SuccessScreen> {
  final ApiService _apiService = ApiService();
  final LocationService _locationService = LocationService();
  
  bool _isLoading = true;
  bool _isSuccess = false;
  String _message = "Verifying Location & Token...";
  String _anomalyMsg = "";

  @override
  void initState() {
    super.initState();
    _processClockIn();
  }

  Future<void> _processClockIn() async {
    try {
      final position = await _locationService.getCurrentLocation();
      final locationStr = _locationService.formatLocation(position);
      
      Map<String, dynamic> response;
      if (widget.isClockOut) {
        response = await _apiService.clockOut(locationStr, widget.qrToken);
      } else {
        response = await _apiService.clockIn(locationStr, widget.qrToken);
      }
      
      if (!mounted) return;
      setState(() {
        _isLoading = false;
        _isSuccess = true;
        _message = widget.isClockOut ? "Clocked Out Successfully" : "Checked In Successfully";
        
        final timeStr = response[widget.isClockOut ? 'clock_out' : 'clock_in'];
        if (timeStr != null) {
          final parsedTime = DateTime.parse(timeStr).toLocal();
          final formattedTime = "${parsedTime.hour}:${parsedTime.minute.toString().padLeft(2, '0')}";
          
          if (!widget.isClockOut) {
            if (response['is_anomaly'] == true) {
              _anomalyMsg = response['anomaly_reason'] ?? 'Anomaly detected';
            } else if (response['status'] == 'LATE') {
              _anomalyMsg = 'Arrived Late at $formattedTime';
            }
          }
        }
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _isLoading = false;
        _isSuccess = false;
        _message = widget.isClockOut ? "Clock Out Failed" : "Check In Failed";
        _anomalyMsg = e.toString().replaceAll('Exception: ', '');
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        children: [
          // Sleek Location Animation Area (Upper half)
          Expanded(
            flex: 3,
            child: Container(
              width: double.infinity,
              color: Colors.white, // Clean white background
              child: Center(
                child: _isLoading
                    ? const CircularProgressIndicator(color: Color(0xFF10B981))
                    : _isSuccess
                        ? Container(
                            width: 150,
                            height: 150,
                            decoration: BoxDecoration(
                              color: const Color(0xFF10B981).withValues(alpha: 0.1),
                              shape: BoxShape.circle,
                            ),
                            child: Center(
                              child: Container(
                                width: 100,
                                height: 100,
                                decoration: BoxDecoration(
                                  color: const Color(0xFF10B981).withValues(alpha: 0.2),
                                  shape: BoxShape.circle,
                                ),
                                child: Center(
                                  child: Container(
                                    width: 50,
                                    height: 50,
                                    decoration: const BoxDecoration(
                                      color: Color(0xFF10B981),
                                      shape: BoxShape.circle,
                                      boxShadow: [
                                        BoxShadow(color: Color(0xFF10B981), blurRadius: 20, spreadRadius: 5)
                                      ],
                                    ),
                                    child: const Icon(Icons.check, color: Colors.white, size: 30),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : Container(
                            width: 100,
                            height: 100,
                            decoration: BoxDecoration(
                              color: Colors.red.withValues(alpha: 0.1),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.error_outline, color: Colors.red, size: 50),
                          ),
              ),
            ),
          ),
          
          // Bottom Card Area (Lower half)
          Expanded(
            flex: 2,
            child: Container(
              width: double.infinity,
              padding: const EdgeInsets.all(32),
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(topLeft: Radius.circular(32), topRight: Radius.circular(32)),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  if (!_isLoading) ...[
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: _isSuccess ? const Color(0xFFE6F7F1) : Colors.red.shade50,
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            _isSuccess ? Icons.check_circle : Icons.error, 
                            color: _isSuccess ? const Color(0xFF10B981) : Colors.red, 
                            size: 16
                          ),
                          const SizedBox(width: 6),
                          Text(
                            _isSuccess ? 'Location & Token Verified' : 'Verification Failed',
                            style: TextStyle(
                              color: _isSuccess ? const Color(0xFF059669) : Colors.red.shade700,
                              fontWeight: FontWeight.bold,
                              fontSize: 12,
                            ),
                          )
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      _message,
                      style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF0F172A)),
                      textAlign: TextAlign.center,
                    ),
                    if (_anomalyMsg.isNotEmpty) ...[
                      const SizedBox(height: 16),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFEF3C7),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          _anomalyMsg,
                          style: const TextStyle(color: Color(0xFFD97706), fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                    const Spacer(),
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.pushAndRemoveUntil(
                            context,
                            MaterialPageRoute(builder: (context) => const MainLayout()),
                            (route) => false,
                          );
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF0F172A),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        child: const Text('Done', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                      ),
                    ),
                  ] else ...[
                    const CircularProgressIndicator(color: Color(0xFF0F172A)),
                    const SizedBox(height: 16),
                    Text(_message, style: const TextStyle(color: Colors.grey)),
                  ]
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
