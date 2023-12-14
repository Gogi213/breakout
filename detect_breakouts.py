# detect_breakouts.py
import numpy as np
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_breakouts(df, phval, phloc, plval, plloc, prd, cwidthu, mintest):
    # logging.info("Обнаружение прорывов")
    # logging.info(f"Размер phval: {len(phval)}, Размер plval: {len(plval)}")

    # logging.info(f"phval: {phval}")
    #
    # # Логирование содержимого phval и plval
    # logging.info(f"phval: {phval}")
    # logging.info(f"plval: {plval}")

    bomax = np.nan  # Потенциальный уровень бычьего прорыва
    bomin = np.nan  # Потенциальный уровень медвежьего прорыва
    bostart = -1    # Индекс начала потенциального прорыва
    num = 0         # Количество баров в потенциальном диапазоне бычьего прорыва
    num1 = 0        # Количество баров в потенциальном диапазоне медвежьего прорыва

    hgst = df['High'].rolling(window=prd).max().shift(1)
    lwst = df['Low'].rolling(window=prd).min().shift(1)

    for i in range(len(df)):
        # Обнаружение бычьего прорыва
        if len(phval) >= mintest and df['Close'][i] > df['Open'][i] and df['Close'][i] > hgst[i]:
            current_bomax = phval[0]
            xx = 0
            tests = []
            for x in range(len(phval)):
                if phval[x] >= df['Close'][i]:
                    break
                xx = x
                current_bomax = max(current_bomax, phval[x])

            current_num = 0
            if xx >= mintest and df['Open'][i] <= current_bomax:
                for x in range(xx + 1):
                    if phval[x] <= current_bomax and phval[x] >= current_bomax - cwidthu:
                        current_num += 1
                        bostart = phloc[x]
                        tests.append(phval[x])  # Добавление валидного теста в tests

                if current_num >= mintest and (np.isnan(bomax) or hgst[i] < current_bomax):
                    bomax = current_bomax
                    num = current_num
                    pair_name = df['Pair'][i]  # Получение названия валютной пары
                    logging.info(
                        f"Бычий прорыв обнаружен для {pair_name} на баре {i}. Уровень прорыва: {bomax}, Количество тестов: {num}, Валидные тесты: {tests}")

    for i in range(len(df)):
        # Обнаружение медвежьего прорыва
        if len(plval) >= mintest and df['Close'][i] < df['Open'][i] and df['Close'][i] < lwst[i]:
            current_bomin = plval[0]
            xx = 0
            tests = []
            for x in range(len(plval)):
                if plval[x] <= df['Close'][i]:
                    break
                xx = x
                current_bomin = min(current_bomin, plval[x])

            current_num = 0
            if xx >= mintest and df['Open'][i] >= current_bomin:
                for x in range(xx + 1):
                    if plval[x] >= current_bomin and plval[x] <= current_bomin + cwidthu:
                        current_num += 1
                        bostart = plloc[x]
                        tests.append(plval[x])  # Добавление валидного теста в tests

                if current_num >= mintest and (np.isnan(bomin) or lwst[i] > current_bomin):
                    bomin = current_bomin
                    num = current_num
                    pair_name = df['Pair'][i]  # Получение названия валютной пары
                    logging.info(
                        f"Медвежий прорыв обнаружен для {pair_name} на баре {i}. Уровень прорыва: {bomin}, Количество тестов: {num}, Валидные тесты: {tests}")

    return bomax, bostart, num, bomin, num1

def pivothigh(df, left, right):
    length = len(df)
    pivot_highs = pd.Series([None] * length)

    for i in range(left, length - right):
        max_left = df['High'].iloc[i - left:i].max()
        max_right = df['High'].iloc[i + 1:i + 1 + right].max()
        current_high = df['High'].iloc[i]

        if current_high > max_left and current_high > max_right:
            pivot_highs.iloc[i] = current_high

    return pivot_highs.copy()

def pivotlow(df, left, right):
    length = len(df)
    pivot_lows = pd.Series([None] * length)

    for i in range(left, length - right):
        min_left = df['Low'].iloc[i - left:i].min()
        min_right = df['Low'].iloc[i + 1:i + 1 + right].min()
        current_low = df['Low'].iloc[i]

        if current_low < min_left and current_low < min_right:
            pivot_lows.iloc[i] = current_low

    return pivot_lows.copy()