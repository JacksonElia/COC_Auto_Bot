from interaction_functions import *
import cv2 as cv
import numpy as np


process_name = "HD-Player.exe"


def main():
    # Runs while BlueStacks is open
    while True:
    # while process_name in [p.name() for p in process_iter()]:
        screenshot = get_screenshot()
        screenshot = np.array(screenshot)
        screenshot = screenshot[:, :, ::-1].copy()
        cv.imshow("coc", screenshot)

        if cv.waitKey(1) == ord("q"):
            cv.destroyWindow()
            break


if __name__ == '__main__':
    main()
