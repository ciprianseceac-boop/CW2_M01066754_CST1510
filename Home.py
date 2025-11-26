import streamlit as st  
import pandas as pd

st.set_page_config(
    page_title="My App",
    page_icon=":smiley:",
    layout="wide",
   
)

df = pd.DataFrame(
{
    "name": ["espy", "adi ", "Catalin"],
    "age": [40, 37,20]
    }
    )
col1, col2 = st.columns(2)

with col1:
    st.subheader("left")

with col2:
    st.subheader("right")

with st.sidebar:
    st.header("Controls")
    options = st.selectbox("choose an option", ["A", "B", "C"])
    
with st.expander("See details"):
    st.write("Here are more details...")
    st.dataframe(df)