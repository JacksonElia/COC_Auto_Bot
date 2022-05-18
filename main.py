from ctypes import windll
from interaction_functions import *
import cv2 as cv
import numpy as np


def main():
    # Make program aware of DPI scaling,
    windll.user32.SetProcessDPIAware()
    hwnd = get_hwnd("downloads")
    win32gui.SetForegroundWindow(hwnd)
    while True:
        screenshot = get_screenshot(hwnd)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        cv.imshow("coc", screenshot)

        if cv.waitKey(1) == ord("q"):
            cv.destroyWindow()
            break


if __name__ == '__main__':
    main()
