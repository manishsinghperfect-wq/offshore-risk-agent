from __future__ import annotations

import statistics
from typing import Dict, List

from schemas.global_risk import BenchmarkComparison


class BenchmarkEngine:
    """Builds benchmark comparisons from global offshore event data."""

    def __init__(self, events: List[Dict]):
        self.events = events

    def build_benchmarks(self) -> Dict[str, BenchmarkComparison]:
        grouped: Dict[tuple[str, str], List[Dict]] = {}
        for event in self.events:
            key = (event["operation_type"], event["risk_category"])
            grouped.setdefault(key, []).append(event)

        output: Dict[str, BenchmarkComparison] = {}
        for (operation_type, category), items in grouped.items():
            costs = [float(item["financial_impact_usd"]) for item in items]
            delays = [float(item["delay_days"]) for item in items]
            triggers = []
            actions = []
            for item in items:
                triggers.extend(item.get("triggers", []))
                actions.extend(item.get("recommended_actions", []))

            benchmark = BenchmarkComparison(
                operation_type=operation_type,
                risk_category=category,
                median_cost_usd=statistics.median(costs),
                p90_cost_usd=max(costs) if len(costs) == 1 else sorted(costs)[int(0.9 * (len(costs) - 1))],
                median_delay_days=statistics.median(delays),
                p90_delay_days=max(delays) if len(delays) == 1 else sorted(delays)[int(0.9 * (len(delays) - 1))],
                benchmark_text=(
                    f"Typical events in {operation_type} for {category} cluster around "
                    f"${statistics.median(costs):,.0f} USD and {statistics.median(delays):.1f} days delay."
                ),
                common_triggers=list(dict.fromkeys(triggers))[:5],
                common_actions=list(dict.fromkeys(actions))[:5],
                confidence=0.78,
            )
            output[f"{operation_type}:{category}"] = benchmark
        return output

    def benchmark_for_risk(self, operation_type: str, risk_category: str) -> BenchmarkComparison | None:
        bench = self.build_benchmarks()
        return bench.get(f"{operation_type}:{risk_category}")
