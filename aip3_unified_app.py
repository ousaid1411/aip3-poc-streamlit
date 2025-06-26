
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
    "🔎 Research & Reference",
    "🤖 Draft Generator",
    "✅ Compliance Simulation",
    "📝 Evaluation Assistant",
    "🔄 Workflow (Coming Soon)"
])


# Page 1: Research & Reference Viewer
@st.cache_data
def load_mock_data():
    return pd.read_csv("mock_tender_data.csv")

mock_tenders = load_mock_data()


with tabs[0]:
    st.subheader("🔎 Research & Reference (Past Tender Search)")
    st.markdown("Search across past tender specifications and evaluation criteria using topic prompts and optional vendor keywords.")

    topic = st.text_input("Enter topic or keyword (e.g. CRM, Cloud, ServiceNow):", "")
    vendor = st.text_input("Optional: Enter vendor name (e.g. IBM, Salesforce):", "")

    if topic:
        filtered = mock_tenders[
            mock_tenders["Keywords"].str.contains(topic, case=False, na=False)
            & mock_tenders["Keywords"].str.contains(vendor, case=False, na=False)
            if vendor else
            mock_tenders["Keywords"].str.contains(topic, case=False, na=False)
        ]

        st.success(f"Found {len(filtered)} matching tenders.")
        st.dataframe(filtered[["Agency", "Title", "Year", "Extract"]], use_container_width=True)

        for i, row in filtered.iterrows():
            st.markdown(f"**🔹 Recommended Spec Prompt:** {row['Recommended Spec Prompt']}")
            if st.button(f"Use for Draft Generator ({row['Title']})", key=f"btn_{i}"):
                st.session_state["selected_prompt"] = row["Recommended Spec Prompt"]
    else:
        st.info("Enter a topic above to begin searching.")

    st.markdown("Search across past tender specifications and evaluation criteria using topic prompts and optional vendor keywords.")

    topic = st.text_input("Enter topic or specification keyword (e.g., CRM, exit mgmt, integration):", "")
    vendor = st.text_input("Optional: Enter vendor keyword (e.g., IBM, ServiceNow):", "")

    sample_tenders = pd.DataFrame([
        {"Agency": "MOF", "Title": "CRM for Licensing Ops", "Spec Match": "CRM, citizen interaction", "Vendors": "Salesforce"},
        {"Agency": "MOM", "Title": "Integration Platform", "Spec Match": "Integration, event bus", "Vendors": "IBM"},
        {"Agency": "MOE", "Title": "Exit Management for SaaS", "Spec Match": "exit, offboarding", "Vendors": "NA"},
        {"Agency": "GovTech", "Title": "Cloud Hosting Services", "Spec Match": "GCC, cloud-native", "Vendors": "AWS"}
    ])

    results = sample_tenders[
        sample_tenders["Spec Match"].str.contains(topic, case=False, na=False)
        & sample_tenders["Vendors"].str.contains(vendor, case=False, na=False)
        if vendor else
        sample_tenders["Spec Match"].str.contains(topic, case=False, na=False)
    ]

    if topic:
        st.success(f"Found {len(results)} matching tenders.")
        st.dataframe(results, use_container_width=True)

        if client:
            st.markdown("### ✨ Suggested Clauses or Specs (AI Generated)")
            prompt_text = f"Suggest procurement specification clauses for {topic} tenders"
            if vendor:
                prompt_text += f" involving {vendor}"

            with st.spinner("Generating suggestions..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a procurement assistant. Suggest standard clauses based on the topic."},
                        {"role": "user", "content": prompt_text}
                    ]
                )
                st.write(response.choices[0].message.content)
    else:
        st.info("Enter a topic above to begin searching.")

# Page 2: Draft Generator
with tabs[1]:
    st.subheader("🤖 AI-Powered Draft Generator")

    use_case = st.selectbox("Select Use Case", ["CRM System", "Cloud Hosting", "Exit Management", "Integration Services"])
    example_prompts = {
        "CRM System": "Draft business requirements for a CRM system.",
        "Cloud Hosting": "Draft specs for cloud-native application hosting on GCC.",
        "Exit Management": "Write clauses for service transition and exit obligations.",
        "Integration Services": "Draft specs for data and system integration services."
    }

    default_prompt = st.session_state.get("selected_prompt", example_prompts[use_case])
prompt = st.text_area("Prompt", value=default_prompt)
    draft_output = ""

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
                draft_output = response.choices[0].message.content
                st.success("Generated Draft:")
                edited = st.text_area("Edit Draft Below (Optional)", value=draft_output, height=300)
                st.download_button("📥 Download Draft as TXT", edited, file_name="draft_spec.txt")
            except Exception as e:
                st.error(f"Error generating draft: {str(e)}")
        else:
            st.warning("OpenAI client not initialized. Check API key.")

# Page 3: Compliance Checker
with tabs[2]:
    st.subheader("✅ Compliance Check Simulation")

    st.markdown("This simulation reviews a tender draft for compliance gaps against IM8 or AGC COC.")
    review_source = st.radio("Select Source:", ["Use generated draft", "Upload tender copy"])

    if review_source == "Upload tender copy":
        uploaded_file = st.file_uploader("Upload a tender document (PDF or text)", type=["pdf", "txt"])
        if uploaded_file:
            st.info(f"Uploaded file: {uploaded_file.name}")
            st.success("✔️ Document parsed successfully (simulated). Proceeding to clause review...")

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
    st.markdown("- ✅ Compliant
- ⚠️ Partial
- ❌ Non-compliant")

    clause_filter = st.multiselect("Filter by Status", ["✅", "⚠️", "❌"], default=["✅", "⚠️", "❌"])
    filtered_df = df[df["Status"].isin(clause_filter)]
    st.dataframe(filtered_df, use_container_width=True)

# Page 4: Evaluation Assistant
with tabs[3]:
    st.subheader("📝 Evaluation Assistant")

    st.markdown("This section helps simulate how vendor proposals might be evaluated based on:")
    st.markdown("- 💰 Cost structure")
    st.markdown("- 👥 Team composition")
    st.markdown("- 🧠 Solution quality")
    st.markdown("---")

    st.subheader("📊 Mock Vendor Evaluation Table")

    eval_data = pd.DataFrame([
        {"Vendor": "Alpha Tech", "Cost (SGD)": 180000, "Team Size": 6, "Score": 84, "Remarks": "Good price-to-value ratio"},
        {"Vendor": "Beta Solutions", "Cost (SGD)": 240000, "Team Size": 8, "Score": 90, "Remarks": "Strong proposal, slightly costlier"},
        {"Vendor": "GammaSoft", "Cost (SGD)": 200000, "Team Size": 5, "Score": 78, "Remarks": "Lean team, less scalable"}
    ])
    st.dataframe(eval_data, use_container_width=True)

# Page 5: Workflow Integration
with tabs[4]:
    st.subheader("🔄 Workflow (Coming Soon)")
    st.info("This section will support one-click export to GeBIZ-ready formats and integrate workflow routing with SGTS and internal systems.")
