import streamlit as st
from database.db import init_db, register_user, login_user

init_db()

st.title("🔐 MindTrack AI Login")

if "user" not in st.session_state:
    st.session_state.user = None

tab1, tab2 = st.tabs(["Login", "Register"])

# ---------- LOGIN ----------
with tab1:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state.user = username
            st.success("Login successful!")
            st.switch_page("app.py")
        else:
            st.error("Invalid credentials")


# ---------- REGISTER ----------
with tab2:
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("Registration successful! Please login.")
        else:
            st.error("User already exists.")
