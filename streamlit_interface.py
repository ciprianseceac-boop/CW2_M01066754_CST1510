import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import numpy as np
from pathlib import Path
from app.users import register_username, login_user
from app.cyber_incidents import migrate_cyber_incidents, get_all_cyber_incidents
from app.schema import create_user_table
from data_migration import migrate_it_tickets, migrate_datasets_metadata

#  Database setup 
DATA_DIR = Path("DATA")
DATA_PATH = DATA_DIR / "intelligence_platform.db"

# Connect to database
conn = sqlite3.connect(DATA_PATH)


#  STREAMLIT INTERFACE 
st.title("Multi-Domain Intelligence Platform")
st.header("User Authentication")

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
    st.subheader("Cybersecurity Dashboard")
    data = get_all_cyber_incidents(conn)
    st.dataframe(data)

elif menu == "IT Operations" and st.session_state["user"]:
    st.subheader("IT Operations Dashboard")
    st.info("IT Operations dashboard coming soon.")

elif menu == "Data Science" and st.session_state["user"]:
    st.subheader("Data Science Dashboard")
    st.info("Data Science dashboard coming soon.")

# Logout
elif menu == "Logout" and st.session_state["user"]:
    if st.button("Logout"):
        st.session_state["user"] = None
        st.success("You have been logged out.")
