# breakout.py
import pandas as pd
import logging
import numpy as np
from detect_breakouts import pivothigh, pivotlow, detect_breakouts

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BreakoutFinder:
    def __init__(self, df, prd=7, prd2=5, bo_len=1500, cwidthu=0.3):
        # logging.info("Инициализация BreakoutFinder")
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
        if self.df.empty:
            logging.warning("DataFrame is empty")
            return

        self.df.reset_index(drop=True, inplace=True)

        # Использование prd2, если уже найдены точки поворота
        left_param = self.prd2 if self.phval or self.plval else self.prd
        right_param = self.prd2 if self.phval or self.plval else self.prd

        pivot_highs = pivothigh(self.df, left=left_param, right=right_param)
        pivot_lows = pivotlow(self.df, left=left_param, right=right_param)
        self.df = self.df.assign(PivotHigh=pivot_highs, PivotLow=pivot_lows)

        for i in range(len(self.df)):
            if not pd.isna(self.df['PivotHigh'][i]):
                self.phval.append(self.df['PivotHigh'][i])
                self.phloc.append(i)

            if not pd.isna(self.df['PivotLow'][i]):
                self.plval.append(self.df['PivotLow'][i])
                self.plloc.append(i)

        self.cleanup_old_pivot_points()

    def calculate_chwidth(self):
        highest_high = [None] * len(self.df)
        lowest_low = [None] * len(self.df)

        for index in range(len(self.df)):
            lll = max(min(index, 1500), 1)
            highest_high[index] = self.df['High'][max(0, index - lll):index].max()
            lowest_low[index] = self.df['Low'][max(0, index - lll):index].min()

        self.df['chwidth'] = [(h - l) * self.cwidthu if h is not None and l is not None else None for h, l in
                              zip(highest_high, lowest_low)]
        print("chwidth calculated and added to DataFrame.")
        return self.df


    def cleanup_old_pivot_points(self):
        # Очистка старых точек Pivot High
        self.phval, self.phloc = self._cleanup_pivot_points(self.phval, self.phloc)

        # Очистка старых точек Pivot Low
        self.plval, self.plloc = self._cleanup_pivot_points(self.plval, self.plloc)

    def _cleanup_pivot_points(self, values, locations):
        cleaned_values = []
        cleaned_locations = []
        for val, loc in zip(values, locations):
            if len(self.df) - loc <= self.bo_len:
                cleaned_values.append(val)
                cleaned_locations.append(loc)
        return cleaned_values, cleaned_locations