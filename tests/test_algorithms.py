import unittest
import cv2

from playstats.algorithms import *
import character_parsing


class TestAlgorithms(unittest.TestCase):

    def test_getImageRegion(self):
        image = cv2.imread("res/getImageRegion.jpg")
        shape = image.shape[1::-1]
        features = PSFeatures(shape, Games.CSGO)
        region = features.regions['health']
        region_image = getImageRegion(image, region)

        cv2.imshow("getImageRegion - health", region_image)
        cv2.waitKey(0)

        self.assertSequenceEqual(region_image.tolist(),
                                 image[region.top_left.y:region.bottom_right.y,
                                       region.top_left.x:region.bottom_right.x]
                                 .tolist())

    def test_createMask(self):
        image = cv2.imread("res/getImageRegion.jpg")
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

        cv2.imshow("mask - health", mask)
        cv2.waitKey(0)

        self.assertTrue(maskOk)

    def test_region_overlaps(self):
        a = ImageRegion(0, 0, 10, 10)
        b = ImageRegion(1, 1, 9, 9)
        self.assertTrue(a.overlaps(b))

        a = ImageRegion(0, 0, 10, 10)
        b = ImageRegion(5, 5, 15, 15)
        self.assertTrue(a.overlaps(b))

        c = ImageRegion(0, 0, 10, 10)
        d = ImageRegion(15, 15, 25, 25)
        self.assertFalse(c.overlaps(d))