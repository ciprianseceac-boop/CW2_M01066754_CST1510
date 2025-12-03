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

tab_login, tab_registration = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Log In"):
        if login_user(conn, login_username, login_password):
            st.session_state['logged_in'] = True
            st.success("You are now logged in.")
            st.session_state['username'] = login_username
        else:
            st.error("Login failed. Please try again.")
    # st.session_state

with tab_registration:
    st.subheader("Register")
    reg_username = st.text_input("Choose a Username", key="reg_username")
    reg_password = st.text_input("Choose a Password", type="password", key="reg_password")
    if st.button("Register"):
        hashed_pwd = hash_password(reg_password)
        add_user(conn, reg_username, hashed_pwd)
        st.success("Registration successful. You can now log in.")
if st.button('Log out'):
    st.session_state['logged_in'] = False
    st.info('you have been logged out')