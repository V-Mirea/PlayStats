import json
import os
import cv2
import numpy as np

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

    print("start frame")
    for region in character_regions:
        region_image = algorithms.getImageRegion(roi, region)

        for key, value in dictionary.items():
            template = cv2.imread(value.path, 0)                  # Todo: This v number might need tweaked
            if algorithms.multiscaleMatchTemplate(region_image, template, sensitivity=200000) is not None:
                found_chars.append((key, region.top_left.x))
                break
    found_chars.sort(key=takePosition)
    print(''.join([x[0] for x in found_chars]))

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
             overlap_area = [contour_regions[i].area() for i in overlaps]
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
        self.img = cv2.imread(path_to_img)
        self.group = group

