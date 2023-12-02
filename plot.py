import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from binance_api import get_top_futures_pairs, get_historical_futures_data

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pivot Point Analysis')
        self.setGeometry(100, 100, 1200, 800)

        # Создание виджетов
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Создание списка валютных пар
        self.pair_list = QListWidget(self)
        self.pair_list.addItems(get_top_futures_pairs(limit=10))  # Примерное количество пар
        self.pair_list.setMaximumWidth(int(self.width() * 0.1))  # Преобразование в целое число
        self.pair_list.clicked.connect(self.pair_selected)

        # Создание области для графика
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.pair_list)

    def pair_selected(self, index):
        symbol = self.pair_list.item(index.row()).text()
        df = get_historical_futures_data(symbol)
        self.plot_data(df)

    def plot_data(self, df):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(df['Close'])  # Пример отображения цены закрытия
        self.canvas.draw()
