import streamlit as st
import torch
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from groq import Groq
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("pages/login.py")

# ---------- STYLE ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

div[data-testid="stChatMessage"] {
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
    background-color: #1F2933;
}

h1, h2, h3 {
    text-align: center;
}

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
# Logout
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.switch_page("pages/login.py")
# ---------- CONFIG ----------
API_KEY = "gsk_......"
MODEL_PATH = "dhanu65/mindtrack-emotion"

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# ---------- LOAD MODEL ----------
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

emotion_map = {
    0: "Depressed",
    1: "Normal",
    2: "Normal",
    3: "Stressed",
    4: "Stressed",
    5: "Normal"
}

st.title("🤖 MindTrack AI Assistant")
st.caption("Emotion-aware mental wellness chatbot")

# ---------- CHAT MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------- USER INPUT ----------
user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    st.chat_message("user").write(user_input)

    # ---------- EMOTION DETECTION ----------
    inputs = tokenizer(user_input, return_tensors="pt",
                       truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_class = torch.argmax(outputs.logits).item()
    emotion = emotion_map[predicted_class]

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

    # ---------- LLM RESPONSE ----------
    conversation = [{
        "role": "system",
        "content": f"""
        You are a mental wellness assistant.
        User emotion is {emotion}.
        Respond empathetically and briefly.
        """
    }]

    conversation.extend(st.session_state.messages)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation,
        temperature=0.7,
    )

    bot_reply = response.choices[0].message.content

    # ---------- TYPING ANIMATION ----------
    message_placeholder = st.chat_message("assistant").empty()

    full_text = ""
    for word in bot_reply.split():
        full_text += word + " "
        message_placeholder.markdown(full_text + "▌")
        time.sleep(0.03)

    message_placeholder.markdown(full_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_text}
    )
