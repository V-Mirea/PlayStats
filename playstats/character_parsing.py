import json
import os
import cv2
import numpy as np
from collections import namedtuple

import algorithms

def takePosition(elem):
    return elem[1]

def readText(roi, dictionary):
    """
    :param roi: ndarray opencv image in BGR format
    :param dictionary: FontDictionary with possible characters
    :return: string containing read text
    """

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    character_regions = findCharacterRegions(roi)

    found_chars = []
    char_match = namedtuple('char_match', 'char value')

    for region in character_regions:  # Loop identified character regions
        region_image = algorithms.getImageRegion(roi, region)
        match = char_match(None, 0)

        for dictionary_char, font_char in dictionary.items():  # Loop each character in the dictionary
            if font_char.image is not None:
                template = cv2.cvtColor(font_char.image, cv2.COLOR_BGR2GRAY)  # Todo: This v number might need tweaked
                reg, maxVal = algorithms.multiscaleMatchTemplate(region_image, template, sensitivity=0)
                if reg is not None and maxVal > match.value:
                    match = char_match(dictionary_char, maxVal)
        if match.char is not None:
            found_chars.append((match.char, region.top_left.x))

    found_chars.sort(key=takePosition)  # Todo: maybe inline the takePosition function?
    if len(found_chars) > 0:
        return ''.join([x[0] for x in found_chars])
    else:
        return ""

def findCharacterRegions(img):
    """
    :param img: ndarray opencv image in BGR format
    :return: int - num of characters in the image
    """

    orig = img.copy()

    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(thresh, 300, 300)
    _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_regions = []  # List of for sure contours
    for i in range(0, len(contours)):  # Loop every detected contour
         x, y, w, h = cv2.boundingRect(contours[i])
         current_contour = algorithms.ImageRegion(x, y, width=w, height=h)

         overlaps = [-1]  # List of contour_regions indexes of regions that overlap with current region
         for i in range(len(contour_regions)):
             if current_contour.overlaps(contour_regions[i]):
                 overlaps.append(i)
         if len(overlaps) > 1:
             overlap_area = [contour_regions[i].area() for i in overlaps[1:]]
             overlap_area.insert(0, current_contour.area())

             max_index = overlap_area.index(max(overlap_area))
             overlaps.pop(max_index)

             addThis = True
             for index in overlaps[::-1]:
                 if index != -1:
                     contour_regions.pop(index)
                 else:
                     addThis = False

             if addThis:
                 contour_regions.append(current_contour)
         else:
             contour_regions.append(current_contour)

    return contour_regions

class FontDictionary(dict):
    def __init__(self, path=None):
        if path:
            self.parse_json_dictionary(path)

    def parse_json_dictionary(self, path):  # Todo: error check (path is folder)
        """
        :param path: string - path to folder
        :return: void
        """

        font_name = os.path.basename(path)

        with open(os.path.join(path, font_name) + ".json", "r")as file:
            json_string = file.read()

        json_obj = json.loads(json_string)
        for group, group_dict in json_obj.items():
            for char, image_path in group_dict.items():
                self[char] = FontCharacter(char, os.path.join(path, image_path), group)

class FontCharacter:
    def __init__(self, char, path_to_img, group):
        self.char = char
        self.path = path_to_img
        self.image = cv2.imread(path_to_img)
        self.group = group

