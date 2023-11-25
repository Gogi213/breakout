import pandas as pd

def find_local_maxima(df, left_span=7, right_span=7):
    local_maxima = []
    for i in range(left_span, len(df) - right_span):
        if df['High'][i] > max(df['High'][i-left_span:i]) and df['High'][i] > max(df['High'][i+1:i+right_span+1]):
            local_maxima.append(i)
    return df.iloc[local_maxima]

def find_tests(df, local_maxima, threshold=0.005):
    tests = []
    last_max_price = 0
    for index, max_row in local_maxima.iterrows():
        max_price = max_row['High']
        if max_price <= last_max_price:
            continue
        last_max_price = max_price

        lower_bound = max_price * (1 - threshold)
        test_candidates = df[(df.index > index) & (df['High'] <= max_price) & (df['High'] >= lower_bound)]
        test_candidates = test_candidates[test_candidates.index > index + 7]

        if not test_candidates.empty:
            max_test = test_candidates.loc[test_candidates['High'].idxmax()]
            tests.append(max_test.name)

    return df.loc[tests]

def find_breakouts(df, local_maxima, tests):
    """
    Определяет пробои.
    """
    breakouts = []
    for index, max_row in local_maxima.iterrows():
        max_price = max_row['High']
        breakout_candidates = df[(df.index > index) & (df['High'] > max_price)]
        for b_index, b_row in breakout_candidates.iterrows():
            if all(df.loc[tests.index[(tests.index < b_index) & (tests['High'] < b_row['High'])]]):
                breakouts.append(b_index)
    return df.loc[breakouts]
