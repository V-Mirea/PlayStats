import unittest
import cv2

from test_algorithms import *

import character_parsing

class TestThrowAways(unittest.TestCase):

    # def test_templates(self):
    #     """ Not a real test. Just testing features"""
    #
    #     feat = PSFeatures((1920, 1080), game=Games.CSGO)
    #     orig = cv2.imread("res/csgo_screen.jpg", cv2.IMREAD_COLOR)
    #     temp = cv2.imread("res/one.jpg", cv2.IMREAD_GRAYSCALE)
    #
    #     health = getImageRegion(orig, feat.regions["health"])
    #     edges = cv2.Canny(health, 300, 300)
    #     edges2 = cv2.Canny(temp, 300, 300)
    #
    #     region = multiscaleMatchTemplate(edges, edges2, cv2.TM_CCOEFF)
    #     translated = translateMaskRegion(region, feat.regions["health"])
    #     cv2.rectangle(orig, translated[0], translated[1], 255)
    #
    #     cv2.imshow("orig", orig)
    #     cv2.waitKey()

    def test_Parser(self):
        feat = PSFeatures((1920, 1080), Games.CSGO)
        img = cv2.imread("res/csgo_screen.jpg")
        region = getImageRegion(img, feat.regions['health'])
        parser = character_parsing.Parser(region)
        parser.findNumberOfCharacters()
        print("test")


if __name__ == '__main__':
    # Run only the tests in the specified classes

    test_classes_to_run = [TestAlgorithms, TestThrowAways]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)