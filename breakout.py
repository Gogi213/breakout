import pandas as pd

# Функции для Breakout Finder
def calculate_channel_width(df, period=1000, cwidthu=0.03):
    period = min(period, len(df))
    rolling_max = df['High'].rolling(window=period).max()
    rolling_min = df['Low'].rolling(window=period).min()
    channel_width = (rolling_max - rolling_min) * cwidthu
    return channel_width

def find_pivot_points(df, prd=5, prd2=3, breakout_length=200):
    df['PivotHigh'] = None
    df['PivotLow'] = None

    pivot_highs = []
    pivot_lows = []

    for i in range(prd, len(df) - prd):
        period = prd2 if len(pivot_highs) > 0 or len(pivot_lows) > 0 else prd

        high_window = df['High'][i-period:i+period+1]
        low_window = df['Low'][i-period:i+period+1]

        if df['High'][i] == high_window.max() and df['High'][i] > high_window[0:period].max() and df['High'][i] > high_window[period+1:].max():
            df.at[i, 'PivotHigh'] = df['High'][i]
            pivot_highs.append((df['High'][i], i))

        if df['Low'][i] == low_window.min() and df['Low'][i] < low_window[0:period].min() and df['Low'][i] < low_window[period+1:].min():
            df.at[i, 'PivotLow'] = df['Low'][i]
            pivot_lows.append((df['Low'][i], i))

        # Удаление старых пивотных точек
        pivot_highs = [(val, idx) for val, idx in pivot_highs if i - idx <= breakout_length]
        pivot_lows = [(val, idx) for val, idx in pivot_lows if i - idx <= breakout_length]

    return df

def find_breakouts(df, channel_width, mintest=2):
    df['BreakoutUp'] = False
    df['BreakoutDown'] = False

    # Для каждого бара в данных
    for i in range(len(df)):
        pivot_highs = df.loc[max(0, i - mintest):i, 'PivotHigh'].dropna()
        pivot_lows = df.loc[max(0, i - mintest):i, 'PivotLow'].dropna()
        close_price = df.loc[i, 'Close']
        open_price = df.loc[i, 'Open']
        highest_price = df['High'].iloc[max(0, i - mintest):i+1].max()
        lowest_price = df['Low'].iloc[max(0, i - mintest):i+1].min()

        # Проверка прорыва вверх
        if len(pivot_highs) >= mintest and close_price > open_price and close_price > highest_price:
            max_pivot_high = pivot_highs.max()
            if open_price <= max_pivot_high and any(max_pivot_high >= ph >= max_pivot_high - channel_width[i] for ph in pivot_highs):
                df.loc[i, 'BreakoutUp'] = True

        # Проверка прорыва вниз
        if len(pivot_lows) >= mintest and close_price < open_price and close_price < lowest_price:
            min_pivot_low = pivot_lows.min()
            if open_price >= min_pivot_low and any(min_pivot_low <= pl <= min_pivot_low + channel_width[i] for pl in pivot_lows):
                df.loc[i, 'BreakoutDown'] = True

    return df