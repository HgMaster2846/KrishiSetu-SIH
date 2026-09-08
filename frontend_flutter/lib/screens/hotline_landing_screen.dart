import 'package:flutter/material.dart';

class HotlineLandingScreen extends StatelessWidget {
  const HotlineLandingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('24?7 AI Farmer Hotline')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const SizedBox(height: 20),
            const CircleAvatar(radius: 48, backgroundColor: Color(0xFFE8F5E9), child: Icon(Icons.phone_forwarded, size: 48, color: Color(0xFF2E7D32))),
            const SizedBox(height: 20),
            const Text('Toll-Free AI Hotline Number', style: TextStyle(fontSize: 14, color: Colors.grey)),
            const Text('1800-260-3300', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: Color(0xFF2E7D32))),
            const SizedBox(height: 10),
            const Text('Farmer speaks naturally in Hindi or local language. Pure conversational AI with zero keypad menus needed.', textAlign: TextAlign.center, style: TextStyle(fontSize: 13, color: Colors.black87)),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () => Navigator.pushNamed(context, '/live_call'),
                icon: const Icon(Icons.call),
                label: const Text('Simulate Incoming Farmer Call'),
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF2E7D32), padding: const EdgeInsets.symmetric(vertical: 16)),
              ),
            ),
            const SizedBox(height: 12),
            OutlinedButton(
              onPressed: () => Navigator.pushNamed(context, '/buyer_dashboard'),
              child: const Text('Open Smart Buyer / Admin Dashboard'),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
