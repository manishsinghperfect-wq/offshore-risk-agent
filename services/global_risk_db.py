"""Global risk event database and querying."""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from schemas.global_risk import GlobalRiskEvent, BenchmarkComparison, RiskStatus
import json
from pathlib import Path


class GlobalRiskDatabase:
    """In-memory global risk event database (can be extended to real DB)."""
    
    def __init__(self):
        self.events: Dict[str, GlobalRiskEvent] = {}
        self.benchmarks: Dict[str, BenchmarkComparison] = {}
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample global risk events."""
        sample_events = [
            {
                "event_id": "GRE-2026-001",
                "title": "DP Failure During Windmill Installation - North Sea",
                "description": "Installation vessel experienced complete DP failure during nacelle lift in heavy weather, causing 3-day operational pause and requiring specialist intervention.",
                "operation_type": "windmill_installation",
                "risk_category": "Vessel/Equipment",
                "severity": "High",
                "date_occurred": datetime(2026, 9, 15),
                "region": "North Sea",
                "companies_affected": ["Major Offshore Contractor"],
                "vessels_involved": ["Installation Vessel A"],
                "status": RiskStatus.ACTIVE,
                "cost_impact_usd": 2_300_000,
                "delay_days": 3.0,
                "source": "Offshore Engineer News",
                "extraction_confidence": 0.85,
                "indicators": ["DP failure", "heavy weather", "nacelle lift", "installation delay"],
            },
            {
                "event_id": "GRE-2026-002",
                "title": "Cable Burial Tool Failure - Gulf of Mexico",
                "description": "Cable laying vessel suffered burial tool malfunction during cable installation, requiring tool recovery and replacement, extending offshore campaign by 5 days.",
                "operation_type": "cable_laying",
                "risk_category": "Vessel/Equipment",
                "severity": "Medium",
                "date_occurred": datetime(2026, 9, 20),
                "region": "Gulf of Mexico",
                "companies_affected": ["Marine Contractor B"],
                "vessels_involved": ["Cable Layer Vessel X"],
                "status": RiskStatus.ACTIVE,
                "cost_impact_usd": 1_800_000,
                "delay_days": 5.0,
                "source": "TradeWinds Maritime News",
                "extraction_confidence": 0.78,
                "indicators": ["burial tool", "cable damage", "equipment failure", "lay schedule"],
            },
            {
                "event_id": "GRE-2026-003",
                "title": "Heavy Lift Rigging Incident - West Africa",
                "description": "Dropped object incident during heavy lift campaign resulted in safety pause, 2-day operational hold, and structural damage assessment.",
                "operation_type": "heavy_lift",
                "risk_category": "HSE",
                "severity": "Critical",
                "date_occurred": datetime(2026, 9, 22),
                "region": "West Africa",
                "companies_affected": ["Boskalis", "Subsea Contractor"],
                "vessels_involved": ["Heavy Lift Vessel Y", "Crane Barge Z"],
                "status": RiskStatus.ACTIVE,
                "cost_impact_usd": 4_500_000,
                "delay_days": 8.0,
                "source": "IMCA Incident Database",
                "extraction_confidence": 0.92,
                "indicators": ["dropped object", "safety", "rigging failure", "heavy lift pause"],
            },
            {
                "event_id": "GRE-2026-004",
                "title": "FPSO Hook-up Mooring Interface Issue - Guyana",
                "description": "Mooring line tension anomaly detected during FPSO hook-up, requiring additional engineering analysis and procedure revision before resuming operations.",
                "operation_type": "fpso_hookup",
                "risk_category": "Operational",
                "severity": "High",
                "date_occurred": datetime(2026, 9, 25),
                "region": "Guyana",
                "companies_affected": ["Offshore Services Ltd"],
                "vessels_involved": ["Hook-up Spread"],
                "status": RiskStatus.MONITORED,
                "cost_impact_usd": 2_100_000,
                "delay_days": 2.5,
                "source": "Operator Public Statement",
                "extraction_confidence": 0.68,
                "indicators": ["mooring", "interface", "hook-up", "operational risk"],
            },
            {
                "event_id": "GRE-2026-005",
                "title": "Windmill Weather Downtime - Southeast Asia",
                "description": "Typhoon season onset in Southeast Asia reduced offshore workability window by 10 days, impacting multiple installation projects.",
                "operation_type": "windmill_installation",
                "risk_category": "Weather/Environment",
                "severity": "Medium",
                "date_occurred": datetime(2026, 9, 28),
                "region": "Southeast Asia",
                "companies_affected": ["Multiple contractors"],
                "vessels_involved": ["Multiple installation vessels"],
                "status": RiskStatus.ACTIVE,
                "cost_impact_usd": 3_200_000,
                "delay_days": 10.0,
                "source": "Maritime Executive",
                "extraction_confidence": 0.81,
                "indicators": ["weather", "downtime", "typhoon", "workability"],
            },
        ]
        
        for evt in sample_events:
            event = GlobalRiskEvent(**evt)
            self.events[event.event_id] = event
    
    def get_events_by_operation_type(self, operation_type: str) -> List[GlobalRiskEvent]:
        """Retrieve global events filtered by operation type."""
        return [e for e in self.events.values() if e.operation_type == operation_type]
    
    def get_events_by_region(self, region: str) -> List[GlobalRiskEvent]:
        """Retrieve global events by geography."""
        return [e for e in self.events.values() if e.region == region]
    
    def get_events_by_risk_category(self, category: str) -> List[GlobalRiskEvent]:
        """Retrieve events by risk category."""
        return [e for e in self.events.values() if e.risk_category == category]
    
    def get_recent_events(self, days: int = 30) -> List[GlobalRiskEvent]:
        """Retrieve events from the last N days."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [e for e in self.events.values() if e.date_occurred >= cutoff]
    
    def get_high_severity_events(self) -> List[GlobalRiskEvent]:
        """Get all high or critical severity events."""
        return [e for e in self.events.values() if e.severity in ["High", "Critical"]]
    
    def find_related_events(self, keywords: List[str]) -> List[GlobalRiskEvent]:
        """Find events matching keywords."""
        results = []
        keywords_lower = [kw.lower() for kw in keywords]
        for event in self.events.values():
            text_search = (
                f"{event.title} {event.description} {' '.join(event.indicators)}"
            ).lower()
            if any(kw in text_search for kw in keywords_lower):
                results.append(event)
        return results
    
    def add_event(self, event: GlobalRiskEvent):
        """Add a new global risk event."""
        self.events[event.event_id] = event
    
    def get_event_summary(self) -> Dict[str, any]:
        """Get summary statistics of global risk events."""
        events = list(self.events.values())
        if not events:
            return {"total_events": 0}
        
        return {
            "total_events": len(events),
            "high_severity_count": len([e for e in events if e.severity in ["High", "Critical"]]),
            "total_cost_impact_usd": sum(e.cost_impact_usd for e in events),
            "total_delay_days": sum(e.delay_days for e in events),
            "affected_regions": list(set(e.region for e in events)),
            "risk_categories": list(set(e.risk_category for e in events)),
            "avg_cost_per_event_usd": sum(e.cost_impact_usd for e in events) / len(events),
            "avg_delay_per_event_days": sum(e.delay_days for e in events) / len(events),
        }
