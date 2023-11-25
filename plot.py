import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from binance_api import get_top_futures_pairs, get_historical_futures_data
from breakout import find_local_maxima, find_tests, find_breakouts

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

    # Находим локальные максимумы, тесты и пробои
    local_maxima = find_local_maxima(df)
    tests = find_tests(df, local_maxima)
    breakouts = find_breakouts(df, local_maxima, tests)

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

    # Добавление маркеров для локальных максимумов, тестов и пробоев
    fig.add_trace(go.Scatter(
        x=local_maxima.index,
        y=local_maxima['High'],
        mode='markers',
        marker=dict(color='blue', size=5),
        name='Local Maxima'
    ))

    fig.add_trace(go.Scatter(
        x=tests.index,
        y=tests['High'],
        mode='markers',
        marker=dict(color='orange', size=5),
        name='Tests'
    ))

    fig.add_trace(go.Scatter(
        x=breakouts.index,
        y=breakouts['High'],
        mode='markers',
        marker=dict(color='green', size=5),
        name='Breakouts'
    ))

    # Соединение локальных максимумов с тестами и добавление горизонтальных линий
    maxima_indices = local_maxima.index.tolist()
    for i in range(len(maxima_indices) - 1):
        max_index = maxima_indices[i]
        next_max_index = maxima_indices[i + 1]
        test_candidates = tests[(tests.index > max_index) & (tests.index < next_max_index)]

        for test_index, test_row in test_candidates.iterrows():
            fig.add_trace(go.Scatter(
                x=[max_index, test_index],
                y=[df.loc[max_index]['High'], test_row['High']],
                mode='lines',
                line=dict(color='lightblue', width=1),
                showlegend=False
            ))

        # Добавление горизонтальной линии от максимума
        fig.add_trace(go.Scatter(
            x=[max_index, df.index[-1]],
            y=[df.loc[max_index]['High'], df.loc[max_index]['High']],
            mode='lines',
            line=dict(color='blue', width=1, dash='dash'),
            showlegend=False
        ))

        # Нумерация и горизонтальные линии для тестов
        for test_number, (test_index, test_row) in enumerate(test_candidates.iterrows(), start=1):
            # Горизонтальная линия от теста
            fig.add_trace(go.Scatter(
                x=[test_index, df.index[-1]],
                y=[test_row['High'], test_row['High']],
                mode='lines',
                line=dict(color='orange', width=1, dash='dash'),
                showlegend=False
            ))

            # Нумерация тестов
            fig.add_annotation(
                x=test_index,
                y=test_row['High'],
                text=str(test_number),
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="#ffffff"
                ),
                align="center",
                bgcolor="orange",
                bordercolor="black",
                borderwidth=2,
                borderpad=4
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
