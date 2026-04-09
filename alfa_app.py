import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import os

# --- MODEL AYARLARI ---
import streamlit as st
import google.generativeai as genai

# API anahtarını kasadan (Secrets) güvenli bir şekilde çekiyoruz
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Model ismini en hızlı ve güncel sürümle güncelledik
model = genai.GenerativeModel('gemini-1.5-flash')
# --- HAFIZA SİSTEMİ ---
MEMORY_FILE = "alfa_hafiza.json"
def hafiza_yukle():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"bilgiler": []}

def hafiza_kaydet(yeni_bilgi):
    hafiza = hafiza_yukle()
    hafiza["bilgiler"].append(yeni_bilgi)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(hafiza, f, ensure_ascii=False, indent=4)

# --- MODERN UI (ÖZEL TASARIM) ---
st.set_page_config(page_title="ALFA | Premium Assistant", page_icon="✨", layout="wide")

# CSS ile Estetik Dokunuşlar
st.markdown("""
    <style>
    /* Arka plan ve yazı tipi */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Mesaj balonları tasarımı */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    /* Başlık stili */
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(#2c3e50, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }

    /* Giriş kutusu (Input) */
    .stChatInputContainer {
        border-radius: 30px !important;
        background-color: white !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Yan Panel (Sidebar) - Düğün Geri Sayımı
with st.sidebar:
    st.markdown("## 💍 Düğün Sayacı")
    # 27 Temmuz 2026 hedefi
    st.date_input("Düğün Tarihi", datetime(2026, 7, 27).date(), disabled=True)
    st.markdown("---")
    st.markdown("### 🎓 Akademik Durum")
    st.progress(75, text="Zaman Algısı Makalesi")
    st.caption("Küre Ansiklopedi için %75 tamamlandı.")

# Ana Başlık
st.markdown('<p class="main-title">ALFA</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Akademik Vizyon & Yaşam Ortaklığı</p>", unsafe_allow_html=True)

# Mesaj Geçmişi
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
    gecmis_bilgiler = "\n".join(hafiza["bilgiler"])

    with st.chat_message("assistant"):
        if "öğren" in prompt.lower() or "unutma" in prompt.lower():
            hafiza_kaydet(prompt)
            cevap = "✨ Bunu hafıza merkezime kaydettim, Feyza. Asla unutmayacağım."
        else:
            full_prompt = f"Sen Feyza'nın premium asistanı ALFA'sın. Feyza akademik bir araştırmacı ve 27 Temmuz'da Erzurum'da evleniyor. Bilgiler: {gecmis_bilgiler}. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            cevap = response.text
        
        st.markdown(cevap)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
