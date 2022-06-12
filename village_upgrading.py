from interaction_functions import *
from time import sleep
import cv2 as cv


class VillageUpgrader:
    """
    Upgrades every building as its able to.
    """

    window_rectangle = []
    suggested_upgrades_rectangle = []
    suggested_upgrades = []
    upgrading_building = False

    ZERO_BUILDERS: tuple
    BUILDER_FACE: tuple
    SUGGESTED_UPGRADES: tuple
    UPGRADE_BUTTON: tuple
    ARROW: tuple
    CHECK_BUTTON: tuple
    ENOUGH_RESOURCES_COLOR = [254, 254, 254]  # In [B, G, R]
    # NEW_BUILDING_COLOR = [13, 255, 13]  # In [B, G, R]

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.ZERO_BUILDERS = (cv.imread("assets/misc/zero_builders.jpg", cv.IMREAD_UNCHANGED), .89)
        self.BUILDER_FACE = (cv.imread("assets/misc/builder_face.jpg", cv.IMREAD_UNCHANGED), .96)
        self.SUGGESTED_UPGRADES = (cv.imread("assets/misc/suggested_upgrades.jpg", cv.IMREAD_UNCHANGED), .8)
        self.UPGRADE_BUTTON = (cv.imread("assets/buttons/upgrade_button.jpg", cv.IMREAD_UNCHANGED), .95)
        self.ARROW = (cv.imread("assets/misc/arrow.jpg", cv.IMREAD_UNCHANGED), .85)
        self.CHECK_BUTTON = (cv.imread("assets/buttons/check_button.jpg", cv.IMREAD_UNCHANGED), .9)

    def open_builder_menu(self, screenshot):
        """
        Opens the builder menu if there are available builders
        :param screenshot: screenshot of bluestacks
        :return:
        """
        if self.check_for_builders(screenshot):
            builder_face_rectangle = find_image_rectangle(self.BUILDER_FACE, screenshot)
            if builder_face_rectangle:
                x, y = get_center_of_rectangle(builder_face_rectangle)
                click(x, y, self.window_rectangle)
                sleep(1.5)

    def find_suggested_upgrades(self, screenshot):
        self.suggested_upgrades = []
        self.suggested_upgrades_rectangle = find_image_rectangle(self.SUGGESTED_UPGRADES, screenshot)
        if self.suggested_upgrades_rectangle:
            for i in range(1, 4):
                self.suggested_upgrades.append([self.suggested_upgrades_rectangle[0],
                                                int(self.suggested_upgrades_rectangle[1] + i * 41.5),
                                                self.suggested_upgrades_rectangle[2],
                                                self.suggested_upgrades_rectangle[3]])
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

    def upgrade_building(self, screenshot) -> bool:
        upgrade_button_rectangle = find_image_rectangle(self.UPGRADE_BUTTON, screenshot)
        arrow_rectangle = find_image_rectangle(self.ARROW, screenshot)
        check_button_rectangle = find_image_rectangle(self.CHECK_BUTTON, screenshot)
        # Checks to see if the upgrade button is present
        if check_button_rectangle:
            x, y = get_center_of_rectangle(check_button_rectangle)
            # Clicks the check button
            click(x, y, self.window_rectangle)
            sleep(.3)
            click(x - 40, y, self.window_rectangle)
            sleep(.3)
            self.upgrading_building = False
            return True
        elif upgrade_button_rectangle:
            x, y = get_center_of_rectangle(upgrade_button_rectangle)
            # Clicks the upgrade button
            click(x, y, self.window_rectangle)
            sleep(.3)
            # Clicks the confirmation button
            click(705, 685, self.window_rectangle)
            sleep(.3)
            self.upgrading_building = False
            return True
        elif arrow_rectangle:
            x = arrow_rectangle[0]
            y = arrow_rectangle[1] + arrow_rectangle[3]
            # Clicks in the bottom left of the arrow, or where its pointing
            click(x, y, self.window_rectangle)
            sleep(1)
        else:
            # If the upgrade button or arrow are not present, it checks to see if there are any available upgrades
            for suggested_upgrade in self.suggested_upgrades:
                # Crops the screenshot for efficiency in color detection
                cropped_screenshot = screenshot[suggested_upgrade[1]:suggested_upgrade[1] + suggested_upgrade[3],
                                     suggested_upgrade[0] + 300:suggested_upgrade[0] + suggested_upgrade[2]]
                # Makes sure there are enough resources for upgrading
                if detect_if_color_present(self.ENOUGH_RESOURCES_COLOR, cropped_screenshot):
                    x, y = get_center_of_rectangle(suggested_upgrade)
                    # Clicks on the building to be upgraded
                    click(x, y, self.window_rectangle)
                    self.upgrading_building = True
                    sleep(1)
                    break
        return False

    def check_for_builders(self, screenshot) -> bool:
        """
        Checks for if there are available builders
        :param screenshot: screenshot of bluestacks
        :return: True if there are builders, False if there aren't
        """
        return not bool(find_image_rectangle(self.ZERO_BUILDERS, screenshot))
