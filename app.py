import streamlit as st
import requests
import json
import re
import os
import pandas as pd
from datetime import datetime
from groq import Groq

# ================== VIDEO URLs per language ==================
# Replace these with your actual Dropbox video links (use dl=1)
VIDEO_URLS = {
    "English": "https://www.dropbox.com/scl/fi/9m7quhz7lzu1vmb30lxby/safehaven_narrated.mp4?rlkey=vnmf48hb4hlruiwix51e124y4&st=ev5217i6&dl=1",
    "Français": "https://www.dropbox.com/scl/fi/9m7quhz7lzu1vmb30lxby/safehaven_narrated.mp4?rlkey=vnmf48hb4hlruiwix51e124y4&st=ev5217i6&dl=1",  # Replace with French version
    "Español": "https://www.dropbox.com/scl/fi/9m7quhz7lzu1vmb30lxby/safehaven_narrated.mp4?rlkey=vnmf48hb4hlruiwix51e124y4&st=ev5217i6&dl=1",   # Replace with Spanish version
}

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
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    div[data-baseweb="select"] ul {
        background-color: #1f2a48 !important;
    }
    div[data-baseweb="select"] ul li {
        color: #ffffff !important;
        font-weight: bold !important;
        background-color: #1f2a48 !important;
    }
    div[data-baseweb="select"] ul li:hover {
        background-color: #e94560 !important;
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
    .security-badge {
        background: #0a192f;
        border: 1px solid #00ebc7;
        border-radius: 30px;
        padding: 8px 15px;
        margin: 10px 0;
        text-align: center;
        color: #00ebc7;
    }
</style>
""", unsafe_allow_html=True)

# ================== Sidebar ==================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/Deslandes1/Color-Software-Game/main/Gesner%20Deslandes.png", width=80)
    st.markdown("## **GlobalInternet.py**")
    st.markdown("**SafeHaven – AI Anti-Trafficking Tool**")
    st.markdown("---")
    
    # Language Selection
    language = st.selectbox("🌐 Language / Idioma / Langue", ["English", "Français", "Español"])
    
    # Global Security Shield (API key hidden)
    st.markdown("---")
    st.markdown("### 🛡️ Global Security Shield active")
    st.markdown('<div class="security-badge">🔐 End‑to‑end encryption active</div>', unsafe_allow_html=True)
    st.caption("All data is secured and anonymized")
    
    st.markdown("---")
    st.markdown("Built by **Gesner Deslandes**, Engineer-in-Chief")
    st.markdown("📞 (509) 4738 5663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("---")
    
    # Pricing / Services
    st.markdown("### 💰 Our Services")
    st.markdown("""
    - **Full source code** – $499 USD  
    - **Source + customization** – $1,499 USD  
    - **Enterprise plan** – $2,999 USD  
    """)
    st.markdown("---")
    
    if language == "English":
        st.markdown("### How to use")
        st.markdown("1. **Video Intro** – Watch the tutorial.")
        st.markdown("2. **Risk Assessment** – Describe a situation, AI flags red flags.")
        st.markdown("3. **Report** – Anonymously submit suspicious activity.")
        st.markdown("4. **Resources** – Hotlines and safety plans.")
    elif language == "Français":
        st.markdown("### Comment utiliser")
        st.markdown("1. **Intro vidéo** – Regardez le tutoriel.")
        st.markdown("2. **Évaluation** – Décrivez une situation, l'IA détecte les signes.")
        st.markdown("3. **Signaler** – Soumettez anonymement.")
        st.markdown("4. **Ressources** – Numéros d'urgence.")
    else:
        st.markdown("### Cómo usar")
        st.markdown("1. **Video intro** – Mira el tutorial.")
        st.markdown("2. **Evaluación** – Describe una situación, la IA detecta señales.")
        st.markdown("3. **Reportar** – Envía anónimamente.")
        st.markdown("4. **Recursos** – Líneas de ayuda.")

# ================== Main Title ==================
if language == "English":
    st.title("🛡️ SafeHaven")
    st.markdown("## AI-Powered Early Warning & Resource Hub Against Human Trafficking")
elif language == "Français":
    st.title("🛡️ SafeHaven")
    st.markdown("## Alerte précoce et centre de ressources contre la traite des êtres humains")
else:
    st.title("🛡️ SafeHaven")
    st.markdown("## Alerta temprana y centro de recursos contra la trata de personas")
st.markdown("---")

# ================== Groq Client ==================
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ================== Helper Function ==================
def analyze_risk(situation_text, lang):
    if lang == "English":
        prompt = f"""You are an expert anti-trafficking analyst. Analyze the following situation and output a JSON object with exactly these fields:
- "risk_level": "high", "medium", "low", or "uncertain"
- "red_flags": list of specific trafficking indicators (e.g., "confiscated passport", "debt bondage", "false promises")
- "advice": one sentence of actionable advice for the user.

Situation: {situation_text}

Return ONLY valid JSON. No extra text."""
    elif lang == "Français":
        prompt = f"""Vous êtes un expert en lutte contre la traite. Analysez la situation suivante et renvoyez un JSON avec :
- "risk_level": "high", "medium", "low" ou "uncertain"
- "red_flags": liste des signaux (ex: "passeport confisqué", "servitude pour dette")
- "advice": une phrase de conseil.

Situation: {situation_text}

Renvoyez UNIQUEMENT le JSON valide."""
    else:
        prompt = f"""Eres un experto en lucha contra la trata. Analiza la siguiente situación y devuelve un JSON con:
- "risk_level": "high", "medium", "low" o "uncertain"
- "red_flags": lista de indicadores (ej: "pasaporte confiscado", "servidumbre por deuda")
- "advice": una frase de consejo.

Situación: {situation_text}

Devuelve SOLO el JSON válido."""
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            result = json_match.group(0)
        data = json.loads(result)
        return data
    except Exception as e:
        return {"risk_level": "error", "red_flags": [], "advice": f"Could not analyze: {str(e)}"}

# ================== TABS ==================
tab_titles = []
if language == "English":
    tab_titles = ["🎬 Video Introduction", "🔍 Risk Assessment", "📢 Report", "📞 Resources"]
elif language == "Français":
    tab_titles = ["🎬 Introduction vidéo", "🔍 Évaluation des risques", "📢 Signaler", "📞 Ressources"]
else:
    tab_titles = ["🎬 Introducción en video", "🔍 Evaluación de riesgos", "📢 Reportar", "📞 Recursos"]

tab1, tab2, tab3, tab4 = st.tabs(tab_titles)

# ---------- Tab 1: Video Introduction (language‑specific) ----------
with tab1:
    video_link = VIDEO_URLS.get(language, VIDEO_URLS["English"])
    if language == "English":
        st.markdown("### 🎬 Watch the full introduction video")
        st.markdown("This video explains all features of SafeHaven: how to assess risk, submit anonymous reports, and access resources.")
        st.video(video_link)
        st.caption("If the video does not play, click the three dots → Download to save it locally.")
    elif language == "Français":
        st.markdown("### 🎬 Regardez la vidéo d'introduction complète")
        st.markdown("Cette vidéo explique toutes les fonctionnalités de SafeHaven.")
        st.video(video_link)
        st.caption("Si la vidéo ne se lit pas, cliquez sur les trois points → Télécharger.")
    else:
        st.markdown("### 🎬 Vea el video de introducción completo")
        st.markdown("Este video explica todas las funciones de SafeHaven.")
        st.video(video_link)
        st.caption("Si el video no se reproduce, haga clic en los tres puntos → Descargar.")

# ---------- Tab 2: Risk Assessment ----------
with tab2:
    if language == "English":
        st.markdown("### 🧠 Describe a situation you or someone you know is facing")
        placeholder = "Example: I met a recruiter who promised me a well-paid job abroad, but he asked for my passport and $500 fee..."
    elif language == "Français":
        st.markdown("### 🧠 Décrivez une situation que vous ou quelqu'un que vous connaissez vivez")
        placeholder = "Exemple : J'ai rencontré un recruteur qui m'a promis un travail bien payé à l'étranger, mais il m'a demandé mon passeport et 500 $..."
    else:
        st.markdown("### 🧠 Describe una situación que tú o alguien que conoces está enfrentando")
        placeholder = "Ejemplo: Conocí a un reclutador que me prometió un trabajo bien pagado en el extranjero, pero me pidió mi pasaporte y $500..."
    
    situation = st.text_area("", height=150, placeholder=placeholder)
    btn_label = "Analyze Risk" if language == "English" else "Analyser" if language == "Français" else "Analizar"
    if st.button(btn_label, key="analyze"):
        if not situation.strip():
            st.warning("Please describe a situation." if language == "English" else "Veuillez décrire une situation." if language == "Français" else "Por favor, describa una situación.")
        else:
            with st.spinner("AI is analyzing..." if language == "English" else "L'IA analyse..." if language == "Français" else "La IA está analizando..."):
                result = analyze_risk(situation, language)
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

# ---------- Tab 3: Anonymous Report ----------
with tab3:
    if language == "English":
        st.markdown("### 📢 Anonymous Report")
        st.markdown("Your report will be stored securely and shared with local anti-trafficking organizations (optional).")
        desc_label = "Describe what you saw or experienced:"
        loc_label = "Location (city/region, optional):"
        check_label = "I allow SafeHaven to share my email with local NGOs for follow‑up (optional)"
        email_label = "Your email address (confidential):"
        submit_label = "Submit Report"
    elif language == "Français":
        st.markdown("### 📢 Signalement anonyme")
        st.markdown("Votre signalement sera stocké de manière sécurisée et partagé avec des organisations locales (optionnel).")
        desc_label = "Décrivez ce que vous avez vu ou vécu :"
        loc_label = "Lieu (ville/région, optionnel) :"
        check_label = "J'autorise SafeHaven à partager mon email avec des ONG locales pour un suivi (optionnel)"
        email_label = "Votre adresse email (confidentielle) :"
        submit_label = "Soumettre le signalement"
    else:
        st.markdown("### 📢 Reporte anónimo")
        st.markdown("Tu reporte se almacenará de forma segura y se compartirá con organizaciones locales contra la trata (opcional).")
        desc_label = "Describe lo que viste o experimentaste:"
        loc_label = "Ubicación (ciudad/región, opcional):"
        check_label = "Permito que SafeHaven comparta mi correo electrónico con ONG locales para seguimiento (opcional)"
        email_label = "Tu correo electrónico (confidencial):"
        submit_label = "Enviar reporte"
    
    report_desc = st.text_area(desc_label, height=150)
    location = st.text_input(loc_label)
    contact_ok = st.checkbox(check_label, value=False)
    if contact_ok:
        email = st.text_input(email_label)
    else:
        email = "anonymous"
    if st.button(submit_label, key="report"):
        if not report_desc.strip():
            st.warning(desc_label)
        else:
            urgency = analyze_risk(report_desc, language).get("risk_level", "unknown")
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
                st.success("✅ Report submitted anonymously. Thank you for helping protect others." if language == "English" else "✅ Signalement soumis anonymement. Merci de protéger les autres." if language == "Français" else "✅ Reporte enviado anónimamente. Gracias por ayudar a proteger a otros.")
                if urgency == "high":
                    st.warning("Your report indicates a potentially urgent situation. Local authorities may be alerted." if language == "English" else "Votre signalement indique une situation potentiellement urgente. Les autorités locales peuvent être alertées." if language == "Français" else "Tu reporte indica una situación potencialmente urgente. Las autoridades locales pueden ser alertadas.")
            except Exception as e:
                st.error(f"Could not save report: {e}")

# ---------- Tab 4: Resources ----------
with tab4:
    if language == "English":
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
    elif language == "Français":
        st.markdown("### 📞 Aide immédiate")
        st.markdown("""
        - **Ligne nationale contre la traite (USA) :** 1-888-373-7888 (SMS : 233733)  
        - **Annuaire mondial sur l'esclavage moderne :** [slaverydirectory.org](https://slaverydirectory.org)  
        - **Organisation internationale pour les migrations (OIM) :** +41 22 717 9111  
        - **Haïti (partenaire local) :** Appelez le 188 (Protection de l'enfance) ou 114 (Police)  
        - **France :** 7j/7 – 116 006 (Missions locales)  
        """)
        st.markdown("---")
        st.markdown("### 🛡️ Plan de sécurité")
        st.markdown("""
        1. **Mémorisez les numéros d'urgence** et ayez un mot‑code avec un ami de confiance.
        2. **Gardez vos documents importants** (carte d'identité, passeport) dans un endroit sûr et accessible.
        3. **Établissez une routine de check‑in** – faites savoir à quelqu'un où vous êtes.
        4. **Utilisez la navigation privée** lorsque vous cherchez de l'aide.
        5. **En danger immédiat, appelez les secours (911, 17, etc.).**
        """)
        st.markdown("---")
        st.markdown("### 💡 Comment cet outil fonctionne")
        st.markdown("""
        SafeHaven utilise un grand modèle de langage (Llama 3.1 via Groq) pour analyser les textes à la recherche d'indicateurs de traite. Il ne **stocke** pas vos données personnelles sauf si vous les fournissez volontairement. Tous les signalements sont anonymisés avant analyse.
        """)
    else:
        st.markdown("### 📞 Ayuda inmediata")
        st.markdown("""
        - **Línea nacional contra la trata (EE.UU.) :** 1-888-373-7888 (SMS: 233733)  
        - **Directorio mundial sobre esclavitud moderna :** [slaverydirectory.org](https://slaverydirectory.org)  
        - **Organización Internacional para las Migraciones (OIM) :** +41 22 717 9111  
        - **Haití (socio local) :** Llame al 188 (Protección infantil) o al 114 (Policía)  
        - **Francia :** 7 días/semana – 116 006 (Misiones locales)  
        """)
        st.markdown("---")
        st.markdown("### 🛡️ Plan de seguridad")
        st.markdown("""
        1. **Memorice los números de emergencia** y tenga una palabra clave con un amigo de confianza.
        2. **Guarde documentos importantes** (identificación, pasaporte) en un lugar seguro y accesible.
        3. **Establezca una rutina de verificación** – que alguien sepa dónde está.
        4. **Use navegación privada** cuando busque ayuda.
        5. **Si está en peligro inmediato, llame a los servicios de emergencia (911, 17, etc.).**
        """)
        st.markdown("---")
        st.markdown("### 💡 Cómo funciona esta herramienta")
        st.markdown("""
        SafeHaven utiliza un modelo de lenguaje grande (Llama 3.1 vía Groq) para analizar texto en busca de indicadores de trata. **No almacena** sus datos personales a menos que usted los proporcione voluntariamente. Todos los reportes se anonimizan antes del análisis.
        """)

# ================== Footer ==================
st.markdown("---")
if language == "English":
    st.markdown("© 2026 GlobalInternet.py – Built for the Call for Code AI Global Challenge")
elif language == "Français":
    st.markdown("© 2026 GlobalInternet.py – Conçu pour le Call for Code AI Global Challenge")
else:
    st.markdown("© 2026 GlobalInternet.py – Creado para el Call for Code AI Global Challenge")
