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


class OpenCVQImage(QtGui.QImage):
    def __init__(self, opencvBgrImg):
        depth, nChannels = opencvBgrImg.depth, opencvBgrImg.nChannels
        if depth != cv2.IPL_DEPTH_8U or nChannels != 3:
            raise ValueError("the input image must be 8-bit, 3-channel")
        w, h = cv2.GetSize(opencvBgrImg)
        opencvRgbImg = cv2.CreateImage((w, h), depth, nChannels)
        # it's assumed the image is in BGR format
        cv2.CvtColor(opencvBgrImg, opencvRgbImg, cv2.CV_BGR2RGB)
        self._imgData = opencvRgbImg.tostring()
        super(OpenCVQImage, self).__init__(self._imgData, w, h, \
                                           QtGui.QImage.Format_RGB888)

class VideoScreen(qt.QWidget):
    startFrame = QtCore.pyqtSignal(np.ndarray)
    newFrame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, parent=None, src=None):
        super().__init__(parent)
        self._frame = None
        self._src = VideoStream(src)
        _, img = self._src.get_frame()

        self.startFrame.connect(self._onNewFrame)
        self.newFrame.connect(process_frame)
        self.startFrame.emit(img)

    #@QtCore.pyqtSlot(np.array)
    def _onNewFrame(self, frame):
        print("copied")
        #np.copyto(self._frame, frame)
        self._frame = frame
        self.newFrame.emit(self._frame)
        self.update()

    def timer(self):
        # gonna want a timer to keep track of when to query next frame
        pass

    def paintEvent(self, e):
        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), qimage2ndarray.array2qimage(self._frame))
        print("painted")
