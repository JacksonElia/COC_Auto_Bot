from interaction_functions import *
from time import sleep
import cv2 as cv
import numpy as np


class VillageUpgrader:
    """
    Upgrades every building as its able to.
    """

    window_rectangle = []

    ZERO_BUILDERS: tuple
    BUILDER_FACE: tuple

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.ZERO_BUILDERS = (cv.imread("assets/misc/zero_builders.jpg", cv.IMREAD_UNCHANGED), .93)
        self.BUILDER_FACE = (cv.imread("assets/misc/builder_face.jpg", cv.IMREAD_UNCHANGED), .96)

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
                x = int(location[0] + builder_face_image.shape[0] / 2)
                y = int(location[1] + builder_face_image.shape[1] / 2)
                click(x, y, self.window_rectangle)

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
