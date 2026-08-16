import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';

void main() {
  runApp(const NuruxApp());
}

class NuruxApp extends StatelessWidget {
  const NuruxApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NuruX',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: const Color(0xFF0F172A),
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0F172A)),
        useMaterial3: true,
        fontFamily: 'Roboto', // Ideally replace with 'Inter' if assets are added
      ),
      home: const SplashScreen(),
    );
  }
}
