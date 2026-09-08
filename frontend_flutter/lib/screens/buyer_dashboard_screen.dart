import 'package:flutter/material.dart';

class BuyerDashboardScreen extends StatelessWidget {
  const BuyerDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Buyer Marketplace'),
        actions: [
          IconButton(icon: const Icon(Icons.trending_up), onPressed: () => Navigator.pushNamed(context, '/mandi_prices')),
          IconButton(icon: const Icon(Icons.local_shipping), onPressed: () => Navigator.pushNamed(context, '/logistics')),
          IconButton(icon: const Icon(Icons.admin_panel_settings), onPressed: () => Navigator.pushNamed(context, '/admin_dashboard')),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: const Color(0xFFE8F5E9),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: const [
                  Icon(Icons.verified_user, color: Color(0xFF2E7D32), size: 36),
                  SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('FreshMart Agro Hub (Buyer)', style: TextStyle(fontWeight: FontWeight.bold)),
                        Text('Trust Score: 96/100 ? Escrow T+0 Verified', style: TextStyle(fontSize: 12, color: Colors.black54)),
                      ],
                    ),
                  )
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          const Text('Live Farmer Listings (Direct from Feature Phones):', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 10),
          Card(
            child: ListTile(
              leading: const CircleAvatar(backgroundColor: Color(0xFFFFEBEE), child: Text('??', style: TextStyle(fontSize: 20))),
              title: const Text('Tomato (Tamatar) ? 200 kg', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: const Text('Rameshwar Singh ? Murthal, Sonipat'),
              trailing: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: const [
                  Text('?25.00/kg', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32))),
                  Text('Active', style: TextStyle(fontSize: 10, color: Colors.green)),
                ],
              ),
              onTap: () => Navigator.pushNamed(context, '/buyer_recommendation'),
            ),
          ),
          Card(
            child: ListTile(
              leading: const CircleAvatar(backgroundColor: Color(0xFFFFF8E1), child: Text('??', style: TextStyle(fontSize: 20))),
              title: const Text('Onion (Pyaz) ? 500 kg', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: const Text('Baldev Preet Singh ? Samalkha, Panipat'),
              trailing: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: const [
                  Text('?32.00/kg', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32))),
                  Text('Active', style: TextStyle(fontSize: 10, color: Colors.green)),
                ],
              ),
            ),
          ),
          Card(
            child: ListTile(
              leading: const CircleAvatar(backgroundColor: Color(0xFFEDE7F6), child: Text('??', style: TextStyle(fontSize: 20))),
              title: const Text('Basmati Rice 1121 ? 2500 kg', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: const Text('Gurnam Singh Gill ? Sirhind, Fatehgarh'),
              trailing: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: const [
                  Text('?74.00/kg', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32))),
                  Text('Active', style: TextStyle(fontSize: 10, color: Colors.green)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
