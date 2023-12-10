import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QListWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtCore import QUrl
import plotly.graph_objects as go
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

        # Создание виджетов
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Горизонтальное расположение виджетов
        self.layout = QHBoxLayout(self.main_widget)

        # Создание области для графика Plotly
        self.graph_view = QWebEngineView(self)
        self.graph_view.setPage(CustomWebEnginePage(self.graph_view))
        self.graph_view.setMinimumSize(960, 800)  # Примерное соотношение для графика
        self.layout.addWidget(self.graph_view)

        # Создание списка валютных пар
        self.pair_list = QListWidget(self)
        self.pair_list.addItems(get_top_futures_pairs(limit=10))
        self.pair_list.setMaximumWidth(240)  # Установка ширины списка валютных пар
        self.pair_list.clicked.connect(self.pair_selected)
        self.layout.addWidget(self.pair_list)

        # Слот для обработки ошибок загрузки
        self.graph_view.loadFinished.connect(self.onLoadFinished)

    def pair_selected(self, index):
        symbol = self.pair_list.item(index.row()).text()
        df = get_historical_futures_data(symbol)
        print(df.head())  # Вывод данных для проверки
        self.plot_data(df)

    def plot_data(self, df):
        fig = go.Figure(data=[go.Candlestick(x=df['Open time'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

        # Путь к директории для сохранения HTML-файлов
        html_dir = "C:\\Users\\Redmi\\PycharmProjects\\breakout\\html_files"
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)

        # Создание пути к HTML-файлу
        temp_file_path = os.path.join(html_dir, "temp_plot.html")
        fig.write_html(temp_file_path)
        print("HTML file saved at:", temp_file_path)  # Вывод пути к файлу

        # Отображение HTML в QWebEngineView
        self.graph_view.load(QUrl.fromLocalFile(os.path.abspath(temp_file_path)))
        self.graph_view.reload()  # Перезагрузка QWebEngineView

    def onLoadFinished(self, ok):
        if not ok:
            print("Ошибка загрузки HTML")
        else:
            print("HTML успешно загружен")