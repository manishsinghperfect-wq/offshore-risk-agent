import json
from pathlib import Path

import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_incidents.json"


def load_incidents():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


st.set_page_config(page_title="Offshore Risk Intelligence", page_icon="🌊", layout="wide")
st.title("🌊 Offshore Risk Intelligence Dashboard")
st.caption("Evidence-linked offshore risk intelligence prototype for wind, cable, heavy lift and FPSO operations.")

incidents = load_incidents()
operation_filter = st.selectbox("Operation type", ["All", *sorted({i["operation_type"] for i in incidents})])
region_filter = st.selectbox("Region", ["All", *sorted({i["region"] for i in incidents})])

filtered = incidents
if operation_filter != "All":
    filtered = [item for item in filtered if item["operation_type"] == operation_filter]
if region_filter != "All":
    filtered = [item for item in filtered if item["region"] == region_filter]

if not filtered:
    st.warning("No incidents match the current filters.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Incidents", len(filtered))
col2.metric("Average cost", f"${sum(item['financial_impact_usd'] for item in filtered) / len(filtered):,.0f}")
col3.metric("Average delay", f"{sum(item['delay_days'] for item in filtered) / len(filtered):.1f} days")
col4.metric("Critical/high", sum(1 for item in filtered if item["severity"] in {"High", "Critical"}))

st.subheader("Evidence-linked risk details")
for item in filtered:
    with st.expander(f"{item['title']} — {item['region']} ({item['severity']})"):
        st.markdown(f"**Operation:** `{item['operation_type']}`")
        st.markdown(f"**Risk category:** `{item['risk_category']}`")
        st.markdown(f"**Financial impact:** ${item['financial_impact_usd']:,} USD")
        st.markdown(f"**Delay impact:** {item['delay_days']} days")
        st.markdown(f"**Likelihood:** {item['likelihood']}")
        st.markdown(f"**Benchmark:** {item['benchmark']}")
        st.write(item["incident_summary"])
        st.write("**Evidence excerpt:**")
        st.write(item["evidence_excerpt"])
        st.markdown(
            f"**Reference:** [{item['source_name']}]({item['source_url']}) | "
            f"Date: {item['source_date']} | Confidence: {item['confidence']:.0%}"
        )
        if item.get("reference_links"):
            st.write("**Related references:**")
            for ref in item["reference_links"]:
                st.markdown(f"- [{ref['label']}]({ref['url']})")
        st.write("**Recommended corrective actions:**")
        for action in item["recommended_actions"]:
            st.write(f"- {action}")

st.subheader("Source coverage")
for source_type in sorted({i["source_type"] for i in filtered}):
    names = ", ".join(sorted({i["source_name"] for i in filtered if i["source_type"] == source_type}))
    st.write(f"- **{source_type}:** {names}")
