from interaction_functions import *
from time import sleep
import cv2 as cv


class AccountChanger:
    """
    Changes COC accounts using Supercell ID
    """

    window_rectangle = []
    number_of_accounts = 1

    accounts_menu_opened = False
    account_number = 0
    scrolled_to_account = False

    def __init__(self, window_rectangle: list, number_of_accounts: int):
        self.window_rectangle = window_rectangle
        self.number_of_accounts = number_of_accounts

        self.SETTINGS_BUTTON = (cv.imread("assets/buttons/settings_button.jpg", cv.IMREAD_UNCHANGED), .85)
        self.SWITCH_ACCOUNTS_BUTTON = (cv.imread("assets/buttons/switch_accounts_button.jpg", cv.IMREAD_UNCHANGED), .95)
        self.COC_ICON = (cv.imread("assets/misc/coc_icon.jpg", cv.IMREAD_UNCHANGED), .9)

    def open_account_menu(self, screenshot: Image):
        # Doesn't try to open the menu if it is already opened
        if self.accounts_menu_opened:
            return
        settings_button_rectangle = find_image_rectangle(self.SETTINGS_BUTTON, screenshot)
        if settings_button_rectangle:
            x, y = get_center_of_rectangle(settings_button_rectangle)
            click(x, y, self.window_rectangle)
            sleep(1.5)
        else:
            switch_accounts_button_rectangle = find_image_rectangle(self.SWITCH_ACCOUNTS_BUTTON, screenshot)
            if switch_accounts_button_rectangle:
                x, y = get_center_of_rectangle(switch_accounts_button_rectangle)
                click(x, y, self.window_rectangle)
                sleep(1.5)
                self.accounts_menu_opened = True

    def select_next_account(self, screenshot: Image):
        # The rectangles are sorted by y (lowest first)
        coc_icon_rectangles = find_image_rectangles(self.COC_ICON, screenshot)
        if coc_icon_rectangles:
            if self.scrolled_to_account:
                if self.account_number < self.number_of_accounts - 3:
                    # Opens the new account
                    click(coc_icon_rectangles[0][0], coc_icon_rectangles[0][1], self.window_rectangle)
                    self.accounts_menu_opened = False
                    self.scrolled_to_account = False
                else:
                    # The last 3 accounts cannot be scrolled to the top of the screem
                    account_index = self.account_number - self.number_of_accounts  # This gets the account index in order from top to bottom
                    click(coc_icon_rectangles[account_index][0], coc_icon_rectangles[account_index][1], self.window_rectangle)
                    self.accounts_menu_opened = False
                    self.scrolled_to_account = False
            else:
                self.account_number += 1
                for i in range(1, self.account_number):
                    # Scrolls by clicking and holding on the 2nd icon and moving the mouse to the first icon
                    click_and_drag(coc_icon_rectangles[0][0], coc_icon_rectangles[0][1], coc_icon_rectangles[1][0],
                                   coc_icon_rectangles[1][1], .003, self.window_rectangle)
                self.scrolled_to_account = True
