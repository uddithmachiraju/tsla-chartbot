def get_bands_data(data):
    support_band = []
    resistance_band = []

    for d in data:
        # Support can be a number or a list
        if "Support" in d:
            support = d["Support"]
            if isinstance(support, list) and support:
                low = min(support)
                high = max(support)
            elif isinstance(support, (int, float)):
                low = high = support
            else:
                continue  # skip if Support is invalid

            support_band.extend([
                {"time": d["time"], "value": low, "color": "#22c55e"},
                {"time": d["time"], "value": high, "color": "#22c55e"}
            ])

        # Resistance can be a number or a list
        if "Resistance" in d:
            resistance = d["Resistance"]
            if isinstance(resistance, list) and resistance:
                low = min(resistance)
                high = max(resistance)
            elif isinstance(resistance, (int, float)):
                low = high = resistance
            else:
                continue  # skip if Resistance is invalid

            resistance_band.extend([
                {"time": d["time"], "value": low, "color": "#ef4444"},
                {"time": d["time"], "value": high, "color": "#ef4444"}
            ])

    bands_series = []

    if support_band:
        bands_series.append({
            "type": "Area",
            "data": support_band,
            "options": {
                "topColor": "#22c55e22",
                "bottomColor": "#22c55e44",
                "lineColor": "#22c55e",
                "lineWidth": 1
            }
        })

    if resistance_band:
        bands_series.append({
            "type": "Area",
            "data": resistance_band,
            "options": {
                "topColor": "#ef444422",
                "bottomColor": "#ef444444",
                "lineColor": "#ef4444",
                "lineWidth": 1
            }
        })

    return bands_series
