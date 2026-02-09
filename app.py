import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from database.db import init_db, save_result
import random
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

/* Hide default Streamlit page menu */
[data-testid="stSidebarNav"] {
    display: none;
}
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
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.switch_page("pages/login.py")

# ---------- DATABASE ----------
init_db()

# ---------- MODEL ----------
MODEL_PATH = "models/emotion_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

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

if st.button("Analyze Emotion"):

    if user_input.strip():

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

        # ---------- SMART CORRECTION ----------
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

        # ---------- SAVE RESULT ----------
        save_result(st.session_state.user, user_input, emotion)


        color_map = {
            "Normal": "#16A34A",
            "Stressed": "#F59E0B",
            "Depressed": "#EF4444"
        }

        color = color_map.get(emotion, "#7C3AED")

        # ---------- EMOTION DISPLAY ----------
        st.markdown(
            f"""
            <div style='padding:12px;border-radius:10px;
            background-color:{color};color:white;
            text-align:center;font-size:18px;'>
            Detected Emotion: {emotion}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------- PERSONALIZED SUGGESTIONS ----------
        suggestions = {
            "Normal": [
                "Keep maintaining your positive routine.",
                "Consider helping someone else today.",
                "Stay active and productive."
            ],
            "Stressed": [
                "Take short breaks between tasks.",
                "Try deep breathing for 2 minutes.",
                "Consider a short walk to relax."
            ],
            "Depressed": [
                "Talk to someone you trust.",
                "Try writing your thoughts in a journal.",
                "Consider seeking professional support."
            ]
        }

        suggestion = random.choice(
            suggestions.get(emotion, [])
        )

        st.markdown(
            f"""
            <div style='padding:12px;border-radius:10px;
            background-color:#1F2933;color:white;
            margin-top:10px;font-size:16px;'>
            💡 Suggestion: {suggestion}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning("Please enter text.")

st.info("Use sidebar to open History or Dashboard pages.")
