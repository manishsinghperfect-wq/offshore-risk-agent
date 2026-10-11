# Competitor/Industry Benchmarking Prompt

You are analyzing how other offshore operators handle a specific risk. Compare your company's approach with industry peers.

## Context

Given:
- **Risk event**: Description of what happened
- **Our response**: What actions did we take?
- **Our costs/timeline**: Financial and schedule impact

Research and assess:

1. **Industry precedents**: How often does this happen?
2. **Peer comparison**: How do competitors handle this risk?
3. **Cost benchmarking**: Are our costs in line with industry averages?
4. **Timeline benchmarking**: How long do repairs typically take?
5. **Lessons learned**: What's the best practice approach?

## Analysis Template

```json
{
  "risk_event": "DP system failure during hook-up",
  
  "industry_prevalence": {
    "frequency_per_year": "estimated number of occurrences globally",
    "affected_operations": "% of FPSO hook-ups affected",
    "trend": "Increasing | Decreasing | Stable",
    "data_sources": ["IMCA DROPS", "DNV reports", "Industry publications"]
  },
  
  "competitor_responses": [
    {
      "company": "Company A",
      "approach": "How they mitigate this risk",
      "typical_downtime": "X days",
      "typical_cost_impact": "$Y million",
      "prevention_measures": ["measure1", "measure2"],
      "detection_methods": ["method1", "method2"]
    },
    {
      "company": "Company B",
      "approach": "...",
      "typical_downtime": "...",
      "typical_cost_impact": "..."
    }
  ],
  
  "cost_comparison": {
    "our_actual_cost_usd": 1200000,
    "industry_average_usd": 950000,
    "industry_range_min_usd": 500000,
    "industry_range_max_usd": 2500000,
    "our_performance_vs_peers": "Above average | In line | Below average",
    "cost_drivers_difference": ["We had to fly in specialist technicians", "..."]
  },
  
  "timeline_comparison": {
    "our_downtime_days": 3.5,
    "industry_average_days": 2.0,
    "industry_range_min_days": 0.5,
    "industry_range_max_days": 7,
    "our_performance_vs_peers": "Slower than average | In line | Faster",
    "reasons_for_difference": ["Supply chain delay", "..."]
  },
  
  "best_practices_observed": [
    {
      "practice": "Dual DP systems",
      "adoption_rate": "60% of fleet",
      "effectiveness": "Reduces frequency by ~40%",
      "cost_to_implement": "$500k per vessel"
    },
    {
      "practice": "Spare DP components pre-positioned on standby vessel",
      "adoption_rate": "40% of fleet",
      "effectiveness": "Reduces downtime by 1-2 days",
      "cost_to_implement": "$200k per campaign"
    }
  ],
  
  "our_gap_analysis": {
    "what_we_did_well": ["Quick incident response", "Good communication"],
    "where_we_lagged": ["Did not have spare DP module onboard", "..."],
    "improvement_opportunities": [
      {
        "area": "Preventive maintenance",
        "gap": "Annual inspection vs industry best practice of 6-monthly",
        "estimated_benefit": "Reduce failure frequency by 30%",
        "implementation_cost": "$100k/year"
      }
    ]
  },
  
  "recommended_corrective_actions": [
    {
      "action": "Increase preventive maintenance frequency",
      "priority": "High",
      "cost_impact": "$100k/year",
      "expected_benefit": "30% reduction in DP failures"
    },
    {
      "action": "Pre-position spare DP module on offshore standby",
      "priority": "High",
      "cost_impact": "$200k per campaign",
      "expected_benefit": "1-2 day reduction in downtime"
    }
  ],
  
  "data_confidence": 0.0 to 1.0,
  "sources_used": ["Public incident reports", "Industry surveys", "Peer interviews"]
}
```

## Key Questions

1. **Are we above or below industry average for cost impact?**
   - If above: What drove the extra cost?
   - If below: What did we do right?

2. **Are we above or below industry average for recovery time?**
   - What determined the recovery timeline?
   - Could it have been faster?

3. **What's the best-in-class response?**
   - Who handles this risk best?
   - What are they doing differently?

4. **What are we missing?**
   - Preventive measures?
   - Detection/monitoring?
   - Emergency response procedures?

5. **Should we adopt peer practices?**
   - Cost-benefit of implementing best practices
   - Timeline for implementation
   - Risk reduction potential
