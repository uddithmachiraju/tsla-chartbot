
def parse_numeric_list(val):
    """
    Parses a string or list-like value to a list of floats.
    Handles malformed or empty strings like ' ', '[', ']', etc.
    """
    if isinstance(val, str):
        val = val.strip("[] ")
        if val:
            try:
                return [float(x.strip()) for x in val.split(',') if x.strip()]
            except ValueError:
                return []
        else:
            return []
    elif isinstance(val, (list, tuple)):
        return [float(x) for x in val if x != '' and x is not None]
    else:
        return []

def generate_support_resistance_bands(df):
    support_bands = []
    resistance_bands = []

    for _, row in df.iterrows():
        time_str = row['timestamp'].strftime('%Y-%m-%d')

        # Parse and clean support and resistance values
        support = parse_numeric_list(row.get('Support'))
        resistance = parse_numeric_list(row.get('Resistance'))

        if support:
            support_bands.append({
                "time": time_str,
                "low": min(support),
                "high": max(support)
            })

        if resistance:
            resistance_bands.append({
                "time": time_str,
                "low": min(resistance),
                "high": max(resistance)
            })

    return support_bands, resistance_bands
