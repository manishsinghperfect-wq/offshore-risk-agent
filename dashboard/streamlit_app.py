[
  {
    "project_id": "T-2025-011",
    "project_name": "North Sea Wind Cluster Phase 2",
    "project_value_usd": 420000000,
    "region": "North Sea",
    "operation_type": "windmill_installation",
    "risks": [
      {
        "id": "PR-001",
        "title": "DP failure during nacelle lift",
        "operation_type": "windmill_installation",
        "region": "North Sea",
        "risk_category": "Vessel / Equipment",
        "severity": "High",
        "likelihood": "Medium",
        "project_value_usd": 420000000,
        "likely_cost_usd": 2350000,
        "likely_delay_days": 3,
        "worst_cost_usd": 4300000,
        "worst_delay_days": 7,
        "triggers": ["DP alarm", "weather change", "nacelle lift operations"],
        "recommended_actions": [
          "Pre-lift DP verification",
          "Redundant positioning support",
          "Weather hold point before critical lift",
          "Dedicated engineering standby"
        ]
      },
      {
        "id": "PR-002",
        "title": "Weather downtime during installation window",
        "operation_type": "windmill_installation",
        "region": "North Sea",
        "risk_category": "Weather / Environmental",
        "severity": "Medium",
        "likelihood": "High",
        "project_value_usd": 420000000,
        "likely_cost_usd": 1800000,
        "likely_delay_days": 5,
        "worst_cost_usd": 3600000,
        "worst_delay_days": 9,
        "triggers": ["wave height", "wind limits", "crane workability"],
        "recommended_actions": [
          "Add contingency weather days",
          "Sequence installation by workability window",
          "Pre-stage vessels for local weather adjustment"
        ]
      }
    ]
  },
  {
    "project_id": "T-2025-022",
    "project_name": "Gulf Cable Route Upgrade",
    "project_value_usd": 240000000,
    "region": "Gulf of Mexico",
    "operation_type": "cable_laying",
    "risks": [
      {
        "id": "PR-010",
        "title": "Cable burial tool failure",
        "operation_type": "cable_laying",
        "region": "Gulf of Mexico",
        "risk_category": "Vessel / Equipment",
        "severity": "High",
        "likelihood": "Medium",
        "project_value_usd": 240000000,
        "likely_cost_usd": 1900000,
        "likely_delay_days": 5,
        "worst_cost_usd": 3600000,
        "worst_delay_days": 8,
        "triggers": ["tool jam", "route deviation", "equipment downtime"],
        "recommended_actions": [
          "Pre-mobilization burial tool inspection",
          "Spare tool package and specialist technician",
          "Contingency route recovery plan"
        ]
      },
      {
        "id": "PR-011",
        "title": "Seabed route uncertainty",
        "operation_type": "cable_laying",
        "region": "Gulf of Mexico",
        "risk_category": "Geotechnical / Route",
        "severity": "Medium",
        "likelihood": "High",
        "project_value_usd": 240000000,
        "likely_cost_usd": 2200000,
        "likely_delay_days": 6,
        "worst_cost_usd": 4200000,
        "worst_delay_days": 10,
        "triggers": ["route change", "geotechnical variation", "boulder obstruction"],
        "recommended_actions": [
          "Additional route survey",
          "Route approval gate before mobilization",
          "Cable slack design and contingency segments"
        ]
      }
    ]
  },
  {
    "project_id": "T-2025-033",
    "project_name": "FPSO Hook-Up Support Campaign",
    "project_value_usd": 310000000,
    "region": "Guyana",
    "operation_type": "fpso_hookup",
    "risks": [
      {
        "id": "PR-020",
        "title": "Mooring interface issue during hook-up",
        "operation_type": "fpso_hookup",
        "region": "Guyana",
        "risk_category": "Operational",
        "severity": "High",
        "likelihood": "Medium",
        "project_value_usd": 310000000,
        "likely_cost_usd": 2100000,
        "likely_delay_days": 2,
        "worst_cost_usd": 3800000,
        "worst_delay_days": 6,
        "triggers": ["interface alignment", "station keeping", "close-in operations"],
        "recommended_actions": [
          "Detailed interface review",
          "Engineering hold point before critical phase",
          "Station keeping readiness checklist"
        ]
      }
    ]
  }
]
