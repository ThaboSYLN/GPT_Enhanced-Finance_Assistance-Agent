import streamlit as st
import hashlib
import os

# File to store user credentials
USER_DB = "user_credentials.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return {line.split(":")[0]: line.split(":")[1].strip() for line in f.readlines()}

def save_user(username, password):
    with open(USER_DB, "a") as f:
        f.write(f"{username}:{hash_password(password)}\n")

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == hash_password(password)

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def register_page():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        users = load_users()
        if username in users:
            st.error("Username already exists")
        else:
            save_user(username, password)
            st.success("Registered successfully! Please log in.")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

def auth_required(func):
    def wrapper(*args, **kwargs):
        if not st.session_state.get('logged_in', False):
            login_page()
        else:
            return func(*args, **kwargs)
    return wrapper