import streamlit as st
from kiteconnect import KiteConnect

# ⚙️ 1. ZERODHA CREDENTIALS (अपनी डिटेल्स यहाँ भरें)
API_KEY = hucynx7stpod5za4
API_SECRET = 7e6wt7b32fozv6spec3q83hzrlqclybd

st.set_page_config(page_title="Tredit AI - Zerodha Connect", page_icon="⚡")

st.title("⚡ Tredit AI — Zerodha Access Token Generator")

# 📥 User Input for Request Token
request_token = st.text_input("ब्राउज़र से मिला Request Token यहाँ पेस्ट करें:", type="password")

if st.button("Generate Access Token"):
    if request_token and API_KEY and API_SECRET:
        try:
            kite = KiteConnect(api_key=API_KEY)
            data = kite.generate_session(request_token, api_secret=API_SECRET)
            access_token = data["access_token"]
            
            st.success("🟢 Access Token सफलतापूर्वक जनरेट हो गया है!")
            st.code(f"ACCESS_TOKEN = '{access_token}'", language="python")
        except Exception as e:
            st.error(f"🔴 त्रुटि (Error): {e}")
    else:
        st.warning("⚠️ कृपया Request Token, API Key और API Secret पूरी तरह भरें।")
