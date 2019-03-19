from psvideo import PSVideo

import cv2
from PyQt5 import QtCore
import numpy as np
from enum import Enum

class Games(Enum):
    CSGO = 1

def getImageRegion(img, region): #
    """
    :param img: numpy ndarray
    :param region: ((topleft x, topleft y), (bottomright x, bottomright y))
    :return: numpy ndarray of that region
    """

    left = region.top_left.x
    top = region.top_left.y
    right = region.bottom_right.x
    bottom = region.bottom_right.y

    return img[top:bottom, left:right]

def createMask(maskSize, regionOfInterest):
    """
    :param maskSize: (w, h)
    :param regionOfInterest: ((topleft x, topleft y), (bottomright x, bottomright y))
    :return: greyscale image masking region of interest
    """

    w, h = maskSize

    mask = np.zeros((h, w), dtype=np.uint8)

    left = regionOfInterest.top_left.x
    top = regionOfInterest.top_left.y
    right = regionOfInterest.bottom_right.x
    bottom = regionOfInterest.bottom_right.y

    mask[top:bottom, left:right] = 255

    return mask

def multiscaleMatchTemplate(image, template, method):
    """
    :param image: ndarray representing source image
    :param template:  ndarray representing template to search for
    :param method: OpenCV matchTemplate comparison method
    :return: return region representing location of template in image
    """

    match = None

    for scale in np.linspace(0.2, 2, 20):
        resized = cv2.resize(template, None, fx=scale, fy=scale)

        if resized.shape[0] > image.shape[0] or resized.shape[1] > image.shape[1]:
            break

        matches = cv2.matchTemplate(image, resized, method)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(matches)

        if match is None or maxVal > match[0]:
            match = (maxVal, maxLoc, scale)

    if match is None:
        return None

    _, maxLoc, scale = match
    tempH = int(template.shape[0] * scale)
    tempW = int(template.shape[1] * scale)
    locX, locY = maxLoc

    return (locX, locY), (locX + tempW, locY + tempH)

def translateMaskRegion(region, maskRegion): # Todo: Needs tested
    """
    :param region: region in terms of maskRegion
    :param maskRegion: region of original picture
    :return: region representing 'region' in the original picture
    """

    return ImageRegion(maskRegion.top_left.x + region.top_left.x, maskRegion.top_left.y + region.top_left.y,
                       maskRegion.top_left.x + region.bottom_right.x, maskRegion.top_left.y + region.bottom_right.y)

class PSVideoData(QtCore.QObject):

    def __init__(self, originalVideo, game):
        """
        :param originalVideo:  VideoCapture of video to process
        :param game: Games enum representing game in video
        """

        self.originalVideo = originalVideo
        self.processedVideo = PSVideo()
        self.game = game
        self.processing = False

    def processVideo(self):
        """
        Processes original video stream and populates processedVideo with data
        Runs asynchronously
        :return: void
        """

        self.processing = True
        if self.originalVideo.isOpened():
            ret, frame = self.originalVideo.read()
            fshape = frame.shape[1::-1]

            features = PSFeatures(fshape, self.game)

            while ret is True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                for key, region in features.regions.items():
                    cv2.rectangle(frame, region.top_left, region.bottom_right, 255, 2)

                processedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.processedVideo.addNextFrame(processedFrame)

                ret, frame = self.originalVideo.read()

        print("finished")
        self.processing = False

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
                "health": ImageRegion(int(width*0.0285), int(height*0.9546),
                                      int(width*0.0625), height-1),
                "armor": ImageRegion(int(width*0.1354), int(height*0.9546),
                                     int(width*0.1708), height-1),
                "money": ImageRegion(int(width*0.0099), int(height*0.3259),
                                     int(width*0.0896), int(height*0.3703))
            }

class ImageRegion:
    # Todo: error check
    def __init__(self, top_left_x, top_left_y, bottom_right_x=None, bottom_right_y=None, width=None, height=None):
        self.top_left = Coords(top_left_x, top_left_y)

        if bottom_right_x and bottom_right_y:
            self.bottom_right = Coords(bottom_right_x, bottom_right_y)
            self.width = self.bottom_right.x - self.top_left.x
            self.height = self.bottom_right.y - self.top_left.y
        elif width and height:
            self.bottom_right = Coords(top_left_x+width, top_left_y+height)
            self.width = width
            self.height = height

    def overlaps(self, region):
        """
        :param region: ImageRegion to test against
        :return: bool if region overlaps given region
        """

        dx = min(self.bottom_right.x, region.bottom_right.x) - max(self.top_left.x, region.top_left.x)
        dy = min(self.bottom_right.y, region.bottom_right.y) - max(self.top_left.y, region.top_left.y)

        if (dx <= 0) and (dy <= 0):
            return False
        else:
            return True

class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y