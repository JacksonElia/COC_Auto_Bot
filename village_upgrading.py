from interaction_functions import *
from time import sleep
import cv2 as cv


class VillageUpgrader:
    """
    Upgrades every building as its able to.
    :param window_rectangle: The rectangle of the application window gotten with GetWindowRect
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
    NOT_ENOUGH_RESOURCES_COLOR = [127, 137, 254]  # In [B, G, R]
    # NEW_BUILDING_COLOR = [13, 255, 13]  # In [B, G, R]

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.ZERO_BUILDERS = (cv.imread("assets/misc/zero_builders.jpg", cv.IMREAD_UNCHANGED), .89)
        self.BUILDER_FACE = (cv.imread("assets/misc/builder_face.jpg", cv.IMREAD_UNCHANGED), .96)
        self.SUGGESTED_UPGRADES = (cv.imread("assets/misc/suggested_upgrades.jpg", cv.IMREAD_UNCHANGED), .8)
        self.SUGGESTED_UPGRADES_2 = (cv.imread("assets/misc/suggested_upgrades_2.jpg", cv.IMREAD_UNCHANGED), .8)
        self.UPGRADE_BUTTON = (cv.imread("assets/buttons/upgrade_button.jpg", cv.IMREAD_UNCHANGED), .91)
        self.ARROW = (cv.imread("assets/misc/arrow.jpg", cv.IMREAD_UNCHANGED), .85)
        self.CHECK_BUTTON = (cv.imread("assets/buttons/check_button.jpg", cv.IMREAD_UNCHANGED), .9)

    def open_builder_menu(self, screenshot):
        """
        Opens the builder menu if there are available builders
        :param screenshot: screenshot of bluestacks
        """
        if self.check_for_builders(screenshot):
            builder_face_rectangle = find_image_rectangle(self.BUILDER_FACE, screenshot)
            if builder_face_rectangle:
                x, y = get_center_of_rectangle(builder_face_rectangle)
                click(x, y, self.window_rectangle)
                self.upgrading_building = False
                sleep(1.5)

    def find_suggested_upgrades(self, screenshot):
        """
        Finds the suggested upgraded rectangles and stores them in suggested_upgrades
        :param screenshot: screenshot of bluestacks
        """
        self.suggested_upgrades = []
        self.suggested_upgrades_rectangle = find_image_rectangle(self.SUGGESTED_UPGRADES, screenshot)
        # Uses the position of the suggested upgrades text to create 3 rectangles where suggested upgrades could be
        if self.suggested_upgrades_rectangle:
            for i in range(1, 4):
                self.suggested_upgrades.append([self.suggested_upgrades_rectangle[0],
                                                int(self.suggested_upgrades_rectangle[1] + i * 41.5),
                                                self.suggested_upgrades_rectangle[2],
                                                self.suggested_upgrades_rectangle[3]])
        else:
            self.suggested_upgrades_rectangle = find_image_rectangle(self.SUGGESTED_UPGRADES_2, screenshot)
            if self.suggested_upgrades_rectangle:
                for i in range(1, 4):
                    self.suggested_upgrades.append([self.suggested_upgrades_rectangle[0],
                                                    int(self.suggested_upgrades_rectangle[1] + i * 41.5),
                                                    self.suggested_upgrades_rectangle[2],
                                                    self.suggested_upgrades_rectangle[3]])
            elif self.check_for_builders(screenshot):
                # Opens the builder menu if suggested upgrades text cannot be found
                self.open_builder_menu(screenshot)

    def show_suggested_upgrades(self, screenshot):
        """
        Shows the suggested upgrade rectangles
        :param screenshot: screenshot of bluestacks
        """
        if self.suggested_upgrades_rectangle:
            top_left = (self.suggested_upgrades_rectangle[0], self.suggested_upgrades_rectangle[1])
            bottom_right = (self.suggested_upgrades_rectangle[0] + self.suggested_upgrades_rectangle[2], self.suggested_upgrades_rectangle[1] + self.suggested_upgrades_rectangle[3])
            cv.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), cv.LINE_4)
            for rectangle in self.suggested_upgrades:
                top_left = (rectangle[0], rectangle[1])
                bottom_right = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
                cv.rectangle(screenshot, top_left, bottom_right, (255, 0, 255), cv.LINE_4)

    def upgrade_building(self, screenshot) -> bool:
        """
        Attempts to upgrade a building by clicking buttons at various stages in the upgrade process
        :param screenshot: screenshot of bluestacks
        :return: True if it has finished upgrading a building, False if it has not
        """
        # This gross looking if statement is for efficiency, it only checks the screenshot for the image if it can't
        # find the previous image in the screenshot
        check_button_rectangle = find_image_rectangle(self.CHECK_BUTTON, screenshot)
        if check_button_rectangle:
            x, y = get_center_of_rectangle(check_button_rectangle)
            # Clicks the check button
            click(x, y, self.window_rectangle)
            sleep(.3)
            # Clicks the X button (for if there are more things e.g. walls)
            click(x - 40, y, self.window_rectangle)
            sleep(.3)
            self.upgrading_building = False
            return True
        else:
            upgrade_button_rectangle = find_image_rectangle(self.UPGRADE_BUTTON, screenshot)
            if upgrade_button_rectangle and self.upgrading_building:
                x, y = get_center_of_rectangle(upgrade_button_rectangle)
                # Clicks the upgrade button
                click(x, y, self.window_rectangle)
                sleep(.3)
                click(1000, 580, self.window_rectangle)  # Clicks the button that appears on the CC rebuild menu
                sleep(.3)
                # Clicks the confirmation button
                click(700, 680, self.window_rectangle)
                sleep(.3)
                self.upgrading_building = False
                return True
            else:
                arrow_rectangle = find_image_rectangle(self.ARROW, screenshot)
                if arrow_rectangle:
                    x = arrow_rectangle[0]
                    y = arrow_rectangle[1] + arrow_rectangle[3]
                    # Clicks in the bottom left of the arrow, or where its pointing
                    click(x, y, self.window_rectangle)
                    sleep(1)
                else:
                    self.find_suggested_upgrades(screenshot)
                    # If the upgrade button or arrow are not present, it checks to see if there are any available upgrades
                    for suggested_upgrade in self.suggested_upgrades:
                        # Crops the screenshot for efficiency in color detection
                        cropped_screenshot = screenshot[suggested_upgrade[1]:suggested_upgrade[1] + suggested_upgrade[3],
                                             suggested_upgrade[0] + 300:suggested_upgrade[0] + suggested_upgrade[2]]
                        # Makes sure there are enough resources for upgrading
                        if not detect_if_color_present(self.NOT_ENOUGH_RESOURCES_COLOR, cropped_screenshot) and not self.upgrading_building:
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
        cropped_screenshot = screenshot[0:145, 0:]
        return not bool(find_image_rectangle(self.ZERO_BUILDERS, cropped_screenshot))
