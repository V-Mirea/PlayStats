import unittest
import cv2

from playstats.algorithms import *

class TestOpenCV(unittest.TestCase):

    def setUp(self):
        #self.testImage = cv2.imread("res/csgo_screen.jpg")
        pass

    def test_templates(self):
        """ Not a real test. Just testing features"""

        feat = PSFeatures((1920, 1080), game=Games.CSGO)
        orig = cv2.imread("res/csgo_screen.jpg", cv2.IMREAD_COLOR)
        temp = cv2.imread("res/one.jpg", cv2.IMREAD_GRAYSCALE)

        health = getImageRegion(orig, feat.regions["health"])
        edges = cv2.Canny(health, 300, 300)
        edges2 = cv2.Canny(temp, 300, 300)

        region = multiscaleMatchTemplate(edges, edges2, cv2.TM_CCOEFF)
        translated = translateMaskRegion(region, feat.regions["health"])
        cv2.rectangle(orig, translated[0], translated[1], 255)

        cv2.imshow("orig", orig)
        cv2.waitKey()

if __name__ == '__main__':
    unittest.main()