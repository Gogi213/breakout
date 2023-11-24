from binance_api import get_top_futures_pairs, get_historical_futures_data
# Если вы перенесли функции из breakout.py в другой файл, импортируйте их здесь
# from another_module import calculate_channel_width, find_pivot_points, find_breakouts

from plot import plot_breakouts
from plot import run_dash_app
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

        # Если вы решили сохранить логику поиска прорывов, добавьте её здесь
        # channel_width = calculate_channel_width(df)
        # df = find_pivot_points(df)
        # df = find_breakouts(df, channel_width)

        # Отрисовка графика для каждой пары
        # Если логика поиска прорывов была удалена, возможно, вам нужно будет изменить эту функцию
        plot_breakouts(df)

        all_data = pd.concat([all_data, df], ignore_index=True)

    # Сохранение данных перед запуском веб-приложения
    csv_filename = "all_futures_data.csv"
    all_data.to_csv(csv_filename, index=False)
    print(f"All data saved to {csv_filename}")

    # Запуск веб-приложения после обработки всех данных
    run_dash_app()

if __name__ == "__main__":
    main()
