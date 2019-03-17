import json
import os
import cv2

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