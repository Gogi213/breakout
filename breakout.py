import pandas as pd

def find_local_maxima(df, window=14):
    """
    Находит локальные максимумы в данных.

    :param df: DataFrame с данными о ценах.
    :param window: Размер окна для определения локального максимума.
    :return: Список индексов локальных максимумов.
    """
    local_maxima_indices = df['High'].rolling(window, center=True).apply(lambda x: x.argmax() if x.max() != x.iloc[0] else 0)
    return local_maxima_indices[local_maxima_indices != 0].index.tolist()

def find_tests(df, local_maxima_indices):
    """
    Функция для поиска тестов.

    :param df: DataFrame с данными о ценах.
    :param local_maxima_indices: Список индексов локальных максимумов.
    :return: Список тестов.
    """
    tests = []
    for index in local_maxima_indices:
        max_row = df.iloc[index]
        test_index = df[(df.index > index) & (df['High'] > max_row['High'])].index.min()
        if pd.notna(test_index):
            test_row = df.loc[test_index]
            tests.append({'max_index': index, 'test_index': test_index, 'max_price': max_row['High'], 'test_price': test_row['High']})
    return tests