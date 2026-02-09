import streamlit as st
from database.db import get_history

# ---------- LOGIN CHECK ----------
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("pages/login.py")

# ---------- STYLE ----------
st.markdown("""
<style>
.block-container {padding-top:2rem;max-width:1100px;}
h1 {text-align:center;}
[data-testid="stSidebarNav"] {display:none;}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("""
<h2>🧠 MindTrack AI</h2>
<p>Emotion & Wellness Assistant</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("Track emotions, chat with AI, and monitor mental wellness.")

st.sidebar.markdown("### Navigate")
st.sidebar.page_link("app.py", label="🏠 App")
st.sidebar.page_link("pages/chatbot.py", label="🤖 Chatbot")
st.sidebar.page_link("pages/dashboard.py", label="📊 Dashboard")
st.sidebar.page_link("pages/history.py", label="📜 History")

# Logout
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.switch_page("pages/login.py")

# ---------- PAGE ----------
st.title("📝 Emotion History")

history = get_history(st.session_state.user)

color_map = {
    "Normal": "#16A34A",
    "Stressed": "#F59E0B",
    "Depressed": "#EF4444"
}

# ✅ Fix added here
if len(history) == 0:
    st.warning("No history available yet.")
else:
    for text, emotion in history[::-1]:
        color = color_map.get(emotion, "#7C3AED")

        st.markdown(
            f"""
            <div style='padding:10px;border-radius:8px;
            background-color:#1F2933;margin-bottom:10px'>
            <b>Text:</b> {text}<br>
            <b>Emotion:</b>
            <span style="color:{color};font-weight:bold;">
                {emotion}
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )
