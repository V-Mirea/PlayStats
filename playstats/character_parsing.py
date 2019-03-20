import json
import os
import cv2

from algorithms import ImageRegion

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

class Parser:
    def __init__(self, roi):
        self.img = roi

    def findNumberOfCharacters(self):
        orig = self.img.copy()
        gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 300, 300)
        _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contour_regions = [] # List of for sure contours
        for i in range(0, len(contours)): # Loop every detected contour
            x, y, w, h = cv2.boundingRect(contours[i])
            current_contour = ImageRegion(x, y, width=w, height=h)

            overlaps = [-1] # List of contour_regions indexes of regions that overlap with current region
            for i in range(len(contour_regions)):
                if current_contour.overlaps(contour_regions[i]):
                    overlaps.append(i)
            if len(overlaps) > 1:
                overlap_area = [contour_regions[i].area() for i in overlaps]
                overlap_area.insert(0, current_contour.area())

                max_index = overlap_area.index(max(overlap_area))
                overlaps.pop(max_index)

                addThis = True
                for index in overlaps:
                    if index != -1:
                        contour_regions.pop(index)
                    else:
                        addThis = False

                if addThis:
                    contour_regions.append(current_contour)
            else:
                contour_regions.append(current_contour)

        return len(contour_regions)
