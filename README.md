# Offshore Risk Intelligence Agent

This repository is a starter platform for an AI-powered offshore risk intelligence agent focused on global offshore operations such as:

- wind turbine installation
- offshore cable laying
- heavy lift and marine spread work
- FPSO hook-up and station keeping
- subsea installation and marine logistics

The goal is to monitor global public information, extract risk signals from news, classify them against a domain taxonomy, estimate cost and schedule impact, benchmark against peer patterns, and recommend corrective actions.

## Capability goals

- global offshore risk monitoring
- event extraction from general industry news and public sources
- operation-specific risk classification
- financial impact and delay estimation
- benchmark vs typical peer behavior
- risk ranking and prioritized corrective actions
- dashboard for executive decision support

## Repository structure

```text
.
├── agents/
│   └── risk_orchestrator.py
├── app.py
├── dashboard/
│   └── streamlit_app.py
├── data/
│   └── sample_incidents.json
├── models/
│   ├── financial_impact.py
│   └── offshore_taxonomy.py
├── services/
│   └── source_registry.py
├── README.md
├── requirements.txt
└── run_demo.py
```

## Recommended architecture

1. Data ingestion module
   - maritime news
   - regulatory / permit changes
   - weather and site constraints
   - vessel schedule and outages
   - company disclosures and incident reports

2. Risk extraction and classification
   - NLP-based extraction from text
   - map against offshore risk taxonomy
   - assign likely operation type and risk category

3. Impact modeling
   - direct cost estimate
   - indirect delay cost
   - schedule impact (days)
   - probability of recurrence and severity

4. Benchmarking engine
   - compare with peer cases
   - benchmark cost, downtime, and response pattern

5. Decisioning layer
   - risk register
   - Monte Carlo style scenario output
   - corrective action prioritization

## Example use case

```python
from agents.risk_orchestrator import OffshoreRiskAgent

agent = OffshoreRiskAgent()

result = agent.analyze_case(
    operation_type='windmill_installation',
    region='North Sea',
    incident_summary='Installation vessel experienced DP failure during turbine nacelle lift. 3-day delay and estimated repair cost of 2.4M USD.'
)

print(result)
```

## Run dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/streamlit_app.py
```

## Run demo

```bash
python run_demo.py
```

## Intended output

The system is designed to produce structured outputs such as:

- risk title and category
- operation type and geography
- cost band and time delay band
- severity and likelihood
- benchmark comparison
- corrective actions
- risk score and priority

## Example data sources to add later

- Reuters / Bloomberg offshore and energy news
- DNV / ABS / Lloyd's Register reports
- MarineTraffic and VesselFinder
a- IMCA, DROPS, and incident databases
- regulator and port authority bulletins
- operator public filings and statements

## Product direction

This repository is intended as a global offshore risk intelligence foundation, not a single project-specific ORR. It is designed to support a broader portfolio of risk monitoring across multiple offshore domains.
