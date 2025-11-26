import streamlit as st  
import pandas as pd
import numpy as np 

df = pd.DataFrame(
{
    "name": ["espy", "adi ", "Catalin"],
    "age": [40, 37,20]
    }
    )

st.title("Welcome to Streamlit")
st.header("This is a simple Streamlit app")
st.subheader("Subheader Example")
st.write("hello world")
st.markdown("### This is a markdown header")
st.caption("This is a caption for the data below")
st.text("This is a simple text element")
st.dataframe(df)    
st.image('C:\\Users\cipri\Desktop\OIP.jpg')

name = st.text_input("Name:")
st.header(f"Hello, {name}!")

age = st.number_input("Age:", min_value=0, max_value=100, value=10)
st.write(age)

val = st.slider("Select a value:", 0, 100, 50)

colour = st.color_picker("Pick a color:", "#2ee52e")
st.write(f"You picked: {colour}")   

name = st.text_input("Enter your name:")
if st.button("Submit"):

    st.success(f"Hello, {name}!")
else:
    st.warning("Please enter your name.")
    
data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)
st.line_chart(data)
st.bar_chart(data)