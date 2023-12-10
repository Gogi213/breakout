# breakout.py
import pandas as pd
import pandas_ta as ta
import logging
import numpy as np
from detect_breakouts import pivothigh, pivotlow

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BreakoutFinder:
    def __init__(self, df, prd=5, prd2=3, bo_len=200, cwidthu=0.03):
        logging.info("Инициализация BreakoutFinder")
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

        if self.df.empty:
            logging.warning("DataFrame is empty")
            return

        self.df.reset_index(drop=True, inplace=True)

        pivot_highs = pivothigh(self.df, left=self.prd, right=self.prd)
        pivot_lows = pivotlow(self.df, left=self.prd, right=self.prd)
        self.df = self.df.assign(PivotHigh=pivot_highs, PivotLow=pivot_lows)

        for i in range(len(self.df)):
            if not pd.isna(self.df['PivotHigh'][i]):
                self.phval.append(self.df['PivotHigh'][i])
                self.phloc.append(i)
            if not pd.isna(self.df['PivotLow'][i]):
                self.plval.append(self.df['PivotLow'][i])
                self.plloc.append(i)
        logging.info("Pivot Points вычислены")

    def calculate_breakout_width(self):
        logging.info("Расчет ширины прорыва")
        highest_high = self.df['High'].rolling(window=self.prd).max()
        lowest_low = self.df['Low'].rolling(window=self.prd).min()
        self.df.loc[:, 'BreakoutWidth'] = (highest_high - lowest_low) * self.cwidthu
        logging.info("Ширина прорыва рассчитана")
