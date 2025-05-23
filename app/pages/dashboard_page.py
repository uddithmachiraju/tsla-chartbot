# import streamlit as st
# from streamlit_lightweight_charts import renderLightweightCharts
# from app.core.data_loader import load_tsla_data  # Adjust path based on your project structure

# def render():
#     st.subheader("📈 TSLA Candlestick Chart with Markers and Bands")

#     # Load preprocessed TSLA data
#     df = load_tsla_data("data/tsla_data.csv") 
#     # st.write(df)

#     # Build candlestick series
#     candlestick_data = [
#         {
#             "time": row["timestamp"],
#             "open": row["open"],
#             "high": row["high"],
#             "low": row["low"],
#             "close": row["close"]
#         }
#         for _, row in df.iterrows()
#     ]

#     # st.write(candlestick_data)

#     # Generate markers
#     markers = []
#     for _, row in df.iterrows():
#         direction = row.get("direction", None)
#         marker = {
#             "time": row["timestamp"],
#             "position": "aboveBar",
#             "shape": "circle",
#             "color": "yellow",
#             "text": "NO DIR"
#         }

#         if direction == "LONG":
#             marker.update({
#                 "position": "belowBar",
#                 "shape": "arrowUp",
#                 "color": "green",
#                 "text": "LONG"
#             })
#         elif direction == "SHORT":
#             marker.update({
#                 "position": "aboveBar",
#                 "shape": "arrowDown",
#                 "color": "red",
#                 "text": "SHORT"
#             })
#         markers.append(marker)
#     # st.write(markers)

#     # Support and Resistance bands
#     support_lower = []
#     support_upper = []
#     resistance_lower = []
#     resistance_upper = []

#     for _, row in df.iterrows():
#         support_vals = row['Support']
#         resistance_vals = row['Resistance']
#         time = row['timestamp']

#         if isinstance(support_vals, list) and all([val == val for val in support_vals]):
#             support_lower.append({"time": time, "value": min(support_vals)})
#             support_upper.append({"time": time, "value": max(support_vals)})

#         if isinstance(resistance_vals, list) and all([val == val for val in resistance_vals]):
#             resistance_lower.append({"time": time, "value": min(resistance_vals)})
#             resistance_upper.append({"time": time, "value": max(resistance_vals)})

#     # Chart config
#     chart_options = {
#         "layout": {
#             "backgroundColor": "#000000",
#             "textColor": "white"
#         },
#         "grid": {
#             "vertLines": {"color": "#444444"},
#             "horzLines": {"color": "#444444"}
#         },
#         "priceScale": {"borderColor": "#71649C"},
#         "timeScale": {"borderColor": "#71649C"},
#     }

#     series = [
#         {
#             "type": "Candlestick",
#             "data": candlestick_data,
#             "markers": markers,
#             "options": {
#                 "wickUpColor": "#26a69a",
#                 "wickDownColor": "#ef5350",
#                 "borderVisible": False
#             }
#         },
#         {
#             "type": "Line",
#             "data": support_lower,
#             "options": {"color": "green", "lineWidth": 1, "lineStyle": 1}
#         },
#         {
#             "type": "Line",
#             "data": support_upper,
#             "options": {"color": "green", "lineWidth": 1, "lineStyle": 1}
#         },
#         {
#             "type": "Line",
#             "data": resistance_lower,
#             "options": {"color": "red", "lineWidth": 1, "lineStyle": 1}
#         },
#         {
#             "type": "Line",
#             "data": resistance_upper,
#             "options": {"color": "red", "lineWidth": 1, "lineStyle": 1}
#         }
#     ]

#     charts = {
#         "chart": chart_options,
#         "series": series
#     }

#     renderLightweightCharts(charts, key="tsla_chart")

from app.core.data_loader import load_tsla_data
from lightweight_charts.widgets import StreamlitChart

chart = StreamlitChart(width=900, height=600)

df = load_tsla_data()
chart.set(df)

chart.load()