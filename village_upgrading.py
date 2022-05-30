from interaction_functions import *
from time import sleep
import cv2 as cv
import numpy as np


class VillageUpgrader:
    """
    Upgrades every building as its able to.
    """

    window_rectangle = []
    suggested_upgrades_rectangle = []
    suggested_upgrades = []

    ZERO_BUILDERS: tuple
    BUILDER_FACE: tuple

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.ZERO_BUILDERS = (cv.imread("assets/misc/zero_builders.jpg", cv.IMREAD_UNCHANGED), .93)
        self.BUILDER_FACE = (cv.imread("assets/misc/builder_face.jpg", cv.IMREAD_UNCHANGED), .96)
        self.SUGGESTED_UPGRADES = (cv.imread("assets/misc/suggested_upgrades.jpg", cv.IMREAD_UNCHANGED), .96)

    def open_builder_menu(self, screenshot):
        """
        Opens the builder menu if there are available builders
        :param screenshot: screenshot of bluestacks
        :return:
        """
        if self.check_for_builders(screenshot):
            builder_face_image, confidence = self.BUILDER_FACE
            threshold = 1 - confidence
            result = cv.matchTemplate(screenshot, builder_face_image, cv.TM_SQDIFF_NORMED)
            location = np.where(result <= threshold)
            location = list(zip(*location[::-1]))
            if location:
                location = location[0]
                x = int(location[0] + builder_face_image.shape[1] / 2)
                y = int(location[1] + builder_face_image.shape[0] / 2)
                click(x, y, self.window_rectangle)

    def find_suggested_upgrades(self, screenshot):
        suggested_upgrades, confidence = self.SUGGESTED_UPGRADES
        threshold = 1 - confidence
        result = cv.matchTemplate(screenshot, suggested_upgrades, cv.TM_SQDIFF_NORMED)
        location = np.where(result <= threshold)
        location = list(zip(*location[::-1]))
        if location:
            location = location[0]
            self.suggested_upgrades_rectangle = [location[0], suggested_upgrades.shape[1], location[1], suggested_upgrades.shape[0]]
            self.suggested_upgrades = []
            for i in range(1, 4):
                self.suggested_upgrades.append([location[0], suggested_upgrades.shape[1], int(location[1] + i * 40.5), suggested_upgrades.shape[0]])

    def show_suggested_upgrades(self, screenshot):
        if self.suggested_upgrades_rectangle:
            top_left = (self.suggested_upgrades_rectangle[0], self.suggested_upgrades_rectangle[2])
            bottom_right = (self.suggested_upgrades_rectangle[0] + self.suggested_upgrades_rectangle[1], self.suggested_upgrades_rectangle[2] + self.suggested_upgrades_rectangle[3])
            cv.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), cv.LINE_4)
            for rectangle in self.suggested_upgrades:
                top_left = (rectangle[0], rectangle[2])
                bottom_right = (rectangle[0] + rectangle[1], rectangle[2] + rectangle[3])
                cv.rectangle(screenshot, top_left, bottom_right, (255, 0, 255), cv.LINE_4)

    def check_for_builders(self, screenshot) -> bool:
            """
            Checks for if there are available builders
            :param screenshot: screenshot of bluestacks
            :return: True if there are builders, False if there aren't
            """
            zero_builders_image, confidence = self.ZERO_BUILDERS
            threshold = 1 - confidence
            result = cv.matchTemplate(screenshot, zero_builders_image, cv.TM_SQDIFF_NORMED)
            location = np.where(result <= threshold)
            location = list(zip(*location[::-1]))
            return not bool(location)
