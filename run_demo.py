# Offshore Risk Intelligence Agent

This repository is a prototype platform for offshore risk intelligence focused on global offshore operations such as:

- wind turbine installation
- offshore cable laying
- heavy lift and marine spread work
- FPSO hook-up and station keeping
- subsea installation and marine logistics

The product direction is to help project teams review a tender, identify major offshore risks, benchmark against global public incidents, and prioritize corrective actions based on evidence.

## Product concept

The prototype now includes the following layers:

1. Project / tender risk register
   - risk title
   - category and severity
   - cost and delay impact
   - recommended actions
   - project risk summaries

2. Global offshore risk data
   - public-source style offshore event records
   - operation, region, and risk category mapping
   - source links and evidence excerpts

3. Benchmark engine
   - median and p90 cost and delay comparisons by operation and risk category
   - common triggers and common mitigation patterns

4. Matching engine
   - links project risks to relevant global incidents
   - scores similarity using operation type, region, category and keywords
   - shows evidence-backed reasons for matches

5. Executive dashboard
   - project overview cards
   - risk register detail
   - benchmark panel
   - global offshore watch list
   - evidence and source references

## Repository structure

```text
.
├── app.py
├── dashboard/
│   └── streamlit_app.py
├── data/
│   ├── project_tenders.json
│   └── sample_incidents.json
├── schemas/
│   └── global_risk.py
├── services/
│   ├── benchmark_engine.py
│   ├── global_risk_db.py
│   ├── risk_linkage.py
│   └── tender_risk_manager.py
├── README.md
├── requirements.txt
└── run_demo.py
```

## Run the dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/streamlit_app.py
```

or

```bash
streamlit run app.py
```

## Product view

This version is designed for a project manager or tender team to answer the following questions:

- What are the major offshore risks relevant to our tender?
- Which global incidents match our risk profile?
- What are the typical cost and delay impacts seen across the industry?
- What actions are usually used to reduce exposure?
- Which risks require immediate mitigation before commercial sign-off?

## Notes

This is a prototype using sample incident data and sample project profiles. It is designed to validate the product workflow and architecture before live-ingestion and production scale-up.
