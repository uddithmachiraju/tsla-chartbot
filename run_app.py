import json 
import pandas as pd
import streamlit as st
from app.core.data_loader import load_tsla_data
from app.pages import dashboard_page, chatbot_page
from data.config import data

df, ohlc_list = load_tsla_data("data/TSLA_data.csv", return_ohlc=True)

def save_ohlc_json(data, output_path="data/ohlc_data.json"):
    """Save OHLC list of dictionaries to a .json file with each dict on its own line."""
    with open(output_path, 'w') as f:
        f.write('[\n')
        for i, record in enumerate(data):
            json_str = json.dumps(record, separators=(',', ': '))
            f.write(json_str + (',\n' if i < len(data) - 1 else '\n'))
        f.write(']\n') 

save_ohlc_json(ohlc_list) 

with open("data/ohlc_data.json", "r") as file:
    data = json.load(file)

st.set_page_config(page_title="TSLA ChartBot", layout="wide")

tab1, tab2 = st.tabs(["Dashboard", "Chatbot"])

with tab1:
    dashboard_page.render(data[:320])

with tab2:
    chatbot_page.render() 
