import 'package:flutter/material.dart';

class AnalyticsDashboardScreen extends StatelessWidget {
  const AnalyticsDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Platform Analytics & ESG Savings')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Card(
            child: ListTile(
              title: Text('Total Logistics Cost Saved', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Across 15 pooled routes in North India'),
              trailing: Text('?3,18,500', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF2E7D32))),
            ),
          ),
          Card(
            child: ListTile(
              title: Text('Carbon Emission Reduction', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('By eliminating empty return truck runs'),
              trailing: Text('4.2 MT CO?', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Colors.green)),
            ),
          ),
        ],
      ),
    );
  }
}
