from interaction_functions import *
from time import sleep
import cv2 as cv


class TrainerAndAttacker:
    """
    Trains and attacks to get loot
    :param window_rectangle: The rectangle of the application window gotten with GetWindowRect
    """

    window_rectangle = []
    town_hall_level = 2
    gold_read = 0
    elixir_read = 0
    total_gold = 0
    total_elixir = 0
    troops_trained = False
    troops_training = False
    attack_desynced = False
    attack_completed = False
    lab_opened = False
    scroll_count = 0

    NOT_ENOUGH_RESOURCES_COLOR = [127, 137, 254]

    LABORATORIES: tuple
    LAB_LOOT_ICONS: tuple
    RESEARCH_BUTTON: tuple
    LABORATORY_MENU_TOP: tuple
    ATTACK_BUTTON: tuple
    ARMY_BUTTON: tuple
    BARBARIAN_BUTTON: tuple
    GOBLIN_BUTTON: tuple
    NEXT_BUTTON: tuple
    POPUP_X_BUTTON: tuple
    ARMY_X_BUTTON: tuple
    LABORATORY_X_BUTTON: tuple
    RETURN_HOME_BUTTON: tuple

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.LABORATORIES = (
            (cv.imread("assets/laboratories/lab1.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab2.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab3.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab4.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab5.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab6.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab7.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab8.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab9.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab10.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab11.jpg", cv.IMREAD_UNCHANGED), .85),
            (cv.imread("assets/laboratories/lab12.jpg", cv.IMREAD_UNCHANGED), .85)
        )

        self.LAB_LOOT_ICONS = (
            (cv.imread("assets/misc/lab_elixir.jpg", cv.IMREAD_UNCHANGED), .92),
            (cv.imread("assets/misc/lab_dark_elixir.jpg", cv.IMREAD_UNCHANGED), .92)
        )

        self.RESEARCH_BUTTON = (cv.imread("assets/buttons/research_button.jpg", cv.IMREAD_UNCHANGED), .91)
        self.LABORATORY_MENU_TOP = (cv.imread("assets/misc/laboratory_menu_top.jpg", cv.IMREAD_UNCHANGED), .94)
        self.ATTACK_BUTTON = (cv.imread("assets/buttons/attack_button.jpg", cv.IMREAD_UNCHANGED), .85)
        self.ARMY_BUTTON = (cv.imread("assets/buttons/army_button.jpg", cv.IMREAD_UNCHANGED), .9)
        self.BARBARIAN_BUTTON = (cv.imread("assets/buttons/barbarian_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.GOBLIN_BUTTON = (cv.imread("assets/buttons/goblin_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.GREY_GOBLIN_BUTTON = (cv.imread("assets/buttons/grey_goblin_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.NEXT_BUTTON = (cv.imread("assets/buttons/next_button.jpg", cv.IMREAD_UNCHANGED), .9)
        self.POPUP_X_BUTTON = (cv.imread("assets/buttons/popup_x_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.ARMY_X_BUTTON = (cv.imread("assets/buttons/army_x_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.LABORATORY_X_BUTTON = (cv.imread("assets/buttons/laboratory_x_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.RETURN_HOME_BUTTON = (cv.imread("assets/buttons/return_home_button.jpg", cv.IMREAD_UNCHANGED), .9)
        self.FINISH_TRAINING = (cv.imread("assets/misc/finish_training.jpg", cv.IMREAD_UNCHANGED), .97)
        self.AVAILABLE_LOOT = (cv.imread("assets/misc/available_loot.jpg", cv.IMREAD_UNCHANGED), .8)
        self.AVAILABLE_LOOT_2 = (cv.imread("assets/misc/available_loot_2.jpg", cv.IMREAD_UNCHANGED), .8)

    def train_troops(self, screenshot: Image):
        """
        Trains either goblins or barbarians for attacking
        :param screenshot: Screenshot of bluestacks
        """
        # Doesn't try to train troops if they have already been trained
        if self.troops_trained:
            return
        # If statement optimized to check the screenshot for as little images as necessary
        army_button_rectangle = find_image_rectangle(self.ARMY_BUTTON, screenshot)
        if army_button_rectangle:
            x, y = get_center_of_rectangle(army_button_rectangle)
            # Clicks the army button
            click(x, y, self.window_rectangle)
            sleep(1)
            # Clicks the train troops tab
            click(x + 330, y - 520, self.window_rectangle)
            sleep(1)
        else:
            goblin_button_rectangle = find_image_rectangle(self.GOBLIN_BUTTON, screenshot)
            if goblin_button_rectangle:
                x, y = get_center_of_rectangle(goblin_button_rectangle)
                click_and_hold(x, y, 3.5, self.window_rectangle)
                sleep(.3)
                # Clicks two more times to make there is no pop up in the way
                click(x, y + 100, self.window_rectangle)
                click(x, y + 100, self.window_rectangle)
                sleep(.3)
                # Closes out of the troop menu
                army_x_button_rectangle = find_image_rectangle(self.ARMY_X_BUTTON, screenshot)
                if army_x_button_rectangle:
                    x, y = get_center_of_rectangle(army_x_button_rectangle)
                    click(x, y, self.window_rectangle)
                    sleep(.3)
                else:
                    click(1300, 40, self.window_rectangle)
                self.troops_training = True
            else:
                barbarian_button_rectangle = find_image_rectangle(self.BARBARIAN_BUTTON, screenshot)
                if barbarian_button_rectangle:
                    x, y = get_center_of_rectangle(barbarian_button_rectangle)
                    click_and_hold(x, y, 3.5, self.window_rectangle)
                    sleep(.3)
                    # Clicks two more times to make there is no pop up in the way
                    click(x, y + 100, self.window_rectangle)
                    click(x, y + 100, self.window_rectangle)
                    sleep(.3)
                    # Closes out of the troop menu
                    army_x_button_rectangle = find_image_rectangle(self.ARMY_X_BUTTON, screenshot)
                    if army_x_button_rectangle:
                        x, y = get_center_of_rectangle(army_x_button_rectangle)
                        click(x, y, self.window_rectangle)
                        sleep(.3)
                    else:
                        click(1300, 40, self.window_rectangle)
                    sleep(1)
                    self.troops_training = True
                else:
                    grey_goblin_button_rectangle = find_image_rectangle(self.GREY_GOBLIN_BUTTON, screenshot)
                    if grey_goblin_button_rectangle:
                        # Checks if troops have been trained
                        finish_training_rectangle = find_image_rectangle(self.FINISH_TRAINING, screenshot)
                        if not finish_training_rectangle:
                            self.troops_trained = True
                            self.troops_training = False
                        else:
                            self.troops_trained = False
                            self.troops_training = True
                        # Closes out of the troop menu
                        army_x_button_rectangle = find_image_rectangle(self.ARMY_X_BUTTON, screenshot)
                        if army_x_button_rectangle:
                            x, y = get_center_of_rectangle(army_x_button_rectangle)
                            click(x, y, self.window_rectangle)
                        else:
                            click(1300, 40, self.window_rectangle)
                        sleep(1)
                    else:
                        popup_x_button_rectangle = find_image_rectangle(self.POPUP_X_BUTTON, screenshot)
                        if popup_x_button_rectangle:
                            self.troops_trained = True
                            self.troops_training = False
                            sleep(.5)

    def find_base_to_attack(self, screenshot: Image):
        """
        Finds a base to attack by reading how much loot there is
        :param screenshot: Screenshot of bluestacks
        :return: True if the attack has been finished
        """
        return_home_button_rectangle = find_image_rectangle(self.RETURN_HOME_BUTTON, screenshot)
        if return_home_button_rectangle:
            # Appears once the attack is finished
            x, y = get_center_of_rectangle(return_home_button_rectangle)
            click(x, y, self.window_rectangle)
            sleep(2)
            self.attack_completed = True
            return
        # Makes sure troops have been trained
        if not self.troops_trained:
            return
        # Uses the next button to decide what it should do based on how much loot it reads
        next_button_rectangle = find_image_rectangle(self.NEXT_BUTTON, screenshot)
        if next_button_rectangle:
            available_loot_rectangle = find_image_rectangle(self.AVAILABLE_LOOT, screenshot)
            if not available_loot_rectangle:
                available_loot_rectangle = find_image_rectangle(self.AVAILABLE_LOOT_2, screenshot)
            if available_loot_rectangle:
                x = available_loot_rectangle[0]
                y = available_loot_rectangle[1]
                # Gets the loot text relative to the available loot text
                gold_cropped_screenshot = screenshot[y + 24:y + 24 + 24, x:x + 155]
                elixir_cropped_screenshot = screenshot[y + 66:y + 66 + 24, x:x + 155]
            else:
                # Gold text is from x: 65-225px y: 135-160px
                gold_cropped_screenshot = screenshot[136:160, 70:225]
                # Elixir text is from x: 65-225px y: 175-200px
                elixir_cropped_screenshot = screenshot[178:202, 70:225]
            # Reads the loot numbers and clears everything except the numbers
            gold_loot_text = read_text(gold_cropped_screenshot).strip().replace("", "").replace(" ", "")
            elixir_loot_text = read_text(elixir_cropped_screenshot).strip().replace("", "").replace(" ", "")
            # Checks to make sure everything was read correctly
            gold = 0
            elixir = 0
            if gold_loot_text.isnumeric():
                gold = int(gold_loot_text)
                self.total_gold += gold
                self.gold_read += 1
            if elixir_loot_text.isnumeric():
                elixir = int(elixir_loot_text)
                self.total_elixir = elixir
                self.elixir_read += 1
            # Attacks if the base has a lot of loot
            if ((self.gold_read > 4 and self.elixir_read > 4) and (1.25 * gold >= self.total_gold / self.gold_read and
                    1.25 * elixir >= self.total_elixir / self.elixir_read * 1.25)) or self.gold_read > 20:
                self.attack(screenshot)
            else:
                # Adds the loot read to the total
                self.total_gold += gold
                self.total_elixir += elixir
                # Clicks on the next button
                x, y = get_center_of_rectangle(next_button_rectangle)
                click(x, y, self.window_rectangle)
                sleep(2)

        else:
            attack_button_rectangle = find_image_rectangle(self.ATTACK_BUTTON, screenshot)
            if attack_button_rectangle:
                # Clicks on the find_base_to_attack button
                x, y = get_center_of_rectangle(attack_button_rectangle)
                click(x, y, self.window_rectangle)
                sleep(1)
                # Clicks on the find match button
                click(x + 1000, y - 230, self.window_rectangle)
                sleep(1)
                # Clicks on the button acknowledging you're breaking your shield or pays for gold if you have none
                click(x + 600, y - 200, self.window_rectangle)
                sleep(2)
            else:
                popup_x_button_rectangle = find_image_rectangle(self.POPUP_X_BUTTON, screenshot)
                if popup_x_button_rectangle:
                    # This will appear if you have no gold, so just start the attack
                    x, y = get_center_of_rectangle(popup_x_button_rectangle)
                    click(x, y, self.window_rectangle)
                    sleep(1)
                    self.attack(1.1)
        return

    def attack(self, screenshot):
        """
        Attacks by placing troops on each side of the base
        :param screenshot: Screenshot of bluestacks
        :return:
        """
        self.troops_trained = False
        # This helps the bot avoid getting stuck when it gets slightly de-synced
        if type(screenshot) != float:
            if not (find_image_rectangle(self.AVAILABLE_LOOT, screenshot) or find_image_rectangle(self.AVAILABLE_LOOT_2, screenshot)):
                self.attack_desynced = True
                return
        # Zooms out the pov
        zoom_out()
        # Selects the troops to deploy
        click(230, 715, self.window_rectangle)
        # Deploys the troops
        for i in range(10 * self.town_hall_level):
            click(450, 590, self.window_rectangle)
            sleep(.05)
            click(935, 590, self.window_rectangle)
            sleep(.05)
            click(450, 115, self.window_rectangle)
            sleep(.05)
            click(935, 115, self.window_rectangle)
            sleep(.05)
            if i % 2 == 0:
                click(230, 715, self.window_rectangle)
            else:
                click(230, 715, self.window_rectangle)

    def upgrade_troops(self, screenshot: Image) -> bool:
        """
        Finds the laboratory and tries to upgrade a troop
        :param screenshot: The screenshot of Bluestacks
        :return: True if it is done trying to upgrade a troop
        """
        if not self.lab_opened:
            research_button_rectangle = find_image_rectangle(self.RESEARCH_BUTTON, screenshot)
            if research_button_rectangle:
                x, y = get_center_of_rectangle(research_button_rectangle)
                click(x, y, self.window_rectangle)
                self.lab_opened = True
                sleep(1.5)
                return False
            for laboratory in self.LABORATORIES:
                laboratory_rectangle = find_image_rectangle(laboratory, screenshot)
                if laboratory_rectangle:
                    x, y = get_center_of_rectangle(laboratory_rectangle)
                    click(x, y, self.window_rectangle)
                    sleep(1.5)
                    return False
                else:
                    return True
        else:
            if self.scroll_count >= 3:
                # Closes out of the laboratory menu
                laboratory_x_button_rectangle = find_image_rectangle(self.LABORATORY_X_BUTTON, screenshot)
                if laboratory_x_button_rectangle:
                    x, y = get_center_of_rectangle(laboratory_x_button_rectangle)
                    click(x, y, self.window_rectangle)
                    sleep(1)
                    return True
            laboratory_menu_top_rectangle = find_image_rectangle(self.LABORATORY_MENU_TOP, screenshot)
            if laboratory_menu_top_rectangle:
                # The top menu rectangle is 355px tall, the bottom menu rectangle is 320px tall
                # crops the screenshot so it is just the troop icons in the lab
                cropped_screenshot = screenshot[laboratory_menu_top_rectangle[1] + laboratory_menu_top_rectangle[3]:
                                                laboratory_menu_top_rectangle[1] + laboratory_menu_top_rectangle[3] + 320,
                                                laboratory_menu_top_rectangle[0]:
                                                laboratory_menu_top_rectangle[0] + laboratory_menu_top_rectangle[2]]
                # This checks for elixir and dark elixir upgrades
                for icon in self.LAB_LOOT_ICONS:
                    icon_rectangles = find_image_rectangles(icon, cropped_screenshot)
                    for rectangle in icon_rectangles:
                        troop_cost_image = cropped_screenshot[rectangle[1]:rectangle[1] + rectangle[3], rectangle[0] - 60:rectangle[0]]
                        if not detect_if_color_present(self.NOT_ENOUGH_RESOURCES_COLOR, troop_cost_image):
                            x, y = get_center_of_rectangle(rectangle)
                            # Clicks on the troop icon
                            click(x + laboratory_menu_top_rectangle[0], y + laboratory_menu_top_rectangle[1] + laboratory_menu_top_rectangle[3], self.window_rectangle)
                            sleep(1)
                            # Clicks on the upgrade button
                            click(laboratory_menu_top_rectangle[0] + laboratory_menu_top_rectangle[2] - 50,
                                  laboratory_menu_top_rectangle[1] + laboratory_menu_top_rectangle[3] + 320, self.window_rectangle)
                            # Closes out of the laboratory menu
                            laboratory_x_button_rectangle = find_image_rectangle(self.LABORATORY_X_BUTTON, screenshot)
                            if laboratory_x_button_rectangle:
                                x, y = get_center_of_rectangle(laboratory_x_button_rectangle)
                                click(x, y, self.window_rectangle)
                                sleep(1)
                                return True
                else:
                    # Scrolls to the right to see if there are any other available upgrades
                    click_and_drag(laboratory_menu_top_rectangle[0] + laboratory_menu_top_rectangle[2] - 50,
                                   laboratory_menu_top_rectangle[1] + laboratory_menu_top_rectangle[3] + 100,
                                   laboratory_menu_top_rectangle[0] + 250,
                                   laboratory_menu_top_rectangle[1] + laboratory_menu_top_rectangle[3] + 100,
                                   .001,
                                   self.window_rectangle)
                    self.scroll_count += 1
                    sleep(1)
            else:
                # Closes out of the laboratory menu
                laboratory_x_button_rectangle = find_image_rectangle(self.LABORATORY_X_BUTTON, screenshot)
                if laboratory_x_button_rectangle:
                    x, y = get_center_of_rectangle(laboratory_x_button_rectangle)
                    click(x, y, self.window_rectangle)
                    sleep(1)
                    return True
        return False
