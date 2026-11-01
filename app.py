from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from services.benchmark_engine import BenchmarkEngine
from services.global_risk_db import GlobalRiskDatabase
from services.risk_linkage import RiskLinkageEngine
from services.tender_risk_manager import TenderRiskManager


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


@st.cache_data
def load_tenders():
    with (DATA_DIR / "project_tenders.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


st.set_page_config(page_title="Offshore Risk Intelligence", page_icon="🌊", layout="wide")
st.title("🌊 Offshore Risk Intelligence Dashboard")
st.caption("Project-linked offshore risk intelligence with global benchmark comparison and evidence-backed matches.")

# Setup
risk_db = GlobalRiskDatabase(str(BASE_DIR))
benchmark_engine = BenchmarkEngine(risk_db.get_all_events())
linkage_engine = RiskLinkageEngine(risk_db)
manager = TenderRiskManager(risk_db, linkage_engine, benchmark_engine)
projects = manager.load_tenders(DATA_DIR / "project_tenders.json")
project_summaries = [manager.build_tender_summary(project) for project in projects]

selected_project = st.selectbox("Project / tender", [item["project_name"] for item in project_summaries])
selected_summary = next(item for item in project_summaries if item["project_name"] == selected_project)

project_value = selected_summary["project_value_usd"]
project_total_cost = selected_summary["summary"]["total_risk_cost_usd"]
project_delay = selected_summary["summary"]["max_delay_days"]
project_high_risk_count = selected_summary["summary"]["high_risk_count"]

st.subheader("Project overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Tender value", f"${project_value:,.0f}")
col2.metric("Risk cost exposure", f"${project_total_cost:,.0f}")
col3.metric("Max delay", f"{project_delay} days")
col4.metric("High / critical", project_high_risk_count)

st.subheader("Project risk register")
for risk in selected_summary["risks"]:
    with st.expander(f"{risk['title']} — {risk['severity']} | {risk['risk_category']}"):
        st.markdown(f"**Operation:** `{risk['operation_type']}`")
        st.markdown(f"**Region:** `{risk['region']}`")
        st.markdown(f"**Likelihood:** {risk['likelihood']}")
        st.markdown(f"**Likely cost:** ${risk['likely_cost_usd']:,} USD")
        st.markdown(f"**Likely delay:** {risk['likely_delay_days']} days")
        st.markdown(f"**Worst cost:** ${risk['worst_cost_usd']:,} USD")
        st.markdown(f"**Worst delay:** {risk['worst_delay_days']} days")
        st.write("**Triggers:**")
        for trigger in risk.get("triggers", []):
            st.write(f"- {trigger}")
        st.write("**Recommended actions:**")
        for action in risk.get("recommended_actions", []):
            st.write(f"- {action}")

        benchmark = risk.get("benchmark")
        if benchmark:
            st.write("**Benchmark comparison:**")
            st.write(benchmark["benchmark_text"])
            st.write(f"Median cost: ${benchmark['median_cost_usd']:.0f} USD")
            st.write(f"P90 cost: ${benchmark['p90_cost_usd']:.0f} USD")
            st.write(f"Median delay: {benchmark['median_delay_days']:.1f} days")
            st.write(f"P90 delay: {benchmark['p90_delay_days']:.1f} days")
            if benchmark.get("common_triggers"):
                st.write("Common triggers:")
                for item in benchmark["common_triggers"]:
                    st.write(f"- {item}")
            if benchmark.get("common_actions"):
                st.write("Common actions:")
                for item in benchmark["common_actions"]:
                    st.write(f"- {item}")

        related_events = risk.get("related_events", [])
        if related_events:
            st.write("**Matching global events:**")
            for match in related_events:
                st.markdown(
                    f"- [{match['title']}]({match['source_url']}) — score {match['score']:.2f} | "
                    f"{match['region']} | {match['source']}"
                )
                st.write(match["evidence_excerpt"])
                st.write("Reasons:")
                for reason in match.get("reasons", []):
                    st.write(f"- {reason}")

st.subheader("Global offshore watch")
all_events = risk_db.get_all_events()
for event in all_events:
    with st.expander(f"{event['title']} — {event['operation_type']} ({event['region']})"):
        st.write(event["incident_summary"])
        st.write(f"**Risk category:** {event['risk_category']}")
        st.write(f"**Severity:** {event['severity']}")
        st.write(f"**Financial impact:** ${event['financial_impact_usd']:,} USD")
        st.write(f"**Delay impact:** {event['delay_days']} days")
        st.write(f"**Source:** [{event['source_name']}]({event['source_url']})")
        st.write(f"**Evidence:** {event['evidence_excerpt']}")
        if event.get("reference_links"):
            st.write("**Related references:**")
            for ref in event["reference_links"]:
                st.markdown(f"- [{ref['label']}]({ref['url']})")

st.subheader("Global benchmark overview")
benchmarks = benchmark_engine.build_benchmarks()
for name, value in sorted(benchmarks.items()):
    st.markdown(f"**{value.operation_type} / {value.risk_category}**")
    st.write(f"Median cost: ${value.median_cost_usd:,.0f} USD | Median delay: {value.median_delay_days:.1f} days")
    st.write(f"P90 cost: ${value.p90_cost_usd:,.0f} USD | P90 delay: {value.p90_delay_days:.1f} days")
    st.write(value.benchmark_text)
    st.write("")
