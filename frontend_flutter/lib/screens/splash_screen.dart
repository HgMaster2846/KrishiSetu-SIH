import 'package:flutter/material.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF2E7D32),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.agriculture_rounded, size: 80, color: Colors.white),
            const SizedBox(height: 16),
            const Text(
              'KrishiSetu AI',
              style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 1),
            ),
            const Text(
              'Feature Phone First Farmer Marketplace',
              style: TextStyle(fontSize: 14, color: Color(0xFFC8E6C9)),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(20)),
              child: const Text('Smart India Hackathon 2026 ? Problem SIH 26033', style: TextStyle(fontSize: 12, color: Colors.white)),
            ),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              onPressed: () => Navigator.pushNamed(context, '/hotline'),
              icon: const Icon(Icons.phone_in_talk),
              label: const Text('Enter Platform & AI Hotline'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.white, foregroundColor: const Color(0xFF2E7D32)),
            )
          ],
        ),
      ),
    );
  }
}
