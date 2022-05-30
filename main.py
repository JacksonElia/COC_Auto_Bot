from ctypes import windll

from village_clearing import *
from village_upgrading import *
from interaction_functions import *
import cv2 as cv
import numpy as np


def main():
    # Makes program aware of DPI scaling,
    windll.user32.SetProcessDPIAware()
    hwnd = get_hwnd("bluestacks")

    # Resizes and moves the window to the front
    win32gui.MoveWindow(hwnd, 100, 100, 1400, 805, True)
    win32gui.SetForegroundWindow(hwnd)

    village_clearer = VillageClearer(win32gui.GetWindowRect(hwnd))
    village_upgrader = VillageUpgrader(win32gui.GetWindowRect(hwnd))

    # The main loop of the bot
    while True:
        screenshot = get_screenshot(hwnd)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        # zoom_out() # TODO: Find a better way of doing this
        # village_clearer.window_rectangle = win32gui.GetWindowRect(hwnd)
        # village_clearer.find_obstacle_rectangles(screenshot)
        # village_clearer.show_obstacles(screenshot)
        # village_clearer.find_resources(screenshot)
        # village_clearer.show_resources(screenshot)
        # village_clearer.collect_resources()
        # village_clearer.clear_obstacle(screenshot)

        # village_upgrader.window_rectangle = win32gui.GetWindowRect(hwnd)
        # village_upgrader.find_suggested_upgrades(screenshot)
        # village_upgrader.show_suggested_upgrades(screenshot)
        # village_upgrader.upgrade_building(screenshot)

        village_upgrader.check_for_builders(screenshot)

        cv.imshow("What the code sees", screenshot)

        if cv.waitKey(1) == ord("q"):
            cv.destroyWindow()
            break


if __name__ == "__main__":
    main()
