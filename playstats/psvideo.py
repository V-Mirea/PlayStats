import algorithms
import character_parsing
from resultscreen import AnalysisResults, CSGOResults

import cv2
from abc import abstractmethod
from PyQt5.QtCore import QObject, pyqtSignal


def makePSVideo(video, game):
    if game is algorithms.Games.CSGO:
        return CSGOVideo(video)

class PSVideo(QObject):
    video_processed = pyqtSignal(dict)

    def __init__(self, originalVideo):
        """
        :param originalVideo:  VideoCapture of video to process
        """

        super().__init__()
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

        self.raw_health = []
        self.raw_armor = []
        self.raw_money = []

    def processVideo(self):
        '''
        Run through the VideoCapture, perform all calculations/analysis,
        save processed frames
        :return:
        '''
        self.processing = True
        if self.originalVideo.isOpened():
            ret, frame = self.originalVideo.read()
            fshape = frame.shape[1::-1]

            features = algorithms.PSFeatures(fshape, self.game)

            self.raw_readings = {}
            for name, region in features.regions.items():
                self.raw_readings[name] = []
            # Main processing
            while ret is True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                #for key, region in features.regions.items():
                #    cv2.rectangle(frame, region.top_left, region.bottom_right, 255, 2)

                dictionary = character_parsing.FontDictionary()
                dictionary.parse_json_dictionary("res\\fonts\\hud")

                identified_chars = []
                for name, region in features.regions.items():  # All regions are text rn so handle all the same for now
                    image_region = algorithms.getImageRegion(frame, region)
                    image_str, image_chars = character_parsing.readText(image_region, dictionary)

                    # Translate each character region from being in terms of feature region to the whole frame
                    for char in image_chars:
                        char["region"] = algorithms.translateMaskRegion(char["region"], region)

                    self.raw_readings[name].append(image_str)
                    identified_chars.extend(image_chars)

                drawnFrame = algorithms.drawIndentifiedCharacters(frame, identified_chars)
                processedFrame = cv2.cvtColor(drawnFrame, cv2.COLOR_BGR2RGB)
                self.addNextFrame(processedFrame)

                ret, frame = self.originalVideo.read()

        self.results = {}
        for name, readings in self.raw_readings.items():
            int_readings = [int(x) for x in readings]  # Todo: error checking
            self.results[name] = int_readings

        #results = CSGOResults()
        #results.health = [int(x) for x in self.raw_health]
        #results.armor = [int(x) for x in self.raw_armor]
        #results.money = [int(x) for x in self.raw_money]
        self.processing = False
        self.video_processed.emit(self.results)
