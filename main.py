from ctypes import windll
from training_and_attacking import *
from village_clearing import *
from village_upgrading import *
from account_changing import *
from interaction_functions import *
from data_storing import *
import cv2 as cv
import numpy as np


def main():
    # Makes program aware of DPI scaling,
    windll.user32.SetProcessDPIAware()
    hwnd = get_hwnd("bluestacks")

    # Resizes and moves the window to the front
    win32gui.MoveWindow(hwnd, 10, 10, 1400, 805, True)
    win32gui.SetForegroundWindow(hwnd)

    # This is how many accounts the bot operates, max is 50
    number_of_accounts = 9

    # The classes that carry out the main functions of the bot
    village_clearer = VillageClearer(win32gui.GetWindowRect(hwnd))
    village_upgrader = VillageUpgrader(win32gui.GetWindowRect(hwnd))
    trainer_and_attacker = TrainerAndAttacker(win32gui.GetWindowRect(hwnd))
    account_changer = AccountChanger(win32gui.GetWindowRect(hwnd), number_of_accounts)
    data_storer = DataStorer(number_of_accounts)

    data_storer.add_new_accounts(number_of_accounts)

    # Variables used to smoothly move between the functions of the bot
    mode = 4
    tries = 0

    # The images used to deal with various pop-ups
    pop_up_buttons = (
        (cv.imread("assets/buttons/reload_game_button.jpg", cv.IMREAD_UNCHANGED), .95),  # Reloads the game if the client and game get de-synced
        (cv.imread("assets/buttons/try_again_button.jpg", cv.IMREAD_UNCHANGED), .95),  # Reconnects to the game if connection is lost
        (cv.imread("assets/buttons/okay_button.jpg", cv.IMREAD_UNCHANGED), .95),
        (cv.imread("assets/buttons/okay_button_2.jpg", cv.IMREAD_UNCHANGED), .95),  # Clicks the okay button that appears when you open an account with recently finished upgrades
        (cv.imread("assets/buttons/okay_button_3.jpg", cv.IMREAD_UNCHANGED), .95),  # Clicks on the okay button that acknowledges you breaking your shield
    )

    # The main loop of the bot
    while True:
        window_rectangle = win32gui.GetWindowRect(hwnd)

        screenshot = get_screenshot(hwnd)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        # zoom_out() # TODO: Find a better way of doing this
        # Deals with various pop-ups that can happen
        for button in pop_up_buttons:
            button_rectangle = find_image_rectangle(button, screenshot)
            if button_rectangle:
                x, y = get_center_of_rectangle(button_rectangle)
                click(x, y, window_rectangle)
                break

        if mode == 1:
            village_clearer.window_rectangle = window_rectangle
            village_clearer.collect_loot_cart(screenshot)
            village_clearer.collect_resources(screenshot)
            if village_clearer.clear_obstacle(screenshot) or tries >= 60:
                mode += 1
                tries = 0
        elif mode == 2:
            village_upgrader.window_rectangle = window_rectangle
            if (village_upgrader.upgrade_building(screenshot) or tries >= 5) and not village_upgrader.upgrading_building:
                mode += 1
                tries = 0
            village_upgrader.show_suggested_upgrades(screenshot)
        elif mode == 3:
            trainer_and_attacker.window_rectangle = window_rectangle
            trainer_and_attacker.train_troops(screenshot)
            if trainer_and_attacker.troops_training and tries > 1:
                trainer_and_attacker.troops_training = False
                mode += 1
                tries = 0
            elif trainer_and_attacker.find_base_to_attack(screenshot) or tries >= 150:
                mode += 1
                tries = 0
            elif trainer_and_attacker.attacked:
                trainer_and_attacker.attacked = False
                mode += 1
                tries = 0
        elif mode == 4:
            account_changer.window_rectangle = window_rectangle
            account_changer.open_account_menu(screenshot)
            account_changer.select_next_account(screenshot)
            if account_changer.account_changed or tries > 100:
                account_changer.account_changed = False
                # mode += 1
                tries = 0
        else:
            mode = 1

        print(mode)
        tries += 1

        # cv.imshow("What the code sees", screenshot)

        if cv.waitKey(1) == ord("q"):
            cv.destroyWindow()
            break


if __name__ == "__main__":
    main()
