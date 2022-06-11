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

    village_clearer = VillageClearer(win32gui.GetWindowRect(hwnd))
    village_upgrader = VillageUpgrader(win32gui.GetWindowRect(hwnd))
    trainer_and_attacker = TrainerAndAttacker(win32gui.GetWindowRect(hwnd))

    mode = 1
    tries = 0

    # The main loop of the bot
    while True:
        window_rectangle = win32gui.GetWindowRect(hwnd)
        win32gui.MoveWindow(hwnd, window_rectangle[0], window_rectangle[1], 1400, 805, True)

        screenshot = get_screenshot(hwnd)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        # zoom_out() # TODO: Find a better way of doing this
        # Reloads the game if the client and game get de-synced
        reload_game = (cv.imread("assets/buttons/return_home_button.jpg", cv.IMREAD_UNCHANGED), .95)
        reload_game_button = find_image_rectangle(reload_game, screenshot)
        if reload_game_button:
            x, y = get_center_of_rectangle(reload_game_button)
            click(x, y, win32gui.GetWindowRect(hwnd))

        if mode == 1:
            village_clearer.window_rectangle = win32gui.GetWindowRect(hwnd)
            village_clearer.find_obstacle_rectangles(screenshot)
            village_clearer.show_obstacles(screenshot)
            village_clearer.find_resources(screenshot)
            village_clearer.show_resources(screenshot)
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
