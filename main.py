import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication
from plot import MainApp
from binance_api import get_top_futures_pairs, get_historical_futures_data, preload_data

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

    # Запуск GUI
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
