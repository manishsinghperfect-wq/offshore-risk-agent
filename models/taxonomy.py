"""Offshore risk taxonomy and classification engine."""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class RiskDomain(str, Enum):
    """High-level risk domains for offshore operations."""
    TECHNICAL = "Technical"  # Vessel, equipment, subsystems
    OPERATIONAL = "Operational"  # Procedures, crew, interfaces
    ENVIRONMENTAL = "Environmental"  # Weather, sea state, currents
    REGULATORY = "Regulatory"  # Permits, compliance, audits
    COMMERCIAL = "Commercial"  # Cost, schedule, contracts
    HSE = "HSE"  # Health, safety, environment
    MARKET = "Market"  # Fuel, insurance, commodity prices


@dataclass
class RiskTaxonomyNode:
    """Single node in offshore risk taxonomy."""
    code: str  # e.g., "TECH-VES-DP"
    name: str  # e.g., "DP System Failure"
    domain: RiskDomain
    operation_types: List[str]  # Applicable operations
    
    # Characteristics
    typical_probability: Tuple[float, float]  # (low, high) range
    typical_cost_impact_usd: Tuple[float, float]
    typical_time_impact_days: Tuple[float, float]
    
    # Indicators (what to look for in news)
    indicators: List[str]
    historical_examples: List[str]
    
    # Treatment guidance
    treatment_strategies: List[str]
    key_mitigation: str


class OffshoreTaxonomy:
    """Master taxonomy for offshore risks."""
    
    VESSEL_EQUIPMENT = [
        RiskTaxonomyNode(
            code="TECH-VES-DP",
            name="DP System Failure",
            domain=RiskDomain.TECHNICAL,
            operation_types=["FPSO_HOOKUP", "WINDMILL_INSTALLATION", "CABLE_LAYING"],
            typical_probability=(0.02, 0.08),
            typical_cost_impact_usd=(500_000, 5_000_000),
            typical_time_impact_days=(1, 5),
            indicators=["blackout", "thruster failure", "power loss", "positioning"],
            historical_examples=["Vessel DP failure Oct 2026 North Sea"],
            treatment_strategies=["Redundancy", "Maintenance", "Spare parts", "DP trials"],
            key_mitigation="Ensure certified DP equipment + spares onboard + backup tugs"
        ),
        RiskTaxonomyNode(
            code="TECH-CRANE-BREAKDOWN",
            name="Crane/Lifting Equipment Breakdown",
            domain=RiskDomain.TECHNICAL,
            operation_types=["WINDMILL_INSTALLATION", "HEAVY_LIFT", "SUBSEA_INSTALLATION"],
            typical_probability=(0.05, 0.12),
            typical_cost_impact_usd=(300_000, 2_000_000),
            typical_time_impact_days=(0.5, 3),
            indicators=["winch failure", "crane outage", "hoist issue", "maintenance delay"],
            historical_examples=["Offshore crane failure 2025"],
            treatment_strategies=["Preventive maintenance", "Spare parts", "Personnel training"],
            key_mitigation="Certified equipment + pre-operation inspection + spare parts cache"
        ),
        RiskTaxonomyNode(
            code="TECH-ROV-LOSS",
            name="ROV Breakdown or Loss",
            domain=RiskDomain.TECHNICAL,
            operation_types=["FPSO_HOOKUP", "SUBSEA_INSTALLATION", "CABLE_LAYING"],
            typical_probability=(0.03, 0.10),
            typical_cost_impact_usd=(1_000_000, 5_000_000),
            typical_time_impact_days=(2, 7),
            indicators=["ROV loss", "tether failure", "entanglement", "recovery"],
            historical_examples=["ROV lost subsea 2024"],
            treatment_strategies=["Backup ROV", "Buoyant design", "Spare tethers"],
            key_mitigation="Dual ROV system onboard + critical spares"
        ),
    ]
    
    OPERATIONAL = [
        RiskTaxonomyNode(
            code="OPS-COLLISION",
            name="Collision with FPSO/Asset",
            domain=RiskDomain.OPERATIONAL,
            operation_types=["FPSO_HOOKUP", "HEAVY_LIFT"],
            typical_probability=(0.01, 0.05),
            typical_cost_impact_usd=(2_000_000, 10_000_000),
            typical_time_impact_days=(2, 14),
            indicators=["collision", "impact", "contact", "grounding"],
            historical_examples=["FPSO collision 2023"],
            treatment_strategies=["Vessel selection", "Tug management", "Qualified masters"],
            key_mitigation="DP2 vessel + qualified tow masters + positioning system"
        ),
        RiskTaxonomyNode(
            code="OPS-DROPPED-OBJECT",
            name="Dropped Object/Load Loss",
            domain=RiskDomain.OPERATIONAL,
            operation_types=["WINDMILL_INSTALLATION", "HEAVY_LIFT", "CABLE_LAYING"],
            typical_probability=(0.02, 0.08),
            typical_cost_impact_usd=(1_000_000, 8_000_000),
            typical_time_impact_days=(1, 10),
            indicators=["dropped object", "load loss", "shackle failure", "rigging"],
            historical_examples=["Blade dropped 2024"],
            treatment_strategies=["Load planning", "Inspection", "Personnel training"],
            key_mitigation="Load analysis + certified rigging + dual checks"
        ),
        RiskTaxonomyNode(
            code="OPS-INTERFACE-FAILURE",
            name="Interface/Coordination Failure",
            domain=RiskDomain.OPERATIONAL,
            operation_types=["FPSO_HOOKUP", "CABLE_LAYING"],
            typical_probability=(0.05, 0.15),
            typical_cost_impact_usd=(500_000, 3_000_000),
            typical_time_impact_days=(1, 5),
            indicators=["coordination issue", "unclear responsibility", "hand-off problem"],
            historical_examples=["Mooring interface incident"],
            treatment_strategies=["Clear procedures", "RACI matrix", "Regular briefings"],
            key_mitigation="Jointly agreed interface procedure + daily coordination meetings"
        ),
    ]
    
    ENVIRONMENTAL = [
        RiskTaxonomyNode(
            code="ENV-WEATHER-DOWNTIME",
            name="Weather/Sea State Downtime",
            domain=RiskDomain.ENVIRONMENTAL,
            operation_types=["WINDMILL_INSTALLATION", "CABLE_LAYING", "HEAVY_LIFT"],
            typical_probability=(0.3, 0.8),
            typical_cost_impact_usd=(0, 5_000_000),
            typical_time_impact_days=(5, 30),
            indicators=["bad weather", "sea state", "wind", "waves", "standby"],
            historical_examples=["North Sea weather window loss"],
            treatment_strategies=["Weather forecasting", "Contingency days", "Vessel choice"],
            key_mitigation="Conservative weather limits + extended offshore window + weather standby costs"
        ),
        RiskTaxonomyNode(
            code="ENV-CURRENT-CONSTRAINT",
            name="Strong Current/Environmental Constraint",
            domain=RiskDomain.ENVIRONMENTAL,
            operation_types=["CABLE_LAYING", "SUBSEA_INSTALLATION", "DEEP_WATER"],
            typical_probability=(0.1, 0.4),
            typical_cost_impact_usd=(500_000, 2_000_000),
            typical_time_impact_days=(2, 8),
            indicators=["current", "deep water", "workability", "constraint"],
            historical_examples=["Guyana deep water challenges"],
            treatment_strategies=["Hydrodynamic analysis", "Personnel training", "Equipment selection"],
            key_mitigation="Pre-op environmental data review + qualified personnel"
        ),
    ]
    
    REGULATORY = [
        RiskTaxonomyNode(
            code="REG-PERMIT-DELAY",
            name="Permit/Approval Delay",
            domain=RiskDomain.REGULATORY,
            operation_types=["WINDMILL_INSTALLATION", "CABLE_LAYING"],
            typical_probability=(0.1, 0.3),
            typical_cost_impact_usd=(500_000, 2_000_000),
            typical_time_impact_days=(5, 30),
            indicators=["permit", "approval", "clearance", "authority"],
            historical_examples=["Vessel clearance delays Guyana"],
            treatment_strategies=["Early planning", "Local agents", "Regulatory liaison"],
            key_mitigation="Early permit submission + local regulatory experts"
        ),
        RiskTaxonomyNode(
            code="REG-COMPLIANCE-CHANGE",
            name="Regulatory Change/New Standard",
            domain=RiskDomain.REGULATORY,
            operation_types=["WINDMILL_INSTALLATION", "CABLE_LAYING", "ALL"],
            typical_probability=(0.05, 0.2),
            typical_cost_impact_usd=(1_000_000, 5_000_000),
            typical_time_impact_days=(3, 15),
            indicators=["new standard", "regulation change", "compliance"],
            historical_examples=["ISO 29001 qualification required"],
            treatment_strategies=["Due diligence", "Legal review", "Specialist contractors"],
            key_mitigation="Early regulatory assessment + pre-qualification"
        ),
    ]
    
    COMMERCIAL = [
        RiskTaxonomyNode(
            code="COM-COST-ESCALATION",
            name="Cost Escalation/Budget Overrun",
            domain=RiskDomain.COMMERCIAL,
            operation_types=["ALL"],
            typical_probability=(0.2, 0.5),
            typical_cost_impact_usd=(1_000_000, 10_000_000),
            typical_time_impact_days=(0, 0),
            indicators=["cost overrun", "budget", "escalation", "inflation"],
            historical_examples=["Project budget 20% overrun"],
            treatment_strategies=["Contingency buffer", "Hedging", "Value engineering"],
            key_mitigation="10-15% contingency budget + quarterly cost reviews"
        ),
        RiskTaxonomyNode(
            code="COM-LD-PENALTY",
            name="Liquidated Damages (Late Delivery)",
            domain=RiskDomain.COMMERCIAL,
            operation_types=["ALL"],
            typical_probability=(0.05, 0.15),
            typical_cost_impact_usd=(500_000, 5_000_000),
            typical_time_impact_days=(0, 0),
            indicators=["delay", "late delivery", "penalty", "LD clause"],
            historical_examples=["LD triggered: 3-day delay"],
            treatment_strategies=["Schedule buffer", "Resource planning", "Contingency days"],
            key_mitigation="Conservative schedule + 10-15% contingency days"
        ),
        RiskTaxonomyNode(
            code="COM-CONTRACT-DISPUTE",
            name="Contract Interpretation/Dispute",
            domain=RiskDomain.COMMERCIAL,
            operation_types=["ALL"],
            typical_probability=(0.05, 0.20),
            typical_cost_impact_usd=(500_000, 3_000_000),
            typical_time_impact_days=(0, 0),
            indicators=["dispute", "contract", "claim", "variation"],
            historical_examples=["Scope ambiguity led to claim"],
            treatment_strategies=["Clear contract", "Change control", "Documentation"],
            key_mitigation="Jointly agreed contract + weekly scope reviews + variation process"
        ),
    ]
    
    HSE = [
        RiskTaxonomyNode(
            code="HSE-PERSONNEL-INJURY",
            name="Personnel Injury/Incident",
            domain=RiskDomain.HSE,
            operation_types=["ALL"],
            typical_probability=(0.05, 0.15),
            typical_cost_impact_usd=(1_000_000, 5_000_000),
            typical_time_impact_days=(1, 10),
            indicators=["injury", "accident", "incident", "near-miss"],
            historical_examples=["Onboard injury incident"],
            treatment_strategies=["HSE procedures", "Training", "Supervision"],
            key_mitigation="SHEQ plan + toolbox talks + incident investigation"
        ),
        RiskTaxonomyNode(
            code="HSE-ENVIRONMENTAL-BREACH",
            name="Environmental Breach",
            domain=RiskDomain.HSE,
            operation_types=["ALL"],
            typical_probability=(0.02, 0.10),
            typical_cost_impact_usd=(2_000_000, 10_000_000),
            typical_time_impact_days=(5, 20),
            indicators=["spill", "environmental", "discharge", "pollution"],
            historical_examples=["Oil spill investigation"],
            treatment_strategies=["Environmental procedures", "Spill response", "Prevention"],
            key_mitigation="Environmental management system + spill kits + drills"
        ),
    ]
    
    MARKET = [
        RiskTaxonomyNode(
            code="MKT-FUEL-PRICE",
            name="Fuel Price Volatility",
            domain=RiskDomain.MARKET,
            operation_types=["ALL"],
            typical_probability=(0.8, 1.0),
            typical_cost_impact_usd=(500_000, 2_000_000),
            typical_time_impact_days=(0, 0),
            indicators=["fuel", "price", "escalation", "commodity"],
            historical_examples=["Fuel cost 30% increase 2026"],
            treatment_strategies=["Hedging", "Fuel adjustment clause", "Efficiency"],
            key_mitigation="Fuel price pass-through clause + efficiency measures"
        ),
        RiskTaxonomyNode(
            code="MKT-INSURANCE-COST",
            name="Insurance Premium Increase",
            domain=RiskDomain.MARKET,
            operation_types=["ALL"],
            typical_probability=(0.3, 0.7),
            typical_cost_impact_usd=(500_000, 1_500_000),
            typical_time_impact_days=(0, 0),
            indicators=["insurance", "premium", "deductible", "CAR"],
            historical_examples=["CAR premium 25% increase"],
            treatment_strategies=["Early insurance placement", "Claims history"],
            key_mitigation="Early insurance tender + claims management"
        ),
    ]
    
    @classmethod
    def get_all_nodes(cls) -> List[RiskTaxonomyNode]:
        """Return all taxonomy nodes."""
        return (
            cls.VESSEL_EQUIPMENT +
            cls.OPERATIONAL +
            cls.ENVIRONMENTAL +
            cls.REGULATORY +
            cls.COMMERCIAL +
            cls.HSE +
            cls.MARKET
        )
    
    @classmethod
    def find_by_code(cls, code: str) -> Optional[RiskTaxonomyNode]:
        """Find taxonomy node by code."""
        for node in cls.get_all_nodes():
            if node.code == code:
                return node
        return None
    
    @classmethod
    def find_by_keywords(cls, keywords: List[str]) -> List[RiskTaxonomyNode]:
        """Find taxonomy nodes matching keywords."""
        results = []
        keywords_lower = [kw.lower() for kw in keywords]
        for node in cls.get_all_nodes():
            # Check indicators
            for indicator in node.indicators:
                if any(kw in indicator.lower() for kw in keywords_lower):
                    results.append(node)
                    break
            # Check name
            if any(kw in node.name.lower() for kw in keywords_lower):
                if node not in results:
                    results.append(node)
        return results
