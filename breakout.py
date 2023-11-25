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
        max_price = max_row['Close']
        # Определяем диапазон цен для тестов
        upper_bound = max_price * 1.01  # 1% выше локального максимума
        lower_bound = max_price * (1 - threshold)  # не ниже 0.5% от локального максимума

        # Фильтруем кандидатов на тесты в этом диапазоне
        test_candidates = df[(df.index > index) & (df['Close'] >= lower_bound) & (df['Close'] <= upper_bound)]

        # Исключаем тесты в диапазоне +/- 7 свечей от локального максимума
        test_candidates = test_candidates[test_candidates.index > index + 7]

        # Выбираем тест с максимальной ценой закрытия
        if not test_candidates.empty:
            max_test = test_candidates.loc[test_candidates['Close'].idxmax()]
            tests.append(max_test.name)

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
