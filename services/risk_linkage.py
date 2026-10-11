"""Link global risks to project-specific ORR items."""
from typing import List, Dict, Tuple
from schemas.global_risk import GlobalRiskEvent, ProjectRiskItem, TenderRiskProfile
from services.global_risk_db import GlobalRiskDatabase


class RiskLinkageEngine:
    """Matches global risk events to project-specific risk items."""
    
    def __init__(self, db: GlobalRiskDatabase):
        self.db = db
    
    def find_relevant_global_risks(
        self,
        project: TenderRiskProfile,
        days_lookback: int = 90,
    ) -> List[GlobalRiskEvent]:
        """Find global risks relevant to a specific project."""
        relevant = []
        
        # Get events for same operation type
        op_type_events = self.db.get_events_by_operation_type(project.operation_type)
        relevant.extend(op_type_events)
        
        # Get events for same region
        region_events = self.db.get_events_by_region(project.geography)
        for e in region_events:
            if e not in relevant:
                relevant.append(e)
        
        # Filter to recent events
        from datetime import datetime, timedelta
        cutoff = datetime.utcnow() - timedelta(days=days_lookback)
        relevant = [e for e in relevant if e.date_occurred >= cutoff]
        
        return relevant
    
    def link_orr_to_global_events(
        self,
        orr_item: ProjectRiskItem,
        global_events: List[GlobalRiskEvent],
    ) -> Tuple[List[str], float]:
        """Link a project risk item to matching global events."""
        linked_event_ids = []
        match_score = 0.0
        
        for event in global_events:
            # Match on operation type
            if event.operation_type == orr_item.operation_type:
                match_score += 0.3
            
            # Match on risk category
            if event.risk_category == orr_item.category:
                match_score += 0.4
            
            # Match on keywords
            keywords = orr_item.title.lower().split() + [orr_item.description.lower()]
            event_text = (
                f"{event.title} {event.description} {' '.join(event.indicators)}"
            ).lower()
            keyword_matches = sum(1 for kw in keywords if kw in event_text)
            if keyword_matches > 0:
                match_score += min(0.3, keyword_matches * 0.1)
            
            if match_score > 0.5:  # Threshold for relevance
                linked_event_ids.append(event.event_id)
                match_score = 0.0  # Reset for next event
        
        return linked_event_ids, match_score
    
    def suggest_risk_mitigation(
        self,
        orr_item: ProjectRiskItem,
        related_events: List[GlobalRiskEvent],
    ) -> List[str]:
        """Suggest mitigation actions based on global event patterns."""
        suggestions = []
        
        if not related_events:
            return suggestions
        
        # Analyze patterns in related events
        categories = [e.risk_category for e in related_events]
        severities = [e.severity for e in related_events]
        
        # If similar events have high severity, recommend preventive measures
        if "High" in severities or "Critical" in severities:
            suggestions.append(
                f"Implement preventive measures: Similar incidents have caused significant impact. "
                f"Consider additional inspection, redundancy, or backup systems."
            )
        
        # If equipment failures are common, recommend spares
        if any("Equipment" in cat for cat in categories):
            suggestions.append(
                "Pre-position critical spare parts and qualified technicians on standby."
            )
        
        # If operational failures, recommend procedures
        if any("Operational" in cat for cat in categories):
            suggestions.append(
                "Develop detailed operational procedures and conduct tabletop exercises "
                "with all parties before execution."
            )
        
        # If weather-related, recommend contingency
        if any("Weather" in cat for cat in categories):
            avg_delay = sum(e.delay_days for e in related_events) / len(related_events)
            suggestions.append(
                f"Add {int(avg_delay * 1.5)} days of weather contingency to project schedule. "
                f"Average delay from similar incidents: {avg_delay:.1f} days."
            )
        
        return suggestions
    
    def estimate_benchmark_impact(
        self,
        orr_item: ProjectRiskItem,
        related_events: List[GlobalRiskEvent],
    ) -> Dict[str, float]:
        """Estimate financial and time impact based on global benchmarks."""
        if not related_events:
            return {
                "benchmark_cost_mean_usd": orr_item.most_likely_cost_usd,
                "benchmark_cost_p95_usd": orr_item.worst_case_cost_usd,
                "benchmark_delay_mean_days": orr_item.most_likely_delay_days,
                "benchmark_delay_p95_days": orr_item.worst_case_delay_days,
            }
        
        costs = [e.cost_impact_usd for e in related_events]
        delays = [e.delay_days for e in related_events]
        
        # Simple percentile calculations
        costs.sort()
        delays.sort()
        
        n = len(costs)
        p95_idx = int(n * 0.95)
        
        return {
            "benchmark_cost_mean_usd": sum(costs) / n,
            "benchmark_cost_p95_usd": costs[min(p95_idx, n - 1)],
            "benchmark_delay_mean_days": sum(delays) / n,
            "benchmark_delay_p95_days": delays[min(p95_idx, n - 1)],
            "sample_size": n,
            "sources": [f"Global event: {e.event_id}" for e in related_events],
        }
