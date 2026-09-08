import 'package:flutter/material.dart';

class BuyerRecommendationScreen extends StatelessWidget {
  const BuyerRecommendationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Buyer Recommendations (USP 3)')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(color: const Color(0xFFE8F5E9), borderRadius: BorderRadius.circular(12)),
            child: const Text(
              'Formula: Mandi 35% + Distance 20% + Demand 20% + Trust 15% + Transport 10%',
              style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Color(0xFF2E7D32)),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: const BorderSide(color: Color(0xFF2E7D32), width: 2)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.between,
                    children: const [
                      Text('Rank #1: FreshMart Agro Hub', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                      Chip(label: Text('96% Match'), backgroundColor: Color(0xFFC8E6C9)),
                    ],
                  ),
                  const Text('Buying Price: ?26.50/kg ? Distance: 42 km ? Pooled Transport: ?1.85/kg'),
                  const SizedBox(height: 8),
                  const Text('Net Farmer Profit: ?24.65/kg (Total ?4,930)', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32))),
                  const SizedBox(height: 12),
                  ElevatedButton(
                    onPressed: () => Navigator.pushNamed(context, '/negotiation'),
                    child: const Text('Initiate AI Negotiation'),
                  )
                ],
              ),
            ),
          ),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text('Rank #2: BigBasket Procurement (92% Match)', style: TextStyle(fontWeight: FontWeight.bold)),
                  Text('Buying Price: ?26.20/kg ? Distance: 15 km ? Trust: 98%'),
                ],
              ),
            ),
          ),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text('Rank #3: Azadpur Mandi Traders (88% Match)', style: TextStyle(fontWeight: FontWeight.bold)),
                  Text('Buying Price: ?25.80/kg ? Distance: 38 km ? Trust: 94%'),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
