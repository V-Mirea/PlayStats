import PyQt5.QtWidgets as qt
from PyQt5 import QtGui, QtCore
import numpy as np
import cv2
import qimage2ndarray

from analysis import AnalysisWindow_ui
from video import VideoStream
from algorithms import process_frame
from videoplayer_ui import VideoPlayer_ui


class AnalysisWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = AnalysisWindow_ui()
        self.ui.setupUi(self)


class VideoPlayer(qt.QWidget):
    _DEFAULT_FPS = 30

    newFrame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, parent=None, src=None):
        super().__init__(parent)
        self.ui = VideoPlayer_ui()
        self.ui.setupUi(self)

        self._frame = None
        self._src = VideoStream(src)

        # This timer will dictate when a new frame should be drawn
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._getNewFrame)
        self._timer.setInterval(1000 / self._DEFAULT_FPS)

        self.newFrame.connect(process_frame)

        self.ui.buttonBack.clicked.connect(self.rewind)
        self.ui.buttonPause.clicked.connect(self.togglePause)

    def rewind(self):
        self._src.src.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self._getNewFrame()

    def resume(self):
        self._timer.start()

    def pause(self):
        self._timer.stop()

    def togglePause(self):
        if self._timer.isActive():
            self.pause()
        else:
            self.resume()

    def _getNewFrame(self):
        ret, frame = self._src.get_frame()
        if ret:
            self._frame = frame  # Todo: make this a copy
            self.newFrame.emit(self._frame)
            self.update()
        else:
            self.pause()

    def paintEvent(self, e):
        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), qimage2ndarray.array2qimage(cv2.resize(self._frame, (self.geometry().width(), self.geometry().height()))))
