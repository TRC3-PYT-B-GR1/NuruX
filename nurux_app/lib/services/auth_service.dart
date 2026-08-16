import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  static const String _accessTokenKey = 'auth_access_token';
  static const String _refreshTokenKey = 'auth_refresh_token';
  static const String _legacyTokenKey = 'auth_token';
  static const String _employeeNameKey = 'employee_name';
  static const String _employeeRoleKey = 'employee_role';

  Future<void> saveAuthData(
    String accessToken,
    String refreshToken,
    String name,
    String role,
  ) async {
    final prefs = await SharedPreferences.getInstance();
    await Future.wait([
      prefs.setString(_accessTokenKey, accessToken),
      prefs.setString(_refreshTokenKey, refreshToken),
      prefs.setString(_employeeNameKey, name),
      prefs.setString(_employeeRoleKey, role),
      prefs.remove(_legacyTokenKey),
    ]);
  }

  Future<void> updateTokens(String accessToken, String refreshToken) async {
    final prefs = await SharedPreferences.getInstance();
    await Future.wait([
      prefs.setString(_accessTokenKey, accessToken),
      prefs.setString(_refreshTokenKey, refreshToken),
    ]);
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_accessTokenKey) ?? prefs.getString(_legacyTokenKey);
  }

  Future<String?> getRefreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_refreshTokenKey);
  }

  Future<String?> getEmployeeName() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_employeeNameKey);
  }

  Future<String?> getEmployeeRole() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_employeeRoleKey);
  }

  Future<void> clearAuthData() async {
    final prefs = await SharedPreferences.getInstance();
    await Future.wait([
      prefs.remove(_accessTokenKey),
      prefs.remove(_refreshTokenKey),
      prefs.remove(_legacyTokenKey),
      prefs.remove(_employeeNameKey),
      prefs.remove(_employeeRoleKey),
    ]);
  }

  bool _isUsableJwt(String? token) {
    if (token == null || token.isEmpty) return false;
    try {
      final segments = token.split('.');
      if (segments.length != 3) return false;
      final payload = jsonDecode(
        utf8.decode(base64Url.decode(base64Url.normalize(segments[1]))),
      ) as Map<String, dynamic>;
      final expiresAt = payload['exp'] as int?;
      if (expiresAt == null) return false;
      return DateTime.now().millisecondsSinceEpoch < expiresAt * 1000;
    } catch (_) {
      return false;
    }
  }

  Future<bool> isLoggedIn() async {
    final accessToken = await getToken();
    if (_isUsableJwt(accessToken)) return true;
    return _isUsableJwt(await getRefreshToken());
  }
}
