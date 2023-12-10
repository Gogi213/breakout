import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication
from plot import MainApp
from binance_api import get_top_futures_pairs, get_historical_futures_data, preload_data
from breakout import BreakoutFinder
from detect_breakouts import detect_breakouts

def main():
    # Загрузка данных при запуске
    preload_data()

    # Агрегация данных по всем валютным парам
    top_pairs = get_top_futures_pairs()
    all_data = pd.DataFrame()
    for pair in top_pairs:
        print(f"Fetching data for {pair}")
        df = get_historical_futures_data(pair)
        df['Pair'] = pair
        all_data = pd.concat([all_data, df], ignore_index=True)

    # Сохранение агрегированных данных перед запуском веб-приложения
    csv_filename = "all_futures_data.csv"
    all_data.to_csv(csv_filename, index=False)
    print(f"All data saved to {csv_filename}")

    # Обработка данных с помощью BreakoutFinder и detect_breakouts
    for pair in top_pairs:
        df_pair = all_data[all_data['Pair'] == pair]
        breakout_finder = BreakoutFinder(df_pair)
        breakout_finder.calculate_pivot_points()
        breakout_finder.calculate_breakout_width()

        # Получение данных из breakout_finder
        phval = breakout_finder.phval
        phloc = breakout_finder.phloc
        plval = breakout_finder.plval
        plloc = breakout_finder.plloc
        prd = breakout_finder.prd
        cwidthu = breakout_finder.cwidthu
        mintest = 3  # Примерное значение, установите его в соответствии с вашей логикой

        # Вызов detect_breakouts с полученными данными
        detect_breakouts(df_pair, phval, phloc, plval, plloc, prd, cwidthu, mintest)

    # Запуск GUI
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
