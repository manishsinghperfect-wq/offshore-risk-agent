from __future__ import annotations

import re
from typing import Dict, List, Optional

from schemas.global_risk import RiskMatch


class RiskLinkageEngine:
    """Matches project risks to relevant global offshore event patterns."""

    def __init__(self, database):
        self.database = database

    @staticmethod
    def _keyword_tokens(text: str) -> set[str]:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return {token for token in text.split() if len(token) > 3}

    def _match_score(self, project_risk: Dict, event: Dict) -> tuple[float, List[str]]:
        reasons: List[str] = []
        score = 0.0

        if project_risk["operation_type"] == event["operation_type"]:
            score += 0.45
            reasons.append("same operation type")
        else:
            score += 0.10

        if project_risk["region"] == event["region"]:
            score += 0.20
            reasons.append("same region")
        elif project_risk["region"] in ["North Sea", "Gulf of Mexico", "West Africa", "Guyana"] and event["region"] in ["North Sea", "Gulf of Mexico", "West Africa", "Guyana"]:
            score += 0.08
            reasons.append("similar offshore region")

        if project_risk["risk_category"] == event["risk_category"]:
            score += 0.20
            reasons.append("same risk category")

        project_tokens = self._keyword_tokens(
            " ".join([
                project_risk.get("title", ""),
                project_risk.get("risk_category", ""),
                " ".join(project_risk.get("triggers", [])),
            ])
        )
        event_tokens = self._keyword_tokens(
            " ".join([
                event.get("title", ""),
                event.get("risk_category", ""),
                event.get("incident_summary", ""),
                event.get("benchmark", ""),
            ])
        )
        overlap = project_tokens & event_tokens
        if overlap:
            score += min(0.15, len(overlap) * 0.03)
            reasons.append("keyword overlap in risk description")

        if project_risk.get("severity") == event.get("severity"):
            score += 0.05
            reasons.append("similar severity")

        return min(score, 1.0), reasons

    def match_project_risk(self, project_risk: Dict) -> List[RiskMatch]:
        matches: List[RiskMatch] = []
        events = self.database.get_all_events()
        for event in events:
            score, reasons = self._match_score(project_risk, event)
            if score >= 0.45:
                matches.append(
                    RiskMatch(
                        project_risk_id=project_risk["id"],
                        event_id=event["id"],
                        match_score=round(score, 3),
                        reasons=reasons,
                        event=event,
                    )
                )
        matches.sort(key=lambda item: item.match_score, reverse=True)
        return matches

    def match_project(self, project_risks: List[Dict]) -> Dict[str, List[RiskMatch]]:
        output: Dict[str, List[RiskMatch]] = {}
        for risk in project_risks:
            output[risk["id"]] = self.match_project_risk(risk)
        return output
