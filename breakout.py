import pandas as pd

# Функции для Breakout Finder
def calculate_channel_width(df, period=300, cwidthu=0.03):
    period = min(period, len(df))
    rolling_max = df['High'].rolling(window=period).max()
    rolling_min = df['Low'].rolling(window=period).min()
    channel_width = (rolling_max - rolling_min) * cwidthu
    return channel_width

def find_pivot_points(df, period=5, breakout_length=200):
    df['PivotHigh'] = df['High'][(df['High'].shift(1) < df['High']) & (df['High'].shift(-1) < df['High'])]
    df['PivotLow'] = df['Low'][(df['Low'].shift(1) > df['Low']) & (df['Low'].shift(-1) > df['Low'])]

    # Удаление старых пивотных точек
    for i in range(len(df)):
        if pd.notna(df.loc[i, 'PivotHigh']) and (i + breakout_length < len(df)):
            df.loc[i, 'PivotHigh'] = None
        if pd.notna(df.loc[i, 'PivotLow']) and (i + breakout_length < len(df)):
            df.loc[i, 'PivotLow'] = None

    return df

def find_breakouts(df, channel_width, mintest=2):
    df['BreakoutUp'] = False
    df['BreakoutDown'] = False
    for i in range(len(df)):
        pivot_high = df.loc[i, 'PivotHigh']
        pivot_low = df.loc[i, 'PivotLow']
        close_price = df.loc[i, 'Close']

        if pd.notna(pivot_high) and len(df.loc[i - mintest:i, 'PivotHigh'].dropna()) >= mintest:
            if close_price > pivot_high + channel_width[i]:
                df.loc[i, 'BreakoutUp'] = True

        if pd.notna(pivot_low) and len(df.loc[i - mintest:i, 'PivotLow'].dropna()) >= mintest:
            if close_price < pivot_low - channel_width[i]:
                df.loc[i, 'BreakoutDown'] = True

    return df
