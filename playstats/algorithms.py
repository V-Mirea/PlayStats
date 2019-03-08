import cv2
from PyQt5 import QtCore
import numpy as np


class Algorithms(QtCore.QObject):
    frameProcessed = QtCore.pyqtSignal(np.ndarray)


    def process_frame(self, frame):
        """

        :param frame: numpy ndarray in BGR format
        :return:
        """



        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frameProcessed.emit(frame)

    def testing(self):
        print("ey")