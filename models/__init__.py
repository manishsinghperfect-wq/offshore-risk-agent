from __future__ import annotations

from typing import Dict, List, Tuple


class OffshoreRiskTaxonomy:
    """Offshore operation risk taxonomy."""

    RISK_LIBRARY = {
        "windmill_installation": {
            "Operational": {
                "title": "Installation vessel operation disruption",
                "keywords": ["dp failure", "lift failure", "nacelle", "jack-up", "weather downtime"],
                "benchmark": "Peer projects usually see 2-8 day downtime with 1-5M USD exposure.",
                "actions": [
                    "Pre-lift vessel and crane readiness check",
                    "Add weather contingency and standby window",
                    "Validate component handling and rigging plan"
                ],
            },
            "Technical": {
                "title": "Equipment or crane outage during installation",
                "keywords": ["crane", "winch", "component failure", "equipment outage"],
                "benchmark": "Helps drive direct repair cost and reduced installation efficiency.",
                "actions": [
                    "Verify crane inspection and spare-part coverage",
                    "Pre-position critical spares and specialist technicians",
                    "Run lifting trial before critical operations"
                ],
            },
            "Weather/Environment": {
                "title": "Weather or sea-state downtime risk",
                "keywords": ["weather", "wave", "wind", "sea state", "standby"],
                "benchmark": "This is often the primary driver for schedule loss in offshore wind work.",
                "actions": [
                    "Use conservative weather limits and forecast review",
                    "Plan contingency days in campaign schedule",
                    "Re-prioritize installation sequence against forecast weather"
                ],
            },
        },
        "cable_laying": {
            "Operational": {
                "title": "Cable lay route or installation interruption",
                "keywords": ["cable damage", "route clearance", "interruption", "lay vessel", "fault"],
                "benchmark": "Route clearance and cable protection failures are common schedule drivers.",
                "actions": [
                    "Validate seabed route and burial assumptions",
                    "Carry spare cable and repair kit readiness",
                    "Review route survey and cable protection design"
                ],
            },
            "Technical": {
                "title": "Cable laying equipment or burial tool failure",
                "keywords": ["burial tool", "tensioner", "cable fault", "lay equipment", "repair"],
                "benchmark": "Equipment failures often lead to short-term downtime and expensive repair uplift.",
                "actions": [
                    "Pre-inspect cable lay equipment and tensioning systems",
                    "Verify spare part strategy for high-risk tools",
                    "Run dry test and pull-in simulation before offshore execution"
                ],
            },
            "Weather/Environment": {
                "title": "Environmental limitation on cable lay operation",
                "keywords": ["current", "weather", "heavy sea", "lay hold", "workability"],
                "benchmark": "Current and weather limits usually govern installation windows.",
                "actions": [
                    "Review metocean constraints before mobilization",
                    "Build weather downtime into schedule risk model",
                    "Set operational stop criteria based on current and wave limits"
                ],
            },
        },
        "heavy_lift": {
            "Operational": {
                "title": "Heavy lift plan or execution interruption",
                "keywords": ["lifting plan", "load out", "dropped object", "rigging", "lifting failure"],
                "benchmark": "Heavy lift incidents create high impact due to cost and safety exposure.",
                "actions": [
                    "Freeze and review lift plan with marine coordinator",
                    "Check rigging certification and planned lift sequence",
                    "Add independent lift review before critical lifts"
                ],
            },
            "Technical": {
                "title": "Crane or lifting equipment outage",
                "keywords": ["crane failure", "lifting gear", "winch failure", "hook issue"],
                "benchmark": "Lifting gear failure is a common root cause behind large schedule delay.",
                "actions": [
                    "Inspect crane and hook assemblies before lift",
                    "Maintain critical spares and skilled riggers on standby",
                    "Run trial lift and test load confirmation"
                ],
            },
            "HSE": {
                "title": "Safety incident during lifting operations",
                "keywords": ["injury", "incident", "safety", "dropped load", "man overboard"],
                "benchmark": "Safety event severity is often independent of cost but very high in consequence.",
                "actions": [
                    "Tighten permit to work and toolbox talk process",
                    "Pause operations for lifting review after near-miss",
                    "Increase supervisory coverage and exclusion zones"
                ],
            },
        },
        "fpso_hookup": {
            "Operational": {
                "title": "Hook-up or station keeping disruption",
                "keywords": ["hook-up", "station keeping", "tug", "moorings", "positioning"],
                "benchmark": "These scenarios often combine direct downtime and vessel spread cost.",
                "actions": [
                    "Run station-keeping trial and tug competence review",
                    "Validate mooring line and hook-up procedures",
                    "Plan backup vessel strategy and spares"
                ],
            },
            "Technical": {
                "title": "Vessel or dynamic positioning failure",
                "keywords": ["dp failure", "breakdown", "blackout", "engine", "propulsion"],
                "benchmark": "DP failures often lead to both schedule loss and major spread cost exposure.",
                "actions": [
                    "Perform DP trial and periodic maintenance checks",
                    "Ensure backup power and critical spare parts onboard",
                    "Assess DP reliability before mobilization"
                ],
            },
            "Commercial": {
                "title": "Delay and variation exposure",
                "keywords": ["delay", "liquidated damages", "variation", "cost escalation", "claim"],
                "benchmark": "Commercial delay risk often compounds hardware and weather risk.",
                "actions": [
                    "Define change control and variation process early",
                    "Protect weather and delay assumptions in the contract",
                    "Review LD risk and mitigation with commercial team"
                ],
            },
        },
    }

    def match_keywords(self, operation_type: str, text: str, default_category: str = "Operational") -> Dict[str, str]:
        operation = self.RISK_LIBRARY.get(operation_type, {})
        if not operation:
            return {
                "risk_category": default_category,
                "title": "General offshore risk",
            }

        best_category = default_category
        best_score = -1

        for category, details in operation.items():
            score = 0
            for keyword in details.get("keywords", []):
                if keyword.lower() in text:
                    score += 1
            if score > best_score:
                best_score = score
                best_category = category

        details = operation.get(best_category, {})
        return {
            "risk_category": best_category,
            "title": details.get("title", "General offshore risk"),
        }

    def get_benchmark_summary(self, risk_category: str, operation_type: str, region: str) -> str:
        operation = self.RISK_LIBRARY.get(operation_type, {})
        details = operation.get(risk_category, {})
        return details.get("benchmark", f"Reference benchmark for {region} offshore operations is in development.")

    def get_corrective_actions(self, risk_category: str, operation_type: str) -> List[str]:
        operation = self.RISK_LIBRARY.get(operation_type, {})
        return operation.get(risk_category, {}).get("actions", [
            "Perform detailed risk review with project and marine experts",
            "Assess required mitigation and contingency before execution"
        ])


if __name__ == "__main__":
    tax = OffshoreRiskTaxonomy()
    print(tax.match_keywords('windmill_installation', 'installation vessel had DP failure during nacelle lift and heavy weather with 3-day delay'))
