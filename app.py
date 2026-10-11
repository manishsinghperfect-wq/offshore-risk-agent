from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from agents.risk_orchestrator import OffshoreRiskAgent

st.set_page_config(page_title="Offshore Risk Intelligence", page_icon="🌊", layout="wide")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_incidents.json"
agent = OffshoreRiskAgent()

with DATA_PATH.open() as f:
    incidents = json.load(f)

st.title("🌊 Offshore Risk Intelligence Dashboard")

operation_filter = st.selectbox(
    "Operation type",
    ["All", "windmill_installation", "cable_laying", "heavy_lift", "fpso_hookup"],
)
region_filter = st.selectbox("Region", ["All", "North Sea", "Gulf of Mexico", "West Africa", "Guyana"])

filtered = incidents
if operation_filter != "All":
    filtered = [item for item in filtered if item["operation_type"] == operation_filter]
if region_filter != "All":
    filtered = [item for item in filtered if item["region"] == region_filter]

rows = []
for item in filtered:
    result = agent.analyze_case(
        operation_type=item["operation_type"],
        region=item["region"],
        incident_summary=item["incident_summary"],
    )
    rows.append(result)

if not rows:
    st.warning("No matching incidents for the selected filters.")
    st.stop()

frame = pd.DataFrame(rows)

st.subheader("Risk overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Incidents", len(frame))
col2.metric("Avg. cost", f"${frame['financial_impact_usd'].mean():,.0f}")
col3.metric("Avg. delay", f"{frame['delay_days'].mean():.1f} days")
col4.metric("High risk count", int((frame['severity'] == 'High').sum()))

st.subheader("Risk table")
st.dataframe(
    frame[["title", "operation_type", "region", "risk_category", "severity", "likelihood", "financial_impact_usd", "delay_days"]],
    use_container_width=True,
)

st.subheader("Corrective actions")
for _, row in frame.iterrows():
    with st.expander(f"{row['title']} ({row['region']})"):
        st.write(f"Risk category: {row['risk_category']}")
        st.write(f"Financial impact: ${row['financial_impact_usd']:,.0f} USD")
        st.write(f"Delay impact: {row['delay_days']} days")
        st.write(f"Benchmark: {row['benchmark']}")
        st.write("Recommended actions:")
        for action in row["corrective_actions"]:
            st.write(f"- {action}")

st.subheader("Source coverage")
source_map = {
    "windmill_installation": ["Reuters Energy", "Offshore Engineer", "MarineTraffic"],
    "cable_laying": ["TradeWinds", "Maritime Executive", "VesselFinder"],
    "heavy_lift": ["Reuters Energy", "MarineLink", "IMCA incident database"],
    "fpso_hookup": ["Offshore Engineer", "Maritime Executive", "Port authority bulletins"],
}
selected = operation_filter if operation_filter != 'All' else 'windmill_installation'
st.write(source_map.get(selected, ["Public news", "Regulatory notices", "Incident reports"]))

