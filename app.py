import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "sample_incidents.json"


def main():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        incidents = json.load(f)

    for item in incidents:
        print(f"\n=== {item['title']} ({item['region']}) ===")
        print(f"Operation: {item['operation_type']}")
        print(f"Severity: {item['severity']}")
        print(f"Financial impact: ${item['financial_impact_usd']:,} USD")
        print(f"Delay: {item['delay_days']} days")
        print(f"Source: {item['source_name']} ({item['source_url']})")
        print(f"Evidence: {item['evidence_excerpt']}")
        print("Actions:")
        for action in item["recommended_actions"]:
            print(f"- {action}")


if __name__ == "__main__":
    main()
