from PyQt5 import QtCore, QtGui, QtWidgets

class ResultsScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)