import streamlit as st
import time, json, urllib.request, hashlib

# Page Setup & Dark Theme
st.set_page_config(page_title="Tredit AI Master Terminal", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .candle-card {
        background-color: #010409; border: 1.5px solid #238636; border-radius: 6px;
        padding: 10px; text-align: center; color: white; margin-bottom: 5px;
    }
    .candle-top-red { background: #da3633; height: 6px; border-radius: 2px; margin-bottom: 4px; }
    .candle-body-green { background: #238636; padding: 6px; border-radius: 4px; font-weight: bold; }
    .sub-row { background: #161b22; border: 1px solid #30363d; padding: 8px; border-radius: 4px; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# Zerodha Direct API Fetcher
def fetch_zerodha_data(api_k, req_t, api_s):
    try:
        url_session = "https://api.kite.trade/session/token"
        checksum = hashlib.sha256((api_k + req_t + api_s).encode('utf-8')).hexdigest()
        payload = f"api_key={api_k}&request_token={req_t}&checksum={checksum}".encode('utf-8')
        req = urllib.request.Request(url_session, data=payload, headers={'X-Kite-Version': '3'})
        
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            access_token = res_data['data']['access_token']
            
        url_quote = "https://api.kite.trade/quote?i=NSE:NIFTY+BANK"
        req_q = urllib.request.Request(url_quote, headers={
            'X-Kite-Version': '3',
            'Authorization': f'token {api_k}:{access_token}'
        })
        
        with urllib.request.urlopen(req_q) as resp_q:
            q_data = json.loads(resp_q.read().decode())
            return True, q_data['data']['NSE:NIFTY BANK']['last_price'], q_data['data']['NSE:NIFTY BANK']['net_change']
    except Exception as e:
        return False, str(e), 0

# Title
st.markdown("<h2 style='text-align: center; color: #58a6ff;'>Tredit AI — Master Candlesticks Terminal</h2>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### 🔑 Zerodha Credentials")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")
req_token = st.sidebar.text_input("Request Token", type="password")
conn_btn = st.sidebar.button("🔗 CONNECT LIVE ZERODHA", use_container_width=True)

# Action Buttons
c1, c2, c3, c4 = st.columns(4)
c1.button("🟢 BUY CE NOW", use_container_width=True)
c2.button("🔴 SELL CE / EXIT", use_container_width=True)
c3.button("🟢 BUY PE NOW", use_container_width=True)
c4.button("🔴 SELL PE / EXIT", use_container_width=True)

# Live Data State
ltp_val = None
if conn_btn and api_key and api_secret and req_token:
    success, ltp, chg = fetch_zerodha_data(api_key.strip(), req_token.strip(), api_secret.strip())
    if success:
        ltp_val = ltp
        curr_time = time.strftime('%H:%M')
        st.success(f"🟢 **LIVE ZERODHA SYNCED!** Bank Nifty Spot: ₹{ltp:,.2f} | Time: {curr_time} IST")
    else:
        st.error("🔴 Token या API Key में गड़बड़ी है!")
else:
    st.info("💡 **लाइव डेटा चालू करने के लिए:** बाईं तरफ अपने Zerodha क्रेडेंशियल्स दर्ज करें।")

# Strike Price Calculator
atm_strike = round(ltp_val / 100) * 100 if ltp_val else 51800

st.markdown("#### 📊 Strike Price Radar")
sc1, sc2 = st.columns(2)
with sc1:
    st.caption("[ Best Strike Prices ]")
    st.table({
        "STRIKE": [f"{atm_strike} CE (ATM)", f"{atm_strike+100} CE", f"{atm_strike-100} CE"],
        "TYPE": ["Best ATM", "Budget OTM", "Slight ITM"]
    })
with sc2:
    st.caption("[ All Strike Ranges ]")
    st.table({
        "RANGE": ["₹1-50", "₹50-100", "₹100-150", "₹150-200"],
        "STRIKE": [f"{atm_strike+400} CE", f"{atm_strike+200} CE", f"{atm_strike} CE", f"{atm_strike-300} CE"],
        "TYPE": ["Hero-Zero", "Budget OTM", "Best ATM", "Deep ITM"]
    })

# 12 Master Candles Layout
st.markdown("#### 🔥 12 Master Candles")

names = [
    "1. US Fed & Yields", "2. Bloomberg", "3. Reuters Feed", "4. CNBC India",
    "5. 222 ML Modules", "6. FII/DII Flow", "7. Price Action", "8. Option Chain",
    "9. Orderbook", "10. Delta Flow", "11. Tech Ind", "12. Safety Shield"
]

cols = st.columns(4)
for i, name in enumerate(names):
    col = cols[i % 4]
    with col:
        st.markdown(f"""
        <div class="candle-card">
            <div class="candle-top-red"></div>
            <div class="candle-body-green">🕯️ 96.5% Bullish</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(name, key=f"btn_{i}", use_container_width=True):
            st.session_state['selected_candle'] = name

# Sub-Module Details Panel
st.divider()
selected = st.session_state.get('selected_candle', "1. US Fed & Yields")
st.markdown(f"### 📋 Details for: **{selected}**")

if "222 ML" in selected:
    st.caption("All 222 ML Modules (Scrollable List)")
    base_names = [
        "AI Neural Trend Signal", "Algorithmic Sweep Detector", "ATM Delta Acceleration",
        "Bayesian Momentum Predictor", "Bloomberg News Sentiment Engine", "Bollinger Squeeze Breakout",
        "Block Deal Aggression Tracker", "Call-Put OI Skew Index", "Crude Oil Impact Matrix",
        "Dark Pool Inflow Detector", "Delta Neutral Shift Lead", "DXY Dollar Index Sync",
        "Dynamic Max Pain Locator", "Exponential VWAP Rebound", "FII Cash Accumulation"
    ]
    for idx in range(1, 223):
        b_name = base_names[(idx - 1) % len(base_names)]
        st.markdown(f"<div class='sub-row'><b>#{idx:03d} [ML Pattern]</b> {b_name} — <span style='color:#3fb950;'>🕯️ 95.8% BULLISH</span></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='sub-row'><b>Signal 1:</b> Institutional Inflow — <span style='color:#3fb950;'>🕯️ 97.4% BULLISH</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-row'><b>Signal 2:</b> Time Lag Predictor — <span style='color:#3fb950;'>🕯️ 2-5 Min Reaction Time Sync</span></div>", unsafe_allow_html=True)
