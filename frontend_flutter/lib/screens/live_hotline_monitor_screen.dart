import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

class LiveHotlineMonitorScreen extends StatefulWidget {
  const LiveHotlineMonitorScreen({super.key});

  @override
  State<LiveHotlineMonitorScreen> createState() => _LiveHotlineMonitorScreenState();
}

class _LiveHotlineMonitorScreenState extends State<LiveHotlineMonitorScreen> {
  final List<Map<String, String>> _transcripts = [
    {"speaker": "AI Sahayak", "time": "00:02", "text": "Namaste! KrishiSetu AI mein aapka swagat hai. Main aapka Digital Mandi Sahayak hoon. Aap konsi fasal bechna chahte hain aur kitni maatra hai?"},
    {"speaker": "Kisan (Farmer)", "time": "00:08", "text": "Mere paas 200 kilo tamatar hai Murthal Sonipat se aur 25 rupaye kilo chahiye."},
    {"speaker": "AI Sahayak", "time": "00:15", "text": "Bahut badhiya! Aapka 200 kilo Tomato, Murthal (Sonipat) se, ₹25/kg par darj ho gaya hai. Mandi benchmark ₹25.80/kg hai. SMS bhej diya gaya hai."},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Live Hotline Monitor (Admin)"),
        backgroundColor: Colors.slate[900],
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            tooltip: "Hotline Setup",
            onPressed: () => Navigator.pushNamed(context, '/setup'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Status Header
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.slate[900],
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  const Icon(Icons.radio, color: Colors.redAccent, size: 36),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text("Active Inbound Call • 1800-260-3300", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                        SizedBox(height: 2),
                        Text("Caller: +91 98123 45001 (Murthal, Sonipat) • Duration: 01:14s", style: TextStyle(color: Colors.white70, fontSize: 12)),
                      ],
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(color: Colors.greenAccent[700], borderRadius: BorderRadius.circular(12)),
                    child: const Text("LIVE WEBSOCKET", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 10)),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Live Entities Card
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.between,
                      children: const [
                        Text("Extracted Entities (AI NLP)", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        Chip(label: Text("Created via AI Hotline", style: TextStyle(fontSize: 10, color: Colors.purple)), visualDensity: VisualDensity.compact),
                      ],
                    ),
                    const Divider(),
                    _entityRow("Crop:", "Tomato (Tamatar)"),
                    _entityRow("Quantity:", "200 kg"),
                    _entityRow("Location:", "Murthal, Sonipat (Haryana)"),
                    _entityRow("Expected Price:", "₹25.00 / kg"),
                    _entityRow("APMC Mandi Rate:", "₹25.80 / kg (Azadpur Mandi)"),
                    _entityRow("Listing ID:", "LIST-001 (ACTIVE)"),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Live Transcript Feed
            const Text("Live Conversational Transcript", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
            const SizedBox(height: 8),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _transcripts.length,
              itemBuilder: (ctx, i) {
                final item = _transcripts[i];
                final isAI = item["speaker"] == "AI Sahayak";
                return Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: isAI ? Colors.purple[50] : Colors.green[50],
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: isAI ? Colors.purple.shade200 : Colors.green.shade200),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.between,
                        children: [
                          Text(item["speaker"]!, style: TextStyle(fontWeight: FontWeight.bold, color: isAI ? Colors.purple[800] : Colors.green[900], fontSize: 12)),
                          Text(item["time"]!, style: const TextStyle(color: Colors.black45, fontSize: 10)),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(item["text"]!, style: const TextStyle(fontSize: 13)),
                    ],
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _entityRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.between,
        children: [
          Text(label, style: const TextStyle(color: Colors.black54, fontSize: 12)),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
        ],
      ),
    );
  }
}
