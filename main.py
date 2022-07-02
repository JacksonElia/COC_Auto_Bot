from ctypes import windll
from training_and_attacking import *
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

    # The classes that carry out the main functions of the bot
    village_clearer = VillageClearer(win32gui.GetWindowRect(hwnd))
    village_upgrader = VillageUpgrader(win32gui.GetWindowRect(hwnd))
    trainer_and_attacker = TrainerAndAttacker(win32gui.GetWindowRect(hwnd))

    # Variables used to smoothly move between the functions of the bot
    mode = 3
    tries = 0

    # The pop-up images
    reload_game_button = (cv.imread("assets/buttons/reload_game_button.jpg", cv.IMREAD_UNCHANGED), .95)
    okay_button = (cv.imread("assets/buttons/okay_button.jpg", cv.IMREAD_UNCHANGED), .95)
    okay_button_2 = (cv.imread("assets/buttons/okay_button_2.jpg", cv.IMREAD_UNCHANGED), .95)
    okay_button_3 = (cv.imread("assets/buttons/okay_button_3.jpg", cv.IMREAD_UNCHANGED), .95)

    # The main loop of the bot
    while True:
        window_rectangle = win32gui.GetWindowRect(hwnd)
        # win32gui.MoveWindow(hwnd, window_rectangle[0], window_rectangle[1], 1400, 805, True)

        screenshot = get_screenshot(hwnd)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        # zoom_out() # TODO: Find a better way of doing this
        # Deals with various pop-ups that can happen
        okay_button_rectangle = find_image_rectangle(okay_button, screenshot)
        if okay_button_rectangle:
            x, y = get_center_of_rectangle(okay_button_rectangle)
            click(x, y, window_rectangle)
        else:
            # Reloads the game if the client and game get de-synced
            reload_game_button_rectangle = find_image_rectangle(reload_game_button, screenshot)
            if reload_game_button_rectangle:
                x, y = get_center_of_rectangle(reload_game_button_rectangle)
                click(x, y, window_rectangle)
            else:
                # Clicks the okay button that appears when you open an account with recently finished upgrades
                okay_button_2_rectangle = find_image_rectangle(okay_button_2, screenshot)
                if okay_button_2_rectangle:
                    x, y = get_center_of_rectangle(okay_button_2_rectangle)
                    click(x, y, window_rectangle)
                else:
                    # Clicks on the okay button that acknowledges you breaking your shield
                    # okay_button_3_rectangle = find_image_rectangle(okay_button_3, screenshot)
                    # if okay_button_3_rectangle:
                    #     x, y = get_center_of_rectangle(okay_button_3_rectangle)
                    #     click(x, y, window_rectangle)
                    pass

        if mode == 1:
            village_clearer.window_rectangle = win32gui.GetWindowRect(hwnd)
            village_clearer.find_obstacle_rectangles(screenshot)
            village_clearer.find_resources(screenshot)
            village_clearer.collect_resources()
            if village_clearer.clear_obstacle(screenshot) or tries == 6:
                mode += 1
                tries = 0
        elif mode == 2:
            village_upgrader.window_rectangle = win32gui.GetWindowRect(hwnd)
            if (village_upgrader.upgrade_building(screenshot) or tries == 5) and not village_upgrader.upgrading_building:
                mode += 1
                tries = 0
            village_upgrader.find_suggested_upgrades(screenshot)
            village_upgrader.show_suggested_upgrades(screenshot)
        elif mode == 3:
            trainer_and_attacker.window_rectangle = win32gui.GetWindowRect(hwnd)
            trainer_and_attacker.train_troops(screenshot)
            if trainer_and_attacker.troops_training and tries > 1:
                mode += 1
                tries = 0
            elif trainer_and_attacker.find_base_to_attack(screenshot) or tries == 150:
                mode += 1
                tries = 0
            elif trainer_and_attacker.attacked:
                trainer_and_attacker.attacked = False
                mode += 1
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
