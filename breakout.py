import pandas as pd

def find_local_maxima(df, left_span=7, right_span=7):
    local_maxima = []
    for i in range(left_span, len(df) - right_span):
        if df['High'][i] > max(df['High'][i-left_span:i]) and df['High'][i] > max(df['High'][i+1:i+right_span+1]):
            local_maxima.append(i)
    return df.iloc[local_maxima]

def find_tests(df, local_maxima, threshold=0.0006, neighbors=5):
    tests = []
    for index, max_row in local_maxima.iterrows():
        max_price = max_row['High']
        lower_bound = max_price * (1 - threshold)
        test_candidates = df[(df.index > index) & (df['High'] <= max_price) & (df['High'] >= lower_bound)]
        test_candidates = test_candidates[test_candidates.index > index + 7]

        for test_index, test_row in test_candidates.iterrows():
            # Проверка, что нет свечей выше максимума между максимумом и тестом
            if df[(df.index > index) & (df.index < test_index) & (df['High'] > max_price)].empty:
                # Проверка, что тест-бар выше своих соседей
                if test_index >= neighbors and test_index < len(df) - neighbors:
                    left_neighbors = df['High'][test_index-neighbors:test_index]
                    right_neighbors = df['High'][test_index+1:test_index+neighbors+1]
                    if test_row['High'] > left_neighbors.max() and test_row['High'] > right_neighbors.max():
                        tests.append(test_index)

    return df.loc[tests]





