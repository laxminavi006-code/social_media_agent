# auth.py
import streamlit as st
import os
import json

USERS_FILE = "users.json"

def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_page():
    st.header("Create account")
    new_user = st.text_input("Choose username", key="reg_user")
    new_pass = st.text_input("Choose password", type="password", key="reg_pass")
    confirm = st.text_input("Confirm password", type="password", key="reg_confirm")

    if st.button("Register"):
        if not new_user or not new_pass:
            st.error("All fields required")
            return
        if new_pass != confirm:
            st.error("Passwords do not match")
            return
        users = _load_users()
        if new_user in users:
            st.error("Username already exists")
            return
        users[new_user] = {"password": new_pass}
        _save_users(users)
        st.success("Registered successfully — please login")
        st.session_state["auth_page"] = "login"
        st.rerun()

def login_page():
    st.header("Login")
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        users = _load_users()
        if user in users and users[user]["password"] == pwd:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user
            st.success(f"Welcome, {user}!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def auth_router():
    st.sidebar.title("Account")
    choice = st.sidebar.radio("Choose", ["Register", "Login"])
    st.session_state["auth_page"] = "register" if choice == "Register" else "login"

    if st.session_state.get("auth_page") == "register":
        register_page()
    else:
        login_page()
