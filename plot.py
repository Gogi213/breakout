import plotly.graph_objects as go

def plot_breakouts(df):
    # Создаем свечной график
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

    # Добавляем маркеры для прорывов вверх
    fig.add_trace(go.Scatter(
        x=df[df['BreakoutUp']].index,
        y=df[df['BreakoutUp']]['High'],
        mode='markers',
        marker=dict(color='Green', size=10),
        name='Breakout Up'
    ))

    # Добавляем маркеры для прорывов вниз
    fig.add_trace(go.Scatter(
        x=df[df['BreakoutDown']].index,
        y=df[df['BreakoutDown']]['Low'],
        mode='markers',
        marker=dict(color='Red', size=10),
        name='Breakout Down'
    ))

    # Настройки графика
    fig.update_layout(
        title='Breakout Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    fig.show()
