
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
        # Filter results
        if vendor:
            filtered = mock_tenders[
                mock_tenders["Keywords"].str.contains(topic, case=False, na=False)
                & mock_tenders["Keywords"].str.contains(vendor, case=False, na=False)
            ]
        else:
            filtered = mock_tenders[
                mock_tenders["Keywords"].str.contains(topic, case=False, na=False)
            ]

        st.success(f"Found {len(filtered)} matching tenders.")
        st.dataframe(filtered[["Agency", "Title", "Year", "Extract"]], use_container_width=True)

        for i, row in filtered.iterrows():
            st.markdown(f"**🔹 Tender:** {row['Title']} ({row['Agency']}, {row['Year']})")
            st.markdown(f"> _{row['Extract']}_")
            st.markdown(f"**✨ Suggested Prompt:** `{row['Recommended Spec Prompt']}`")
            
            if st.button(f"Use this Prompt for Draft Generator", key=f"use_prompt_{i}"):
                st.session_state["selected_prompt"] = row["Recommended Spec Prompt"]
                st.success("✅ Loaded into Draft Generator tab.")
    else:
        st.info("Enter a topic to begin searching.")

   
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
    prompt = st.text_area("Prompt", value=default_prompt)if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = example_prompts["CRM System"]

# Use selected prompt if exists, else fallback to example for selected use case
selected_use_case_prompt = example_prompts.get(use_case, "")
default_prompt = st.session_state.get("selected_prompt", selected_use_case_prompt)

prompt = st.text_area("Prompt", value=default_prompt, key="draft_prompt")

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
    st.markdown("- ✅ Compliant\n- ⚠️ Partial\n- ❌ Non-compliant")

    clause_filter = st.multiselect("Filter by Status", ["✅", "⚠️", "❌"], default=["✅", "⚠️", "❌"])
    filtered_df = df[df["Status"].isin(clause_filter)]
    st.dataframe(filtered_df, use_container_width=True)

# Page 4: Evaluation Assistant
with tabs[3]:
    st.subheader("📝 Evaluation Assistant")
    st.markdown("Upload vendor proposals and define evaluation criteria to simulate scoring and shortlisting.")

    # Upload proposals
    proposal_files = st.file_uploader("📤 Upload Vendor Proposals (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True)

    # Define criteria
    st.markdown("### 🧮 Define Evaluation Criteria")
    criteria = st.text_area("Enter criteria (comma-separated)", value="Cost, Team Size, Solution Quality")

    # Simulated processing
    if st.button("Evaluate Proposals"):
        if not proposal_files or not criteria:
            st.warning("Please upload at least one proposal and enter evaluation criteria.")
        else:
            st.success(f"✅ {len(proposal_files)} proposals received")
            parsed_criteria = [c.strip() for c in criteria.split(",")]

            # Simulated output (mocked scores)
            st.markdown("### 📊 Evaluation Results (Simulated)")
            eval_data = pd.DataFrame([
                {"Vendor": f"Vendor {i+1}", **{crit: f"{round(70 + 10*i + j*2)}" for j, crit in enumerate(parsed_criteria)}}
                for i in range(len(proposal_files))
            ])
            st.dataframe(eval_data, use_container_width=True)
            st.info("Scores are randomly simulated for demo purposes.")

# Page 5: Workflow Integration
with tabs[4]:
    st.subheader("🔄 Workflow (Coming Soon)")
    st.info("This section will support one-click export to GeBIZ-ready formats and integrate workflow routing with SGTS and internal systems.")
