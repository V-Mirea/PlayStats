import PyQt5.QtWidgets as qt
from PyQt5 import QtGui, QtCore
import numpy as np
import cv2
import qimage2ndarray
import threading

from analysis_ui import AnalysisWindow_ui
import algorithms
from videoplayer_ui import VideoPlayer_ui
from psvideo import *
from resultscreen import *

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
        self.ui.buttonStats.clicked.connect(self.seeResults)

        # Create and add video player
        self._screen = VideoPlayer(self)
        layout = qt.QGridLayout(self.ui.widget)
        layout.addWidget(self._screen)
        self.ui.widget.setLayout(layout)

    @QtCore.pyqtSlot(dict)
    def processingFinished(self, results):
        self.ui.statusbar.showMessage("Analysis complete")
        self.ui.buttonStats.setEnabled(True)
        self.analysis_results = results

    ## Button events ##
    @QtCore.pyqtSlot()
    def seeResults(self):
        self.result = ResultsScreen(self.analysis_results)
        self.result.show()

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

        if filter is None or filter == "":
            filterType = None
            for key in FILTERS.keys():
                for value in FILTERS[key]:
                    if fileName.endswith(value):
                        filterType = key
        else:
            filterType = filter[0:filter.index(" (")]

        game = self.getGame()

        if filterType == "Videos":
            cap = cv2.VideoCapture(fileName)
            self.ui.statusbar.showMessage("Analyzing video")
            self.ui.buttonStats.setEnabled(False)
            self._screen.startAnalysis(cap, game)
            self._screen.video.video_processed.connect(self.processingFinished) # Todo: make sure this wont cause problems
            self._screen.pause()
        elif filterType == "Images":
            pic = cv2.imread(fileName)
            self._screen.newFrame.emit(pic)

    ## Other methods ##

    def getGame(self):
        game = self.ui.comboGame.currentText()
        if game == "Counter Strike: Global Offensive":
            return algorithms.Games.CSGO

class VideoPlayer(qt.QWidget):
    _DEFAULT_FPS = 30

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = VideoPlayer_ui()
        self.ui.setupUi(self)

        self.video_screen = VideoScreen()
        self.ui.verticalLayout.insertWidget(0, self.video_screen)

        self._frame = None
        self.video = None

        # This timer will dictate when a new frame should be drawn
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._getNewFrame)
        self._timer.setInterval(1000 / self._DEFAULT_FPS)

        self.ui.buttonBack.clicked.connect(self.rewind)
        self.ui.buttonPause.clicked.connect(self.togglePause)

    def startAnalysis(self, videoCapture, game):
        """
        Create algorithms object and start processing the video
        :param videoCapture: VideoCapture object to process
        :param game: Games enum representing game in video
        :return: void
        """

        self.video = makePSVideo(videoCapture, game)

        self.video_screen.frame = cv2.cvtColor(videoCapture.read()[1], cv2.COLOR_BGR2RGB)
        self.video_screen.update()

        t = threading.Thread(target=self.video.processVideo)
        t.start()

    def _getNewFrame(self):
        """
        Grab next frame from processed video
        Pause timer if no new frames
        :return: void
        """
        frame = self.video.getNextFrame(self.ui.checkShowAnalysis.isChecked())
        if frame is None:
            if self.video.processing:
                pass  # Todo: do something here?
            else:
                self.pause()
        else:
            self.video_screen.frame = frame
            self.video_screen.update()

    def rewind(self):
        """
        Sets processed video to beginning of stream
        :return: void
        """

        self.video.videoIndex = 0
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

class VideoScreen(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.frame = None

    def paintEvent(self, e):
        """
        Override of QWidget function.
        Paints self._frame across the widget
        :param e:
        :return: void
        """

        if self.frame is None:
            return

        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), qimage2ndarray.array2qimage(cv2.resize(self.frame, (self.geometry().width(), self.geometry().height()))))