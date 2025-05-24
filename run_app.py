import json 
import pandas as pd
import streamlit as st
from app.core.data_loader import load_tsla_data
from app.pages import dashboard_page

st.set_page_config(page_title="TSLA ChartBot", layout="wide")

tab1, tab2 = st.tabs(["Dashboard", "Chatbot"])

with tab1:
    dashboard_page.render()
