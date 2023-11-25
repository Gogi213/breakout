import pandas as pd

def find_local_maxima(df, left_span=7, right_span=7):
    local_maxima = []
    for i in range(left_span, len(df) - right_span):
        if df['High'][i] > max(df['High'][i-left_span:i]) and df['High'][i] > max(df['High'][i+1:i+right_span+1]):
            local_maxima.append(i)
    return df.iloc[local_maxima]

def find_tests(df, local_maxima, threshold=0.005):
    tests = []
    for index, max_row in local_maxima.iterrows():
        max_price = max_row['High']
        lower_bound = max_price * (1 - threshold)
        test_candidates = df[(df.index > index) & (df['High'] <= max_price) & (df['High'] >= lower_bound)]
        test_candidates = test_candidates[test_candidates.index > index + 7]

        last_test_price = max_price
        for test_index, test_row in test_candidates.iterrows():
            if test_row['High'] < last_test_price:
                tests.append(test_index)
                last_test_price = test_row['High']

    return df.loc[tests]
