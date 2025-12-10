import streamlit as st
import pandas as pd
from app.db import get_connection
from app.cyber_incidents import get_all_cyber_incidents

st.title("Cyber Incidents Dashboard")

# Session state check
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to access the dashboard.")
    if st.button("Go to Login Page"):
        st.session_state['logged_in'] = False
        st.switch_page("home.py")
    st.stop()
else:
    st.success(f"Welcome {st.session_state['username']}!")

# Load data
try:
    conn = get_connection()
    data = get_all_cyber_incidents(conn)
except Exception as e:
    st.error(f"Failed to load data: {str(e)}")
    st.stop()

if data.empty:
    st.error("No incident data available.")
    st.stop()

# Sidebar filter
with st.sidebar:
    st.header('Navigation')
    severity_ = st.selectbox('Severity', options=['All'] + list(data['severity'].unique()))
    
    st.divider()
    if st.button('Logout', use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.switch_page("home.py")

# Clean timestamps
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
data = data.dropna(subset=['timestamp'])

# Filtered data
if severity_ == 'All':
    filtered_data = data
else:
    filtered_data = data[data['severity'] == severity_]


col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Total Incidents", len(filtered_data))
with col_m2:
    st.metric("Critical", len(filtered_data[filtered_data['severity'] == 'Critical']))
with col_m3:
    st.metric("High", len(filtered_data[filtered_data['severity'] == 'High']))
with col_m4:
    st.metric("Medium/Low", len(filtered_data[filtered_data['severity'].isin(['Medium', 'Low'])]))

# Layout
col1, col2 = st.columns(2)
with col1:
    st.header("Incidents by Status")
    st.bar_chart(filtered_data['status'].value_counts())

with col2:
    st.header("Incidents Over Time")
    time_counts = filtered_data.groupby('timestamp').size()
    st.line_chart(time_counts)

st.subheader("Filtered Incidents")
st.write(filtered_data)
