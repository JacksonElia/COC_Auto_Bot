from ctypes import windll
from interaction_functions import *
import cv2 as cv
import numpy as np


def main():
    # Make program aware of DPI scaling,
    windll.user32.SetProcessDPIAware()
    hwnd = get_hwnd("bluestacks")
    win32gui.SetForegroundWindow(hwnd)

    obstacle_list = [
        cv.imread("assets/obstacles/jpg/bush.jpg", cv.IMREAD_UNCHANGED),
        cv.imread("assets/obstacles/jpg/large_tree.jpg", cv.IMREAD_UNCHANGED),
        cv.imread("assets/obstacles/jpg/left_trunk.jpg", cv.IMREAD_UNCHANGED),
        cv.imread("assets/obstacles/jpg/log.jpg", cv.IMREAD_UNCHANGED),
        cv.imread("assets/obstacles/jpg/medium_tree.jpg", cv.IMREAD_UNCHANGED),
        cv.imread("assets/obstacles/jpg/mushroom.jpg", cv.IMREAD_UNCHANGED),
        cv.imread("assets/obstacles/jpg/right_trunk.jpg", cv.IMREAD_UNCHANGED),
        cv.imread("assets/obstacles/jpg/small_tree.jpg", cv.IMREAD_UNCHANGED)
    ]

    threshold = 0.06

    while True:
        screenshot = get_screenshot(hwnd)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        for obstacle in obstacle_list:
            result = cv.matchTemplate(screenshot, obstacle, cv.TM_SQDIFF_NORMED)
            locations = np.where(result <= threshold)

            # We can zip those up into a list of (x, y) position tuples
            locations = list(zip(*locations[::-1]))
            print(locations)

            if locations:
                print('Found needle.')

                needle_w = obstacle.shape[1]
                needle_h = obstacle.shape[0]
                line_color = (0, 255, 0)
                line_type = cv.LINE_4

                # Loop over all the locations and draw their rectangle
                for loc in locations:
                    # Determine the box positions
                    top_left = loc
                    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                    # Draw the box
                    cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)

            else:
                print('Needle not found.')

        cv.imshow('Matches', screenshot)

        if cv.waitKey(1) == ord("q"):
            cv.destroyWindow()
            break


if __name__ == '__main__':
    main()
