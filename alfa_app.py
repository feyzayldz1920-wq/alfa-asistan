import streamlit as st
import google.generativeai as genai

# --- KRİTİK BAĞLANTI (404/V1BETA HATASINI ÖNLEYEN VERSİYON) ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ HATA: Secrets kısmında 'GEMINI_API_KEY' bulunamadı!")
    st.stop()

try:
    # transport='rest' parametresi 404/v1beta hatalarını baypas etmek için eklendi
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    
    # Model ismini Google'ın en yeni kabul ettiği formatta yazıyoruz
    model = genai.GenerativeModel('gemini-1.5-flash')
    bağlantı_tamam = True
except Exception as e:
    st.error(f"⚠️ Yapılandırma Hatası: {e}")
    bağlantı_tamam = False

# --- MODERN ARAYÜZ ---
st.set_page_config(page_title="ALFA | Premium Assistant", page_icon="✨")
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
            # ALFA'nın karakter tanımı
            full_prompt = f"Sen Feyza'nın asistanı ALFA'sın. Feyza araştırmacıdır ve 27 Temmuz'da Erzurum'da evleniyor. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Google'dan boş yanıt döndü.")
                
        except Exception as e:
            # Eğer 1.5-flash yine nazlanırsa, gemini-pro modelini yedek olarak deniyoruz
            try:
                model_yedek = genai.GenerativeModel('gemini-pro')
                response = model_yedek.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error(f"⚠️ Google Yanıt Vermedi: {e}")
