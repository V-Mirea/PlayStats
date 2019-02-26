import PyQt5.QtWidgets as qt
from PyQt5 import QtGui, QtCore
from analysis import AnalysisWindow_ui


class AnalysisWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = AnalysisWindow_ui()
        self.ui.setupUi(self)

class VideoScreen(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.frame = QtGui.QImage()

    def paintEvent(self, _):
        painter = qt.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.paintImage = QtGui.QImage()

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.frame = image
        self.paintEvent()


