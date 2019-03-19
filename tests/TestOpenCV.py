import unittest
import cv2

from playstats.algorithms import *
import character_parsing

class TestOpenCV(unittest.TestCase):

    def setUp(self):
        #self.testImage = cv2.imread("res/csgo_screen.jpg")
        pass

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


if __name__ == '__main__':
    unittest.main()