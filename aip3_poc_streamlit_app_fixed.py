
import streamlit as st
from openai import OpenAI
import os

# Load API key from Streamlit secrets (or fallback to environment variable)
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Reference mock data
reference_data = {
    "CRM System": [
        "The system shall support multi-channel communication (email, SMS, chat).",
        "The system must log all interactions for audit trail purposes."
    ],
    "Security": [
        "All data must be encrypted at rest and in transit.",
        "Role-based access controls shall be enforced."
    ]
}

# Compliance checklist
compliance_requirements = {
    "IM8": ["Data encryption", "Access control", "Audit logging"],
    "AGC COC": ["Asset classification", "Third-party risk", "Business continuity"]
}

st.title("🧠 AIP³ - AI Partner for Public Procurement (PoC)")
st.subheader("Generate & Check Draft Procurement Clauses")

# Input area
prompt = st.text_area("Enter your requirement prompt:", "Draft functional requirements for a CRM system.")

if st.button("Generate Draft"):
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a Singapore government procurement officer drafting IT specifications."},
                {"role": "user", "content": prompt}
            ]
        )
        draft = response.choices[0].message.content
        st.success("Generated Draft:")
        st.write(draft)

        # Compliance Check
        st.subheader("✅ Compliance Check")
        for standard, checks in compliance_requirements.items():
            st.markdown(f"**{standard} Requirements Check:**")
            for item in checks:
                if item.lower() in draft.lower():
                    st.markdown(f"- ✅ `{item}` present")
                else:
                    st.markdown(f"- ❌ `{item}` missing")

        # Reference Clauses
        st.subheader("📚 Reference Clauses from Past Tenders")
        for topic, examples in reference_data.items():
            st.markdown(f"**{topic}:**")
            for example in examples:
                st.markdown(f"- 📄 _{example}_")

    except Exception as e:
        st.error(f"Error generating draft: {str(e)}")
