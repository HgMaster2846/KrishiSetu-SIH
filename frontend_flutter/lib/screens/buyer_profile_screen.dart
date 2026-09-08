import 'package:flutter/material.dart';

class BuyerProfileScreen extends StatelessWidget {
  const BuyerProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Buyer Profile')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          ListTile(leading: Icon(Icons.business), title: Text('Company: FreshMart Retail Pvt Ltd')),
          ListTile(leading: Icon(Icons.verified), title: Text('Trust Score: 96/100 (Verified APMC/GSTIN)')),
          ListTile(leading: Icon(Icons.history), title: Text('Completed Deals: 342')),
        ],
      ),
    );
  }
}
