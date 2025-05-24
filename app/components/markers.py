# app/components/markers.py

def generate_markers(data):
    markers = []
    previous_direction = None

    for d in data:
        direction = d.get("direction")

        if direction != previous_direction:
            if direction == "LONG":
                markers.append({
                    "time": d["time"],
                    "position": "belowBar",
                    "shape": "arrowUp",
                    "color": "#22c55e",
                    "text": "LONG"
                })
            elif direction == "SHORT":
                markers.append({
                    "time": d["time"],
                    "position": "aboveBar",
                    "shape": "arrowDown",
                    "color": "#ef4444",
                    "text": "SHORT"
                })
            elif direction:
                markers.append({
                    "time": d["time"],
                    "position": "inBar",
                    "shape": "circle",
                    "color": "#facc15",
                    "text": "NEUTRAL"
                })

            previous_direction = direction

    return markers
