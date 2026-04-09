import streamlit as st
import google.generativeai as genai

# --- KRİTİK BAĞLANTI KONTROLÜ ---
# Kodu öyle bir yazdım ki, anahtar gelmeden sayfa bile yüklenmeyecek
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ HATA: Secrets kısmında 'GEMINI_API_KEY' bulunamadı!")
    st.info("Lütfen Streamlit Ayarlar > Secrets kısmına GEMINI_API_KEY = 'ANAHTARIN' şeklinde ekleme yap.")
    st.stop() 

# Anahtar varsa devam et
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # PC'de çalışan en stabil model
    model = genai.GenerativeModel('gemini-1.5-flash')
    bağlantı_tamam = True
except Exception as e:
    st.error(f"⚠️ Yapılandırma Hatası: {e}")
    bağlantı_tamam = False

# --- ARAYÜZ ---
st.title("✨ ALFA Çevrimiçi")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Feyza, bugün neyi başarmak istersin?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            full_prompt = f"Sen Feyza'nın asistanı ALFA'sın. Feyza araştırmacıdır ve 27 Temmuz'da Erzurum'da evleniyor. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Google Yanıt Vermedi: {e}")
