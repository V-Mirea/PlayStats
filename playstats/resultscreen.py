from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class AnalysisResults:
    pass

class CSGOResults(AnalysisResults):
    def __init__(self):
        self.frames = 0
        self.health = []
        self.armor = []
        self.money = []

class ResultsScreen(QtWidgets.QWidget):
    def __init__(self, results):  # Todo: For now takes only CSGOResults. Make whole class more generic
        super().__init__()
        self.results = results
        self.title = ""
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.figure = Figure()
        self.plot_canvas = FigureCanvas(self.figure)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self)

        graph_health = self.figure.add_subplot(311)
        graph_health.set_ylabel('Health')
        graph_health.plot(range(1, len(self.results.health)+1), self.results.health)

        graph_armor = self.figure.add_subplot(312)
        graph_armor.set_ylabel('Armor')
        graph_armor.plot(range(1, len(self.results.armor) + 1), self.results.armor)

        graph_money = self.figure.add_subplot(313)
        graph_money.set_ylabel('Money')
        graph_money.plot(range(1, len(self.results.money) + 1), self.results.money)

        self.plot_canvas.draw()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.plot_canvas)
        main_layout.addWidget(self.plot_toolbar)
        self.setLayout(main_layout)