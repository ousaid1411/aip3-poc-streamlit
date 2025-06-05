
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AIP³ Assistant", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Go to page:", ["📄 Business Requirements", "✅ Compliance Check Simulation"])

# Page 1: Business Requirements Viewer
if page == "📄 Business Requirements":
    st.title("📄 Part 2, Chapter 3 - Business Requirements: CRM System")

    # Sidebar references
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

# Page 2: Compliance Check Table
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
    else:  # AGC COC Checks
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
