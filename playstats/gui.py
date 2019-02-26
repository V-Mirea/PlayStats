import PyQt5.QtWidgets as qt
from PyQt5 import QtGui, QtCore
import numpy as np
import cv2
import qimage2ndarray

from analysis import AnalysisWindow_ui
from video import VideoStream
from algorithms import process_frame

class AnalysisWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = AnalysisWindow_ui()
        self.ui.setupUi(self)

class VideoScreen(qt.QWidget):
    _DEFAULT_FPS = 30

    newFrame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, parent=None, src=None):
        super().__init__(parent)
        self._frame = None
        self._src = VideoStream(src)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._getNewFrame)
        self._timer.setInterval(1000 / self._DEFAULT_FPS)

        self.newFrame.connect(process_frame)

    def _getNewFrame(self):
        _, frame = self._src.get_frame()
        self._frame =  frame # Todo: make this a copy
        self.newFrame.emit(self._frame)
        self.update()

    def paintEvent(self, e):
        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), qimage2ndarray.array2qimage(cv2.resize(self._frame, (self.geometry().width(), self.geometry().height()))))
