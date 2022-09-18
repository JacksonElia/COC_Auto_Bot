from ctypes import windll
from ast import literal_eval

from training_and_attacking import *
from village_clearing import *
from village_upgrading import *
from account_changing import *
from village_building import *
from interaction_functions import *
from data_storing import *
import cv2 as cv
import numpy as np


class AutoBot:

    # Variables used to smoothly move between the functions of the bot
    mode = 1
    tries = 0

    # The images used to deal with various pop-ups
    pop_up_buttons = (
        # Reloads the game if the client and game get de-synced
        (cv.imread("assets/buttons/reload_game_button.jpg", cv.IMREAD_UNCHANGED), .95),
        # Reconnects to the game if connection is lost
        (cv.imread("assets/buttons/try_again_button.jpg", cv.IMREAD_UNCHANGED), .95),
        (cv.imread("assets/buttons/okay_button.jpg", cv.IMREAD_UNCHANGED), .95),
        # Clicks the okay button that appears when you open an account with recently finished upgrades
        (cv.imread("assets/buttons/okay_button_2.jpg", cv.IMREAD_UNCHANGED), .95),
        # Clicks on the okay button that acknowledges you breaking your shield
        (cv.imread("assets/buttons/okay_button_3.jpg", cv.IMREAD_UNCHANGED), .95),
        # Clicks on the okay button when you get treasury loot
        (cv.imread("assets/buttons/okay_button_4.jpg", cv.IMREAD_UNCHANGED), .95),
        # Returns home after watching someone attack the selected base
        (cv.imread("assets/buttons/return_home_villager_button.jpg", cv.IMREAD_UNCHANGED), .93),
        # Clicks the x button that appears in the Town Hall Upgraded popup
        (cv.imread("assets/buttons/new_th_x_button.jpg", cv.IMREAD_UNCHANGED), .94)
    )

    pop_up_button_i = 0

    def __init__(self, number_of_accounts):

        # Makes program aware of DPI scaling,
        windll.user32.SetProcessDPIAware()
        self.hwnd = get_hwnd("bluestacks")

        # Resizes and moves the window to the front
        win32gui.MoveWindow(self.hwnd, 10, 10, 1400, 805, True)
        win32gui.SetForegroundWindow(self.hwnd)

        window_rectangle = win32gui.GetWindowRect(self.hwnd)

        # The classes that carry out the main functions of the bot
        self.village_clearer = VillageClearer(win32gui.GetWindowRect(window_rectangle))
        self.village_upgrader = VillageUpgrader(win32gui.GetWindowRect(window_rectangle))
        self.trainer_and_attacker = TrainerAndAttacker(win32gui.GetWindowRect(window_rectangle))
        self.account_changer = AccountChanger(win32gui.GetWindowRect(window_rectangle), number_of_accounts)
        self.village_builder = VillageBuilder(win32gui.GetWindowRect(window_rectangle))
        self.data_storer = DataStorer(number_of_accounts)

        # Makes sure the csv file has rows for each account
        self.data_storer.add_new_accounts()

    def run_bot(self):

        sleep(3)
        # The main loop of the bot
        while True:
            window_rectangle = win32gui.GetWindowRect(self.hwnd)

            screenshot = get_screenshot(self.hwnd)
            screenshot = np.array(screenshot)
            screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

            # Deals with various pop-ups that can happen, only does one per frame rather than all of them every frame
            self.pop_up_button_i += 1
            if self.pop_up_button_i >= len(self.pop_up_buttons):
                self.pop_up_button_i = 0
            button = self.pop_up_buttons[self.pop_up_button_i]
            button_rectangle = find_image_rectangle(button, screenshot)
            if button_rectangle:
                x, y = get_center_of_rectangle(button_rectangle)
                click(x, y, window_rectangle)

            if self.mode == 1:  # Clears the village of obstacles and collects loot
                self.village_clearer.window_rectangle = window_rectangle
                self.village_clearer.collect_resources(screenshot)
                # Only collects the loot cart if the account is TH5 or above
                if int(self.data_storer.get_account_info(self.account_changer.account_number)[0]) > 4:
                    self.village_clearer.collect_loot_cart(screenshot)
                if self.village_clearer.clear_obstacle(screenshot) or self.tries >= 6:
                    self.data_storer.update_account_info(self.account_changer.account_number,
                                                    rocks_removed=self.village_clearer.rocks_removed)
                    self.mode += 1
                    self.tries = 0
            elif self.mode == 2:  # Upgrades and purchases buildings
                self.village_upgrader.window_rectangle = window_rectangle
                if ((self.village_upgrader.upgrade_building(screenshot) or self.tries >= 10) and
                        not self.village_upgrader.upgrading_building or self.tries >= 30):
                    self.mode += 1
                    self.tries = 0
                    self.village_upgrader.upgrading_building = False
                # village_upgrader.show_suggested_upgrades(screenshot)
            elif self.mode == 3:  # Trains troops and attacks for loot
                self.trainer_and_attacker.window_rectangle = window_rectangle
                if not self.trainer_and_attacker.attack_completed:
                    self.trainer_and_attacker.train_troops(screenshot)
                if self.trainer_and_attacker.attack_completed:
                    # Attempts to upgrade a troop in the laboratory
                    if self.trainer_and_attacker.upgrade_troops(screenshot):
                        self.trainer_and_attacker.scroll_count = 0
                        self.trainer_and_attacker.lab_opened = False
                        self.trainer_and_attacker.attack_completed = False
                        self.mode += 1
                        self.tries = 0
                elif self.trainer_and_attacker.troops_training or self.tries > 300:
                    self.trainer_and_attacker.troops_training = False
                    self.trainer_and_attacker.attack_completed = False
                    self.mode += 1
                    self.tries = 0
                elif self.trainer_and_attacker.attack_desynced:
                    self.trainer_and_attacker.attack_desynced = False
                    self.trainer_and_attacker.attack_completed = False
                    self.data_storer.update_account_info(self.account_changer.account_number,
                                                    total_gold=self.trainer_and_attacker.total_gold,
                                                    total_elixir=self.trainer_and_attacker.total_elixir,
                                                    gold_read=self.trainer_and_attacker.gold_read,
                                                    elixir_read=self.trainer_and_attacker.elixir_read,
                                                    )
                    self.mode += 1
                    self.tries = 0
                else:
                    self.trainer_and_attacker.find_base_to_attack(screenshot)
                    if self.trainer_and_attacker.attack_completed:
                        # Stores the collected account data in a csv file
                        self.data_storer.update_account_info(self.account_changer.account_number,
                                                        total_gold=self.trainer_and_attacker.total_gold,
                                                        total_elixir=self.trainer_and_attacker.total_elixir,
                                                        gold_read=self.trainer_and_attacker.gold_read,
                                                        elixir_read=self.trainer_and_attacker.elixir_read,
                                                        )
            elif self.mode == 4:  # Sets base layouts
                # Stores the town hall level for the account in a csv file
                town_hall_level = self.village_builder.get_town_hall_level(screenshot)
                if town_hall_level > 0:
                    self.data_storer.update_account_info(self.account_changer.account_number,
                                                    town_hall=self.village_builder.get_town_hall_level(screenshot))
                self.village_builder.town_hall_level = int(self.data_storer.get_account_info(self.account_changer.account_number)[0])
                if self.village_builder.town_hall_level >= 4 and randrange(0, 11) == 10:
                    self.village_builder.building_base = True
                if self.village_builder.building_base:
                    self.village_builder.window_rectangle = window_rectangle
                    if self.village_builder.base_link_entered:
                        # Handles base editing and saving
                        if self.village_builder.handle_base_edit(screenshot):
                            self.village_builder.base_link_entered = False
                            sleep(1)
                            # Once the process is done, it closes out of the base window
                            x_out()
                            sleep(.5)
                            self.village_builder.building_base = False
                            self.mode += 1
                            self.tries = 0
                    else:
                        # Opens chrome and enters the base link
                        self.village_builder.copy_base_layout(screenshot)
                else:
                    self.village_builder.building_base = False
                    self.mode += 1
                    self.tries = 0
                # Sometimes Bluestacks glitches and the window for base layouts just doesn't get pulled up
                if self.tries >= 30:
                    self.village_builder.building_base = False
                    self.mode += 1
                    self.tries = 0
            elif self.mode == 5:  # Changes Supercell ID accounts
                self.account_changer.window_rectangle = window_rectangle
                self.account_changer.open_account_menu(screenshot)
                self.account_changer.select_next_account(screenshot)
                if self.account_changer.account_changed or self.tries > 100:
                    self.account_changer.accounts_menu_opened = False
                    self.account_changer.account_changed = False
                    # Reads values from csv file for the new account
                    self.village_clearer.rocks_removed = literal_eval(
                        self.data_storer.get_account_info(self.account_changer.account_number)[1])
                    self.village_upgrader.town_hall_level = int(self.data_storer.get_account_info(self.account_changer.account_number)[0])
                    self.trainer_and_attacker.town_hall_level = int(self.data_storer.get_account_info(self.account_changer.account_number)[0])
                    self.trainer_and_attacker.total_gold = int(self.data_storer.get_account_info(self.account_changer.account_number)[2])
                    self.trainer_and_attacker.total_elixir = int(self.data_storer.get_account_info(self.account_changer.account_number)[3])
                    self.trainer_and_attacker.gold_read = int(self.data_storer.get_account_info(self.account_changer.account_number)[4])
                    self.trainer_and_attacker.elixir_read = int(self.data_storer.get_account_info(self.account_changer.account_number)[5])
                    self.mode += 1
                    self.tries = 0
            else:
                self.mode = 1

            print(self.mode)
            self.tries += 1

            # cv.imshow("What the code sees", screenshot)

            if cv.waitKey(1) == ord("q"):
                cv.destroyWindow()
                break