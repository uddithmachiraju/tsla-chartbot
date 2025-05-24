import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
from data.config import example_data 

example_data = example_data[:500]

def render():
    theme = st.sidebar.radio("Choose Theme", ["Dark", "Light"])
    show_volume = st.sidebar.checkbox("Show Volume", value=True)
    show_moving_avg = st.sidebar.checkbox("Show Moving Average (SMA)", value=True)

    bg_color = "#111827" if theme == "Dark" else "#FFFFFF"
    text_color = "#e5e7eb" if theme == "Dark" else "#1f2937"
    grid_color = "#374151" if theme == "Dark" else "#e5e7eb"

    window_size = 500
    display_candles = 100  # number of candles to zoom in on

    total_len = len(example_data)
    visible_data = example_data[-window_size:]  # Get last 500 candles

    # Calculate start and end index for zoomed 100 candles in the center
    start_index = (window_size - display_candles) // 2
    end_index = start_index + display_candles
    visible_range = {
        "from": visible_data[start_index]["time"],
        "to": visible_data[end_index - 1]["time"]
    }

    series = [{
        "type": "Candlestick",
        "data": visible_data,
        "options": {
            "upColor": "#22c55e",
            "downColor": "#ef4444",
            "wickUpColor": "#22c55e",
            "wickDownColor": "#ef4444",
            "borderVisible": False
        }
    }]

    if show_volume:
        volume_data = [
            {"time": d["time"], "value": d.get("volume", 0), "color": "#22c55e" if d["close"] >= d["open"] else "#ef4444"}
            for d in visible_data
        ]
        series.append({
            "type": "Histogram",
            "data": volume_data,
            "options": {
                "priceFormat": {"type": "volume"},
                "color": "#8884d8",
                "lineWidth": 1.5,
                "priceLineVisible": False,
                "scaleMargins": {"top": 0.85, "bottom": 0}
            }
        })

    if show_moving_avg:
        def sma(source, period=10):
            sma_values = []
            for i in range(len(source)):
                if i < period - 1:
                    sma_values.append(None)
                else:
                    closes = [source[j]["close"] for j in range(i - period + 1, i + 1)]
                    sma_values.append(sum(closes) / period)
            return [{"time": source[i]["time"], "value": v} for i, v in enumerate(sma_values) if v]

        sma_data = sma(visible_data, period=10)
        series.append({
            "type": "Line",
            "data": sma_data,
            "options": {
                "color": "#3b82f6",
                "lineWidth": 2,
                "lineStyle": 0,
                "crossHairMarkerVisible": True
            }
        })

    config = [{
        "chart": {
            "layout": {"background": {"type": "solid", "color": bg_color}, "textColor": text_color},
            "grid": {"vertLines": {"color": grid_color}, "horzLines": {"color": grid_color}},
            "crosshair": {"mode": 1},
            "timeScale": {
                "borderColor": grid_color,
                "visible": True,
                "visibleRange": visible_range
            },
            "rightPriceScale": {"borderColor": grid_color},
            "width": 950,
            "height": 600
        },
        "series": series
    }]

    renderLightweightCharts(config)
