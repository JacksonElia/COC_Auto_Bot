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

    OBSTACLES = ()
    RESOURCES = ()
    BUTTONS = ()
    NOT_ENOUGH_RESOURCES_COLOR = [127, 137, 254]  # In [B, G, R]

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.OBSTACLES = (
            (cv.imread("assets/obstacles/jpg/bush.jpg", cv.IMREAD_UNCHANGED), .97),
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

        self.BUTTONS = (
            (cv.imread("assets/buttons/remove_button.jpg", cv.IMREAD_UNCHANGED), .9),
            ()
        )

    def show_rectangles(self, screenshot: Image):
        self.show_obstacles(screenshot)
        self.show_resources(screenshot)

    def find_obstacle_rectangles(self, screenshot: Image):
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
        if self.obstacle_rectangles:
            remove_button_image, confidence = self.BUTTONS[0]
            threshold = 1 - confidence
            result = cv.matchTemplate(screenshot, remove_button_image, cv.TM_SQDIFF_NORMED)
            location = np.where(result <= threshold)
            location = list(zip(*location[::-1]))
            if location:
                location = location[0]
                rectangle = [location[0], remove_button_image.shape[0], location[1], remove_button_image.shape[1]]

                line_color = (0, 0, 255)
                line_type = cv.LINE_4
                top_left = (rectangle[0], rectangle[2])
                bottom_right = (rectangle[0] + rectangle[1], rectangle[2] + rectangle[3])
                cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)

                # Check if there are resources to remove the obstacle
                cropped_screenshot = screenshot[rectangle[2]:rectangle[2] + rectangle[3],
                                     rectangle[0]:rectangle[0] + rectangle[1]]
                if not detect_if_color_present(self.NOT_ENOUGH_RESOURCES_COLOR, cropped_screenshot):
                    print("Enough Resources")
                    x, y = (int(rectangle[0] + rectangle[1] / 2), int(rectangle[2] + rectangle[3] / 2))
                    # click(x, y, self.window_rectangle)
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
                x, y = (int(rectangle[0] + rectangle[2] / 2), int(rectangle[1] + rectangle[3] / 2))
                click(x, y, self.window_rectangle)
                sleep(.5)  # The remove button takes a little bit of time to appear

        # TODO: Check if there are builders

    def show_obstacles(self, screenshot: Image):
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
        for rectangle in self.resource_rectangles:
            x, y = (int(rectangle[0] + rectangle[2] / 2), int(rectangle[1] + rectangle[3] / 2))
            click(x, y, self.window_rectangle)

    def show_resources(self, screenshot: Image):
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
