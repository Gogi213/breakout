import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QListWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtCore import QUrl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from binance_api import get_top_futures_pairs, get_historical_futures_data

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, sourceID):
        print("JS:", message)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Crypto Analysis')
        self.setGeometry(100, 100, 1200, 800)

        # Создание главного виджета и главного layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        # Создание горизонтального layout для графика и списка
        self.h_layout = QHBoxLayout()
        self.main_layout.addLayout(self.h_layout)

        # Создание области для графика Plotly
        self.graph_view = QWebEngineView(self)
        self.graph_view.setPage(CustomWebEnginePage(self.graph_view))
        self.h_layout.addWidget(self.graph_view, 1)  # Добавление с соотношением 1

        # Создание списка валютных пар
        self.pair_list = QListWidget(self)
        self.pair_list.addItems(get_top_futures_pairs(limit=55))
        self.pair_list.setMaximumWidth(240)
        self.pair_list.clicked.connect(self.pair_selected)
        self.h_layout.addWidget(self.pair_list)  # Добавление без соотношения

        # Слот для обработки ошибок загрузки
        self.graph_view.loadFinished.connect(self.onLoadFinished)

    def pair_selected(self, index):
        symbol = self.pair_list.item(index.row()).text()
        df = get_historical_futures_data(symbol)
        print(df.head())
        self.plot_data(df)

    def plot_data(self, df):
        # Создание фигуры с двумя подграфиками
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.03, subplot_titles=('Candlestick', 'Volume'),
                            row_heights=[0.8, 0.2])  # Изменение соотношения высоты подграфиков

        # Добавление свечного графика
        fig.add_trace(go.Candlestick(x=df['Open time'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close']), row=1, col=1)

        # Добавление графика объема
        fig.add_trace(go.Bar(x=df['Open time'], y=df['Volume'], name='Volume'), row=2, col=1)

        # Обновление макета графика
        fig.update_layout(xaxis_rangeslider_visible=False)

        # Путь к директории для сохранения HTML-файлов
        html_dir = "C:\\Users\\Redmi\\PycharmProjects\\breakout\\html_files"
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)

        # Создание пути к HTML-файлу
        temp_file_path = os.path.join(html_dir, "temp_plot.html")
        fig.write_html(temp_file_path)
        print("HTML file saved at:", temp_file_path)

        # Отображение HTML в QWebEngineView
        self.graph_view.load(QUrl.fromLocalFile(os.path.abspath(temp_file_path)))
        self.graph_view.reload()

    def onLoadFinished(self, ok):
        if not ok:
            print("Ошибка загрузки HTML")
        else:
            print("HTML успешно загружен")
