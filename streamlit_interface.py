import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import numpy as np
from pathlib import Path

# --- Database setup ---
DATA_DIR = Path("DATA")
DATA_PATH = DATA_DIR / "intelligence_platform.db"

# Now you can safely connect
conn = sqlite3.connect(DATA_PATH)


# ---------------- STREAMLIT INTERFACE ----------------
st.title("Multi-Domain Intelligence Platform")
st.header("User Authentication")

# Connect to database
conn = sqlite3.connect(DATA_PATH)

# Run migrations automatically at startup
migrate_cyber_incidents(conn)
migrate_it_tickets(conn)
migrate_datasets_metadata(conn)

# Ensure user table exists
create_user_table(conn)

# Initialize session state
if "user" not in st.session_state:
    st.session_state["user"] = None

# Sidebar menu
if st.session_state["user"]:
    menu = st.sidebar.selectbox("Menu", ["Cybersecurity", "IT Operations", "Data Science", "Logout"])
else:
    menu = st.sidebar.selectbox("Menu", ["Register", "Login"])

# Register page
if menu == "Register" and not st.session_state["user"]:
    reg_name = st.text_input("Username")
    reg_pass = st.text_input("Password", type="password")
    if st.button("Register"):
        success, msg = register_username(conn, reg_name.strip(), reg_pass.strip())
        st.success(msg) if success else st.error(msg)

# Login page
elif menu == "Login" and not st.session_state["user"]:
    login_name = st.text_input("Username")
    login_pass = st.text_input("Password", type="password")
    if st.button("Login"):
        success, msg = login_user(conn, login_name.strip(), login_pass.strip())
        if success:
            st.session_state["user"] = login_name.strip()
            st.success(msg)
            st.info(f"Welcome, {login_name}!")
        else:
            st.error(msg)

# Dashboards
elif menu == "Cybersecurity" and st.session_state["user"]:
    show_cybersecurity_dashboard(conn)

elif menu == "IT Operations" and st.session_state["user"]:
    show_it_dashboard(conn)

elif menu == "Data Science" and st.session_state["user"]:
    show_data_dashboard(conn)

# Logout
elif menu == "Logout" and st.session_state["user"]:
    if st.button("Logout"):
        st.session_state["user"] = None
        st.success("You have been logged out.")
