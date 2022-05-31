from interaction_functions import *
from time import sleep
import cv2 as cv


class TrainerAndAttacker:
    """
    Trains and attacks to get loot
    """

    window_rectangle = []

    ATTACK_BUTTON: tuple
    ARMY_BUTTON: tuple
    BARBARIAN_BUTTON: tuple
    GOBLIN_BUTTON: tuple

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.ATTACK_BUTTON = (cv.imread("assets/buttons/attack_button.jpg", cv.IMREAD_UNCHANGED), .92)
        self.ARMY_BUTTON = (cv.imread("assets/buttons/army_button.jpg", cv.IMREAD_UNCHANGED), .96)
        self.BARBARIAN_BUTTON = (cv.imread("assets/buttons/barbarian_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.GOBLIN_BUTTON = (cv.imread("assets/buttons/goblin_button.jpg", cv.IMREAD_UNCHANGED), .94)

    def train_troops(self, screenshot: Image):
        army_button_rectangle = find_image_rectangle(self.ARMY_BUTTON, screenshot)
        barbarian_button_rectangle = find_image_rectangle(self.BARBARIAN_BUTTON, screenshot)
        goblin_button_rectangle = find_image_rectangle(self.GOBLIN_BUTTON, screenshot)
        if army_button_rectangle:
            x, y = get_center_of_rectangle(army_button_rectangle)
            click(x, y, self.window_rectangle)
            sleep(1)
            click(x + 330, y - 520, self.window_rectangle)
        elif goblin_button_rectangle:
            x, y = get_center_of_rectangle(goblin_button_rectangle)
            click_and_hold(x, y, 6, self.window_rectangle)
            sleep(.3)
            # Clicks two more times to make there is no pop up in the way
            click(x, y + 100, self.window_rectangle)
            click(x, y + 100, self.window_rectangle)
            sleep(.3)
            # Closes out of the troop menu
            x_out()
            sleep(1)
        elif barbarian_button_rectangle:
            x, y = get_center_of_rectangle(barbarian_button_rectangle)
            click_and_hold(x, y, 6, self.window_rectangle)
            sleep(.3)
            # Clicks one more time to make sure there is no pop up in the way
            click(x, y, self.window_rectangle)
            sleep(.3)
            # Closes out of the troop menu
            x_out()
