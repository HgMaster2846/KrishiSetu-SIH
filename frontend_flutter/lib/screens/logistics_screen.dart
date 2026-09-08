import 'package:flutter/material.dart';

class LogisticsScreen extends StatelessWidget {
  const LogisticsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pooled Logistics AI (USP 5)')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: const Color(0xFFE8F5E9),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: const BorderSide(color: Color(0xFF2E7D32))),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text('Shared Transport Savings Analysis (Murthal -> Azadpur)', style: TextStyle(fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  Text('Original Solo Transport Cost: ?1,200', style: TextStyle(decoration: TextDecoration.lineThrough, color: Colors.grey)),
                  Text('Shared Truck Cost: ?450 (?2.25/kg)', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32), fontSize: 18)),
                  Text('Farmer Savings: ?750 (62.5% Cost Reduction)', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.green)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: ListTile(
              leading: const Icon(Icons.local_shipping, size: 36, color: Colors.blue),
              title: const Text('Truck HR-10-AJ-4821 (Tata 407)', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: const Text('Driver: Gurpreet Singh (+919711001001)\nRoute: Ambala -> Murthal -> Azadpur Mandi'),
              trailing: ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/transaction_success'),
                child: const Text('Assign'),
              ),
            ),
          )
        ],
      ),
    );
  }
}
