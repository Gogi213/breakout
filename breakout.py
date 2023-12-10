# breakout.py
import pandas as pd
import pandas_ta as ta
import logging
from detect_breakouts import pivothigh, pivotlow

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BreakoutFinder:
    def __init__(self, df, prd=5, prd2=3, bo_len=200, cwidthu=0.03):
        self.df = df
        self.prd = prd
        self.prd2 = prd2
        self.bo_len = bo_len
        self.cwidthu = cwidthu
        self.phval = []  # Массив для хранения значений Pivot High
        self.phloc = []  # Массив для хранения местоположений Pivot High
        self.plval = []  # Массив для хранения значений Pivot Low
        self.plloc = []  # Массив для хранения местоположений Pivot Low

    def calculate_pivot_points(self):
        logging.info("Вычисление Pivot Points")
        self.df['PivotHigh'] = pivothigh(self.df, left=self.prd, right=self.prd)
        self.df['PivotLow'] = pivotlow(self.df, left=self.prd, right=self.prd)

        # Хранение значений и местоположений Pivot Points
        for i in range(len(self.df)):
            if not pd.isna(self.df['PivotHigh'][i]):
                self.phval.append(self.df['PivotHigh'][i])
                self.phloc.append(i)
            if not pd.isna(self.df['PivotLow'][i]):
                self.plval.append(self.df['PivotLow'][i])
                self.plloc.append(i)

    def calculate_breakout_width(self):
        # Расчет ширины прорыва
        highest_high = self.df['High'].rolling(window=self.prd).max()
        lowest_low = self.df['Low'].rolling(window=self.prd).min()
        self.df['BreakoutWidth'] = (highest_high - lowest_low) * self.cwidthu

    def detect_breakouts(self):
        # Вводная часть для обнаружения прорывов
        bomax = np.nan  # Потенциальный уровень бычьего прорыва
        bostart = -1  # Индекс начала потенциального бычьего прорыва
        num = 0  # Количество баров в потенциальном диапазоне бычьего прорыва
        hgst = self.df['High'].rolling(window=self.prd).max().shift(1)  # Наивысший максимум в периоде prd

        bomin = np.nan  # Потенциальный уровень медвежьего прорыва
        num1 = 0  # Количество баров в потенциальном диапазоне медвежьего прорыва
        lwst = self.df['Low'].rolling(window=self.prd).min().shift(1)  # Самый низкий минимум в периоде prd
