from interaction_functions import *
from time import sleep
import cv2 as cv
import numpy as np


class VillageClearer:
    """
    Finds obstacles and resources on the screen, stores their locations, and collects/clears them.
    :param window_rectangle: The rectangle of the application window gotten with GetWindowRect
    """
    window_rectangle = []
    obstacle_rectangles = []
    resource_rectangles = []

    obstacles_attempted_to_remove = []

    OBSTACLES: tuple
    RESOURCES: tuple
    REMOVE_BUTTON: tuple
    ZERO_BUILDERS: tuple
    NOT_ENOUGH_RESOURCES_COLOR = [127, 137, 254]  # In [B, G, R]

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.OBSTACLES = (
            (cv.imread("assets/obstacles/jpg/bush.jpg", cv.IMREAD_UNCHANGED), .97),
            (cv.imread("assets/obstacles/jpg/gem_box.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/large_tree.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/left_trunk.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/log.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/medium_tree.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/mushroom.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/right_trunk.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/small_tree.jpg", cv.IMREAD_UNCHANGED), .93)
        )

        self.RESOURCES = (
            (cv.imread("assets/resources/elixir_icon.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/resources/gold_icon.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/resources/normal_grave.jpg", cv.IMREAD_UNCHANGED), .94)
            # TODO: Add dark elixir icon, presents, and grave
        )

        self.REMOVE_BUTTON = (cv.imread("assets/buttons/remove_button.jpg", cv.IMREAD_UNCHANGED), .96)
        self.ZERO_BUILDERS = (cv.imread("assets/misc/zero_builders.jpg", cv.IMREAD_UNCHANGED), .9)

    def show_rectangles(self, screenshot: Image):
        """
        Shows obstacles and resources
        :param screenshot: the screenshot of bluestacks
        :return:
        """
        self.show_obstacles(screenshot)
        self.show_resources(screenshot)

    def find_obstacle_rectangles(self, screenshot: Image):
        """
        Finds all of the rectangles for visible obstacles
        :param screenshot: the screenshot of bluestacks
        :return:
        """
        self.obstacle_rectangles = []
        for obstacle, confidence in self.OBSTACLES:
            # Threshold is confidence inverted because of cv.TM_SQDIFF_NORMED
            threshold = 1 - confidence
            result = cv.matchTemplate(screenshot, obstacle, cv.TM_SQDIFF_NORMED)
            locations = np.where(result <= threshold)
            # Makes a list of (x, y) tuples for the pixel coordinates
            locations = list(zip(*locations[::-1]))

            obstacle_width = obstacle.shape[1]
            obstacle_height = obstacle.shape[0]

            # Makes a list of rectangle lists that go [x, y, w, h]
            rectangle_list = []
            for location in locations:
                rectangle_list.append([
                    int(location[0]),
                    int(location[1]),
                    obstacle_width,
                    obstacle_height
                ])

            # Gets rid of rectangles too close together
            self.obstacle_rectangles += list(cv.groupRectangles(rectangle_list, 1, .5)[0])

    def clear_obstacle(self, screenshot: Image):
        """
        Clears all of the obstacles that are visible if it is able to
        :param screenshot: the screenshot of bluestacks
        :return:
        """
        if self.obstacle_rectangles and self.check_for_builders(screenshot):
            remove_button_image, confidence = self.REMOVE_BUTTON
            threshold = 1 - confidence
            result = cv.matchTemplate(screenshot, remove_button_image, cv.TM_SQDIFF_NORMED)
            location = np.where(result <= threshold)
            location = list(zip(*location[::-1]))
            if location:
                location = location[0]
                rectangle = [location[0], location[1], remove_button_image.shape[1], remove_button_image.shape[1]]
                line_color = (0, 0, 255)
                line_type = cv.LINE_4
                top_left = (rectangle[0], rectangle[1])
                bottom_right = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
                cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)

                # Check if there are resources to remove the obstacle
                cropped_screenshot = screenshot[rectangle[1]:rectangle[1] + rectangle[3],
                                     rectangle[0]:rectangle[0] + rectangle[2]]
                if not detect_if_color_present(self.NOT_ENOUGH_RESOURCES_COLOR, cropped_screenshot):
                    print("Enough Resources")
                    x = int(rectangle[0] + rectangle[2] / 2)
                    y = int(rectangle[1] + rectangle[3] / 2)
                    click(x, y, self.window_rectangle)
                    sleep(1)
                    return
                else:
                    print("Not Enough")

            rectangle = None
            obstacle_attempted = False

            # Checks to make sure that there hasn't already been an attempt to remove the obstacle
            while True:
                # Makes sure there are still obstacles to check
                if self.obstacle_rectangles:
                    # Gets the first obstacle in the list to remove
                    rectangle = self.obstacle_rectangles.pop(0)
                    # Checks if the obstacle has already been checked
                    for attempted_obstacle in self.obstacles_attempted_to_remove:
                        if (abs(attempted_obstacle[0] - rectangle[0]) < 5 and
                                abs(attempted_obstacle[1] - rectangle[1]) < 5):
                            obstacle_attempted = True
                    if not obstacle_attempted:
                        break
                else:
                    break

            if rectangle is not None:
                self.obstacles_attempted_to_remove.append(rectangle)
                x = int(rectangle[0] + rectangle[2] / 2)
                y = int(rectangle[1] + rectangle[3] / 2)
                click(x, y, self.window_rectangle)
                sleep(1)  # The remove button takes a little bit of time to appear

    def show_obstacles(self, screenshot: Image):
        """
        Shows every obstacle rectangle
        :param screenshot: the screenshot of bluestacks
        :return:
        """
        line_color = (255, 0, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for rectangle in self.obstacle_rectangles:
            # Draw the box
            top_left = (rectangle[0], rectangle[1])
            bottom_right = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
            center = (int(rectangle[0] + rectangle[2] / 2), int(rectangle[1] + rectangle[3] / 2))
            cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)
            cv.drawMarker(screenshot, center, marker_color, marker_type)

    def find_resources(self, screenshot: Image):
        """
        Finds all of the rectangles for the visible resources
        :param screenshot: the screenshot of bluestacks
        :return:
        """
        self.resource_rectangles = []
        for resource, confidence in self.RESOURCES:
            threshold = 1 - confidence
            result = cv.matchTemplate(screenshot, resource, cv.TM_SQDIFF_NORMED)
            locations = np.where(result <= threshold)
            # Makes a list of (x, y) tuples for the pixel coordinates
            locations = list(zip(*locations[::-1]))

            resource_width = resource.shape[1]
            resource_height = resource.shape[0]

            # Makes a list of rectangle lists that go [x, y, w, h]
            rectangle_list = []
            for location in locations:
                rectangle_list.append([
                    int(location[0]),
                    int(location[1]),
                    resource_width,
                    resource_height
                ])

            # Gets rid of rectangles too close together
            self.resource_rectangles += list(cv.groupRectangles(rectangle_list, 1, .5)[0])

    def collect_resources(self):
        """
        Collects all of the visible collectors and graves
        :return:
        """
        for rectangle in self.resource_rectangles:
            x = int(rectangle[0] + rectangle[2] / 2)
            y = int(rectangle[1] + rectangle[3] / 2)
            click(x, y, self.window_rectangle)

    def show_resources(self, screenshot: Image):
        """
        Shows every resource rectangle
        :param screenshot:
        :return:
        """
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_SQUARE

        for rectangle in self.resource_rectangles:
            # Draw the box
            top_left = (rectangle[0], rectangle[1])
            bottom_right = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
            center = (int(rectangle[0] + rectangle[2] / 2), int(rectangle[1] + rectangle[3] / 2))
            cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)
            cv.drawMarker(screenshot, center, marker_color, marker_type)

    def collect_loot_cart(self):
        pass

    # TODO: Only check the top of the screen
    def check_for_builders(self, screenshot) -> bool:
        """
        Checks for if there are available builders
        :param screenshot: Screenshot of bluestacks
        :return: True if there are builders, False if there aren't
        """
        zero_builders_image, confidence = self.ZERO_BUILDERS
        threshold = 1 - confidence
        result = cv.matchTemplate(screenshot, zero_builders_image, cv.TM_SQDIFF_NORMED)
        location = np.where(result <= threshold)
        location = list(zip(*location[::-1]))
        return not bool(location)
