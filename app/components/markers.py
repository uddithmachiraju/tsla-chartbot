
def generate_markers(df):
    markers = []
    for _, row in df.iterrows():
        time_str = row['timestamp'].strftime('%Y-%m-%d')
        direction = row.get('direction', None)
        if direction == "LONG":
            markers.append({
                "time": time_str,
                "position": "belowBar",
                "color": "green",
                "shape": "arrowUp",
                "text": "LONG"
            })
        elif direction == "SHORT":
            markers.append({
                "time": time_str,
                "position": "aboveBar",
                "color": "red",
                "shape": "arrowDown",
                "text": "SHORT"
            })
        else:
            markers.append({
                "time": time_str,
                "position": "inBar",
                "color": "yellow",
                "shape": "circle",
                "text": "NEUTRAL"
            })
    return markers
