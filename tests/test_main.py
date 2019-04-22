import unittest
import cv2

from test_algorithms import *
from test_psvideo import *
from test_character_parsing import *

import character_parsing
import algorithms

class TestThrowAways(unittest.TestCase):

    def test_prevalentColors(self):
        cap = cv2.VideoCapture("res/action_clip.mp4")
        while (True):
            ret, frame = cap.read()
            if not ret:
                break

            fshape = frame.shape[1::-1]

            features = algorithms.PSFeatures(fshape, algorithms.Games.CSGO)
            health = algorithms.getImageRegion(frame, features.regions["health"])
            armor = algorithms.getImageRegion(frame, features.regions["armor"])
            dic = character_parsing.FontDictionary("res\\fonts\\hud")

            print("Health: %s" % character_parsing.readText(health, dic))
            print("Armor: %s" % character_parsing.readText(armor, dic))
            #cv2.imshow("region", frame)
            #cv2.waitKey(0)

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