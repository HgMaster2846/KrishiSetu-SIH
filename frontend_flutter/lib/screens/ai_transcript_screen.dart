import 'package:flutter/material.dart';

class AITranscriptScreen extends StatelessWidget {
  const AITranscriptScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Speech-to-Text Transcript')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text('Extracted Structured Entities (USP 2):', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: const [
              Chip(label: Text('Crop: Tomato'), backgroundColor: Color(0xFFE8F5E9)),
              Chip(label: Text('Quantity: 200 kg'), backgroundColor: Color(0xFFE8F5E9)),
              Chip(label: Text('Expected: ?25/kg'), backgroundColor: Color(0xFFE8F5E9)),
              Chip(label: Text('Location: Murthal, Sonipat'), backgroundColor: Color(0xFFE8F5E9)),
              Chip(label: Text('Mandi Avg: ?25.80/kg'), backgroundColor: Color(0xFFFFF3E0)),
            ],
          ),
          const SizedBox(height: 20),
          const Card(
            child: Padding(
              padding: EdgeInsets.all(16.0),
              child: Text(
                'Full Audio Conversation:\n\nAI: Namaste! KrishiSetu AI mein aapka swagat hai. Aap konsi fasal bechna chahte hain?\n\nFarmer: Mere paas 200 kilo tamatar hai.\n\nAI: Aap kis gaon se bol rahe hain?\n\nFarmer: Murthal, Sonipat.\n\nAI: Aapko kitna daam chahiye?\n\nFarmer: 25 rupaye kilo.',
                style: TextStyle(height: 1.6),
              ),
            ),
          )
        ],
      ),
    );
  }
}
