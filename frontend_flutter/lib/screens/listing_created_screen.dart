import 'package:flutter/material.dart';

class ListingCreatedScreen extends StatelessWidget {
  const ListingCreatedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Listing Created Instantly')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            const Icon(Icons.check_circle, size: 72, color: Color(0xFF2E7D32)),
            const SizedBox(height: 12),
            const Text('Listing Active on Marketplace!', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const Text('Listing ID: LIST-001 ? Created via AI Voice Hotline', style: TextStyle(color: Colors.grey, fontSize: 12)),
            const SizedBox(height: 24),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: const [
                    ListTile(title: Text('Crop & Quantity'), trailing: Text('Tomato ? 200 kg', style: TextStyle(fontWeight: FontWeight.bold))),
                    Divider(),
                    ListTile(title: Text('Farmer Expected Price'), trailing: Text('?25.00 / kg', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32)))),
                    Divider(),
                    ListTile(title: Text('APMC Mandi Benchmark'), trailing: Text('?25.80 / kg', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.blue))),
                    Divider(),
                    ListTile(title: Text('Location'), trailing: Text('Murthal, Sonipat (Haryana)')),
                  ],
                ),
              ),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/buyer_recommendation'),
                child: const Text('View AI Recommended Buyers (Top 3)'),
              ),
            ),
            const SizedBox(height: 10),
            TextButton(
              onPressed: () => Navigator.pushNamed(context, '/sms_confirmation'),
              child: const Text('Simulate Farmer SMS View'),
            ),
          ],
        ),
      ),
    );
  }
}
