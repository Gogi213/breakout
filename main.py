from binance_api import get_top_futures_pairs, get_historical_futures_data
from plot import plot_breakouts, run_dash_app
import pandas as pd
from binance_api import preload_data

# Импорт функций из breakout.py
from breakout import find_local_maxima, find_tests, find_breakouts

# Загрузка данных при запуске
preload_data()

def main():
    top_pairs = get_top_futures_pairs()
    all_data = pd.DataFrame()

    for pair in top_pairs:
        print(f"Fetching data for {pair}")
        df = get_historical_futures_data(pair)
        df['Pair'] = pair

        # Применение логики индикатора пробоя
        local_maxima = find_local_maxima(df)
        tests = find_tests(df, local_maxima)
        breakouts = find_breakouts(df, local_maxima, tests)

        # Добавление результатов в DataFrame
        df['Local_Maxima'] = df.index.isin(local_maxima.index)
        df['Tests'] = df.index.isin(tests.index)
        df['Breakouts'] = df.index.isin(breakouts.index)

        # Отрисовка графика для каждой пары
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
