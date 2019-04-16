import algorithms
import character_parsing

import cv2
from abc import abstractmethod


def makePSVideo(video, game):
    if game is algorithms.Games.CSGO:
        return CSGOVideo(video)

class PSVideo:
    def __init__(self, originalVideo):
        """
        :param originalVideo:  VideoCapture of video to process
        """

        self.originalVideo = originalVideo
        self.processing = False

        self.processedFrames = []  # Stores frames in RGB format
        self.videoIndex = 0

    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def processVideo(self):
        """
        Processes original video stream and populates processedFrames with data
        Runs asynchronously
        :return: void
        """
        pass

    def addNextFrame(self, frame):
        """
        :param frame: numpy ndarray in RBG format
        :return: void
        """

        self.processedFrames.append(frame)

    def getNextFrame(self):
        if self.videoIndex < len(self.processedFrames):
            self.videoIndex += 1
            return self.processedFrames[self.videoIndex - 1]

        return None

class CSGOVideo(PSVideo):
    def __init__(self, originalVideo):
        super().__init__(originalVideo)
        self.game = algorithms.Games.CSGO
        self.text_color = None

    def processVideo(self):
        self.processing = True
        if self.originalVideo.isOpened():
            ret, frame = self.originalVideo.read()
            fshape = frame.shape[1::-1]

            features = algorithms.PSFeatures(fshape, self.game)

            # Main processing
            while ret is True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                for key, region in features.regions.items():
                    cv2.rectangle(frame, region.top_left, region.bottom_right, 255, 2)

                health_region = algorithms.getImageRegion(frame, features.regions["armor"])
                print(character_parsing.findNumberOfCharacters(health_region))

                processedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.addNextFrame(processedFrame)

                ret, frame = self.originalVideo.read()

        print("finished")
        self.processing = False
