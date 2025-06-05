# AIP³ - AI Partner for Public Procurement (PoC)

This is a lightweight Streamlit application that demonstrates how AIP³ can assist government officers with:
- Generating procurement draft clauses using GPT-4
- Performing mock compliance checks (IM8 and AGC COC)
- Viewing reference clauses from past tenders

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/aip3-poc-streamlit.git
cd aip3-poc-streamlit
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key

Option 1 (locally via environment variable):
```bash
export OPENAI_API_KEY=your-key-here
```

Option 2 (Streamlit Cloud):
- Go to your deployed app's settings → Secrets
- Add:
```
OPENAI_API_KEY = "your-key-here"
```

### 4. Run the app
```bash
streamlit run aip3_poc_streamlit_app_fixed.py
```

## 🌐 Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to https://streamlit.io/cloud and click "New app"
3. Select your repo and main file: `aip3_poc_streamlit_app_fixed.py`
4. Add your OpenAI API key in "Secrets"
