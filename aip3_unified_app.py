
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
st.sidebar.title("🧭 AIP³ Assistant")

page = st.sidebar.radio("Choose function:", [
    "📘 Document Viewer",
    "✅ Compliance Simulation",
    "🤖 Draft Generator",
    "📝 Evaluation Assistant (Coming Soon)",
    "🔄 Workflow (Coming Soon)"
])

# Page 1: Document Viewer
if page == "📘 Document Viewer":
    st.title("📘 Business Requirements Viewer")

    st.subheader("Search Past Tenders")
    agency = st.selectbox("Select Agency", ["MOF", "MOE", "MOM", "HDB", "GovTech"])
    category = st.selectbox("Select Product Type", ["CRM", "Cloud Hosting", "Integration", "Exit Mgmt"])

    st.markdown(f"🔍 Showing results for **{agency}** – *{category}*")

    mock_results = pd.DataFrame([
        {"Tender Title": "CRM for Ground Ops", "Agency": "MOF", "Year": 2022, "Extract": "Client data unification required"},
        {"Tender Title": "SaaS Exit Management", "Agency": "MOE", "Year": 2023, "Extract": "All assets must be tagged for exit"},
        {"Tender Title": "Integrated Cloud Hosting", "Agency": "GovTech", "Year": 2024, "Extract": "Govinfra GCC hosting mandatory"}
    ])

    filtered = mock_results[(mock_results["Agency"] == agency) & (mock_results["Tender Title"].str.contains(category.split()[0], case=False))]
    st.dataframe(filtered, use_container_width=True)

    st.divider()

    st.subheader("Tender Clause Extractor (Optional)")
    clause_text = st.text_area("Paste tender clause for analysis (optional):")

    if st.button("Extract Key Requirement"):
        if client:
            with st.spinner("Extracting..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're a government procurement analyst. Summarize and classify tender clauses."},
                        {"role": "user", "content": clause_text}
                    ]
                )
                st.success("Extracted Insight:")
                st.write(response.choices[0].message.content)
        else:
            st.warning("OpenAI client not initialized. Check API key.")

# Page 2: Compliance Checker
elif page == "✅ Compliance Simulation":
    st.title("✅ Compliance Check Simulation")

    selected_tab = st.radio("Choose Standard:", ["IM8 Checks", "AGC COC Checks"])

    if selected_tab == "IM8 Checks":
        data = {
            "Tender Section": ["4. Security", "8. System Availability", "3. Technical"],
            "Clause": ["4.2", "8.1", "3.5"],
            "Status": ["❌", "⚠️", "✅"],
            "Remarks": [
                "Missing data encryption clause (IM8 Section 4.1)",
                "Availability target below IM8 minimum 99.5%",
                "Aligns with IM8 cloud zoning (Govinfra–GCC)"
            ]
        }
    else:
        data = {
            "Tender Section": ["5. Maintenance", "6. Testing", "4. Security"],
            "Clause": ["5.3", "6.2", "4.5"],
            "Status": ["⚠️", "✅", "❌"],
            "Remarks": [
                "Lacks clear maintenance SLA reference (COC Part 1.A Clause 3)",
                "Includes acceptance test framework (COC Part 1.B Clause 2.1)",
                "Does not mention asset protection tagging (COC Part 1.B Clause 7)"
            ]
        }

    df = pd.DataFrame(data)

    st.markdown("### Clause Legend")
    st.markdown("- ✅ Compliant\n- ⚠️ Partial\n- ❌ Non-compliant")

    clause_filter = st.multiselect("Filter by Status", ["✅", "⚠️", "❌"], default=["✅", "⚠️", "❌"])
    filtered_df = df[df["Status"].isin(clause_filter)]
    st.dataframe(filtered_df, use_container_width=True)

# Page 3: AI Draft Generator
elif page == "🤖 Draft Generator":
    st.title("🤖 AI-Powered Draft Generator")

    use_case = st.selectbox("Select Use Case", ["CRM System", "Cloud Hosting", "Exit Management", "Integration Services"])
    example_prompts = {
        "CRM System": "Draft business requirements for a CRM system.",
        "Cloud Hosting": "Draft specs for cloud-native application hosting on GCC.",
        "Exit Management": "Write clauses for service transition and exit obligations.",
        "Integration Services": "Draft specs for data and system integration services."
    }

    prompt = st.text_area("Prompt", value=example_prompts[use_case])

    if st.button("Generate Draft"):
        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a government procurement officer drafting tender specifications."},
                        {"role": "user", "content": prompt}
                    ]
                )
                draft = response.choices[0].message.content
                st.success("Generated Draft:")
                st.write(draft)
            except Exception as e:
                st.error(f"Error generating draft: {str(e)}")
        else:
            st.warning("OpenAI client not initialized. Check API key.")

# Page 4: Evaluation Assistant (Coming Soon)
elif page == "📝 Evaluation Assistant (Coming Soon)":
    st.title("📝 Evaluation Assistant")
    st.info("This section will guide officers on scorecard criteria, vendor scoring, and justification summaries.")

# Page 5: Workflow Integration Placeholder
elif page == "🔄 Workflow (Coming Soon)":
    st.title("🔄 GeBIZ / SG Tech Stack Integration")
    st.info("This section will support one-click export to GeBIZ-ready formats and integrate workflow routing with SGTS and internal systems.")
