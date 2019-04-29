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

        self.title = "PlayStats - Results"
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.width = 640
        self.height = 480

        screen = QtWidgets.QDesktopWidget().availableGeometry()
        self.left = (screen.width() / 2) - (self.width / 2)
        self.top = (screen.height() / 2) - (self.height / 2)

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

            if i != num_results-1:
                subplot.set_xticklabels([])
            else:
                subplot.set_xlabel("frame")

        self.plot_canvas.draw()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.plot_canvas)
        main_layout.addWidget(self.plot_toolbar)
        self.setLayout(main_layout)