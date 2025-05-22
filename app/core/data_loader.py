import pandas as pd
import ast
import os

def safe_parse_list(val):
    """Safely parse a stringified list from the CSV. Returns [nan] for invalid lists."""
    try:
        parsed = ast.literal_eval(val)
        if isinstance(parsed, list) and parsed:
            return parsed
        else:
            return [float('nan')]
    except Exception:
        return [float('nan')]

def load_tsla_data(filepath = "data/tsla_data.csv"):
    """Load and preprocess TSLA stock data from a CSV file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"TSLA data file not found at {filepath}")

    df = pd.read_csv(filepath)

    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Parse Support and Resistance columns
    df['Support'] = df['Support'].apply(safe_parse_list)
    df['Resistance'] = df['Resistance'].apply(safe_parse_list)

    # Add min and max values for plotting bands
    df['support_min'] = df['Support'].apply(min)
    df['support_max'] = df['Support'].apply(max)
    df['resistance_min'] = df['Resistance'].apply(min)
    df['resistance_max'] = df['Resistance'].apply(max)

    # Price trend info
    df['bullish'] = df['close'] > df['open']

    return df
