import PyQt5.QtWidgets as qt
from PyQt5 import QtGui, QtCore
import numpy as np
import cv2
import qimage2ndarray

from analysis_ui import AnalysisWindow_ui
import algorithms
from videoplayer_ui import VideoPlayer_ui

FILTERS = {"Videos": [".avi", ".mp4"], "Images": [".png", ".jpg"]}
FILTERLIST = ""

# Use FILTERS map to make a list of filters for FileDialog
for key, val in FILTERS.items():
    if FILTERLIST != "":
        FILTERLIST += ";;"

    FILTERLIST += key + " (*" + " *".join(val) + ")"

class AnalysisWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = AnalysisWindow_ui()
        self.ui.setupUi(self)

        self.ui.buttonBrowse.clicked.connect(self.browseDirectory)
        self.ui.buttonStart.clicked.connect(self.startAnalysis)

        # Create and add video player
        self._screen = VideoPlayer(self)
        layout = qt.QGridLayout(self.ui.widget)
        layout.addWidget(self._screen)
        self.ui.widget.setLayout(layout)

    @QtCore.pyqtSlot()
    def browseDirectory(self):
        """
        Connected to browse button.
        Opens file dialog and starts analysis on selected item
        :return: void
        """

        fileName, filter = qt.QFileDialog.getOpenFileName(filter=FILTERLIST)
        self.ui.txtFileName.setText(fileName)
        self.startAnalysis(filter)

    @QtCore.pyqtSlot()
    def startAnalysis(self, filter=None):
        """
        Parses file name in textbox and sets up video player according to media type
        :param filter: string when called from browseDirectory
        :return: void
        """

        fileName = self.ui.txtFileName.text()

        if filter is None:
            filterType = None
            for key in FILTERS.keys():
                for value in FILTERS[key]:
                    if fileName.endswith(value):
                        filterType = key
        else:
            filterType = filter[0:filter.index(" (")]

        if filterType == "Videos":
            cap = cv2.VideoCapture(fileName)
            self._screen.setSource(cap)
            self._screen.pause()
        elif filterType == "Images":
            pic = cv2.imread(fileName)
            self._screen.newFrame.emit(pic)

class VideoPlayer(qt.QWidget):
    _DEFAULT_FPS = 30

    newFrame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, parent=None, src=None):
        super().__init__(parent)
        self.ui = VideoPlayer_ui()
        self.ui.setupUi(self)

        self._frame = None
        self._src = src
        self.algo = algorithms.Algorithms()

        # This timer will dictate when a new frame should be drawn
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._getNewFrame)
        self._timer.setInterval(1000 / self._DEFAULT_FPS)

        self.newFrame.connect(self.algo.process_frame)
        self.algo.frameProcessed.connect(self.displayFrame)

        self.ui.buttonBack.clicked.connect(self.rewind)
        self.ui.buttonPause.clicked.connect(self.togglePause)

    def rewind(self):
        """
        Sets videosource to beginning of stream
        :return: void
        """

        self._src.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self._getNewFrame()

    def play(self):
        """
        Starts timer to dictate playing video
        :return: void
        """

        self._timer.start()

    def pause(self):
        """
        Stops timer to dictate pausing video
        :return: void
        """
        self._timer.stop()

    def togglePause(self):
        if self._timer.isActive():
            self.pause()
        else:
            self.play()

    def _getNewFrame(self):
        """
        Gets next frame from source and emits signal, sharing that frame.
        Pauses playback if no more frames.
        :return: void
        """

        if self._src.isOpened():
            ret, frame = self._src.read()
        if ret:
            self.newFrame.emit(frame)
        else:
            self.pause()

    @QtCore.pyqtSlot(np.ndarray)
    def displayFrame(self, frame):
        """
        Slot for function handling processing to return processed frame and display it
        :param frame:
        :return: void
        """

        self._frame = frame
        self.update()

    def paintEvent(self, e):
        """
        Override of QWidget function.
        Paints self._frame across the widget
        :param e:
        :return: void
        """

        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), qimage2ndarray.array2qimage(cv2.resize(self._frame, (self.geometry().width(), self.geometry().height()))))

    def setSource(self, src):
        """
        Sets the video source to src
        :param src: cv2.Videocapture object
        :return: void
        """

        if type(src) is not cv2.VideoCapture:
            raise TypeError("Given source is type " + type(src).__name__ +
                            ". Expected type " + cv2.VideoCapture.__name__)

        self._src = src
        self._getNewFrame()
