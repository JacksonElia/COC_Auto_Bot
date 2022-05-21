from interaction_functions import *
import cv2 as cv
import numpy as np


class VillageClearer:
    window_rectangle = []

    obstacles = ()
    resources = ()
    obstacle_rectangles = []
    resource_rectangles = []

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.obstacles = (
            (cv.imread("assets/obstacles/jpg/bush.jpg", cv.IMREAD_UNCHANGED), .97),
            (cv.imread("assets/obstacles/jpg/large_tree.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/left_trunk.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/log.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/medium_tree.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/mushroom.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/right_trunk.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/small_tree.jpg", cv.IMREAD_UNCHANGED), .93)
        )

        self.resources = (
            (cv.imread("assets/resources/elixir_icon.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/resources/gold_icon.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/resources/normal_grave.jpg", cv.IMREAD_UNCHANGED), .94)
            # TODO: Add dark elixir icon, presents, and grave
        )

    def show_rectangles(self, screenshot: Image):
        self.show_obstacles(screenshot)
        self.show_resources(screenshot)

    def find_obstacle_rectangles(self, screenshot: Image):
        self.obstacle_rectangles = []
        for obstacle, confidence in self.obstacles:
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

    def clear_obstacles(self):
        pass

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
        for resource, confidence in self.resources:
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
