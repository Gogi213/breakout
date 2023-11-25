import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from binance_api import get_top_futures_pairs, get_historical_futures_data
from breakout import find_local_maxima, find_tests

# Инициализация Dash-приложения
app = dash.Dash(__name__)

# Получение списка пар
top_pairs = get_top_futures_pairs()

# Разметка приложения
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='breakout-graph', config={'scrollZoom': True, 'displayModeBar': True})
    ], style={'display': 'inline-block', 'width': '92%', 'height': '250%'}),

    html.Div([
        html.Div([html.Button(pair, id=pair, n_clicks=0) for pair in top_pairs],
                 style={'display': 'flex', 'flexDirection': 'column'})
    ], style={'display': 'inline-block', 'width': '8%'})
], style={'display': 'flex'})

# Обратный вызов для обновления графика
@app.callback(
    Output('breakout-graph', 'figure'),
    [Input(pair, 'n_clicks') for pair in top_pairs]
)
def update_graph(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        selected_pair = top_pairs[0]
    else:
        selected_pair = ctx.triggered[0]['prop_id'].split('.')[0]

    df = get_historical_futures_data(selected_pair)

    # Находим локальные максимумы и тесты
    local_maxima = find_local_maxima(df)
    tests = find_tests(df, local_maxima)

    # Создание графика с Plotly
    fig = go.Figure()

    # Добавление свечного графика
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlesticks'
    ))

    # Добавление маркеров и линий для тестов
    for max_index, max_row in local_maxima.iterrows():
        test_indices = tests[(tests.index > max_index) & (tests['High'] < max_row['High'])].index[:7]
        for i, test_index in enumerate(test_indices, start=1):
            test_row = df.loc[test_index]
            # Добавление линии от максимума к тесту
            fig.add_trace(go.Scatter(
                x=[max_index, test_index],
                y=[max_row['High'], test_row['High']],
                mode='lines',
                line=dict(color='lightblue', width=2),
                showlegend=False
            ))
            # Обозначение тестов
            fig.add_annotation(
                x=test_index,
                y=test_row['High'],
                text=str(i),
                showarrow=True,
                arrowhead=1
            )

    # Настройка внешнего вида графика
    fig.update_layout(
        title=f'Breakout Analysis for {selected_pair}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        height=750  # Установка высоты графика
    )

    # Настройки для интерактивности (панорамирование, масштабирование)
    fig.update_xaxes(rangeslider_visible=True)

    return fig

# Функция для запуска Dash-приложения
def run_dash_app():
    app.run_server(debug=True)

# Функция для отрисовки графика (вызывается из main.py)
def plot_breakouts(df):
    # Здесь может быть логика отрисовки графика без Dash
    pass
