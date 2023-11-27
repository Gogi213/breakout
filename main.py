# main,py
from binance_api import get_top_futures_pairs, get_historical_futures_data
import pandas as pd
from binance_api import preload_data


# Загрузка данных при запуске
preload_data()
def main():
    top_pairs = get_top_futures_pairs()
    all_data = pd.DataFrame()
    for pair in top_pairs:
        print(f"Fetching data for {pair}")
        df = get_historical_futures_data(pair)
        df['Pair'] = pair

        all_data = pd.concat([all_data, df], ignore_index=True)
    # Сохранение данных перед запуском веб-приложения
    csv_filename = "all_futures_data.csv"
    all_data.to_csv(csv_filename, index=False)
    print(f"All data saved to {csv_filename}")

if __name__ == "__main__":
    main()