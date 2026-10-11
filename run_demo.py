from agents.risk_orchestrator import OffshoreRiskAgent


def main():
    agent = OffshoreRiskAgent()
    sample_cases = [
        {
            "operation_type": "windmill_installation",
            "region": "North Sea",
            "incident_summary": "Installation vessel had DP failure during nacelle lift, leading to 3-day delay and 2.3M USD cost impact.",
        },
        {
            "operation_type": "cable_laying",
            "region": "Gulf of Mexico",
            "incident_summary": "Cable burial tool failure caused route interruption and 5-day schedule hit.",
        },
        {
            "operation_type": "heavy_lift",
            "region": "West Africa",
            "incident_summary": "Heavy lift rigging failure triggered safety stop and crane downtime across the campaign.",
        },
    ]

    for case in sample_cases:
        risk = agent.analyze_case(**case)
        print("\n=== Risk analysis ===")
        for key, value in risk.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
