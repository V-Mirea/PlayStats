import PyQt5.QtWidgets as qt
from PyQt5 import QtGui, QtCore
from analysis import AnalysisWindow_ui
from pyqtgraph import ImageView


class AnalysisWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = AnalysisWindow_ui()
        self.ui.setupUi(self)

class VideoScreen(qt.QWidget):
    def __init__(self, parent=None, src=None):
        qt.QWidget.__init__(self, parent)
        self.frame = QtGui.QImage()

        self.layout = qt.QGridLayout(self)
        self.image_view = ImageView()
        self.layout.addWidget(self.image_view)
        self.setLayout(self.layout)

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.frame = image
        self.paintEvent()


