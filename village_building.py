from interaction_functions import *
from time import sleep
from pyperclip import copy, paste
from pydirectinput import keyDown, keyUp
import cv2 as cv


class VillageBuilder:
    """
    Sets village layouts based on the Town hall level
    :param window_rectangle: The rectangle of the application window gotten with GetWindowRect
    """

    window_rectangle = []
    town_hall_level = 2
    building_base = False
    base_link_entered = False
    base_copied = False
    canceling_edit = False

    TOWN_HALLS: tuple

    BASE_LINKS = (
        "must be th4 to copy bases",
        "must be th4 to copy bases",
        "must be th4 to copy bases",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH4%3AHV%3AAAAALQAAAAHkquOpivBodm0qRz1DaEbD",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH5%3AHV%3AAAAARwAAAAGRO7_IiFECUbLA7vJGxz9e",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH6%3AHV%3AAAAALgAAAAHsNlLRw9Ed-W7oXj9YjukP",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH7%3AHV%3AAAAAWAAAAAFZmfC1lPx30LHaZ5OGyOCG",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH8%3AHV%3AAAAAIAAAAAH84TzqPnUD7I4WSBls_KYZ",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH9%3AHV%3AAAAAEQAAAAIcAOeCtge-W2UNbAZJ3K7g",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH10%3AHV%3AAAAAVgAAAAFZjxWSqIPS1ULAqQpocogk",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH11%3AHV%3AAAAAMwAAAAGseEXdKmvf_Sljb8p5Xpdp",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH12%3AHV%3AAAAAIQAAAAH8MlHeqvETps2HjiM9nzao",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH13%3AHV%3AAAAAAQAAAAH1vRXQwkkxF-AuqcsNE34B",
        "https://link.clashofclans.com/en?action=OpenLayout&id=TH14%3AHV%3AAAAALAAAAAHuYCXPQ0h8bzRVZv93-6Zc"
    )

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.TOWN_HALLS = (
            (cv.imread("assets/townhalls/th2.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th3.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/townhalls/th4.jpg", cv.IMREAD_UNCHANGED), .97),
            (cv.imread("assets/townhalls/th5.jpg", cv.IMREAD_UNCHANGED), .97),
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

        self.HOME_BUTTON = (cv.imread("assets/buttons/home_button.jpg", cv.IMREAD_UNCHANGED), .95)
        self.CHROME_BUTTON = (cv.imread("assets/buttons/chrome_button.jpg", cv.IMREAD_UNCHANGED), .95)
        self.REFRESH_BUTTON = (cv.imread("assets/buttons/refresh_button.jpg", cv.IMREAD_UNCHANGED), .95)
        self.I_HAVE_CLASH_BUTTON = (cv.imread("assets/buttons/i_have_clash_button.jpg", cv.IMREAD_UNCHANGED), .96)

        self.ACTIVE_VILLAGE = (cv.imread("assets/misc/active_village.jpg", cv.IMREAD_UNCHANGED), .9)
        self.ACTIVE_VILLAGE_2 = (cv.imread("assets/misc/active_village_2.jpg", cv.IMREAD_UNCHANGED), .9)
        self.SAVE_BUTTON = (cv.imread("assets/buttons/save_button.jpg", cv.IMREAD_UNCHANGED), .95)
        self.OKAY_BUTTON = (cv.imread("assets/buttons/okay_button_edit_mode.jpg", cv.IMREAD_UNCHANGED), .95)
        self.CANCEL_BUTTON = (cv.imread("assets/buttons/cancel_button.jpg", cv.IMREAD_UNCHANGED), .95)

    def get_town_hall_level(self, screenshot: Image) -> int:
        zoom_out()
        for i, th in enumerate(self.TOWN_HALLS):
            if find_image_rectangle(th, screenshot):
                print("TH" + str(i + 2) + " Found")
                return i + 2
        return 0

    def copy_base_layout(self, screenshot: Image):
        i_have_clash_button_rectangle = find_image_rectangle(self.I_HAVE_CLASH_BUTTON, screenshot)
        if self.base_copied and i_have_clash_button_rectangle:
            x, y = get_center_of_rectangle(i_have_clash_button_rectangle)
            click(x, y, self.window_rectangle)
            sleep(.3)
            click(x, y, self.window_rectangle)
            sleep(3)
            self.base_link_entered = True
            self.base_copied = False
        else:
            refresh_button_rectangle = find_image_rectangle(self.REFRESH_BUTTON, screenshot)
            if refresh_button_rectangle:
                x, y = get_center_of_rectangle(refresh_button_rectangle)
                # Clicks on the search bar
                click(x + 200, y + 10, self.window_rectangle)
                sleep(1)
                # Pastes the base link into the search bar
                base_link = self.BASE_LINKS[self.town_hall_level - 1]
                copy(base_link)
                keyDown("ctrl")
                keyDown("v")
                sleep(.1)
                keyUp("ctrl")
                keyUp("v")
                sleep(.5)
                # Presses enter to search
                keyDown("return")
                sleep(.1)
                keyUp("return")
                self.base_copied = True
            else:
                chrome_button_rectangle = find_image_rectangle(self.CHROME_BUTTON, screenshot)
                if chrome_button_rectangle:
                    x, y = get_center_of_rectangle(chrome_button_rectangle)
                    click(x, y, self.window_rectangle)
                    sleep(1.5)
                else:
                    home_button_rectangle = find_image_rectangle(self.HOME_BUTTON, screenshot)
                    if home_button_rectangle:
                        x, y = get_center_of_rectangle(home_button_rectangle)
                        click(x, y, self.window_rectangle)
                        sleep(1.5)
                    else:
                        # This handles if the bluestacks window decides to misbehave
                        click(250, -10, self.window_rectangle)
                        sleep(1.5)

    def handle_base_edit(self, screenshot: Image) -> bool:
        active_village_rectangle = find_image_rectangle(self.ACTIVE_VILLAGE, screenshot)
        if not active_village_rectangle:
            active_village_rectangle = find_image_rectangle(self.ACTIVE_VILLAGE_2, screenshot)
        if active_village_rectangle:
            x, y = get_center_of_rectangle(active_village_rectangle)
            click(x, y + 200, self.window_rectangle)
            sleep(1.5)
        else:
            okay_button_rectangle = find_image_rectangle(self.OKAY_BUTTON, screenshot)
            if okay_button_rectangle:
                x, y = get_center_of_rectangle(okay_button_rectangle)
                click(x, y, self.window_rectangle)
                sleep(1.5)
                # The Okay button is the same for 2 stages during this
                if self.canceling_edit:
                    self.canceling_edit = False
                    return True
            else:
                save_button_rectangle = find_image_rectangle(self.SAVE_BUTTON, screenshot)
                if save_button_rectangle:
                    x, y = get_center_of_rectangle(save_button_rectangle)
                    click(x, y, self.window_rectangle)
                    sleep(1.5)
                    return True
                else:
                    cancel_button_rectangle = find_image_rectangle(self.CANCEL_BUTTON, screenshot)
                    if cancel_button_rectangle:
                        x, y = get_center_of_rectangle(cancel_button_rectangle)
                        click(x, y, self.window_rectangle)
                        sleep(1.5)
                        self.canceling_edit = True
        return False
