
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.header('Research Tool')

user_input = st.text_input('Enter Your Text')

if st.button:
    st.text('Some random text')
