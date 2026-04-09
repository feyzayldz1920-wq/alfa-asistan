import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import os

# --- MODEL AYARLARI ---
# Secrets'tan anahtarı çekip konfigüre ediyoruz
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Kabul edilen model ismini buraya yazdık
model = genai.GenerativeModel('gemini-pro')

# --- HAFIZA SİSTEMİ ---
MEMORY_FILE = "alfa_hafiza.json"

def hafiza_yukle():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"bilgiler": []}
    return {"bilgiler": []}

def hafiza_kaydet(yeni_bilgi):
    hafiza = hafiza_yukle()
    hafiza["bilgiler"].append(yeni_bilgi)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(hafiza, f, ensure_ascii=False, indent=4)

# --- MODERN UI ---
st.set_page_config(page_title="ALFA | Premium Assistant", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); font-family: 'Inter', sans-serif; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.7) !important; backdrop-filter: blur(10px); border-radius: 20px !important; margin-bottom: 15px; padding: 15px; border: 1px solid rgba(255, 255, 255, 0.3) !important; }
    .main-title { font-size: 3rem !important; font-weight: 800; background: -webkit-linear-gradient(#2c3e50, #000000); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Yan Panel
with st.sidebar:
    st.markdown("## 💍 Düğün Sayacı")
    st.date_input("Düğün Tarihi", datetime(2026, 7, 27).date(), disabled=True)
    st.markdown("---")
    st.markdown("### 🎓 Akademik Durum")
    st.progress(75)
    st.caption("Zaman Algısı Makalesi: %75 tamamlandı.")

st.markdown('<p class="main-title">ALFA</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş ve Zeka
if prompt := st.chat_input("Feyza, bugün neyi başarmak istersin?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    hafiza = hafiza_yukle()
    gecmis_bilgiler = ", ".join(hafiza["bilgiler"]) if hafiza["bilgiler"] else "Henüz kayıt yok."

    with st.chat_message("assistant"):
        if any(kelime in prompt.lower() for kelime in ["öğren", "unutma", "kaydet"]):
            hafiza_kaydet(prompt)
            cevap = "✨ Bunu hafıza merkezime kaydettim, Feyza. Asla unutmayacağım."
        else:
            try:
                # Sistemin Feyza'yı tanıması için talimat:
                full_prompt = (
                    f"Sen Feyza'nın asistanı ALFA'sın. Feyza araştırmacıdır ve 27 Temmuz'da Erzurum'da evleniyor. "
                    f"Hafıza: {gecmis_bilgiler}\n\nSoru: {prompt}"
                )
                response = model.generate_content(full_prompt)
                cevap = response.text if response.text else "Cevap üretilemedi."
            except Exception as e:
                cevap = f"Ufak bir sorun: {str(e)}"
        
        st.markdown(cevap)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
