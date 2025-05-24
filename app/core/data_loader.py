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
        return np.min(lst)
    else:
        return float('nan')

def load_tsla_data(filepath="data/tsla_data.csv", return_ohlc=False):
    """Load and preprocess TSLA stock data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.
        return_ohlc (bool): If True, return OHLC formatted data as list of dicts.

    Returns:
        DataFrame OR (DataFrame, List[Dict]): Full cleaned DataFrame,
            and optionally OHLC data as a Python list of dictionaries.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"TSLA data file not found at {filepath}")

    df = pd.read_csv(filepath)

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df = df.sort_values(by='timestamp')

    # Parse 'Support' and 'Resistance' columns
    if 'Support' in df.columns:
        df['Support'] = df['Support'].apply(safe_parse_list).apply(mean_of_list_or_nan)
    if 'Resistance' in df.columns:
        df['Resistance'] = df['Resistance'].apply(safe_parse_list).apply(mean_of_list_or_nan)

    df = df.dropna(subset=['open', 'high', 'low', 'close', 'direction', 'Support', 'Resistance'])

    # Prepare OHLC formatted list of dicts
    ohlc_data = df[['timestamp', 'direction', 'open', 'high', 'low', 'close', 'Support', 'Resistance']].copy()
    ohlc_data['time'] = ohlc_data['timestamp'].dt.strftime('%Y-%m-%d')
    ohlc_data = ohlc_data[['time', 'direction', 'open', 'high', 'low', 'close', 'Support', 'Resistance']]
    formatted_data = ohlc_data.to_dict('records')

    if return_ohlc:
        return df[['timestamp', 'direction', 'open', 'high', 'low', 'close', 'Support', 'Resistance']], formatted_data
    else:
        return df[['timestamp', 'direction', 'open', 'high', 'low', 'close', 'Support', 'Resistance']]
