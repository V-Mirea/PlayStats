from psvideo import PSVideo

import cv2
from PyQt5 import QtCore
import numpy as np

from enum import Enum

class Games(Enum):
    CSGO = 1

class Algorithms(QtCore.QObject):

    def __init__(self, originalVideo, game):
        """
        :param originalVideo:  VideoCapture of video to process
        :param game: Games enum representing game in video
        """

        self.originalVideo = originalVideo
        self.processedVideo = PSVideo()
        self.game = game

    # Todo: make this async
    def processVideo(self):
        """
        Processes original video stream and populates processedVideo with data
        :return: void
        """

        if self.originalVideo.isOpened():
            ret, frame = self.originalVideo.read()
            fshape = frame.shape[1::-1]

            features = PSFeatures(fshape, self.game)

            while ret is True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                for key, region in features.regions.items():
                    cv2.rectangle(frame, region[0], region[1], 255, 2)

                processedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.processedVideo.addNextFrame(processedFrame)

                ret, frame = self.originalVideo.read()

class PSFeatures:
    def __init__(self, screenSize, game=None):
        """

        :param screenSize: tuple (width, height) (px)
        :param game: Games enum
        """

        width, height = screenSize

        if game is None:
            self.regions = {}
        elif game is Games.CSGO:
            self.regions = {
                "health":
                    ((0, int(height*0.9416)),
                     (int(width*0.2198), height-1)),
                "money":
                    ((int(width*0.0099), int(height*0.3259)),
                     (int(width*0.0896), int(height*0.3703)))
            }
