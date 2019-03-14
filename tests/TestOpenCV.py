import unittest
import cv2

from playstats.algorithms import *

class TestOpenCV(unittest.TestCase):

    def setUp(self):
        self.testImage = cv2.imread("res/csgo_screen.jpg")

if __name__ == '__main__':
    unittest.main()