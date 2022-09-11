from interaction_functions import *
from time import sleep
from random import shuffle
import cv2 as cv


class VillageClearer:
    """
    Finds obstacles and resources on the screen, stores their locations, and collects/clears them.
    :param window_rectangle: The rectangle of the application window gotten with GetWindowRect
    """
    window_rectangle = []
    obstacle_rectangles = []
    resource_rectangles = []

    obstacles_attempted_to_remove = []

    OBSTACLES: tuple
    STONES: tuple
    RESOURCES: tuple
    REMOVE_BUTTON: tuple
    REMOVE_BUTTON_2: tuple
    ZERO_BUILDERS: tuple
    NOT_ENOUGH_RESOURCES_COLOR = [127, 137, 254]  # In [B, G, R]

    rocks_removed = False

    def __init__(self, window_rectangle: list):
        self.window_rectangle = window_rectangle

        self.OBSTACLES = (
            (cv.imread("assets/obstacles/jpg/bush.jpg", cv.IMREAD_UNCHANGED), .97),
            (cv.imread("assets/obstacles/jpg/gem_box.jpg", cv.IMREAD_UNCHANGED), .92),
            (cv.imread("assets/obstacles/jpg/large_tree.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/left_trunk.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/log.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/medium_tree.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/mushroom.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/right_trunk.jpg", cv.IMREAD_UNCHANGED), .96),
            (cv.imread("assets/obstacles/jpg/small_tree.jpg", cv.IMREAD_UNCHANGED), .93)
        )

        self.STONES = (
            (cv.imread("assets/obstacles/jpg/small_stone_1.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/small_stone_2.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/small_stone_3.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/small_stone_4.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/large_stone.jpg", cv.IMREAD_UNCHANGED), .95),
            (cv.imread("assets/obstacles/jpg/medium_stone.jpg", cv.IMREAD_UNCHANGED), .95),
        )

        self.RESOURCES = (
            (cv.imread("assets/resources/elixir_icon.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/resources/gold_icon.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/resources/dark_elixir_icon.jpg", cv.IMREAD_UNCHANGED), .93),
            (cv.imread("assets/resources/normal_grave.jpg", cv.IMREAD_UNCHANGED), .96)
            # TODO: add presents
        )

        self.LOOT_CART = (cv.imread("assets/resources/loot_cart.jpg", cv.IMREAD_UNCHANGED), .94)
        self.REMOVE_BUTTON = (cv.imread("assets/buttons/remove_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.REMOVE_BUTTON_2 = (cv.imread("assets/buttons/remove_button_2.jpg", cv.IMREAD_UNCHANGED), .94)
        self.COLLECT_BUTTON = (cv.imread("assets/buttons/collect_button.jpg", cv.IMREAD_UNCHANGED), .94)
        self.ZERO_BUILDERS = (cv.imread("assets/misc/zero_builders.jpg", cv.IMREAD_UNCHANGED), .92)

    def show_rectangles(self, screenshot: Image):
        """
        Shows obstacles and resources
        :param screenshot: the screenshot of bluestacks
        :return:
        """
        self.show_obstacles(screenshot)
        self.show_resources(screenshot)

    def clear_obstacle(self, screenshot: Image) -> bool:
        """
        Clears all the obstacles that are visible if it is able to
        :param screenshot: the screenshot of bluestacks
        :return: True if it removes an obstacle
        """
        # Cropped screenshot for better efficiency and so that the bot doesn't click on buttons by accident
        self.obstacle_rectangles = []
        # Doesn't try to remove any obstacles if there are no builders
        if not self.check_for_builders(screenshot):
            return True
        zoom_out()
        cropped_screenshot = screenshot[145:screenshot.shape[0] - 60, 100:screenshot.shape[1] - 100]
        for obstacle in self.OBSTACLES:
            self.obstacle_rectangles += find_image_rectangles(obstacle, cropped_screenshot)
        if not self.rocks_removed:
            stones = []
            for stone in self.STONES:
                stones += find_image_rectangles(stone, cropped_screenshot)
            # Assumes that all the stones have been removed if no stones were found but another obstacle was found
            if self.obstacle_rectangles and not stones:
                self.rocks_removed = False
            self.obstacle_rectangles += stones
        if self.obstacle_rectangles:
            remove_button_rectangle = find_image_rectangle(self.REMOVE_BUTTON, screenshot)
            # Tries to find the remove button used for gold obstacles if it can't find the one used for normal elixir obstacles
            # Does this rather than making the confidence lower to avoid it clicking the cancel button
            if not remove_button_rectangle:
                remove_button_rectangle = find_image_rectangle(self.REMOVE_BUTTON_2, screenshot)
            if remove_button_rectangle:
                # Check if there are resources to remove the obstacle
                cropped_screenshot = screenshot[remove_button_rectangle[1]:remove_button_rectangle[1] + remove_button_rectangle[3],
                                     remove_button_rectangle[0]:remove_button_rectangle[0] + remove_button_rectangle[2]]
                if not detect_if_color_present(self.NOT_ENOUGH_RESOURCES_COLOR, cropped_screenshot):
                    print("Enough Resources")
                    x, y = get_center_of_rectangle(remove_button_rectangle)
                    click(x, y, self.window_rectangle)
                    sleep(.3)
                    return True
                else:
                    print("Not Enough")

            rectangle = None

            while True:
                # Makes sure there are still obstacles to check
                if self.obstacle_rectangles:
                    # Gets a random obstacle in the list to remove
                    shuffle(self.obstacle_rectangles)
                    rectangle = self.obstacle_rectangles.pop(0)
                    obstacle_attempted = False
                    # Checks if the obstacle has already been checked
                    for attempted_obstacle in self.obstacles_attempted_to_remove:
                        if (abs(attempted_obstacle[0] - rectangle[0]) < 10 and
                                abs(attempted_obstacle[1] - rectangle[1]) < 10):
                            obstacle_attempted = True
                    if not obstacle_attempted:
                        break
                else:
                    break

            if rectangle is not None:
                self.obstacles_attempted_to_remove.append(rectangle)
                x, y = get_center_of_rectangle(rectangle)
                click(x + 100, y + 145, self.window_rectangle)
                sleep(1.3)  # The remove button takes a little of time to appear

        return False

    def show_obstacles(self, screenshot: Image):
        """
        Shows every obstacle rectangle
        :param screenshot: the screenshot of bluestacks
        :return:
        """
        line_color = (255, 0, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for rectangle in self.obstacle_rectangles:
            # Draw the box
            top_left = (rectangle[0], rectangle[1])
            bottom_right = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
            center = (int(rectangle[0] + rectangle[2] / 2), int(rectangle[1] + rectangle[3] / 2))
            cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)
            cv.drawMarker(screenshot, center, marker_color, marker_type)

    def collect_resources(self, screenshot):
        """
        Collects all the visible collectors and graves
        :return:
        """
        self.resource_rectangles = []
        cropped_screenshot = screenshot[145:screenshot.shape[0] - 60, 100:screenshot.shape[1] - 100]
        for resource in self.RESOURCES:
            self.resource_rectangles += find_image_rectangles(resource, cropped_screenshot)
        for rectangle in self.resource_rectangles:
            x, y = get_center_of_rectangle(rectangle)
            click(x + 100, y + 145, self.window_rectangle)

    def show_resources(self, screenshot: Image):
        """
        Shows every resource rectangle
        :param screenshot:
        :return:
        """
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_SQUARE

        for rectangle in self.resource_rectangles:
            # Draw the box
            top_left = (rectangle[0], rectangle[1])
            bottom_right = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
            center = get_center_of_rectangle(rectangle)
            cv.rectangle(screenshot, top_left, bottom_right, line_color, line_type)
            cv.drawMarker(screenshot, center, marker_color, marker_type)

    def collect_loot_cart(self, screenshot):
        """
        Collects the loot cart if it's on the screen
        :param screenshot: Screenshot of Bluestacks
        :return:
        """
        collect_button_rectangle = find_image_rectangle(self.COLLECT_BUTTON, screenshot)
        if collect_button_rectangle:
            x, y = get_center_of_rectangle(collect_button_rectangle)
            click(x, y, self.window_rectangle)
            sleep(1.5)
        else:
            loot_cart_rectangle = find_image_rectangle(self.LOOT_CART, screenshot)
            if loot_cart_rectangle:
                x, y = get_center_of_rectangle(loot_cart_rectangle)
                click(x, y, self.window_rectangle)
                sleep(1.5)

    def check_for_builders(self, screenshot) -> bool:
        """
        Checks for if there are available builders
        :param screenshot: screenshot of bluestacks
        :return: True if there are builders, False if there aren't
        """
        cropped_screenshot = screenshot[0:145, 0:]
        return not bool(find_image_rectangle(self.ZERO_BUILDERS, cropped_screenshot))
