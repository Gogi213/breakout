import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from binance_api import get_top_futures_pairs, get_historical_futures_data
from breakout import calculate_channel_width, find_pivot_points, find_breakouts

# Инициализация Dash-приложения
app = dash.Dash(__name__)

# Получение списка пар
top_pairs = get_top_futures_pairs()

# Разметка приложения
app.layout = html.Div([
    dcc.Dropdown(
        id='pair-dropdown',
        options=[{'label': pair, 'value': pair} for pair in top_pairs],
        value=top_pairs[0]
    ),
    dcc.Graph(id='breakout-graph')
])

# Обратный вызов для обновления графика
@app.callback(
    Output('breakout-graph', 'figure'),
    [Input('pair-dropdown', 'value')]
)
def update_graph(selected_pair):
    df = get_historical_futures_data(selected_pair)
    channel_width = calculate_channel_width(df)
    df = find_pivot_points(df)
    df = find_breakouts(df, channel_width)

    # Создание графика с Plotly
    fig = go.Figure()

    # Добавление свечного графика
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='Candlesticks'))

    # Добавление линий прорыва и других элементов, если они есть в df
    if 'BreakoutHigh' in df.columns and 'BreakoutLow' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['BreakoutHigh'], mode='lines', name='Breakout High'))
        fig.add_trace(go.Scatter(x=df.index, y=df['BreakoutLow'], mode='lines', name='Breakout Low'))

    # Настройка внешнего вида графика
    fig.update_layout(title=f'Breakout Analysis for {selected_pair}',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)
    return fig

# Функция для запуска Dash-приложения
def run_dash_app():
    app.run_server(debug=True)

# Функция для отрисовки графика (вызывается из main.py)
def plot_breakouts(df):
    # Здесь может быть логика отрисовки графика без Dash
    pass
