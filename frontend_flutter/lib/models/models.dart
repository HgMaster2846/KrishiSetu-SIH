// 1. Listing Model
class Listing {
  final String id;
  final String farmerId;
  final String farmerName;
  final String farmerPhone;
  final String cropName;
  final String category;
  final double quantityKg;
  final double expectedPricePerKg;
  final double farmerMinPrice;
  final double? currentBestOffer;
  final String village;
  final String district;
  final String state;
  final String harvestDate;
  final String status;
  final double aiMandiBenchmark;

  Listing({
    required this.id,
    required this.farmerId,
    required this.farmerName,
    required this.farmerPhone,
    required this.cropName,
    required this.category,
    required this.quantityKg,
    required this.expectedPricePerKg,
    required this.farmerMinPrice,
    this.currentBestOffer,
    required this.village,
    required this.district,
    required this.state,
    required this.harvestDate,
    required this.status,
    required this.aiMandiBenchmark,
  });

  factory Listing.fromJson(Map<String, dynamic> json) {
    return Listing(
      id: json['id'] ?? '',
      farmerId: json['farmer_id'] ?? '',
      farmerName: json['farmer_name'] ?? '',
      farmerPhone: json['farmer_phone'] ?? '',
      cropName: json['crop_name'] ?? '',
      category: json['category'] ?? 'Vegetable',
      quantityKg: (json['quantity_kg'] as num?)?.toDouble() ?? 0.0,
      expectedPricePerKg: (json['expected_price_per_kg'] as num?)?.toDouble() ?? 0.0,
      farmerMinPrice: (json['farmer_min_price'] as num?)?.toDouble() ?? 0.0,
      currentBestOffer: (json['current_best_offer'] as num?)?.toDouble(),
      village: json['village'] ?? '',
      district: json['district'] ?? '',
      state: json['state'] ?? '',
      harvestDate: json['harvest_date'] ?? '',
      status: json['status'] ?? 'ACTIVE',
      aiMandiBenchmark: (json['ai_mandi_benchmark'] as num?)?.toDouble() ?? 0.0,
    );
  }
}

// 2. Buyer Model
class Buyer {
  final String id;
  final String name;
  final String company;
  final String phone;
  final String district;
  final String state;
  final double distanceKm;
  final int trustScore;
  final bool verified;
  final int totalDeals;
  final String paymentTerms;

  Buyer({
    required this.id,
    required this.name,
    required this.company,
    required this.phone,
    required this.district,
    required this.state,
    required this.distanceKm,
    required this.trustScore,
    required this.verified,
    required this.totalDeals,
    required this.paymentTerms,
  });

  factory Buyer.fromJson(Map<String, dynamic> json) {
    return Buyer(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      company: json['company'] ?? '',
      phone: json['phone'] ?? '',
      district: json['district'] ?? '',
      state: json['state'] ?? '',
      distanceKm: (json['distance_km'] as num?)?.toDouble() ?? 50.0,
      trustScore: json['trust_score'] ?? 90,
      verified: json['verified'] ?? true,
      totalDeals: json['total_deals'] ?? 100,
      paymentTerms: json['payment_terms'] ?? 'Instant Escrow',
    );
  }
}

// 3. Negotiation Model
class NegotiationOffer {
  final String sender;
  final double amountPerKg;
  final String message;
  final String timestamp;

  NegotiationOffer({required this.sender, required this.amountPerKg, required this.message, required this.timestamp});
}

class NegotiationSession {
  final String id;
  final String listingId;
  final String buyerId;
  final String buyerName;
  final double farmerMinPrice;
  final double currentBuyerOffer;
  final double? currentAiCounter;
  final String status;
  final String aiReasoning;
  final List<NegotiationOffer> offers;

  NegotiationSession({
    required this.id,
    required this.listingId,
    required this.buyerId,
    required this.buyerName,
    required this.farmerMinPrice,
    required this.currentBuyerOffer,
    this.currentAiCounter,
    required this.status,
    required this.aiReasoning,
    required this.offers,
  });
}

// 4. Truck Route Model
class TruckRoute {
  final String id;
  final String driverName;
  final String driverPhone;
  final String truckNumber;
  final String truckType;
  final String origin;
  final String destination;
  final double totalCapacityKg;
  final double availableCapacityKg;
  final double sharedCostTotal;
  final double soloCostTotal;
  final double farmerSavings;
  final bool isRecommended;

  TruckRoute({
    required this.id,
    required this.driverName,
    required this.driverPhone,
    required this.truckNumber,
    required this.truckType,
    required this.origin,
    required this.destination,
    required this.totalCapacityKg,
    required this.availableCapacityKg,
    required this.sharedCostTotal,
    required this.soloCostTotal,
    required this.farmerSavings,
    required this.isRecommended,
  });

  factory TruckRoute.fromJson(Map<String, dynamic> json) {
    return TruckRoute(
      id: json['id'] ?? '',
      driverName: json['driver_name'] ?? '',
      driverPhone: json['driver_phone'] ?? '',
      truckNumber: json['truck_number'] ?? '',
      truckType: json['truck_type'] ?? '',
      origin: json['origin'] ?? '',
      destination: json['destination'] ?? '',
      totalCapacityKg: (json['total_capacity_kg'] as num?)?.toDouble() ?? 3000.0,
      availableCapacityKg: (json['available_capacity_kg'] as num?)?.toDouble() ?? 1000.0,
      sharedCostTotal: (json['shared_cost_total'] as num?)?.toDouble() ?? 450.0,
      soloCostTotal: (json['solo_cost_total'] as num?)?.toDouble() ?? 1200.0,
      farmerSavings: (json['farmer_savings'] as num?)?.toDouble() ?? 750.0,
      isRecommended: json['is_recommended'] ?? false,
    );
  }
}
