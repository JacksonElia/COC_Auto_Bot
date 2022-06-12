from interaction_functions import *
from time import sleep
import cv2 as cv


class TrainerAndAttacker:
    """
    Trains and attacks to get loot
    """

    window_rectangle = []
    gold_read = 0
    elixir_read = 0
    total_gold = 0
    total_elixir = 0
    troops_trained = False
    troops_training = False

    ATTACK_BUTTON: tuple
    ARMY_BUTTON: tuple
    BARBARIAN_BUTTON: tuple
    GOBLIN_BUTTON: tuple
    NEXT_BUTTON: tuple
    POPUP_X_BUTTON: tuple
    RETURN_HOME_BUTTON: tuple

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.ATTACK_BUTTON = (cv.imread("assets/buttons/attack_button.jpg", cv.IMREAD_UNCHANGED), .92)
        self.ARMY_BUTTON = (cv.imread("assets/buttons/army_button.jpg", cv.IMREAD_UNCHANGED), .96)
        self.BARBARIAN_BUTTON = (cv.imread("assets/buttons/barbarian_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.GOBLIN_BUTTON = (cv.imread("assets/buttons/goblin_button.jpg", cv.IMREAD_UNCHANGED), .92)
        self.GREY_GOBLIN_BUTTON = (cv.imread("assets/buttons/grey_goblin_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.NEXT_BUTTON = (cv.imread("assets/buttons/next_button.jpg", cv.IMREAD_UNCHANGED), .9)
        self.POPUP_X_BUTTON = (cv.imread("assets/buttons/popup_x_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.RETURN_HOME_BUTTON = (cv.imread("assets/buttons/return_home_button.jpg", cv.IMREAD_UNCHANGED), .9)
        self.FINISH_TRAINING = (cv.imread("assets/misc/finish_training.jpg", cv.IMREAD_UNCHANGED), .97)

    def train_troops(self, screenshot: Image):
        # Doesn't try to train troops if they have already been trained
        if self.troops_trained:
            return
        army_button_rectangle = find_image_rectangle(self.ARMY_BUTTON, screenshot)  # TODO: Optimize when images are loaded
        barbarian_button_rectangle = find_image_rectangle(self.BARBARIAN_BUTTON, screenshot)
        goblin_button_rectangle = find_image_rectangle(self.GOBLIN_BUTTON, screenshot)
        grey_goblin_button_rectangle = find_image_rectangle(self.GREY_GOBLIN_BUTTON, screenshot)
        popup_x_button = find_image_rectangle(self.POPUP_X_BUTTON, screenshot)
        if army_button_rectangle:
            x, y = get_center_of_rectangle(army_button_rectangle)
            click(x, y, self.window_rectangle)
            sleep(1)
            click(x + 330, y - 520, self.window_rectangle)
            sleep(1)
        elif goblin_button_rectangle:
            x, y = get_center_of_rectangle(goblin_button_rectangle)
            click_and_hold(x, y, 3.5, self.window_rectangle)
            sleep(.3)
            # Clicks two more times to make there is no pop up in the way
            click(x, y + 100, self.window_rectangle)
            click(x, y + 100, self.window_rectangle)
            sleep(.3)
            # Closes out of the troop menu
            x_out()
            self.troops_training = True
        elif barbarian_button_rectangle:
            x, y = get_center_of_rectangle(barbarian_button_rectangle)
            click_and_hold(x, y, 3.5, self.window_rectangle)
            sleep(.3)
            # Clicks two more times to make there is no pop up in the way
            click(x, y + 100, self.window_rectangle)
            click(x, y + 100, self.window_rectangle)
            sleep(.3)
            # Closes out of the troop menu
            x_out()
            sleep(1)
            self.troops_training = True
        elif grey_goblin_button_rectangle:
            # Checks if troops have been trained
            finish_training_rectangle = find_image_rectangle(self.FINISH_TRAINING, screenshot)
            if not finish_training_rectangle:
                self.troops_trained = True
                self.troops_training = False
            # Closes out of the troop menu
            x_out()
            sleep(1)
        elif popup_x_button:
            self.troops_trained = True
            self.troops_training = False
            x_out()
            sleep(.5)
            x_out()

    def find_base_to_attack(self, screenshot: Image) -> bool:
        return_home_button_rectangle = find_image_rectangle(self.RETURN_HOME_BUTTON, screenshot)
        if return_home_button_rectangle:
            # Appears once the attack is finished
            x, y = get_center_of_rectangle(return_home_button_rectangle)
            click(x, y, self.window_rectangle)
            sleep(1)
            return True
        # Makes sure troops have been trained
        if not self.troops_trained:
            return False
        attack_button_rectangle = find_image_rectangle(self.ATTACK_BUTTON, screenshot)
        next_button_rectangle = find_image_rectangle(self.NEXT_BUTTON, screenshot)
        popup_x_button = find_image_rectangle(self.POPUP_X_BUTTON, screenshot)
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
        elif next_button_rectangle:
            # Gold text is from x: 65-225px y: 135-160px
            gold_cropped_screenshot = screenshot[136:160, 70:225]
            # Elixir text is from x: 65-225px y: 175-200px
            elixir_cropped_screenshot = screenshot[176:200, 70:225]
            # Reads the loot numbers and clears everything except the numbers
            gold_loot_text = read_text(gold_cropped_screenshot).strip().replace("", "").replace(" ", "")
            elixir_loot_text = read_text(elixir_cropped_screenshot).strip().replace("", "").replace(" ", "")
            print("Gold: " + gold_loot_text)
            print("Elixir: " + elixir_loot_text)
            # Checks to make sure everything was read correctly
            gold = 0
            elixir = 0
            if gold_loot_text.isnumeric():
                print("a")
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
                self.attack()
            else:
                # Adds the loot read to the total
                self.total_gold += gold
                self.total_elixir += elixir
                # Clicks on the next button
                x, y = get_center_of_rectangle(next_button_rectangle)
                click(x, y, self.window_rectangle)
                sleep(2)
        elif popup_x_button:
            # This will appear if you have no gold, so just start the attack
            x, y = get_center_of_rectangle(popup_x_button)
            click(x, y, self.window_rectangle)
            sleep(1)
            self.attack()
        return False

    def attack(self):
        self.troops_trained = False
        # Coords for attacking
        # x: 450 y: 590
        # x: 935 y: 590
        # x: 450 y: 115
        # x: 935 y: 115
        # Coords of goblin
        # x: 230 y: 715
        click(230, 715, self.window_rectangle)
        for i in range(10):
            click(450, 590, self.window_rectangle)
            sleep(.1)
            click(935, 590, self.window_rectangle)
            sleep(.1)
            click(450, 115, self.window_rectangle)
            sleep(.1)
            click(935, 115, self.window_rectangle)
            sleep(.1)
