import 'package:flutter/material.dart';

class TransactionSuccessScreen extends StatelessWidget {
  const TransactionSuccessScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Deal Completed Receipt')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            const Icon(Icons.check_circle_outline, size: 80, color: Color(0xFF2E7D32)),
            const SizedBox(height: 16),
            const Text('Trade Successfully Completed!', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const Text('Digital Mandi Escrow Disbursed', style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 24),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: const [
                    ListTile(title: Text('Farmer Name'), trailing: Text('Rameshwar Singh')),
                    ListTile(title: Text('Buyer Name'), trailing: Text('FreshMart Agro Hub')),
                    ListTile(title: Text('Net Payment Released'), trailing: Text('?5,100.00', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32), fontSize: 16))),
                    ListTile(title: Text('Logistics Transport Saved'), trailing: Text('?750.00 (Pooled)', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.green))),
                  ],
                ),
              ),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/admin_dashboard'),
                child: const Text('View Platform Admin Portal'),
              ),
            )
          ],
        ),
      ),
    );
  }
}
