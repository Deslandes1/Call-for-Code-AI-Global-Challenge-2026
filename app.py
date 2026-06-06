import streamlit as st
import requests
import json
import re
from groq import Groq
import pandas as pd
from datetime import datetime

# ================== Page Config ==================
st.set_page_config(
    page_title="SafeHaven | Anti-Trafficking AI",
    page_icon="🛡️",
    layout="wide"
)

# ================== Custom CSS ==================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f2a48 0%, #0a192f 100%);
        border-right: 2px solid #e94560;
    }
    h1, h2, h3 {
        color: #ffd966 !important;
    }
    p, li, .stMarkdown {
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #e94560 !important;
        color: white !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        width: 100%;
    }
    .risk-box {
        background: rgba(233, 69, 96, 0.2);
        border-left: 5px solid #e94560;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .safe-box {
        background: rgba(46, 125, 50, 0.2);
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ================== Sidebar ==================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/Deslandes1/Color-Software-Game/main/Gesner%20Deslandes.png", width=80)
    st.markdown("## **GlobalInternet.py**")
    st.markdown("**SafeHaven – AI Anti-Trafficking Tool**")
    st.markdown("---")
    st.markdown("Built by **Gesner Deslandes**, Engineer-in-Chief")
    st.markdown("📞 (509) 4738 5663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. **Risk Assessment** – Describe a situation and let AI flag red flags.")
    st.markdown("2. **Report** – Anonymously submit a suspicious activity.")
    st.markdown("3. **Resources** – Find hotlines and safety plans.")

# ================== Main Title ==================
st.title("🛡️ SafeHaven")
st.markdown("## AI-Powered Early Warning & Resource Hub Against Human Trafficking")
st.markdown("---")

# ================== Groq Client ==================
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ================== Helper Function ==================
def analyze_risk(situation_text):
    """Call Groq LLM to analyze trafficking risk."""
    prompt = f"""You are an expert anti-trafficking analyst. Analyze the following situation and output a JSON object with exactly these fields:
- "risk_level": "high", "medium", "low", or "uncertain"
- "red_flags": list of specific trafficking indicators (e.g., "confiscated passport", "debt bondage", "false promises")
- "advice": one sentence of actionable advice for the user.

Situation: {situation_text}

Return ONLY valid JSON. No extra text."""
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        # Extract JSON (handle markdown code blocks)
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            result = json_match.group(0)
        data = json.loads(result)
        return data
    except Exception as e:
        return {"risk_level": "error", "red_flags": [], "advice": f"Could not analyze: {str(e)}"}

# ================== Tabs ==================
tab1, tab2, tab3 = st.tabs(["🔍 Risk Assessment", "📢 Report Suspicious Activity", "📞 Resources & Help"])

# ---------- Tab 1: Risk Assessment ----------
with tab1:
    st.markdown("### 🧠 Describe a situation you or someone you know is facing")
    situation = st.text_area("Write in your own words (Creole, English, French – AI understands):", height=150,
                             placeholder="Example: I met a recruiter who promised me a well-paid job abroad, but he asked for my passport and $500 fee...")
    if st.button("Analyze Risk", key="analyze"):
        if not situation.strip():
            st.warning("Please describe a situation.")
        else:
            with st.spinner("AI is analyzing..."):
                result = analyze_risk(situation)
            risk = result.get("risk_level", "unknown")
            flags = result.get("red_flags", [])
            advice = result.get("advice", "")
            if risk == "high":
                st.markdown(f'<div class="risk-box"><h3>⚠️ HIGH RISK ⚠️</h3><p>{advice}</p></div>', unsafe_allow_html=True)
                st.error("**Red flags detected:**")
                for flag in flags:
                    st.write(f"- {flag}")
                st.warning("**Immediate action:** Contact a local hotline (see Resources tab).")
            elif risk == "medium":
                st.markdown(f'<div class="risk-box"><h3>⚠️ MEDIUM RISK</h3><p>{advice}</p></div>', unsafe_allow_html=True)
                st.warning("**Red flags:** " + ", ".join(flags) if flags else "No clear red flags but stay vigilant.")
            elif risk == "low":
                st.markdown(f'<div class="safe-box"><h3>✅ LOW RISK</h3><p>{advice}</p></div>', unsafe_allow_html=True)
                st.info("No major red flags detected. Continue to monitor.")
            else:
                st.error(f"Analysis error: {advice}")

# ---------- Tab 2: Report Suspicious Activity ----------
with tab2:
    st.markdown("### 📢 Anonymous Report")
    st.markdown("Your report will be stored securely and shared with local anti-trafficking organizations (optional).")
    report_desc = st.text_area("Describe what you saw or experienced:", height=150)
    location = st.text_input("Location (city/region, optional):")
    contact_ok = st.checkbox("I allow SafeHaven to share my email with local NGOs for follow‑up (optional)", value=False)
    if contact_ok:
        email = st.text_input("Your email address (confidential):")
    else:
        email = "anonymous"
    if st.button("Submit Report", key="report"):
        if not report_desc.strip():
            st.warning("Please describe the situation.")
        else:
            # Optional: analyze report for urgency
            urgency = analyze_risk(report_desc).get("risk_level", "unknown")
            # Save to CSV (simple file-based storage)
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "description": report_desc,
                "location": location,
                "email": email,
                "urgency": urgency
            }
            try:
                df_existing = pd.read_csv("reports.csv") if os.path.exists("reports.csv") else pd.DataFrame()
                df_new = pd.DataFrame([report_data])
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv("reports.csv", index=False)
                st.success("✅ Report submitted anonymously. Thank you for helping protect others.")
                if urgency == "high":
                    st.warning("Your report indicates a potentially urgent situation. Local authorities may be alerted.")
            except Exception as e:
                st.error(f"Could not save report: {e}")

# ---------- Tab 3: Resources ----------
with tab3:
    st.markdown("### 📞 Immediate Help")
    st.markdown("""
    - **National Human Trafficking Hotline (USA):** 1-888-373-7888 (SMS: 233733)  
    - **Global Modern Slavery Directory:** [slaverydirectory.org](https://slaverydirectory.org)  
    - **International Organization for Migration (IOM):** +41 22 717 9111  
    - **Haiti (local partner):** Call 188 (Child Protection) or 114 (Police)  
    - **France:** 7 days/week – 116 006 (Missions locales)  
    """)
    st.markdown("---")
    st.markdown("### 🛡️ Safety Plan")
    st.markdown("""
    1. **Memorize emergency numbers** and have a code word with a trusted friend.
    2. **Keep important documents** (ID, passport) in a safe, accessible place.
    3. **Establish a check‑in routine** – let someone know where you are.
    4. **Use private browsing** when searching for help.
    5. **If in immediate danger, call emergency services (911, 17, etc.).**
    """)
    st.markdown("---")
    st.markdown("### 💡 How this tool works")
    st.markdown("""
    SafeHaven uses a large language model (Llama 3.1 via Groq) to analyze text for trafficking indicators. It does **not** store your personal data unless you voluntarily provide it. All reports are anonymized before analysis.
    """)

# ================== Footer ==================
st.markdown("---")
st.markdown("© 2026 GlobalInternet.py – Built for the Call for Code AI Global Challenge")
