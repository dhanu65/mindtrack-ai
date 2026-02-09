import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import get_history

# ---------- LOGIN CHECK ----------
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("pages/login.py")

# ---------- STYLE ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}
h1 {text-align:center;}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("""
<h2 style='margin-bottom:0;'>🧠 MindTrack AI</h2>
<p style='margin-top:0;'>Emotion & Wellness Assistant</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.info(
    "Track emotions, chat with AI, and monitor mental wellness."
)

st.sidebar.markdown("### Navigate")

st.sidebar.page_link("app.py", label="🏠 App")
st.sidebar.page_link("pages/chatbot.py", label="🤖 Chatbot")
st.sidebar.page_link("pages/dashboard.py", label="📊 Dashboard")
st.sidebar.page_link("pages/history.py", label="📜 History")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.switch_page("pages/login.py")

# ---------- PAGE TITLE ----------
st.title("📊 Emotion Analytics Dashboard")

# ---------- LOAD USER HISTORY ----------
history = get_history(st.session_state.user)

if len(history) == 0:
    st.warning("No data available yet.")
else:
    df = pd.DataFrame(history, columns=["text", "emotion"])

    emotion_counts = df["emotion"].value_counts().reset_index()
    emotion_counts.columns = ["emotion", "count"]

    fig = px.bar(
        emotion_counts,
        x="emotion",
        y="count",
        color="emotion",
        title="Emotion Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Table")
    st.dataframe(df, use_container_width=True)
