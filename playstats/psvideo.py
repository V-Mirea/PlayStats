import algorithms

import cv2


class PSVideo:
    def __init__(self, originalVideo, game):
        """
        :param originalVideo:  VideoCapture of video to process
        :param game: Games enum representing game in video
        """

        self.originalVideo = originalVideo
        self.game = game
        self.processing = False

        self.processedFrames = []  # Stores frames in RGB format
        self.videoIndex = 0

    def processVideo(self):
        """
        Processes original video stream and populates processedFrames with data
        Runs asynchronously
        :return: void
        """

        self.processing = True
        if self.originalVideo.isOpened():
            ret, frame = self.originalVideo.read()
            fshape = frame.shape[1::-1]

            features = algorithms.PSFeatures(fshape, self.game)

            while ret is True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                for key, region in features.regions.items():
                    cv2.rectangle(frame, region.top_left, region.bottom_right, 255, 2)

                processedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.addNextFrame(processedFrame)

                ret, frame = self.originalVideo.read()

        print("finished")
        self.processing = False

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

