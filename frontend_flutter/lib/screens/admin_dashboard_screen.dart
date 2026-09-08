import 'package:flutter/material.dart';

class AdminDashboardScreen extends StatelessWidget {
  const AdminDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Admin & Fraud Dashboard')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            children: const [
              Expanded(child: Card(child: Padding(padding: EdgeInsets.all(16), child: Column(children: [Text('20', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)), Text('Farmers')])))),
              Expanded(child: Card(child: Padding(padding: EdgeInsets.all(16), child: Column(children: [Text('20', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)), Text('Buyers')])))),
              Expanded(child: Card(child: Padding(padding: EdgeInsets.all(16), child: Column(children: [Text('40', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)), Text('Listings')])))),
            ],
          ),
          const SizedBox(height: 16),
          const Text('Fraud Alerts (USP 7):', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          const Card(
            color: Color(0xFFFFEBEE),
            child: ListTile(
              leading: Icon(Icons.warning, color: Colors.red),
              title: Text('QuickDeal Wholesale (Unverified)', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Bid ?15/kg for Tomato (42% below Mandi benchmark). Locked by AI.'),
            ),
          ),
        ],
      ),
    );
  }
}
