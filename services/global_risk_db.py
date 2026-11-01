from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class RiskStatus(str, Enum):
    ACTIVE = "Active"
    MONITORING = "Monitoring"
    CLOSED = "Closed"


@dataclass
class ReferenceLink:
    label: str
    url: str


@dataclass
class GlobalRiskEvent:
    id: str
    title: str
    operation_type: str
    region: str
    risk_category: str
    severity: str
    likelihood: str
    financial_impact_usd: float
    delay_days: float
    benchmark: str
    incident_summary: str
    evidence_excerpt: str
    source_name: str
    source_url: str
    source_type: str
    source_date: str
    confidence: float = 0.7
    recommended_actions: List[str] = field(default_factory=list)
    reference_links: List[ReferenceLink] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "GlobalRiskEvent":
        refs = [ReferenceLink(**item) for item in payload.get("reference_links", [])]
        return cls(
            id=payload["id"],
            title=payload["title"],
            operation_type=payload["operation_type"],
            region=payload["region"],
            risk_category=payload["risk_category"],
            severity=payload["severity"],
            likelihood=payload["likelihood"],
            financial_impact_usd=float(payload["financial_impact_usd"]),
            delay_days=float(payload["delay_days"]),
            benchmark=payload.get("benchmark", ""),
            incident_summary=payload.get("incident_summary", ""),
            evidence_excerpt=payload.get("evidence_excerpt", ""),
            source_name=payload.get("source_name", ""),
            source_url=payload.get("source_url", ""),
            source_type=payload.get("source_type", ""),
            source_date=payload.get("source_date", ""),
            confidence=float(payload.get("confidence", 0.7)),
            recommended_actions=payload.get("recommended_actions", []),
            reference_links=refs,
        )


@dataclass
class ProjectRisk:
    id: str
    title: str
    operation_type: str
    region: str
    risk_category: str
    severity: str
    likelihood: str
    project_value_usd: float
    likely_cost_usd: float
    likely_delay_days: float
    worst_cost_usd: float
    worst_delay_days: float
    triggers: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    status: str = "Active"
    evidence_links: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BenchmarkComparison:
    operation_type: str
    risk_category: str
    median_cost_usd: float
    p90_cost_usd: float
    median_delay_days: float
    p90_delay_days: float
    benchmark_text: str
    common_triggers: List[str]
    common_actions: List[str]
    confidence: float = 0.75


@dataclass
class TenderRiskProfile:
    project_name: str
    project_id: str
    project_value_usd: float
    region: str
    operation_type: str
    overall_risk_score: float = 0.0
    risks: List[ProjectRisk] = field(default_factory=list)
    risk_budget_mean_usd: float = 0.0
    risk_budget_p80_usd: float = 0.0
    risk_budget_p95_usd: float = 0.0
    status: str = "Active"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RiskMatch:
    project_risk_id: str
    event_id: str
    match_score: float
    reasons: List[str]
    event: GlobalRiskEvent
