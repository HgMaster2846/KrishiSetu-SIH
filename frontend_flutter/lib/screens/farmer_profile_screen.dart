import 'package:flutter/material.dart';

class FarmerProfileScreen extends StatelessWidget {
  const FarmerProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Farmer Voice Profile (Read-Only)')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          ListTile(leading: Icon(Icons.person), title: Text('Rameshwar Singh')),
          ListTile(leading: Icon(Icons.phone), title: Text('+919812345001 (Nokia 105 Feature Phone)')),
          ListTile(leading: Icon(Icons.location_on), title: Text('Murthal, Sonipat, Haryana')),
          ListTile(leading: Icon(Icons.eco), title: Text('Land: 3.5 Acres ? Registered via Voice Hotline')),
        ],
      ),
    );
  }
}
