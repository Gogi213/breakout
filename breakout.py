import pandas as pd

def find_local_maxima(df, window=1000):
    """
    Находит локальные максимумы в данных.
    """
    local_maxima = df['Close'].rolling(window=window, min_periods=1).max()
    return df[df['Close'] == local_maxima]

def find_tests(df, local_maxima, threshold=0.005):
    """
    Определяет тесты локальных максимумов.
    """
    tests = []
    for index, max_row in local_maxima.iterrows():
        max_price = max_row['Close']
        test_candidates = df[(df.index > index) & (df['Close'] <= max_price * (1 + threshold))]
        tests.extend(test_candidates.index.tolist())
    return df.loc[tests]

def find_breakouts(df, local_maxima, tests):
    breakouts = []
    for index, max_row in local_maxima.iterrows():
        max_price = max_row['Close']
        breakout_candidates = df[(df.index > index) & (df['Close'] > max_price)]
        for b_index, b_row in breakout_candidates.iterrows():
            if all(df.loc[tests.index[(tests.index < b_index) & (tests['Close'] < b_row['Close'])]]):
                breakouts.append(b_index)
    return df.loc[breakouts]

