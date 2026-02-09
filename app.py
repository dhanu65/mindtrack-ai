import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from database.db import init_db, save_result

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
h1, h2, h3 {
    text-align: center;
}
[data-testid="stSidebarNav"] {display:none;}
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

# ---------- DATABASE ----------
init_db()

# ---------- MODEL ----------
MODEL_PATH = "dhanu65/mindtrack-emotion"   # HuggingFace model

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# ---------- UI ----------
st.title("🧠 MindTrack AI")
st.caption("AI-powered Emotion Detection System")

with st.container(border=True):
    user_input = st.text_area("Enter your text:")

emotion_map = {
    0: "Depressed",
    1: "Normal",
    2: "Normal",
    3: "Stressed",
    4: "Stressed",
    5: "Normal"
}

# Session storage for result
if "emotion_result" not in st.session_state:
    st.session_state.emotion_result = None

# ---------- ANALYSIS ----------
if st.button("Analyze Emotion"):
    if user_input.strip() != "":
        inputs = tokenizer(
            user_input,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        with torch.no_grad():
            outputs = model(**inputs)

        predicted_class = torch.argmax(outputs.logits).item()
        emotion = emotion_map[predicted_class]

        # Rule correction
        text_lower = user_input.lower()

        if any(word in text_lower for word in [
            "depressed", "hopeless", "empty",
            "worthless", "sad", "low"
        ]):
            emotion = "Depressed"

        elif any(word in text_lower for word in [
            "stress", "deadline", "pressure",
            "overwhelmed", "anxious"
        ]):
            emotion = "Stressed"

        elif "not sad" in text_lower or "not depressed" in text_lower:
            emotion = "Normal"

        save_result(user_input, emotion)

        st.session_state.emotion_result = emotion

    else:
        st.warning("Please enter text.")

# ---------- RESULT DISPLAY ----------
if st.session_state.emotion_result:

    color_map = {
        "Normal": "#16A34A",
        "Stressed": "#F59E0B",
        "Depressed": "#EF4444"
    }

    color = color_map.get(
        st.session_state.emotion_result, "#7C3AED"
    )

    st.markdown(
        f"""
        <div style='padding:12px;border-radius:10px;
        background-color:{color};color:white;
        text-align:center;font-size:18px;'>
        Detected Emotion: {st.session_state.emotion_result}
        </div>
        """,
        unsafe_allow_html=True
    )

st.info("Use sidebar to open Chatbot, Dashboard, or History pages.")
