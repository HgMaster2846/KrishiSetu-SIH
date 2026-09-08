import 'package:flutter/material.dart';

class OtpVerificationScreen extends StatelessWidget {
  const OtpVerificationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pickup OTP Verification')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            const Icon(Icons.pin, size: 64, color: Color(0xFF2E7D32)),
            const SizedBox(height: 12),
            const Text('Feature Phone DTMF / SMS OTP', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            const Text('Enter 6-digit handover OTP from farmer SMS to release Escrow payment:'),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(color: const Color(0xFFE8F5E9), borderRadius: BorderRadius.circular(12)),
              child: const Text('5 8 2 9 1 4', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, letterSpacing: 8, color: Color(0xFF2E7D32))),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/transaction_success'),
                child: const Text('Verify Produce Handover'),
              ),
            )
          ],
        ),
      ),
    );
  }
}
