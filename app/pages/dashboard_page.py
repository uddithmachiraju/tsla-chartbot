import streamlit as st
from app.components.markers import generate_markers
from app.components.bands import get_bands_data
from streamlit_lightweight_charts import renderLightweightCharts

def sma(source, period=10):
    sma_values = []
    for i in range(len(source)):
        if i < period - 1:
            sma_values.append(None)
        else:
            closes = [source[j]["close"] for j in range(i - period + 1, i + 1)]
            sma_values.append(sum(closes) / period)
    return [{"time": source[i]["time"], "value": v} for i, v in enumerate(sma_values) if v]

def render(data):
    # Sidebar chart options
    show_volume = st.sidebar.checkbox("Show Volume", value=True)
    show_moving_avg = st.sidebar.checkbox("Show Moving Average (SMA)", value=True)
    show_bands = st.sidebar.checkbox("Show Support/Resistance Bands", value=False)

    series = []

    # Candlestick series
    series.append({
        "type": "Candlestick",
        "data": data,
        "markers": generate_markers(data),
        "options": {
            "upColor": "#22c55e",
            "downColor": "#ef4444",
            "wickUpColor": "#22c55e",
            "wickDownColor": "#ef4444",
            "borderVisible": False
        }
    })

    # Volume series
    if show_volume:
        volume_data = [
            {
                "time": d["time"],
                "value": d.get("volume", 0),
                "color": "#22c55e" if d["close"] >= d["open"] else "#ef4444"
            }
            for d in data
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

    # Moving average line
    if show_moving_avg:
        sma_data = sma(data, period=10)
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

    # Support/Resistance Bands
    if show_bands:
        series.extend(get_bands_data(data))

    config = [{
        "chart": {
            "layout": {
                "background": {"type": "solid", "color": "#FFFFFF"},
                "textColor": "#1f2937"
            },
            "grid": {
                "vertLines": {"color": "#e5e7eb"},
                "horzLines": {"color": "#e5e7eb"}
            },
            "crosshair": {"mode": 1},
            "timeScale": {"borderColor": "#e5e7eb"},
            "rightPriceScale": {"borderColor": "#e5e7eb"},
            "width": 950,
            "height": 600
        },
        "series": series
    }]

    renderLightweightCharts(config)
