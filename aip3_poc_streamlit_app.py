
import streamlit as st
import openai
import json

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

# Load reference clauses (mock)
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

# Load compliance requirements (mock)
compliance_requirements = {
    "IM8": ["Data encryption", "Access control", "Audit logging"],
    "AGC COC": ["Asset classification", "Third-party risk", "Business continuity"]
}

st.title("🧠 AIP³ - AI Partner for Public Procurement (PoC)")
st.subheader("Generate & Check Draft Procurement Clauses")

# Step 1: Input prompt
prompt = st.text_area("Enter your requirement prompt:", "Draft functional requirements for a CRM system.")

if st.button("Generate Draft"):
    # GPT Call
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a Singapore government procurement officer drafting IT specifications."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        draft = response['choices'][0]['message']['content']
        st.success("Generated Draft:")
        st.write(draft)
    except Exception as e:
        st.error(f"Error: {str(e)}")

    # Step 2: Compliance Check (Mock)
    st.subheader("✅ Compliance Check")
    for standard, clauses in compliance_requirements.items():
        st.markdown(f"**{standard} Requirements Check:**")
        for clause in clauses:
            if clause.lower() in draft.lower():
                st.markdown(f"- ✅ `{clause}` present")
            else:
                st.markdown(f"- ❌ `{clause}` missing")

    # Step 3: Reference Clauses
    st.subheader("📚 Reference Clauses from Past Tenders")
    for topic, refs in reference_data.items():
        st.markdown(f"**{topic}:**")
        for ref in refs:
            st.markdown(f"- 📄 _{ref}_")
