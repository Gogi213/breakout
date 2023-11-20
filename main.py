from binance_api import get_top_futures_pairs, get_historical_futures_data
from breakout import calculate_channel_width, find_pivot_points, find_breakouts
import pandas as pd

def main():
    top_pairs = get_top_futures_pairs()
    all_data = pd.DataFrame()

    for pair in top_pairs:
        print(f"Fetching data for {pair}")
        df = get_historical_futures_data(pair)
        df['Pair'] = pair

        # Применение логики поиска прорывов
        channel_width = calculate_channel_width(df)
        df = find_pivot_points(df)
        df = find_breakouts(df, channel_width)

        all_data = pd.concat([all_data, df], ignore_index=True)

    # Сохранение данных
    csv_filename = "all_futures_data.csv"
    all_data.to_csv(csv_filename, index=False)
    print(f"All data saved to {csv_filename}")

if __name__ == "__main__":
    main()
