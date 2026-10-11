"""Tender and project risk profile management."""
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from schemas.global_risk import TenderRiskProfile, ProjectRiskItem
from services.global_risk_db import GlobalRiskDatabase
from services.risk_linkage import RiskLinkageEngine


class TenderRiskManager:
    """Manage risk registers and profiles for specific tenders/projects."""
    
    def __init__(self, global_db: GlobalRiskDatabase):
        self.global_db = global_db
        self.linkage_engine = RiskLinkageEngine(global_db)
        self.tenders: dict = {}  # tender_id -> TenderRiskProfile
    
    def create_tender_profile(
        self,
        tender_id: str,
        project_name: str,
        client: str,
        operation_type: str,
        geography: str,
        estimated_cost_usd: float,
        estimated_duration_months: float,
        offshore_window: str,
    ) -> TenderRiskProfile:
        """Create a new tender risk profile."""
        profile = TenderRiskProfile(
            tender_id=tender_id,
            project_name=project_name,
            client=client,
            operation_type=operation_type,
            geography=geography,
            estimated_cost_usd=estimated_cost_usd,
            estimated_duration_months=estimated_duration_months,
            offshore_window=offshore_window,
        )
        self.tenders[tender_id] = profile
        return profile
    
    def add_risk_item(
        self,
        tender_id: str,
        orr_id: str,
        title: str,
        description: str,
        category: str,
        initial_probability: float,
        initial_impact: str,
        best_case_cost_usd: float,
        most_likely_cost_usd: float,
        worst_case_cost_usd: float,
        best_case_delay_days: float,
        most_likely_delay_days: float,
        worst_case_delay_days: float,
        treatment_strategy: str,
        mitigation_actions: Optional[List[str]] = None,
        owner: Optional[str] = None,
    ) -> ProjectRiskItem:
        """Add a risk item to a tender's ORR."""
        if tender_id not in self.tenders:
            raise ValueError(f"Tender {tender_id} not found")
        
        tender = self.tenders[tender_id]
        risk_item = ProjectRiskItem(
            orr_id=orr_id,
            project_id=tender_id,
            title=title,
            description=description,
            category=category,
            operation_type=tender.operation_type,
            initial_probability=initial_probability,
            initial_impact=initial_impact,
            best_case_cost_usd=best_case_cost_usd,
            most_likely_cost_usd=most_likely_cost_usd,
            worst_case_cost_usd=worst_case_cost_usd,
            best_case_delay_days=best_case_delay_days,
            most_likely_delay_days=most_likely_delay_days,
            worst_case_delay_days=worst_case_delay_days,
            treatment_strategy=treatment_strategy,
            mitigation_actions=mitigation_actions or [],
            owner=owner,
        )
        
        # Link to global events
        related_events = self.linkage_engine.find_relevant_global_risks(tender)
        linked_ids, _ = self.linkage_engine.link_orr_to_global_events(risk_item, related_events)
        risk_item.related_global_events = linked_ids
        
        # Get mitigation suggestions from global patterns
        suggestions = self.linkage_engine.suggest_risk_mitigation(risk_item, related_events)
        risk_item.mitigation_actions.extend(suggestions)
        
        tender.orr_items.append(risk_item)
        return risk_item
    
    def calculate_risk_budget(
        self,
        tender_id: str,
        use_percentiles: bool = True,
    ) -> dict:
        """Calculate Monte Carlo style risk budget for tender."""
        if tender_id not in self.tenders:
            raise ValueError(f"Tender {tender_id} not found")
        
        tender = self.tenders[tender_id]
        items = tender.orr_items
        
        if not items:
            return {
                "mean_usd": 0,
                "p50_usd": 0,
                "p80_usd": 0,
                "p95_usd": 0,
            }
        
        # Simple calculation: use most_likely as mean
        costs = [item.most_likely_cost_usd * item.initial_probability for item in items]
        worst_cases = [item.worst_case_cost_usd for item in items]
        
        mean = sum(costs)
        total_worst = sum(worst_cases)
        
        # Percentiles (simplified)
        sorted_costs = sorted(costs)
        n = len(sorted_costs)
        p50_idx = int(n * 0.5)
        p80_idx = int(n * 0.8)
        p95_idx = int(n * 0.95)
        
        return {
            "mean_usd": round(mean, 2),
            "p50_usd": round(sorted_costs[min(p50_idx, n - 1)], 2) if sorted_costs else 0,
            "p80_usd": round(sorted_costs[min(p80_idx, n - 1)], 2) if sorted_costs else 0,
            "p95_usd": round(sorted_costs[min(p95_idx, n - 1)], 2) if sorted_costs else 0,
            "worst_case_total_usd": round(total_worst, 2),
        }
    
    def get_tender_summary(
        self,
        tender_id: str,
    ) -> dict:
        """Get comprehensive summary of tender and its risks."""
        if tender_id not in self.tenders:
            return {"error": f"Tender {tender_id} not found"}
        
        tender = self.tenders[tender_id]
        related_global = self.linkage_engine.find_relevant_global_risks(tender)
        risk_budget = self.calculate_risk_budget(tender_id)
        
        high_risks = [r for r in tender.orr_items if r.initial_impact in ["High", "Critical"]]
        
        return {
            "tender_id": tender.tender_id,
            "project_name": tender.project_name,
            "operation_type": tender.operation_type,
            "geography": tender.geography,
            "estimated_cost_usd": tender.estimated_cost_usd,
            "orr_count": len(tender.orr_items),
            "high_risk_count": len(high_risks),
            "risk_budget": risk_budget,
            "related_global_events": len(related_global),
            "global_event_ids": [e.event_id for e in related_global],
            "top_risks": [
                {
                    "orr_id": r.orr_id,
                    "title": r.title,
                    "impact": r.initial_impact,
                    "cost_exposure_usd": r.most_likely_cost_usd,
                    "related_global_events": r.related_global_events,
                }
                for r in high_risks
            ],
        }
