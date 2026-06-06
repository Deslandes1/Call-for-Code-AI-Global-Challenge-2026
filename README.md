# 🛡️ SafeHaven – AI‑Powered Anti‑Trafficking Early Warning System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-deployed-app-url.streamlit.app)
[![Call for Code](https://img.shields.io/badge/Call%20for%20Code-2026-blue)](https://callforcode.org)

**SafeHaven** is an AI‑driven tool designed to help individuals, social workers, and law enforcement identify and report potential human trafficking situations. It uses a large language model (Llama 3.1 via Groq) to analyze text, flag red flags, and provide actionable advice – all while protecting user privacy.

Built for the **Call for Code AI Global Challenge 2026** (theme: *United Against Trafficking*).

---

## 🌟 Live Demo

👉 [**Launch SafeHaven on Streamlit Cloud**](https://hospital-management-system-software-built-by-gesner-deslandes.streamlit.app/)  
*(Replace with your actual deployed app URL)*

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎬 **Video Introduction** | A narrated walkthrough explaining all app functionalities (available in English, French, Spanish). |
| 🔍 **Risk Assessment** | Paste any situation (e.g., a suspicious job offer) → AI returns risk level (high/medium/low), red flags, and immediate advice. |
| 📢 **Anonymous Reporting** | Submit a confidential report with description, location, and optional email. Reports are saved locally for NGO follow‑up. |
| 📞 **Resources** | Country‑specific hotlines (USA, Haiti, France, IOM), a safety plan, and an explanation of how the AI works. |
| 🌐 **Multilingual UI** | Switch between **English**, **Français**, and **Español** – all text, prompts, and resources adapt instantly. |
| 🛡️ **Global Security Shield** | End‑to‑end encryption badge (API key never exposed). |

---

## 🧠 How It Works

1. **User inputs** a situation in natural language (Creole, English, or French supported).
2. **Groq LLM** (Llama 3.1 8B) analyzes the text for trafficking indicators (e.g., passport confiscation, debt bondage, false promises).
3. **System returns**:
   - Risk level (High / Medium / Low / Uncertain)
   - List of specific red flags
   - One‑sentence actionable advice
4. **Anonymous reports** are saved to a local CSV file (can be shared with authorities).
5. **Resources tab** provides immediate helplines and a safety plan.

---

## 🛠️ Tech Stack

- **Frontend & Deployment**: [Streamlit](https://streamlit.io)
- **AI Model**: Groq Cloud – Llama 3.1 8B (via Groq API)
- **Audio/Video** (for intro video): Dropbox hosting
- **Data Storage**: CSV (local file, can be extended to cloud)
- **Languages**: Python 3.12+

---

## 📁 Project Structure
