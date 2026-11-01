import json
from pathlib import Path

from services.benchmark_engine import BenchmarkEngine
from services.global_risk_db import GlobalRiskDatabase
from services.risk_linkage import RiskLinkageEngine
from services.tender_risk_manager import TenderRiskManager


BASE_DIR = Path(__file__).resolve().parent
DB = GlobalRiskDatabase(str(BASE_DIR))
BENCH = BenchmarkEngine(DB.get_all_events())
LINK = RiskLinkageEngine(DB)
MANAGER = TenderRiskManager(DB, LINK, BENCH)


def main():
    tenders = MANAGER.load_tenders(BASE_DIR / "data" / "project_tenders.json")
    for tender in tenders:
        summary = MANAGER.build_tender_summary(tender)
        print(f"\n=== {summary['project_name']} ===")
        print(f"Project value: ${summary['project_value_usd']:,} USD")
        print(f"Risk count: {summary['summary']['risk_count']}")
        print(f"Risk cost exposure: ${summary['summary']['total_risk_cost_usd']:,} USD")
        print(f"Maximum delay: {summary['summary']['max_delay_days']} days")
        for risk in summary["risks"]:
            print(f"- {risk['title']}: {risk['severity']} / {risk['risk_category']} / {risk['likely_cost_usd']:,} USD")
            if risk.get("related_events"):
                print("  Related events:")
                for match in risk["related_events"][:2]:
                    print(f"    * {match['title']} (score {match['score']:.2f})")


if __name__ == "__main__":
    main()
