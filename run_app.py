import streamlit as st
# from app.pages import dashboard_page, chatbot_page  # uncomment and fix import path if needed
from app.core.data_loader import load_tsla_data
from lightweight_charts.widgets import StreamlitChart

st.set_page_config(page_title="TSLA ChartBot", layout="wide")

tab1, tab2 = st.tabs(["Dashboard", "Chatbot"])

with tab1:
    # Load data and show chart inside Dashboard tab
    df = load_tsla_data()
    chart = StreamlitChart(width=900, height=600)
    chart.set(df)
    chart.load()
    
