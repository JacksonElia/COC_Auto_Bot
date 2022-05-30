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
    SUGGESTED_UPGRADES: tuple
    UPGRADE_BUTTON: tuple
    ENOUGH_RESOURCES_COLOR = [254, 254, 254]  # In [B, G, R]

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.ZERO_BUILDERS = (cv.imread("assets/misc/zero_builders.jpg", cv.IMREAD_UNCHANGED), .9)
        self.BUILDER_FACE = (cv.imread("assets/misc/builder_face.jpg", cv.IMREAD_UNCHANGED), .96)
        self.SUGGESTED_UPGRADES = (cv.imread("assets/misc/suggested_upgrades.jpg", cv.IMREAD_UNCHANGED), .96)
        self.UPGRADE_BUTTON = (cv.imread("assets/buttons/upgrade_button.jpg", cv.IMREAD_UNCHANGED), .95)

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
        self.suggested_upgrades_rectangle = []
        self.suggested_upgrades = []
        suggested_upgrades, confidence = self.SUGGESTED_UPGRADES
        threshold = 1 - confidence
        result = cv.matchTemplate(screenshot, suggested_upgrades, cv.TM_SQDIFF_NORMED)
        location = np.where(result <= threshold)
        location = list(zip(*location[::-1]))
        if location:
            location = location[0]
            self.suggested_upgrades_rectangle = [location[0], location[1], suggested_upgrades.shape[1], suggested_upgrades.shape[0]]
            self.suggested_upgrades = []
            for i in range(1, 4):
                self.suggested_upgrades.append([location[0], int(location[1] + i * 40.5), suggested_upgrades.shape[1], suggested_upgrades.shape[0]])
        elif self.check_for_builders(screenshot):
            self.open_builder_menu(screenshot)

    def show_suggested_upgrades(self, screenshot):
        if self.suggested_upgrades_rectangle:
            top_left = (self.suggested_upgrades_rectangle[0], self.suggested_upgrades_rectangle[1])
            bottom_right = (self.suggested_upgrades_rectangle[0] + self.suggested_upgrades_rectangle[2], self.suggested_upgrades_rectangle[1] + self.suggested_upgrades_rectangle[3])
            cv.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), cv.LINE_4)
            for rectangle in self.suggested_upgrades:
                top_left = (rectangle[0], rectangle[1])
                bottom_right = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
                cv.rectangle(screenshot, top_left, bottom_right, (255, 0, 255), cv.LINE_4)

    def upgrade_building(self, screenshot):
        upgrade_button_image, confidence = self.UPGRADE_BUTTON
        threshold = 1 - confidence
        result = cv.matchTemplate(screenshot, upgrade_button_image, cv.TM_SQDIFF_NORMED)
        location = np.where(result <= threshold)
        location = list(zip(*location[::-1]))
        if location:
            location = location[0]
            rectangle = [location[0], location[1], upgrade_button_image.shape[1], upgrade_button_image.shape[0]]
            x = int(rectangle[0] + rectangle[2] / 2)
            y = int(rectangle[1] + rectangle[3] / 2)
            # Clicks the upgrade button, then the confirmation button
            click(x, y, self.window_rectangle)
            sleep(.3)
            click(x, y, self.window_rectangle)
            sleep(.3)
        else:
            for suggested_upgrade in self.suggested_upgrades:
                cropped_screenshot = screenshot[suggested_upgrade[1]:suggested_upgrade[1] + suggested_upgrade[3],
                                     suggested_upgrade[0] + 300:suggested_upgrade[0] + suggested_upgrade[2]]
                # Makes sure there are enough resources for upgrading
                if detect_if_color_present(self.ENOUGH_RESOURCES_COLOR, cropped_screenshot):
                    x = int(suggested_upgrade[0] + suggested_upgrade[2] / 2)
                    y = int(suggested_upgrade[1] + suggested_upgrade[3] / 2)
                    click(x, y, self.window_rectangle)
                    sleep(1)
                    break

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
            print(not bool(location))
            return not bool(location)
