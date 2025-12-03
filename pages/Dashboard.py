import streamlit as st
import pandas as pd
from app.db import get_connection
from app.cyber_incidents import get_all_cyber_incidents

st.title("Cyber Incidents Dashboard")

# Session state check
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to access the dashboard.")
    st.stop()
else:
    st.success(f"Welcome {st.session_state['username']}!")

# Load data
conn = get_connection()
data = get_all_cyber_incidents(conn)

if data.empty:
    st.error("No incident data available.")
    st.stop()

# Sidebar filter
with st.sidebar:
    st.header('Navigation')
    severity_ = st.selectbox('Severity', data['severity'].unique())

# Clean timestamps
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
data = data.dropna(subset=['timestamp'])

# Filtered data
filtered_data = data[data['severity'] == severity_]

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
