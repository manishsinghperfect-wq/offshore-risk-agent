"""Offshore incident and risk event schemas."""
from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from schemas.orr import OperationType, RiskCategory


class IncidentSeverity(str, Enum):
    """Incident impact severity."""
    MINOR = "Minor"
    MODERATE = "Moderate"
    MAJOR = "Major"
    CRITICAL = "Critical"
    FATALITY = "Fatality"


class IncidentType(str, Enum):
    """Incident classification."""
    EQUIPMENT_FAILURE = "Equipment Failure"
    COLLISION = "Collision"
    DROPPED_OBJECT = "Dropped Object"
    ENVIRONMENTAL = "Environmental"
    HSE = "HSE Incident"
    REGULATORY = "Regulatory"
    FINANCIAL = "Financial Impact"
    DELAY = "Schedule Delay"
    OTHER = "Other"


class VesselType(str, Enum):
    """Vessel classification."""
    FPSO = "FPSO"
    INSTALLATION_VESSEL = "Installation Vessel"
    CLV = "Cable Layer Vessel"
    HEAVY_LIFT = "Heavy Lift Vessel"
    SUPPLY_VESSEL = "Supply Vessel"
    TUG = "Tug"
    WTG_INSTALLATION = "WTG Installation Vessel"
    CRANE_VESSEL = "Crane Vessel"
    SUBSEA_SUPPORT = "Subsea Support"


@dataclass
class Location:
    """Geographic location of incident."""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    region: Optional[str] = None  # e.g., "North Sea", "Gulf of Mexico"
    water_depth_m: Optional[float] = None
    country: Optional[str] = None


@dataclass
class FinancialImpact:
    """Quantified financial consequences."""
    direct_cost_usd: Optional[float] = None  # Repair, replacement
    indirect_cost_usd: Optional[float] = None  # Lost revenue, delays
    insurance_claim_usd: Optional[float] = None
    cost_estimate_confidence: str = "Low"  # Low, Medium, High


@dataclass
class TimeImpact:
    """Schedule consequences."""
    days_delay: Optional[float] = None
    downtime_hours: Optional[float] = None
    operational_impact: Optional[str] = None
    time_estimate_confidence: str = "Low"


@dataclass
class VesselInvolved:
    """Vessel details for incident."""
    name: str
    imo: Optional[str] = None
    type: Optional[VesselType] = None
    operator: Optional[str] = None
    flag_state: Optional[str] = None
    age_years: Optional[int] = None
    dp_class: Optional[str] = None  # DP0/DP1/DP2/DP3


@dataclass
class IncidentEvent:
    """Single offshore industry incident from news/data sources."""
    incident_id: str  # Unique identifier
    title: str
    description: str
    
    # Classification
    type: IncidentType
    severity: IncidentSeverity
    category: Optional[RiskCategory] = None
    operation_type: Optional[OperationType] = None
    
    # Timeline
    date_occurred: datetime
    date_reported: Optional[datetime] = None
    date_discovered: Optional[datetime] = None
    
    # Location
    location: Optional[Location] = None
    
    # Vessel/Asset info
    vessels: List[VesselInvolved] = field(default_factory=list)
    company: Optional[str] = None
    project_name: Optional[str] = None
    
    # Impact
    financial_impact: Optional[FinancialImpact] = None
    time_impact: Optional[TimeImpact] = None
    hse_injuries: Optional[int] = None
    environmental_impact: Optional[str] = None
    
    # Root cause
    root_cause: Optional[str] = None
    contributing_factors: List[str] = field(default_factory=list)
    
    # Response
    immediate_actions: Optional[str] = None
    corrective_actions: List[str] = field(default_factory=list)
    lessons_learned: Optional[str] = None
    
    # Source & metadata
    source: str  # e.g., "MarineTraffic", "DNV", "News Feed", "IMCA DROPS"
    source_url: Optional[str] = None
    confidence_score: float = 0.8  # AI extraction confidence 0-1
    
    # Industry response
    industry_precedents: List[str] = field(default_factory=list)
    peer_incidents: List[str] = field(default_factory=list)  # Similar incident IDs
    
    # Enrichment
    extracted_risks: List[str] = field(default_factory=list)  # Linked ORR numbers
    ai_summary: Optional[str] = None  # LLM generated summary
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)


@dataclass
class RiskIntelligenceReport:
    """AI-generated risk analysis report."""
    report_id: str
    incident_ids: List[str]  # Linked incidents
    
    # Risk assessment
    identified_risks: List[Dict[str, Any]]  # What risks emerged?
    risk_severity: IncidentSeverity
    probability_recurrence: float  # 0-1
    
    # Financial modeling
    cost_impact_mean_usd: float
    cost_impact_p95_usd: float
    cost_impact_range: tuple  # (min, max)
    time_impact_mean_days: float
    time_impact_p95_days: float
    
    # Benchmarking
    peer_comparison: str  # How do competitors handle this?
    industry_frequency: Optional[str]  # Common, rare, unheard of
    trend: Optional[str]  # Increasing, decreasing, stable
    
    # Recommendations
    preventive_measures: List[str]
    detective_measures: List[str]
    mitigative_measures: List[str]
    
    # Related ORR items
    matching_orr: List[str]  # Which ORR items does this relate to?
    
    # Status
    created_at: datetime = field(default_factory=datetime.utcnow)
    report_confidence: float = 0.7  # 0-1
    requires_review: bool = True  # Flag for domain expert review
