
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
    "🔄 Workflow (Coming Soon)"
])

# Page 1: Document Viewer (Placeholder for Intelligent Search & Builder)
if page == "📘 Document Viewer":
    st.title("📘 Business Requirements Viewer")

    st.sidebar.header("📂 References")
    st.sidebar.markdown("🔘 **Custom CRM Solution – Ministry of Finance**")
    st.sidebar.markdown("🔵 **Procurement System – Agency for Digital Services**")
    st.sidebar.markdown("🟡 **Client Management Portal – Municipal Council**")

    st.markdown("""
    This page showcases procurement business requirements across use cases:

    #### Example – Custom CRM System:
    1. Centralizes client data in a unified platform  
    2. Tracks and manages client interactions across channels  
    3. Includes reporting and analytics for client engagement insights  
    """)

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

# Page 4: Placeholder for Workflow
elif page == "🔄 Workflow (Coming Soon)":
    st.title("🔄 GeBIZ / SG Tech Stack Integration")
    st.info("This section will support one-click export to GeBIZ-ready formats and integrate workflow routing with SGTS and internal systems.")
