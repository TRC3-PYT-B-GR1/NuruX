import 'package:flutter/material.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:url_launcher/url_launcher.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import 'login_screen.dart';
import 'main_layout.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  final AuthService _authService = AuthService();
  final ApiService _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    _checkAppUpdateAndLogin();
  }

  Future<void> _checkAppUpdateAndLogin() async {
    // Artificial delay for splash screen branding
    await Future.delayed(const Duration(seconds: 2));

    if (!mounted) return;

    try {
      final latestVersionData = await _apiService.getLatestVersion();
      if (latestVersionData.isNotEmpty && latestVersionData.containsKey('version_code')) {
        final packageInfo = await PackageInfo.fromPlatform();
        final currentVersionCode = int.tryParse(packageInfo.buildNumber) ?? 0;
        final serverVersionCode = latestVersionData['version_code'] as int;

        if (serverVersionCode > currentVersionCode) {
          // Show update dialog
          await _showUpdateDialog(latestVersionData);
          return; // Stop flow here if update dialog is shown
        }
      }
    } catch (e) {
      debugPrint("Failed to check app version: $e");
    }

    // Proceed to login check
    _proceedToApp();
  }

  Future<void> _showUpdateDialog(Map<String, dynamic> data) async {
    final isMandatory = data['is_mandatory'] ?? false;
    final apkUrl = data['apk_url'] ?? data['download_url'] ?? data['apk_file'];

    return showDialog(
      context: context,
      barrierDismissible: !isMandatory,
      builder: (context) {
        return PopScope(
          canPop: !isMandatory,
          child: AlertDialog(
            title: const Text('Update Available'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Version ${data['version_name']} is available.'),
                if (data['release_notes'] != null && data['release_notes'].isNotEmpty) ...[
                  const SizedBox(height: 8),
                  const Text('Release Notes:', style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(data['release_notes']),
                ]
              ],
            ),
            actions: [
              if (!isMandatory)
                TextButton(
                  onPressed: () {
                    Navigator.pop(context);
                    _proceedToApp();
                  },
                  child: const Text('Later'),
                ),
              ElevatedButton(
                onPressed: () async {
                  if (apkUrl != null) {
                    final fullUrl = apkUrl.startsWith('http') ? apkUrl : '${ApiService.baseUrl.replaceAll('/api', '')}$apkUrl';
                    final uri = Uri.parse(fullUrl);
                    try {
                      await launchUrl(uri, mode: LaunchMode.externalApplication);
                    } catch (e) {
                      debugPrint('Could not launch update URL: $e');
                    }
                  }
                  if (!isMandatory && context.mounted) {
                    Navigator.pop(context);
                    _proceedToApp();
                  }
                },
                child: const Text('Update Now'),
              ),
            ],
          ),
        );
      },
    );
  }

  Future<void> _proceedToApp() async {
    final isLoggedIn = await _authService.isLoggedIn();
    if (!mounted) return;

    if (isLoggedIn) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const MainLayout()),
      );
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A), // Slate 900
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Using a simple icon for the NuruX logo for now
            const Icon(
              Icons.wb_sunny_rounded, // Matches the sun-like logo in the design
              color: Color(0xFFF59E0B), // Amber 500
              size: 80,
            ),
            const SizedBox(height: 40),
            const Text(
              'NuruX',
              style: TextStyle(
                color: Colors.white,
                fontSize: 32,
                fontWeight: FontWeight.bold,
                letterSpacing: 1.2,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Next generation intelligent workforce',
              style: TextStyle(
                color: Colors.white.withValues(alpha: 0.6),
                fontSize: 14,
              ),
            ),
            const SizedBox(height: 60),
            const CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Color(0xFFF59E0B)),
            ),
          ],
        ),
      ),
    );
  }
}
