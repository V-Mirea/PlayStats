import unittest
import cv2

from test_algorithms import *
from test_psvideo import *
from test_character_parsing import *

import character_parsing

class TestThrowAways(unittest.TestCase):

    def test_prevalentColors(self):
        frame = cv2.imread("res/prevalentColors.jpg")
        fshape = frame.shape[1::-1]
        features = algorithms.PSFeatures(fshape, algorithms.Games.CSGO)

        character_parsing.findNumberOfCharacters(algorithms.getImageRegion(frame, features.regions["health"]))

if __name__ == '__main__':
    # Run only the tests in the specified classes

    test_classes_to_run = [TestThrowAways]
    #test_classes_to_run = [TestAlgorithms, TestPSVideo, TestCharacterParsing]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)