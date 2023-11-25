import pandas as pd

def find_local_maxima(df, left_span=7, right_span=7):
    """
    Находит локальные максимумы в данных.
    """
    local_maxima = []
    for i in range(left_span, len(df) - right_span):
        if df['Close'][i] > max(df['Close'][i-left_span:i]) and df['Close'][i] > max(df['Close'][i+1:i+right_span+1]):
            local_maxima.append(i)
    return df.iloc[local_maxima]

def find_tests(df, local_maxima, threshold=0.005):
    tests = []
    for index, max_row in local_maxima.iterrows():
        max_price = max_row['Close']
        # Находим тесты, которые следуют после локального максимума
        test_candidates = df[(df.index > index) & (df['Close'] <= max_price * (1 + threshold))]
        # Исключаем тесты в диапазоне +/- 7 свечей от локального максимума
        test_candidates = test_candidates[test_candidates.index > index + 7]
        tests.extend(test_candidates.index.tolist())
    return df.loc[tests]




def find_breakouts(df, local_maxima, tests):
    """
    Определяет пробои.
    """
    breakouts = []
    for index, max_row in local_maxima.iterrows():
        max_price = max_row['Close']
        breakout_candidates = df[(df.index > index) & (df['Close'] > max_price)]
        for b_index, b_row in breakout_candidates.iterrows():
            if all(df.loc[tests.index[(tests.index < b_index) & (tests['Close'] < b_row['Close'])]]):
                breakouts.append(b_index)
    return df.loc[breakouts]
