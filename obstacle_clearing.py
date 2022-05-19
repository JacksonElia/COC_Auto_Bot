from interaction_functions import *
import cv2 as cv
import numpy as np


class ObstacleClearer:
    threshold = 0.1
    obstacle_list = []
    obstacle_rectangles = []

    def __init__(self, confidence):
        self.obstacle_list = [
            cv.imread("assets/obstacles/jpg/bush.jpg", cv.IMREAD_UNCHANGED),
            cv.imread("assets/obstacles/jpg/large_tree.jpg", cv.IMREAD_UNCHANGED),
            cv.imread("assets/obstacles/jpg/left_trunk.jpg", cv.IMREAD_UNCHANGED),
            cv.imread("assets/obstacles/jpg/log.jpg", cv.IMREAD_UNCHANGED),
            cv.imread("assets/obstacles/jpg/medium_tree.jpg", cv.IMREAD_UNCHANGED),
            cv.imread("assets/obstacles/jpg/mushroom.jpg", cv.IMREAD_UNCHANGED),
            cv.imread("assets/obstacles/jpg/right_trunk.jpg", cv.IMREAD_UNCHANGED),
            cv.imread("assets/obstacles/jpg/small_tree.jpg", cv.IMREAD_UNCHANGED)
        ]
        # Threshold is confidence inverted because of cv.TM_SQDIFF_NORMED
        self.threshold = 1 - confidence

    def find_obstacle_rectangles(self, screenshot: Image):
        self.obstacle_rectangles = []
        for obstacle in self.obstacle_list:
            result = cv.matchTemplate(screenshot, obstacle, cv.TM_SQDIFF_NORMED)
            locations = np.where(result <= self.threshold)
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

    def show_obstacle_locations(self, screenshot: Image):
        line_color = (255, 0, 0)
        line_type = cv.LINE_4

        for rectangle in self.obstacle_rectangles:
            # Draw the box
            top_left = (rectangle[0], rectangle[1])
            bottom_right = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
            cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)

    def clear_obstacles(self):
        pass
