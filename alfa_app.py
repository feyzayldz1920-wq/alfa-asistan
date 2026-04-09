import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import os

# --- MODEL AYARLARI (ZIRHLI YAPILANDIRMA) ---
def setup_alfa():
    try:
        # Secrets'tan anahtarı çekiyoruz
        api_key = st.secrets.get("GEMINI_API_KEY")
        
        if not api_key:
            st.error("❌ HATA: Secrets kısmında 'GEMINI_API_KEY' bulunamadı!")
            return None
        
        # PC'de çalışan o anahtarı sisteme tanıtıyoruz
        genai.configure(api_key=api_key, transport='rest')
        return True
    except Exception as e:
        st.error(f"❌ Yapılandırma hatası: {e}")
        return None

# --- HAFIZA SİSTEMİ ---
MEMORY_FILE = "alfa_hafiza.json"

def hafiza_yukle():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {"bilgiler": []}
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
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stChatMessage { border-radius: 20px !important; margin-bottom: 15px; background-color: rgba(255, 255, 255, 0.7) !important; }
    .main-title { font-size: 3rem !important; font-weight: 800; text-align: center; color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# Yan Panel
with st.sidebar:
    st.markdown("## 💍 Düğün Sayacı")
    st.date_input("Düğün Tarihi", datetime(2026, 7, 27).date(), disabled=True)
    st.markdown("---")
    st.markdown("### 🎓 Akademik Durum")
    st.progress(75)

st.markdown('<p class="main-title">ALFA</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ANA DÖNGÜ ---
if setup_alfa():
    if prompt := st.chat_input("Feyza, emrindeyim..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        hafiza = hafiza_yukle()
        gecmis_bilgiler = ", ".join(hafiza["bilgiler"]) if hafiza["bilgiler"] else ""

        with st.chat_message("assistant"):
            # PC'de çalışan modellerin listesi
            modeller = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            cevap = ""
            success = False

            for m_name in modeller:
                try:
                    model = genai.GenerativeModel(m_name)
                    full_prompt = f"Sen Feyza'nın asistanı ALFA'sın. Feyza araştırmacıdır ve 27 Temmuz'da Erzurum'da evleniyor. Hafıza: {gecmis_bilgiler}\n\nSoru: {prompt}"
                    response = model.generate_content(full_prompt)
                    cevap = response.text
                    success = True
                    break
                except: continue

            if not success:
                cevap = "⚠️ PC'de çalışan anahtar burada yetki hatası alıyor. Lütfen Secrets kısmındaki yazımı (GEMINI_API_KEY) kontrol et."

            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
