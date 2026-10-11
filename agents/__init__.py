from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from models.offshore_taxonomy import OffshoreRiskTaxonomy
from models.financial_impact import estimate_cost_and_delay


@dataclass
class RiskFinding:
    title: str
    operation_type: str
    region: str
    risk_category: str
    severity: str
    likelihood: str
    financial_impact_usd: float
    delay_days: float
    benchmark: str
    corrective_actions: List[str]
    confidence: float


class OffshoreRiskAgent:
    """AI-style offshore risk intelligence agent."""

    def __init__(self, taxonomy: Optional[OffshoreRiskTaxonomy] = None):
        self.taxonomy = taxonomy or OffshoreRiskTaxonomy()

    def analyze_case(
        self,
        operation_type: str,
        region: str,
        incident_summary: str,
        source_name: str = "Public News / Event Feed",
    ) -> Dict[str, Any]:
        """Analyze an offshore event or news item into a structured risk output."""

        keywords = incident_summary.lower()
        matched = self.taxonomy.match_keywords(
            operation_type=operation_type,
            text=keywords,
            default_category="Operational",
        )

        # Estimate impact from event phrases
        impact = estimate_cost_and_delay(
            operation_type=operation_type,
            risk_category=matched["risk_category"],
            text=incident_summary,
            region=region,
        )

        benchmark = self.taxonomy.get_benchmark_summary(
            matched["risk_category"],
            operation_type,
            region,
        )

        actions = self.taxonomy.get_corrective_actions(
            matched["risk_category"],
            operation_type,
        )

        risk = RiskFinding(
            title=matched["title"],
            operation_type=operation_type,
            region=region,
            risk_category=matched["risk_category"],
            severity=impact["severity"],
            likelihood=impact["likelihood"],
            financial_impact_usd=impact["cost_usd"],
            delay_days=impact["delay_days"],
            benchmark=benchmark,
            corrective_actions=actions,
            confidence=impact["confidence"],
        )

        return {
            "title": risk.title,
            "operation_type": risk.operation_type,
            "region": risk.region,
            "risk_category": risk.risk_category,
            "severity": risk.severity,
            "likelihood": risk.likelihood,
            "financial_impact_usd": risk.financial_impact_usd,
            "delay_days": risk.delay_days,
            "benchmark": risk.benchmark,
            "corrective_actions": risk.corrective_actions,
            "source_name": source_name,
            "confidence": risk.confidence,
        }

    def analyze_batch(self, items: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Analyze multiple offshore cases."""
        return [self.analyze_case(**item) for item in items]


if __name__ == "__main__":
    agent = OffshoreRiskAgent()
    sample = {
        "operation_type": "windmill_installation",
        "region": "North Sea",
        "incident_summary": "Installation vessel had DP failure during heavy weather while lifting nacelle, causing a three-day delay and repair cost around 2.3M USD.",
    }
    print(agent.analyze_case(**sample))
