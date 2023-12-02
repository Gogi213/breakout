# detect_breakouts.py
import numpy as np

def detect_breakouts(df, phval, phloc, plval, plloc, prd, cwidthu, mintest):
    # Вводная часть для обнаружения прорывов
    bomax = np.nan
    bostart = -1
    num = 0
    hgst = df['High'].rolling(window=prd).max().shift(1)

    bomin = np.nan
    num1 = 0
    lwst = df['Low'].rolling(window=prd).min().shift(1)

    # Обнаружение бычьего прорыва
    if len(phval) >= mintest and df['Close'] > df['Open'] and df['Close'] > hgst:
        bomax = phval[0]
        xx = 0
        for x in range(len(phval)):
            if phval[x] >= df['Close']:
                break
            xx = x
            bomax = max(bomax, phval[x])

        if xx >= mintest and df['Open'] <= bomax:
            for x in range(xx + 1):
                if phval[x] <= bomax and phval[x] >= bomax - cwidthu:
                    num += 1
                    bostart = phloc[x]

            if num < mintest or hgst >= bomax:
                bomax = np.nan

    # Здесь будет код для обнаружения медвежьего прорыва

    # Возвращаем результаты
    return bomax, bostart, num, bomin, num1

# Пример использования функции
# Результаты функции можно использовать для дальнейшего анализа или визуализации
