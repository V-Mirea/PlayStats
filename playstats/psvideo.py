import cv2


class PSVideo:
    def __init__(self):
        self.frames = []  # Stores frames in RGB format
        self.index = 0

    def addNextFrame(self, frame):
        """

        :param frame: numpy ndarray in RBG format
        :return: void
        """

        self.frames.append(frame)

    def getNextFrame(self):
        if self.index < len(self.frames):
            self.index += 1
            return self.frames[self.index - 1]

        return None

