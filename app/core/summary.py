import statistics

def summarize_data(data):
    closes = [d["close"] for d in data if "close" in d]
    opens = [d["open"] for d in data if "open" in d]
    highs = [d["high"] for d in data if "high" in d]
    lows = [d["low"] for d in data if "low" in d]
    supports = [d["Support"] for d in data if isinstance(d["Support"], (int, float))]
    resistances = [d["Resistance"] for d in data if isinstance(d["Resistance"], (int, float))]

    bullish_days = sum(1 for d in data if d["direction"] == "LONG")
    bearish_days = sum(1 for d in data if d["direction"] == "SHORT")

    summary = {
        "Total data points": len(data),
        "Bullish days": bullish_days,
        "Bearish days": bearish_days,
        "Average Open": round(statistics.mean(opens), 2),
        "Average Close": round(statistics.mean(closes), 2),
        "Average High": round(statistics.mean(highs), 2),
        "Average Low": round(statistics.mean(lows), 2),
        "Average Support": round(statistics.mean(supports), 2) if supports else None,
        "Average Resistance": round(statistics.mean(resistances), 2) if resistances else None,
    }

    return summary
