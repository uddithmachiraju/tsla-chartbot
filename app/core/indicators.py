
def is_bullish_day(row):
    return row['close'] > row['open']

def count_bullish_days(df):
    return df[df['close'] > df['open']].shape[0]
