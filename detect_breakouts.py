# detect_breakouts.py
import numpy as np

def detect_breakouts(df, phval, phloc, plval, plloc, prd, cwidthu, mintest):
    # Вводная часть для обнаружения прорывов
    bomax = np.nan  # Потенциальный уровень бычьего прорыва
    bostart = -1  # Индекс начала потенциального бычьего прорыва
    num = 0  # Количество баров в потенциальном диапазоне бычьего прорыва
    hgst = df['High'].rolling(window=prd).max().shift(1)  # Наивысший максимум в периоде prd

    bomin = np.nan  # Потенциальный уровень медвежьего прорыва
    num1 = 0  # Количество баров в потенциальном диапазоне медвежьего прорыва
    lwst = df['Low'].rolling(window=prd).min().shift(1)  # Самый низкий минимум в периоде prd

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

    # Обнаружение медвежьего прорыва
    if len(plval) >= mintest and df['Close'] < df['Open'] and df['Close'] < lwst:
        bomin = plval[0]
        xx = 0
        for x in range(len(plval)):
            if plval[x] <= df['Close']:
                break
            xx = x
            bomin = min(bomin, plval[x])

        if xx >= mintest and df['Open'] >= bomin:
            for x in range(xx + 1):
                if plval[x] >= bomin and plval[x] <= bomin + cwidthu:
                    num1 += 1
                    bostart = plloc[x]

            if num1 < mintest or lwst <= bomin:
                bomin = np.nan

    # Возвращаем результаты
    return bomax, bostart, num, bomin, num1

# Пример использования функции
# Результаты функции можно использовать для дальнейшего анализа или визуализации
