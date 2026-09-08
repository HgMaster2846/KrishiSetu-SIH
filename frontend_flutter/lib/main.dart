import 'package:flutter/material.dart';
import 'core/theme/app_theme.dart';
import 'screens/splash_screen.dart';
import 'screens/hotline_landing_screen.dart';
import 'screens/live_call_screen.dart';
import 'screens/ai_transcript_screen.dart';
import 'screens/listing_created_screen.dart';
import 'screens/buyer_dashboard_screen.dart';
import 'screens/buyer_recommendation_screen.dart';
import 'screens/negotiation_screen.dart';
import 'screens/mandi_prices_screen.dart';
import 'screens/logistics_screen.dart';
import 'screens/sms_confirmation_screen.dart';
import 'screens/otp_verification_screen.dart';
import 'screens/transaction_success_screen.dart';
import 'screens/admin_dashboard_screen.dart';
import 'screens/buyer_profile_screen.dart';
import 'screens/farmer_profile_screen.dart';
import 'screens/analytics_dashboard_screen.dart';
import 'screens/setup_dashboard_screen.dart';
import 'screens/live_hotline_monitor_screen.dart';

void main() {
  runApp(const KrishiSetuApp());
}

class KrishiSetuApp extends StatelessWidget {
  const KrishiSetuApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'KrishiSetu AI',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      initialRoute: '/',
      routes: {
        '/': (context) => const SplashScreen(),
        '/hotline': (context) => const HotlineLandingScreen(),
        '/live_call': (context) => const LiveCallScreen(),
        '/ai_transcript': (context) => const AITranscriptScreen(),
        '/listing_created': (context) => const ListingCreatedScreen(),
        '/buyer_dashboard': (context) => const BuyerDashboardScreen(),
        '/buyer_recommendation': (context) => const BuyerRecommendationScreen(),
        '/negotiation': (context) => const NegotiationScreen(),
        '/mandi_prices': (context) => const MandiPricesScreen(),
        '/logistics': (context) => const LogisticsScreen(),
        '/sms_confirmation': (context) => const SmsConfirmationScreen(),
        '/otp_verification': (context) => const OtpVerificationScreen(),
        '/transaction_success': (context) => const TransactionSuccessScreen(),
        '/admin_dashboard': (context) => const AdminDashboardScreen(),
        '/buyer_profile': (context) => const BuyerProfileScreen(),
        '/farmer_profile': (context) => const FarmerProfileScreen(),
        '/analytics': (context) => const AnalyticsDashboardScreen(),
        '/setup': (context) => const SetupDashboardScreen(),
        '/hotline_monitor': (context) => const LiveHotlineMonitorScreen(),
      },
    );
  }
}

