# app.py
import streamlit as st
from config import GROQ_API_KEY, MODEL_FALLBACKS
from auth import auth_router
from ui import main_ui
from agent import SocialMediaAgent

st.set_page_config(page_title="Social Media Agent — Pro", layout="wide", page_icon="🤖")

# ensure session defaults
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Initialize agent (show friendly error if key missing)
try:
    agent = SocialMediaAgent(api_key=GROQ_API_KEY, models=MODEL_FALLBACKS)
except Exception as e:
    st.error(f"Agent initialization error: {e}")
    st.stop()

if not st.session_state.get("logged_in", False):
    auth_router()
else:
    main_ui(agent)
