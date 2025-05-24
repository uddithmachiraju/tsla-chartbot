import streamlit as st
from app.components.markers import generate_markers
from app.components.bands import get_bands_data
from streamlit_lightweight_charts import renderLightweightCharts

def render(data):
    theme = st.sidebar.radio("Choose Theme", ["Dark", "Light"])
    show_volume = st.sidebar.checkbox("Show Volume", value=True)
    show_moving_avg = st.sidebar.checkbox("Show Moving Average (SMA)", value=True)
    show_bands = st.sidebar.checkbox("Show Support/Resistance Bands", value=False)

    bg_color = "#111827" if theme == "Dark" else "#FFFFFF"
    text_color = "#e5e7eb" if theme == "Dark" else "#1f2937"
    grid_color = "#374151" if theme == "Dark" else "#e5e7eb"

    series = []

    # Generate candlestick data and markers
    markers = generate_markers(data)

    series.append({
        "type": "Candlestick",
        "data": data,
        "markers": markers,
        "options": {
            "upColor": "#22c55e",
            "downColor": "#ef4444",
            "wickUpColor": "#22c55e",
            "wickDownColor": "#ef4444",
            "borderVisible": False
        }
    })

    # Volume histogram
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

    # Moving Average (SMA)
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

    # ✅ Add support/resistance bands if selected
    if show_bands:
        bands_series = get_bands_data(data)
        series.extend(bands_series)

    # Chart config
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
