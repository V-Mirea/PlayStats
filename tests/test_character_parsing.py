import unittest
import cv2

import character_parsing
import algorithms


class TestCharacterParsing(unittest.TestCase):

    def test_readText(self):
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

            print(character_parsing.readText(health, dic))
            print(character_parsing.readText(armor, dic))
            # cv2.imshow("region", region)
            # cv2.waitKey(0)