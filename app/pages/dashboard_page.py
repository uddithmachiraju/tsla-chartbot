import streamlit as st
import time
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

def animate_chart_step(data, step, show_volume, show_moving_avg, show_bands, theme):
    bg_color = "#111827" if theme == "Dark" else "#FFFFFF"
    text_color = "#e5e7eb" if theme == "Dark" else "#1f2937"
    grid_color = "#374151" if theme == "Dark" else "#e5e7eb"

    sliced_data = data[:step]
    series = []

    # Candlesticks
    series.append({
        "type": "Candlestick",
        "data": sliced_data,
        "markers": generate_markers(sliced_data),
        "options": {
            "upColor": "#22c55e",
            "downColor": "#ef4444",
            "wickUpColor": "#22c55e",
            "wickDownColor": "#ef4444",
            "borderVisible": False
        }
    })

    # Volume
    if show_volume:
        volume_data = [
            {
                "time": d["time"],
                "value": d.get("volume", 0),
                "color": "#22c55e" if d["close"] >= d["open"] else "#ef4444"
            }
            for d in sliced_data
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

    # SMA
    if show_moving_avg:
        sma_data = sma(sliced_data, period=10)
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
        series.extend(get_bands_data(sliced_data))

    config = [{
        "chart": {
            "layout": {"background": {"type": "solid", "color": bg_color}, "textColor": text_color},
            "grid": {"vertLines": {"color": grid_color}, "horzLines": {"color": grid_color}},
            "crosshair": {"mode": 1},
            "timeScale": {"borderColor": grid_color},
            "rightPriceScale": {"borderColor": grid_color},
            "width": 950,
            "height": 600
        },
        "series": series
    }]

    renderLightweightCharts(config)

def render(data):
    # Sidebar options
    theme = st.sidebar.radio("Choose Theme", ["Dark", "Light"])
    show_volume = st.sidebar.checkbox("Show Volume", value=True)
    show_moving_avg = st.sidebar.checkbox("Show Moving Average (SMA)", value=True)
    show_bands = st.sidebar.checkbox("Show Support/Resistance Bands", value=False)

    # Session state to manage replay
    if 'replay_step' not in st.session_state:
        st.session_state.replay_step = 20
    if 'replaying' not in st.session_state:
        st.session_state.replaying = False

    # Button triggers
    if st.button("Start Replay Animation"):
        st.session_state.replaying = True
        st.session_state.replay_step = 20

    # Replay chart animation
    if st.session_state.replaying:
        if st.session_state.replay_step <= len(data):
            animate_chart_step(data, st.session_state.replay_step,
                               show_volume, show_moving_avg, show_bands, theme)
            st.session_state.replay_step += 1
            time.sleep(0.3)
            st.experimental_rerun()
        else:
            st.session_state.replaying = False
            st.session_state.replay_step = 20
        return

    # Static chart rendering
    bg_color = "#111827" if theme == "Dark" else "#FFFFFF"
    text_color = "#e5e7eb" if theme == "Dark" else "#1f2937"
    grid_color = "#374151" if theme == "Dark" else "#e5e7eb"

    series = []

    # Candlestick
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

    # Volume
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

    # SMA
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

    # Bands
    if show_bands:
        series.extend(get_bands_data(data))

    config = [{
        "chart": {
            "layout": {
                "background": {"type": "solid", "color": bg_color},
                "textColor": text_color
            },
            "grid": {
                "vertLines": {"color": grid_color},
                "horzLines": {"color": grid_color}
            },
            "crosshair": {"mode": 1},
            "timeScale": {"borderColor": grid_color},
            "rightPriceScale": {"borderColor": grid_color},
            "width": 950,
            "height": 600
        },
        "series": series
    }]

    renderLightweightCharts(config)
