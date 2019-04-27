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

        num_results = len(self.results)
        for i in range(num_results):
            result = list(self.results.items())[i]
            subplot = self.figure.add_subplot(num_results, 1, i+1)
            subplot.set_ylabel(result[0])
            subplot.plot(range(1, len(result[1]) + 1), result[1])

        self.plot_canvas.draw()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.plot_canvas)
        main_layout.addWidget(self.plot_toolbar)
        self.setLayout(main_layout)