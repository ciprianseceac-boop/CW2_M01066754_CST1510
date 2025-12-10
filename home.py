import streamlit as st
from app.users import add_user, hash_password, login_user
from app.db import get_connection
conn = get_connection()

st.title("Home Page")
st.write("Welcome to the Cyber Incidents Intelligence Platform.")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = ""

if st.session_state['logged_in']:
    st.success(f"Welcome back, {st.session_state['username']}!")
    st.info("You are already logged in. Navigate to the Dashboard from the sidebar or logout below.")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button('Logout', use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()
    with col2:
        if st.button('Go to Dashboard', use_container_width=True):
            st.switch_page("pages/Dashboard.py")
else:
    tab_login, tab_registration = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In"):
            success, message = login_user(conn, login_username, login_password)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['username'] = login_username
                st.success(message)
                st.switch_page("pages/Dashboard.py")
            else:
                st.error(message)

    with tab_registration:
        st.subheader("Register")
        reg_username = st.text_input("Choose a Username", key="reg_username")
        reg_password = st.text_input("Choose a Password", type="password", key="reg_password")
        if st.button("Register"):
            if not reg_username or not reg_password:
                st.error("Username and password cannot be empty.")
            elif len(reg_password) < 4:
                st.error("Password must be at least 4 characters long.")
            else:
                try:
                    hashed_pwd = hash_password(reg_password)
                    add_user(conn, reg_username, hashed_pwd)
                    st.success("Registration successful. You can now log in.")
                except Exception as e:
                    if "UNIQUE constraint failed" in str(e):
                        st.error("Username already exists. Please choose another.")
                    else:
                        st.error(f"Registration failed: {str(e)}")