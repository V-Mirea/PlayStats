import unittest
import cv2

from playstats.algorithms import *


class TestAlgorithms(unittest.TestCase):

    def test_getImageRegion(self):
        image = cv2.imread("res/csgo_screen.jpg")
        shape = image.shape[1::-1]
        features = PSFeatures(shape, Games.CSGO)
        region = features.regions['health']
        region_image = getImageRegion(image, region)

        self.assertSequenceEqual(region_image.tolist(),
                                 image[region.top_left.y:region.bottom_right.y,
                                       region.top_left.x:region.bottom_right.x]
                                 .tolist())

    def test_createMask(self):
        image = cv2.imread("res/csgo_screen.jpg")
        shape = image.shape[1::-1]
        features = PSFeatures(shape, Games.CSGO)
        region = features.regions['health']

        mask = createMask(shape, region)
        foreground = getImageRegion(mask, region)

        maskOk = True
        for pixel in foreground.flatten():
            if pixel != 255:
                maskOk = False
                break

        if maskOk:
            numWhite = 0
            for pixel in mask.flatten():
                if pixel == 255:
                    numWhite += 1
            if numWhite != len(foreground.flatten()):
                maskOk = False

        self.assertTrue(maskOk)
