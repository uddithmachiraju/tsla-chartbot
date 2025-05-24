import pandas as pd
import numpy as np 
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

def mean_of_list_or_nan(lst):
    if isinstance(lst, list) and lst:
        return np.mean(lst)
    else:
        return float('nan')

def load_tsla_data(filepath="data/tsla_data.csv"):
    """Load and preprocess TSLA stock data from a CSV file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"TSLA data file not found at {filepath}")

    df = pd.read_csv(filepath)

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df = df.sort_values(by='timestamp')

    # Parse 'Support' and 'Resistance' columns (assuming they are stringified lists)
    if 'Support' in df.columns:
        df['Support'] = df['Support'].apply(safe_parse_list).apply(mean_of_list_or_nan)
    if 'Resistance' in df.columns:
        df['Resistance'] = df['Resistance'].apply(safe_parse_list).apply(mean_of_list_or_nan)

    df = df.dropna(subset=['open', 'high', 'low', 'close'])

    # Rename timestamp to 'time' for the chart library
    # df = df.rename(columns={"timestamp": "time"})

    # Sort by time
    df = df.sort_values(by="timestamp")

    return df[['timestamp', 'open', 'high', 'low', 'close', 'Support', 'Resistance']]
