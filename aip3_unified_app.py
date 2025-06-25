
# Trigger rebuild

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

# Navigation
page = st.sidebar.selectbox("Go to page:", [
    "📄 Business Requirements Viewer",
    "✅ Compliance Check Simulation",
    "🤖 Draft Generator (AI)"
])

# Business Requirements Page
if page == "📄 Business Requirements Viewer":
    st.title("📄 Part 2, Chapter 3 - Business Requirements: CRM System")

    st.sidebar.header("References")
    st.sidebar.markdown("🔘 **Custom CRM Solution – Ministry of Finance**")
    st.sidebar.markdown("🔵 **Procurement System – Agency for Digital Services**")
    st.sidebar.markdown("🟡 **Client Management Portal – Municipal Council**")

    st.markdown("""
    To a custom-developed Customer Relationship Management (CRM) system will manage interactions,
    relationships, and data related to the organization’s clients.

    ### Customizing custom-developed CRM system:
    1. The CRM system must centralize client data in a single, unified platform.  
    2. The system should be capable of tracking and managing client interactions across various channels.  
    3. A comprehensive reporting and analytics tool must be included to provide insights into client-related activities.
    """)

# Compliance Check Page
elif page == "✅ Compliance Check Simulation":
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
    st.dataframe(df, use_container_width=True)

# Draft Generator Page
elif page == "🤖 Draft Generator (AI)":
    st.title("🤖 AI-Powered Draft Generator")

    prompt = st.text_area("Enter your procurement requirement prompt:", "Draft business requirements for a CRM system.")

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

