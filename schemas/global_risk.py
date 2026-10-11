"""Global offshore risk intelligence database schema."""
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RiskStatus(str, Enum):
    EMERGING = "Emerging"
    ACTIVE = "Active"
    MONITORED = "Monitored"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


@dataclass
class GlobalRiskEvent:
    """Single global offshore risk event detected from public sources."""
    event_id: str
    title: str
    description: str
    operation_type: str  # windmill_installation, cable_laying, heavy_lift, fpso_hookup
    risk_category: str  # Vessel/Equipment, Operational, Weather, Commercial, HSE
    severity: str  # Low, Medium, High, Critical
    date_occurred: datetime
    region: str  # North Sea, Gulf of Mexico, Southeast Asia, West Africa, Guyana
    companies_affected: List[str]
    vessels_involved: List[str]
    status: RiskStatus
    
    # Financial and time impact
    cost_impact_usd: float
    delay_days: float
    
    # Source and confidence
    source: str  # News feed, Regulatory bulletin, Incident database
    source_url: Optional[str] = None
    extraction_confidence: float = 0.7
    
    # Risk indicators for project relevance
    indicators: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)


@dataclass
class ProjectRiskItem:
    """Risk item specific to a tender/project, linked to global events."""
    orr_id: str  # e.g., "001", "ORR-2026-001"
    project_id: str
    title: str
    description: str
    category: str
    operation_type: str
    
    # Risk assessment
    initial_probability: float  # 0-1
    initial_impact: str  # Low, Medium, High, Critical
    residual_probability: Optional[float] = None
    residual_impact: Optional[str] = None
    
    # Financial and schedule
    best_case_cost_usd: float
    most_likely_cost_usd: float
    worst_case_cost_usd: float
    
    best_case_delay_days: float
    most_likely_delay_days: float
    worst_case_delay_days: float
    
    # Treatment
    treatment_strategy: str  # Treat, Take, Transfer, Exploit
    mitigation_actions: List[str] = field(default_factory=list)
    owner: Optional[str] = None
    
    # Link to global events
    related_global_events: List[str] = field(default_factory=list)  # event_ids
    
    # Status
    status: str = "Active"  # Active, Closed, Superseded
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TenderRiskProfile:
    """Risk profile for a specific tender/project."""
    tender_id: str
    project_name: str
    client: str
    operation_type: str
    geography: str
    estimated_cost_usd: float
    estimated_duration_months: float
    offshore_window: str
    
    # Risk register
    orr_items: List[ProjectRiskItem] = field(default_factory=list)
    
    # Risk budget (Monte Carlo style)
    risk_budget_mean_usd: float = 0.0
    risk_budget_p50_usd: float = 0.0
    risk_budget_p80_usd: float = 0.0
    risk_budget_p95_usd: float = 0.0
    risk_budget_std_dev_usd: float = 0.0
    
    # Link to global risk events
    relevant_global_events: List[str] = field(default_factory=list)  # event_ids
    similar_projects: List[str] = field(default_factory=list)
    
    # Key risks
    top_risks: List[str] = field(default_factory=list)  # orr_ids
    
    # Status
    status: str = "Active"  # Active, Planning, Closed
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BenchmarkComparison:
    """Benchmark data for risk comparison across projects."""
    benchmark_id: str
    operation_type: str
    risk_category: str
    region: str
    
    # Historical data
    sample_size: int
    avg_cost_impact_usd: float
    median_cost_impact_usd: float
    cost_range_min_usd: float
    cost_range_max_usd: float
    
    avg_delay_days: float
    median_delay_days: float
    delay_range_min_days: float
    delay_range_max_days: float
    
    # Frequency
    incidents_per_year: float
    occurrence_probability: float  # 0-1
    
    # Best practices
    mitigation_strategies: List[str] = field(default_factory=list)
    detection_methods: List[str] = field(default_factory=list)
    
    # Data sources
    data_sources: List[str] = field(default_factory=list)
    confidence: float = 0.7
