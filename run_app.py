import streamlit as st 

st.set_page_config(page_title = "TSLA ChartBot", layout = "wide") 

tab1, tab2 = st.tabs(
    [
        "Dashboard",
        "Chatbot"
    ]
)