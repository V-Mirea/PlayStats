from psvideo import *

import cv2
from PyQt5 import QtCore
import numpy as np
from enum import Enum
from collections import namedtuple
from operator import itemgetter

Coords = namedtuple("Coords", "x y")

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

def multiscaleMatchTemplate(image, template, method=cv2.TM_CCOEFF, sensitivity=200000):  #  Todo: Sensitivity needs looked at
    """
    :param image: ndarray representing source image
    :param template:  ndarray representing template to search for
    :param method: OpenCV matchTemplate comparison method
    :return: region representing location of template in image, number representing strength of match
    """

    match = None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10)

    for scale in np.linspace(0.2, 2, 20):
        resized = cv2.resize(template, None, fx=scale, fy=scale)

        if resized.shape[0] > image.shape[0] or resized.shape[1] > image.shape[1]:
            break

        matches = cv2.matchTemplate(thresh, resized, method)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(matches)

        if match is None or maxVal > match[0]:
            match = (maxVal, maxLoc, scale)

    if match is None or match[0] < sensitivity:
        return None, 0

    val, maxLoc, scale = match
    tempH = int(template.shape[0] * scale)
    tempW = int(template.shape[1] * scale)
    locX, locY = maxLoc

    matchRegion = ImageRegion(locX, locY, width=tempW, height=tempH)
    return matchRegion, val

def translateMaskRegion(region, maskRegion): # Todo: Needs tested
    """
    :param region: region in terms of maskRegion
    :param maskRegion: region of original picture
    :return: region representing 'region' in the original picture
    """

    return ImageRegion(maskRegion.top_left.x + region.top_left.x, maskRegion.top_left.y + region.top_left.y,
                       maskRegion.top_left.x + region.bottom_right.x, maskRegion.top_left.y + region.bottom_right.y)

class PSFeatures:
    def __init__(self, screenSize, game=None):
        """

        :param screenSize: tuple (width, height) (px)
        :param game: Games enum
        """

        width, height = screenSize

        if game is Games.CSGO:
            self.regions = {
                "health": ImageRegion(int(width*0.0285), int(height*0.9546),
                                      int(width*0.0625), height-1),
                "armor": ImageRegion(int(width*0.1354), int(height*0.9546),
                                     int(width*0.1708), height-1),
                "money": ImageRegion(int(width*0.0235), int(height*0.3259),
                                     int(width*0.0896), int(height*0.3703))
            }
        else:
            self.regions = {}

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

    def area(self):
        return self.width * self.height

    def overlaps(self, region):
        """
        :param region: ImageRegion to test against
        :return: bool if region overlaps given region
        """

        dx = min(self.bottom_right.x, region.bottom_right.x) - max(self.top_left.x, region.top_left.x)
        dy = min(self.bottom_right.y, region.bottom_right.y) - max(self.top_left.y, region.top_left.y)

        if (dx >= 0) and (dy >= 0):
            return True
        else:
            return False

def findPrevalentColors(images, n=1):
    """
    :param images: list of ndarray images in any format
    :param n: number of colors to find
    :return: list most frequently occuring n colors from the images
                from most frequent to less frequent
    """

    colors = []

    for image in images:
        for pixel in image.reshape(-1, image.shape[-1]):  # Flatten to 1D array of arrays
            if any((c["color"] == pixel).all() for c in colors):  # If pixel color already found
                next(c for c in colors if (c["color"] == pixel).all())["occurrences"] += 1  # Increase occurrences by 1
            else:
                colors.append({"color": pixel, "occurrences": 1})  # Else add it to the list

    colors = sorted(colors, key=itemgetter('occurrences'), reverse=True)  # Sort from most to least common
    return colors[:n]  # Return n most common
