"""Offshore Risk Register (ORR) data models."""
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


class RiskType(str, Enum):
    """Risk classification."""
    RISK = "Risk"
    UNCERTAINTY = "Uncertainty"
    OPPORTUNITY = "Opportunity"


class RiskStatus(str, Enum):
    """Risk lifecycle status."""
    ACTIVE = "Active"
    CLOSED_EXPIRED = "Closed - Expired"
    CLOSED_SUPERSEDED = "Closed - Superseded"
    POINT_OF_ATTENTION = "Point of Attention"


class RiskLevel(str, Enum):
    """Severity classification."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
    UNCERTAINTY = "Uncertainty"


class OperationType(str, Enum):
    """Offshore operation classification."""
    FPSO_HOOKUP = "FPSO Hook-up"
    WINDMILL_INSTALLATION = "Windmill Installation"
    CABLE_LAYING = "Cable Laying"
    HEAVY_LIFT = "Heavy Lift"
    SUBSEA_INSTALLATION = "Subsea Installation"
    DECOMMISSIONING = "Decommissioning"


class RiskCategory(str, Enum):
    """Risk domain classification."""
    VESSEL_EQUIPMENT = "Vessel/Equipment"
    OPERATIONAL = "Operational"
    WEATHER_ENVIRONMENT = "Weather/Environment"
    REGULATORY_COMPLIANCE = "Regulatory/Compliance"
    COMMERCIAL = "Commercial"
    HSE = "HSE"
    MARKET = "Market"
    INTERFACE = "Interface"


class TreatmentStrategy(str, Enum):
    """Risk response strategy."""
    TREAT = "Treat"
    TAKE = "Take"
    TRANSFER = "Transfer"
    EXPLOIT = "Exploit"  # For opportunities
    QUALIFIED = "Qualified"


@dataclass
class RiskAction:
    """Risk mitigation action."""
    description: str
    owner: Optional[str] = None
    due_date: Optional[datetime] = None
    cost: Optional[float] = None
    status: str = "Pending"


@dataclass
class FinancialScenario:
    """Cost/time scenario."""
    best_case: float  # BC
    most_likely: float  # ML
    worst_case: float  # WC
    unit: str = "USD"  # or days, etc


@dataclass
class ORRItem:
    """Single Opportunity & Risk Register entry."""
    or_number: str  # e.g., "1", "14", "78"
    title: str
    type: RiskType
    status: RiskStatus
    category: RiskCategory
    operation_type: OperationType
    
    # Description
    cause: str
    event: str
    consequence: str
    
    # Scoring
    initial_score: Optional[float] = None
    initial_level: Optional[RiskLevel] = None
    residual_score: Optional[float] = None
    residual_level: Optional[RiskLevel] = None
    probability: Optional[float] = None  # 0-1
    
    # Financial impact
    cost_scenario: Optional[FinancialScenario] = None
    time_scenario: Optional[FinancialScenario] = None
    affected_asset: Optional[str] = None  # e.g., "Hook-up spread"
    asset_day_rate: Optional[float] = None
    
    # Treatment
    treatment: Optional[TreatmentStrategy] = None
    actions: List[RiskAction] = None
    allowance: Optional[float] = None  # Risk budget allocation
    
    # Metadata
    owner: Optional[str] = None
    created_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    notes: Optional[str] = None
    
    # Monte Carlo linkage
    distribution_type: Optional[str] = None  # "Uniform", "Triangular", "Normal"
    
    def __post_init__(self):
        if self.actions is None:
            self.actions = []


@dataclass
class MonteCarloResult:
    """Single risk Monte Carlo simulation output."""
    or_number: str
    title: str
    mean: float
    p50: float
    p80: float
    p90: float
    p95: float
    min_val: float
    max_val: float
    std_dev: float
    positive_frequency: float  # % of iterations with positive contribution
    correlation_with_output: float  # -1 to 1
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None


@dataclass
class ProjectRiskProfile:
    """Aggregated risk for a project."""
    project_id: str
    project_name: str
    operation_type: OperationType
    geography: str
    
    # Total risk budget
    total_mean: float
    total_p50: float
    total_p80: float
    total_p95: float
    total_std_dev: float
    
    # Composition
    active_orr_count: int
    modeled_count: int
    risks_high: int
    risks_medium: int
    risks_low: int
    
    # Distribution
    negative_probability: float  # % below zero
    tail_skewness: Optional[float] = None
    
    # By WBS
    by_workstream: dict = None  # {workstream: mean_contribution}
    
    # Individual results
    orr_items: List[ORRItem] = None
    mc_results: List[MonteCarloResult] = None
    
    def __post_init__(self):
        if self.by_workstream is None:
            self.by_workstream = {}
        if self.orr_items is None:
            self.orr_items = []
        if self.mc_results is None:
            self.mc_results = []
