import 'package:flutter/material.dart';

class LiveCallScreen extends StatefulWidget {
  const LiveCallScreen({super.key});

  @override
  State<LiveCallScreen> createState() => _LiveCallScreenState();
}

class _LiveCallScreenState extends State<LiveCallScreen> {
  int step = 0;
  final List<Map<String, dynamic>> dialogue = [
    {
      "ai": "Namaste! KrishiSetu AI mein aapka swagat hai. Aap konsi fasal bechna chahte hain aur kitni maatra hai?",
      "farmer": "Mere paas 200 kilo tamatar hai."
    },
    {
      "ai": "Maine darj kar liya hai: 200 kilo Tamatar. Aap kis gaon aur zile se bol rahe hain?",
      "farmer": "Murthal, Sonipat."
    },
    {
      "ai": "Murthal, Sonipat se. Bahut achha. Aapko kitna daam chahiye prati kilo?",
      "farmer": "25 rupaye kilo."
    },
    {
      "ai": "Bahut badhiya! 200 kilo Tamatar, Murthal (Sonipat) se, ?25/kg par darj ho gaya hai. Mandi rate ?25.80/kg hai. SMS bhej diya gaya hai.",
      "farmer": "Dhanyawad!"
    }
  ];

  @override
  Widget build(BuildContext context) {
    final current = dialogue[step];
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text('Live Voice Call ? 1800-260-3300'),
        backgroundColor: const Color(0xFF1E293B),
        foregroundColor: Colors.white,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              const Text('Call Connected (Bhashini Hindi AI)', style: TextStyle(color: Color(0xFF4ADE80), fontSize: 12)),
              const SizedBox(height: 10),
              const Text('00:24', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
              const Spacer(),
              // Waveform representation
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(7, (i) => Container(
                  margin: const EdgeInsets.symmetric(horizontal: 4),
                  width: 6,
                  height: 20.0 + (i % 3) * 15,
                  decoration: BoxDecoration(color: const Color(0xFF4ADE80), borderRadius: BorderRadius.circular(4)),
                )),
              ),
              const SizedBox(height: 30),
              // AI Speech Bubble
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: const Color(0xFF1E293B), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFF334155))),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('AI Sahayak (Hotline):', style: TextStyle(color: Color(0xFF4ADE80), fontWeight: FontWeight.bold, fontSize: 12)),
                    const SizedBox(height: 4),
                    Text(current["ai"]!, style: const TextStyle(color: Colors.white, fontSize: 14)),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              // Farmer Response Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    if (step < dialogue.length - 1) {
                      setState(() => step++);
                    } else {
                      Navigator.pushReplacementNamed(context, '/listing_created');
                    }
                  },
                  icon: const Icon(Icons.mic),
                  label: Text('Farmer: "${current["farmer"]}"'),
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF2E7D32), padding: const EdgeInsets.symmetric(vertical: 14)),
                ),
              ),
              const Spacer(),
              IconButton.filled(
                onPressed: () => Navigator.pop(context),
                icon: const Icon(Icons.call_end),
                style: IconButton.styleFrom(backgroundColor: Colors.red, iconSize: 32),
              ),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}
