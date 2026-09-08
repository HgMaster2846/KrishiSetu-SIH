import 'package:flutter/material.dart';

class NegotiationScreen extends StatefulWidget {
  const NegotiationScreen({super.key});

  @override
  State<NegotiationScreen> createState() => _NegotiationScreenState();
}

class _NegotiationScreenState extends State<NegotiationScreen> {
  double currentOffer = 24.0;
  String aiStatus = "AI Counter: ?25.80/kg (Mandi Average: ?25.80/kg)";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Autonomous Negotiation (USP 4)')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Card(
              color: const Color(0xFFFFF8E1),
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: const [
                    Text('Farmer Min Price: ?23.50/kg', style: TextStyle(fontWeight: FontWeight.bold)),
                    Text('Mandi Avg: ?25.80/kg', style: TextStyle(color: Colors.blue, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: ListView(
                children: [
                  const Align(
                    alignment: Alignment.centerLeft,
                    child: Card(color: Color(0xFFF1F5F9), child: Padding(padding: EdgeInsets.all(12), child: Text('Buyer FreshMart: We offer ?24.00/kg.'))),
                  ),
                  const Align(
                    alignment: Alignment.centerRight,
                    child: Card(color: Color(0xFFE8F5E9), child: Padding(padding: EdgeInsets.all(12), child: Text('KrishiSetu AI: APMC modal rate is ?25.80/kg. We counter at ?25.80/kg.'))),
                  ),
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Card(color: const Color(0xFFF1F5F9), child: Padding(padding: const EdgeInsets.all(12), child: Text('Buyer FreshMart: Counter offer ?$currentOffer/kg.'))),
                  ),
                ],
              ),
            ),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: () {
                      setState(() {
                        currentOffer = 25.50;
                      });
                      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('AI: Current mandi avg is ?25.80. ?25.50/kg is accepted! SMS sent to farmer.')));
                    },
                    style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF2E7D32)),
                    child: const Text('Lock Deal @ ?25.50/kg'),
                  ),
                ),
                const SizedBox(width: 8),
                OutlinedButton(
                  onPressed: () => Navigator.pushNamed(context, '/logistics'),
                  child: const Text('Go to Logistics'),
                )
              ],
            )
          ],
        ),
      ),
    );
  }
}
