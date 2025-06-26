
import streamlit as st
import pandas as pd
import os

# Optional: OpenAI API integration for draft generation
try:
    from openai import OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=openai_api_key)
except:
    client = None

st.set_page_config(page_title="AIP³ Unified App", layout="wide")
st.title("🤖 AIP³ — AI Partner for Public Procurement")
st.markdown("##### Navigate the key functions below:")

tabs = st.tabs([
    "📘 Document Viewer",
    "🤖 Draft Generator",
    "✅ Compliance Simulation",
    "📝 Evaluation Assistant",
    "🔄 Workflow (Coming Soon)"
])

# Page 1: Document Viewer
with tabs[0]:
    st.subheader("🔍 Research & Reference")

    st.markdown("""
    Search from just one place using natural prompts and optional keywords.
    Get matched tenders + AI-suggested clauses based on evaluation criteria.
    """)

    topic_prompt = st.text_input("Describe your topic (e.g. CRM for internal operations)", value="CRM for internal operations")
    keyword_input = st.text_input("Optional: Add specific keywords (e.g. IBM, ServiceNow)", value="IBM")

    if st.button("Search Past Tenders"):
        with st.spinner("Searching..."):
            tender_db = pd.DataFrame([
                {"Agency": "MOE", "Tender Title": "CRM for School Ops", "Year": 2022, "Keywords": "CRM, IBM"},
                {"Agency": "MOM", "Tender Title": "Workforce Mgmt Tool", "Year": 2021, "Keywords": "ServiceNow, SaaS"},
                {"Agency": "HDB", "Tender Title": "Citizen Feedback CRM", "Year": 2023, "Keywords": "CRM, GovTech"}
            ])

            filtered = tender_db[
                tender_db["Tender Title"].str.contains(topic_prompt.split()[0], case=False) |
                tender_db["Keywords"].str.contains(keyword_input, case=False)
            ]

            st.success(f"Found {len(filtered)} matching tenders:")
            st.dataframe(filtered, use_container_width=True)

            if not filtered.empty and client:
                st.markdown("### ✨ Suggested Specifications (AI-Powered)")
                combined_prompt = f"Based on tenders like: {topic_prompt} and keyword: {keyword_input}, suggest 3 key clauses to consider."
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're a government procurement expert."},
                        {"role": "user", "content": combined_prompt}
                    ]
                )
                st.info(response.choices[0].message.content)
