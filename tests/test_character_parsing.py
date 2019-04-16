import unittest
import cv2

import character_parsing
import algorithms


class TestCharacterParsing(unittest.TestCase):

    def test_numOfChars(self):
        img = cv2.imread("res/character_parsing.jpg")
        features = algorithms.PSFeatures(img.shape[1::-1], algorithms.Games.CSGO)

        health_region = algorithms.getImageRegion(img, features.regions["health"])
        print(character_parsing.findNumberOfCharacters(health_region))