from interaction_functions import *
from time import sleep
import cv2 as cv


class VillageBuilder:
    """
    Sets village layouts based on the Town hall level
    :param window_rectangle: The rectangle of the application window gotten with GetWindowRect
    """

    window_rectangle = []

    TOWN_HALLS: tuple

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.TOWN_HALLS = (
            (cv.imread("assets/townhalls/th2.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th3.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th4.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/townhalls/th5.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/townhalls/th6.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/townhalls/th7.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/townhalls/th8.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th9.jpg", cv.IMREAD_UNCHANGED), .91),
            (cv.imread("assets/townhalls/th10.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th11.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th12.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th13.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th14.jpg", cv.IMREAD_UNCHANGED), .93),
        )

    def get_town_hall_level(self, screenshot: Image):
        zoom_out()
        for i, th in enumerate(self.TOWN_HALLS):
            if find_image_rectangle(th, screenshot):
                print("TH" + str(i + 2) + " Found")

    def copy_base_layout(self, screenshot: Image):
        pass
    
