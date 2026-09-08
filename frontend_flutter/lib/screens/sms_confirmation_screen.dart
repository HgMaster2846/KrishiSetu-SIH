import 'package:flutter/material.dart';

class SmsConfirmationScreen extends StatelessWidget {
  const SmsConfirmationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(title: const Text('Feature Phone SMS Simulator (USP 6)'), backgroundColor: const Color(0xFF1E293B)),
      body: Center(
        child: Container(
          width: 320,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(color: const Color(0xFF022C22), border: Border.all(color: const Color(0xFF4ADE80)), borderRadius: BorderRadius.circular(16)),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [
              Text('SMS INBOX ? Sender: KR-SETU', style: TextStyle(color: Color(0xFF4ADE80), fontWeight: FontWeight.bold, fontSize: 12)),
              Divider(color: Color(0xFF166534)),
              SizedBox(height: 8),
              Text(
                'KrishiSetu AI\n\nTomato ? 200kg\nBuyer: FreshMart\nPrice: ?25.5/kg\nPickup: Tomorrow 8 AM\nTruck: HR-10-AJ-4821\n\nReply YES or Press 1.',
                style: TextStyle(color: Colors.white, fontFamily: 'monospace', height: 1.4),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
