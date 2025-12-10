import streamlit as st
import pandas as pd
from app.db import get_connection
from app.cyber_incidents import (
    get_all_cyber_incidents, 
    get_phishing_trend, 
    get_severity_distribution,
    get_category_breakdown
)

st.title(" Cybersecurity Dashboard")

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
    phishing_trend = get_phishing_trend(conn)
    severity_dist = get_severity_distribution(conn)
    category_breakdown = get_category_breakdown(conn)
except Exception as e:
    st.error(f"Failed to load data: {str(e)}")
    st.stop()

if data.empty:
    st.error("No incident data available.")
    st.stop()

# Sidebar filter
with st.sidebar:
    st.header(' Filters')
    severity_ = st.selectbox('Severity', options=['All'] + list(data['severity'].unique()))
    category_ = st.selectbox('Category', options=['All'] + list(data['category'].unique()))
    
    st.divider()
    if st.button('Logout', use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.switch_page("home.py")

# Clean timestamps
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
data = data.dropna(subset=['timestamp'])

# Filtered data
filtered_data = data.copy()
if severity_ != 'All':
    filtered_data = filtered_data[filtered_data['severity'] == severity_]
if category_ != 'All':
    filtered_data = filtered_data[filtered_data['category'] == category_]

# METRICS
st.subheader(" Key Metrics")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Total Incidents", len(filtered_data))
with col_m2:
    critical_count = len(filtered_data[filtered_data['severity'] == 'Critical'])
    st.metric("Critical", critical_count, delta=None if critical_count == 0 else f"{critical_count} urgent")
with col_m3:
    open_count = len(filtered_data[filtered_data['status'] == 'Open'])
    st.metric("Open Cases", open_count)
with col_m4:
    phishing_count = len(filtered_data[filtered_data['category'] == 'Phishing'])
    st.metric("Phishing Attacks", phishing_count)

st.divider()

#  PHISHING SPIKE DETECTION 
if not phishing_trend.empty:
    st.subheader(" Phishing Trend Analysis")
    phishing_trend['date'] = pd.to_datetime(phishing_trend['date'])
    st.line_chart(phishing_trend.set_index('date')['phishing_count'])
    
    # Spike detection
    avg_phishing = phishing_trend['phishing_count'].mean()
    max_phishing = phishing_trend['phishing_count'].max()
    if max_phishing > avg_phishing * 1.5:
        st.warning(f" **Phishing Spike Detected!** Peak: {int(max_phishing)} incidents (Average: {avg_phishing:.1f})")
        st.markdown("**Recommendation:** Review security policies and increase user awareness training.")
    else:
        st.info(f" Phishing levels stable. Average: {avg_phishing:.1f} incidents per day")

st.divider()

# ANALYTICS 
st.subheader(" Security Analytics")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Severity Distribution")
    st.bar_chart(severity_dist.set_index('severity')['count'])

with col2:
    st.markdown("### Category Breakdown")
    st.bar_chart(category_breakdown.set_index('category')['count'])

st.divider()

#  WORKFLOW ANALYSIS 
st.subheader(" Workflow Analysis")

col3, col4 = st.columns(2)
with col3:
    st.markdown("### Status Overview")
    status_counts = filtered_data['status'].value_counts()
    st.bar_chart(status_counts)

with col4:
    st.markdown("### Incidents Over Time")
    time_counts = filtered_data.groupby(filtered_data['timestamp'].dt.date).size()
    st.line_chart(time_counts)

st.divider()

#  RECOMMENDATIONS 
st.subheader(" Security Recommendations")

recommendations = []

# Check for critical incidents
critical_open = len(filtered_data[(filtered_data['severity'] == 'Critical') & (filtered_data['status'] == 'Open')])
if critical_open > 0:
    recommendations.append(f"🚨 **Critical Alert**: {critical_open} critical incident(s) still open - immediate action required!")

# Check for phishing spikes
if not phishing_trend.empty and max_phishing > avg_phishing * 1.5:
    recommendations.append(f"📌 **Phishing Spike**: Unusual phishing activity detected - implement additional email filtering.")

# Check open incident ratio
open_percentage = (open_count / len(filtered_data)) * 100 if len(filtered_data) > 0 else 0
if open_percentage > 30:
    recommendations.append(f"📌 **High Open Rate**: {open_percentage:.1f}% of incidents are open - consider allocating more resources.")

# Check for workflow bottlenecks
if 'Misconfiguration' in filtered_data['category'].values:
    misconfig_count = len(filtered_data[filtered_data['category'] == 'Misconfiguration'])
    if misconfig_count > len(filtered_data) * 0.2:
        recommendations.append(f"📌 **Workflow Issue**: {misconfig_count} misconfiguration incidents - review deployment processes.")

if recommendations:
    for rec in recommendations:
        st.markdown(rec)
else:
    st.success(" No critical issues detected. Security posture is healthy!")

st.divider()

# DETAILED DATA
st.subheader(" Incident Details")
st.dataframe(
    filtered_data[['incident_id', 'timestamp', 'severity', 'category', 'status', 'description']], 
    use_container_width=True,
    hide_index=True
)
