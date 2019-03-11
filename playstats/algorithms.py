from psvideo import PSVideo

import cv2
from PyQt5 import QtCore
import numpy as np


class Algorithms(QtCore.QObject):

    def __init__(self, originalVideo):
        """
        :param originalVideo:  VideoCapture of video to process
        """

        self.originalVideo = originalVideo
        self.processedVideo = PSVideo()

    # Todo: make this async
    def processVideo(self):
        """
        Processes original video stream and populates processedVideo with data
        :return: void
        """

        if self.originalVideo.isOpened():
            ret, frame = self.originalVideo.read()

            while ret is True:
                processedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.processedVideo.addNextFrame(processedFrame)

                ret, frame = self.originalVideo.read()
