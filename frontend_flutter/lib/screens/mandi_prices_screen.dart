import 'package:flutter/material.dart';

class MandiPricesScreen extends StatelessWidget {
  const MandiPricesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Live APMC Mandi Intelligence')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Card(
            child: ListTile(
              title: Text('Tomato (Azadpur Mandi, Delhi)', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Arrivals: 420 Tonnes ? High Demand'),
              trailing: Text('?28.50 / kg', style: TextStyle(color: Color(0xFF2E7D32), fontWeight: FontWeight.bold, fontSize: 16)),
            ),
          ),
          Card(
            child: ListTile(
              title: Text('Onion (Okhla Mandi, Delhi)', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Arrivals: 580 Tonnes ? Stable'),
              trailing: Text('?35.50 / kg', style: TextStyle(color: Color(0xFF2E7D32), fontWeight: FontWeight.bold, fontSize: 16)),
            ),
          ),
          Card(
            child: ListTile(
              title: Text('Basmati Rice 1121 (Karnal Terminal)', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Arrivals: 850 Tonnes ? Bullish'),
              trailing: Text('?76.00 / kg', style: TextStyle(color: Color(0xFF2E7D32), fontWeight: FontWeight.bold, fontSize: 16)),
            ),
          ),
          Card(
            child: ListTile(
              title: Text('Mustard / Sarson (Alwar Krishi Mandi)', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Arrivals: 620 Tonnes ? Peak Rate'),
              trailing: Text('?61.50 / kg', style: TextStyle(color: Color(0xFF2E7D32), fontWeight: FontWeight.bold, fontSize: 16)),
            ),
          ),
        ],
      ),
    );
  }
}
