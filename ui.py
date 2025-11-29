# ui.py
import streamlit as st
from datetime import datetime
import os
import json

HISTORY_FILE = "history.json"

def _load_history(user):
    if not user:
        return []
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
        return data.get(user, [])
    except Exception:
        return []

def _save_history(user, item):
    try:
        data = {}
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
        data.setdefault(user, []).insert(0, item)
        data[user] = data[user][:200]
        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def _download_text(name, text):
    st.download_button(
        label=f"Download {name}",
        data=text.encode("utf-8"),
        file_name=f"{name.replace(' ','_')}.txt",
        mime="text/plain"
    )

# ------------------------------------------------------
# NEW: Animated Heading CSS (does NOT disappear)
# ------------------------------------------------------
def animated_heading_css():
    css = """
    <style>
    .animated-title {
        font-size: 40px;
        font-weight: 800;
        color: #5A00FF;
        text-align: center;
        margin-top: -10px;
        animation: slideIn 1.2s ease-out, glow 2s infinite alternate;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 10px #b07bff;
        }
        to {
            text-shadow: 0 0 25px #7f00ff;
        }
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #333;
        margin-bottom: 12px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ------------------------------------------------------
# LIGHT & DARK CARD STYLES
# ------------------------------------------------------

def style_light():
    css = """
    <style>
    .card {
        background: #ffffff;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def style_dark():
    css = """
    <style>
    .card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ------------------------------------------------------
# MAIN UI
# ------------------------------------------------------

def main_ui(agent):

    # Theme
    theme = st.sidebar.selectbox("Theme", ["Light", "Dark"], index=1)
    if theme == "Light":
        style_light()
    else:
        style_dark()

    # Inject animated heading CSS
    animated_heading_css()

    # Animated Title
    st.markdown("<h1 class='animated-title'>✨ Social Media Agent ✨</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Create captions, reels, hashtags & weekly plans — fast.</div>", unsafe_allow_html=True)

    # Sidebar Profile
    st.sidebar.markdown("### 👤 Profile")
    username = st.session_state.get("username")
    st.sidebar.write(f"**{username}**")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Recent")
    history_items = _load_history(username)
    for i, it in enumerate(history_items[:8]):
        st.sidebar.write(f"{i+1}. {it.get('type','')} — {it.get('topic','')}")

    # Input Card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Inputs")
    topic = st.text_input("Enter topic / brief", placeholder="e.g. Maldives trip, Uppittu, Startup launch")
    creativity = st.slider("Creativity", 0.0, 1.0, 0.7)
    st.markdown("</div>", unsafe_allow_html=True)

    # Feature Buttons
    st.subheader("Features")
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Generate 5 Captions"):
            if not topic:
                st.error("Enter topic")
            else:
                with st.spinner("Generating..."):
                    resp = agent.generate_advanced_captions(topic, creativity)
                    text = resp["text"] if isinstance(resp, dict) else resp
                    st.session_state["captions"] = text
                    _save_history(username, {"type":"captions","topic":topic,"text":text})

    with c2:
        if st.button("Generate Reel Script"):
            if not topic:
                st.error("Enter topic")
            else:
                with st.spinner("Generating..."):
                    resp = agent.generate_reel_script(topic, creativity)
                    text = resp["text"] if isinstance(resp, dict) else resp
                    st.session_state["reel"] = text
                    _save_history(username, {"type":"reel","topic":topic,"text":text})

    with c3:
        if st.button("Smart Hashtags"):
            if not topic:
                st.error("Enter topic")
            else:
                with st.spinner("Generating..."):
                    resp = agent.generate_hashtags(topic, 20)
                    text = resp["text"] if isinstance(resp, dict) else resp
                    st.session_state["hashtags"] = text
                    _save_history(username, {"type":"hashtags","topic":topic,"text":text})

    st.markdown("---")

    # Outputs
    left, right = st.columns([2,1])

    # LEFT SIDE
    with left:
        st.subheader("Captions")
        caps = st.session_state.get("captions")
        if caps:
            st.code(caps)
            _download_text("captions", caps)

        st.subheader("Reels Script")
        reel = st.session_state.get("reel")
        if reel:
            st.code(reel)
            _download_text("reel_script", reel)

        st.subheader("Weekly Planner")
        if st.button("Create Weekly Planner"):
            if not topic:
                st.error("Enter topic")
            else:
                with st.spinner("Generating..."):
                    resp = agent.generate_weekly_plan(topic)
                    text = resp["text"] if isinstance(resp, dict) else resp
                    st.session_state["plan"] = text
                    _save_history(username, {"type":"plan","topic":topic,"text":text})

        plan = st.session_state.get("plan")
        if plan:
            st.code(plan)
            _download_text("weekly_plan", plan)

    # RIGHT SIDE
    with right:
        st.subheader("Hashtags")
        tags = st.session_state.get("hashtags")
        if tags:
            st.code(tags)
            _download_text("hashtags", tags)

        st.subheader("Caption Score")
        caption_to_score = st.text_area("Paste caption", height=120)

        if st.button("Score Caption"):
            to_score = caption_to_score.strip()
            if not to_score:
                st.error("No caption entered.")
            else:
                with st.spinner("Scoring..."):
                    resp = agent.score_caption(to_score, topic or "general")
                    text = resp["text"] if isinstance(resp, dict) else resp
                    st.session_state["score"] = text
                    _save_history(username, {"type":"score","topic":topic,"text":text})

        if st.session_state.get("score"):
            st.code(st.session_state["score"])

        st.markdown("---")

        st.subheader("Image → Caption")
        uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

        if uploaded and st.button("Generate Caption from Image"):
            img_bytes = uploaded.read()
            with st.spinner("Analyzing image..."):
                resp = agent.image_to_caption(img_bytes, topic_hint=topic)
                text = resp["text"] if isinstance(resp, dict) else resp
                st.session_state["img_caption"] = text
                _save_history(username, {"type":"image_caption","topic":topic,"text":text})

        if st.session_state.get("img_caption"):
            st.code(st.session_state["img_caption"])
            _download_text("image_caption", st.session_state["img_caption"])

    st.markdown("---")
    st.caption("Made for the 48-hour AI Agent Challenge — Pro features.")
