import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import 'auth_service.dart';

class ApiService {
  static const String _configuredBaseUrl = String.fromEnvironment('API_BASE_URL');

  static String get baseUrl {
    if (_configuredBaseUrl.isNotEmpty) {
      return _configuredBaseUrl.replaceFirst(RegExp(r'/$'), '');
    }
    if (kReleaseMode) return 'https://nurux.duckdns.org/api';
    if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8000/api';
    }
    return 'http://localhost:8000/api';
  }

  final AuthService _authService = AuthService();

  Map<String, dynamic> _decodeObject(http.Response response) {
    final decoded = jsonDecode(response.body);
    return Map<String, dynamic>.from(decoded as Map);
  }

  String _errorMessage(http.Response response, String fallback) {
    try {
      final decoded = jsonDecode(response.body);
      if (decoded is Map) {
        final detail = decoded['detail'] ?? decoded['error'];
        if (detail != null) return detail.toString();
        return decoded.values.first.toString();
      }
    } catch (_) {}
    return fallback;
  }

  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/accounts/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );
    if (response.statusCode != 200) {
      throw Exception(_errorMessage(response, 'Unable to sign in.'));
    }

    final data = _decodeObject(response);
    final user = Map<String, dynamic>.from(data['user'] as Map);
    final fullName = '${user['first_name'] ?? ''} ${user['last_name'] ?? ''}'.trim();
    await _authService.saveAuthData(
      data['access'] as String,
      data['refresh'] as String,
      fullName.isNotEmpty ? fullName : (user['username'] ?? username).toString(),
      (user['role'] ?? 'employee').toString(),
    );
    return data;
  }

  Future<bool> _refreshSession() async {
    final refreshToken = await _authService.getRefreshToken();
    if (refreshToken == null) return false;
    final response = await http.post(
      Uri.parse('$baseUrl/accounts/refresh/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh': refreshToken}),
    );
    if (response.statusCode != 200) {
      await _authService.clearAuthData();
      return false;
    }
    final data = _decodeObject(response);
    await _authService.updateTokens(
      data['access'] as String,
      (data['refresh'] ?? refreshToken) as String,
    );
    return true;
  }

  Future<http.Response> _sendAuthenticated(
    String method,
    String path, {
    Map<String, dynamic>? body,
  }) async {
    Future<http.Response> send() async {
      final token = await _authService.getToken();
      if (token == null) throw Exception('Your session has expired. Please sign in again.');
      final uri = Uri.parse('$baseUrl$path');
      final headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      };
      if (method == 'GET') return http.get(uri, headers: headers);
      if (method == 'POST') {
        return http.post(uri, headers: headers, body: body == null ? null : jsonEncode(body));
      }
      throw UnsupportedError('Unsupported HTTP method: $method');
    }

    var response = await send();
    if (response.statusCode == 401 && await _refreshSession()) response = await send();
    if (response.statusCode == 401) {
      await _authService.clearAuthData();
      throw Exception('Your session has expired. Please sign in again.');
    }
    return response;
  }

  Future<void> logout() async {
    final refreshToken = await _authService.getRefreshToken();
    if (refreshToken != null) {
      try {
        await _sendAuthenticated('POST', '/accounts/logout/', body: {'refresh': refreshToken});
      } catch (_) {}
    }
    await _authService.clearAuthData();
  }

  Future<Map<String, dynamic>> clockIn(String gpsLocation, String qrToken) async {
    final response = await _sendAuthenticated(
      'POST',
      '/attendance/attendance/clock_in/',
      body: {'gps_location': gpsLocation, 'qr_token': qrToken},
    );
    if (response.statusCode == 200 || response.statusCode == 201) return _decodeObject(response);
    throw Exception(_errorMessage(response, 'Failed to clock in.'));
  }

  Future<Map<String, dynamic>> clockOut(String gpsLocation, String qrToken) async {
    final response = await _sendAuthenticated(
      'POST',
      '/attendance/attendance/clock_out/',
      body: {'gps_location': gpsLocation, 'qr_token': qrToken},
    );
    if (response.statusCode == 200) return _decodeObject(response);
    throw Exception(_errorMessage(response, 'Failed to clock out.'));
  }

  Future<Map<String, dynamic>> getTodayAttendanceStatus() async {
    final response = await _sendAuthenticated('GET', '/attendance/attendance/today/');
    if (response.statusCode == 200) return _decodeObject(response);
    throw Exception(_errorMessage(response, 'Failed to fetch today\'s attendance.'));
  }

  Future<Map<String, dynamic>> getLatestVersion() async {
    final response = await http.get(Uri.parse('$baseUrl/system/latest-version/'));
    if (response.statusCode == 200) return _decodeObject(response);
    if (response.statusCode == 404) return {};
    throw Exception('Failed to check app version.');
  }

  Future<List<dynamic>> _getList(String path, String fallback) async {
    final response = await _sendAuthenticated('GET', path);
    if (response.statusCode != 200) throw Exception(_errorMessage(response, fallback));
    final data = jsonDecode(response.body);
    if (data is Map && data.containsKey('results')) return data['results'] as List<dynamic>;
    return data as List<dynamic>;
  }

  Future<List<dynamic>> getAttendanceHistory() =>
      _getList('/attendance/attendance/', 'Failed to fetch attendance history.');

  Future<List<dynamic>> getLeaveBalances() =>
      _getList('/leave/leave-balances/', 'Failed to fetch leave balances.');

  Future<List<dynamic>> getLeaveRequests() =>
      _getList('/leave/leave-requests/', 'Failed to fetch leave requests.');

  Future<Map<String, dynamic>> submitLeaveRequest({
    required String leaveType,
    required String startDate,
    required String endDate,
    required String reason,
  }) async {
    final response = await _sendAuthenticated(
      'POST',
      '/leave/leave-requests/',
      body: {
        'leave_type': leaveType,
        'start_date': startDate,
        'end_date': endDate,
        'reason': reason,
      },
    );
    if (response.statusCode == 201) return _decodeObject(response);
    throw Exception(_errorMessage(response, 'Failed to submit leave request.'));
  }
}
