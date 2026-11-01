# Offshore Risk Intelligence Agent

This repository is a prototype platform for an AI-powered offshore risk intelligence agent focused on global offshore operations such as:

- wind turbine installation
- offshore cable laying
- heavy lift and marine spread work
- FPSO hook-up and station keeping
- subsea installation and marine logistics

The goal is to monitor public industry information, classify risk signals against an offshore taxonomy, estimate financial and schedule impact, link them to project-level risk registers, and present evidence-backed recommendations with source references.

## What this prototype does

- gathers a sample set of offshore risk events from public-source categories
- classifies them by operation type, geography and risk category
- stores cost and delay impact for each event
- links evidence and source references to each risk
- shows a dashboard for tender/project risk review
- demonstrates how project risks can be linked to global offshore exposures

## Repository structure

```text
.
├── dashboard/
│   └── streamlit_app.py
├── data/
│   └── sample_incidents.json
├── services/
│   └── source_registry.py
├── app.py
├── README.md
├── requirements.txt
├── run_demo.py
└── schemas/
    └── global_risk.py
```

## Evidence-linked model

The prototype now includes an explicit evidence layer for each offshore event:

- title
- operation type
- region
- risk category
- severity
- cost impact
- delay impact
- source name
- source URL
- source type
- evidence excerpt
- relevant references
- corrective actions

This enables a project manager or tender team to see not only the risk, but also where it came from and why it matters.

## Run the dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/streamlit_app.py
```

or run the root app:

```bash
streamlit run app.py
```

## Run the demo

```bash
python run_demo.py
```

## Example public sources included in the prototype

- Offshore Engineer
- WindEurope
- TradeWinds
- IMCA
- MarineLink
- Subsea 7
- TechnipFMC
- Boskalis
- Van Oord
- MODEC
- Shell
- Ørsted
- DNV
- MarineTraffic
- VesselFinder

These are used as representative reference sources for a prototype and demonstrate how the system can display source links and evidence panels.

## Product direction

This repository is intended as a global offshore risk intelligence foundation, not a single project-specific ORR. It is designed to support a broader portfolio of risk monitoring across multiple offshore sectors and to provide evidence-backed benchmarking for project teams.

## Notes

This is a prototype and the sample incidents are illustrative. For a production-ready system, the next step would be to add automated feeds, validated source APIs, LLM-based extraction and a proper database layer.
