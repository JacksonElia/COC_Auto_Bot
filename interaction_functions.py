from PIL import Image, ImageGrab
from time import sleep
from pyautogui import scroll
from pydirectinput import keyDown, keyUp
import pytesseract
import cv2 as cv
import numpy as np
import win32api
import win32con
import win32gui


def click(x: int, y: int, window_rectangle: list):
    """
    Clicks at the specified pixel coordinates relative to the window.
    :param x: x pixel
    :param y: y pixel
    :param window_rectangle: the list with the rectangle for the window
    :return:
    """
    move_mouse_to_position(x, y, window_rectangle)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def click_and_hold(x: int, y: int, hold_time: float, window_rectangle: list):
    """
    Clicks and holds at the specified pixel coordinates relative to the window.
    :param x: x pixel
    :param y: y pixel
    :param hold_time: how long it holds the click for
    :param window_rectangle: the list with the rectangle for the window
    :return:
    """
    move_mouse_to_position(x, y, window_rectangle)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    sleep(hold_time)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def click_and_drag(first_x: int, first_y: int, second_x: int, second_y: int, drag_time: float, window_rectangle: list):
    """
    Clicks and drags the cursor from one position to another position using pixel coordinates relative to the window
    :param first_x: the first location's x pixel
    :param first_y: the first location's y pixel
    :param second_x: the second location's x pixel
    :param second_y: the second location's y pixel
    :param drag_time: how many seconds it takes to drag the cursor per pixel
    :param window_rectangle: the list with the rectangle for the window
    :return:
    """
    move_mouse_to_position(first_x, first_y, window_rectangle)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

    while True:
        cursor_x, cursor_y = win32api.GetCursorPos()

        # Ends the dragging if the cursor has made it to the second position
        if cursor_x == second_x + window_rectangle[0] and cursor_y == second_y + window_rectangle[1]:
            break

        if cursor_x < second_x + window_rectangle[0]:
            win32api.SetCursorPos((cursor_x + 1, cursor_y))
        elif cursor_x > second_x + window_rectangle[0]:
            win32api.SetCursorPos((cursor_x - 1, cursor_y))

        if cursor_y < second_y + window_rectangle[1]:
            win32api.SetCursorPos((cursor_x, cursor_y + 1))
        elif cursor_y > second_y + window_rectangle[1]:
            win32api.SetCursorPos((cursor_x, cursor_y - 1))

        sleep(drag_time)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def move_mouse_to_position(x: int, y: int, window_rectangle: list):
    """
    Moves the mouse to the specified pixel coordinates relative to the window.
    :param x: x pixel
    :param y: y pixel
    :param window_rectangle: the list with the rectangle for the window
    :return:
    """
    win32api.SetCursorPos((x + window_rectangle[0], y + window_rectangle[1]))


def zoom_out():
    """
    Zooms out the village
    :return:
    """
    # Uses pydirectinput because win32api wasn't working for keyboard inputs here
    keyDown("ctrl")
    keyDown("-")
    sleep(.5)
    keyUp("ctrl")
    keyUp("-")


def x_out():
    """
    Closes out of menus
    :return:
    """
    keyDown("esc")
    sleep(.1)
    keyUp("esc")


def scroll_up(clicks: int):
    """
    Scrolls a specified amount up
    :param clicks: How many times it scrolls up
    :return:
    """
    for _ in range(clicks):
        scroll(200)


def get_hwnd(window_title: str):
    """
    Gets the window handle of the specified application.
    :param window_title: the title of the application
    :return: the window handle
    """
    def enum_cb(hwnd, result):
        win_list.append((hwnd, win32gui.GetWindowText(hwnd)))

    top_list, win_list = [], []
    win32gui.EnumWindows(enum_cb, top_list)
    hwnd_list = [(hwnd, title) for hwnd, title in win_list if window_title in title.lower()]

    if len(hwnd_list) != 0:
        return hwnd_list[0][0]
    return None


def get_screenshot(hwnd: int) -> Image:
    """
    Takes a screenshot of the specified application.
    :param hwnd: the window handle of the application.
    :return: the screenshot of the specified application
    """
    bbox = win32gui.GetWindowRect(hwnd)
    return ImageGrab.grab(bbox)


def find_image_rectangle(image_tuple: tuple, screenshot: Image) -> list:
    """
    Attempts to find the rectangle of an image in a screenshot, this is good for when the image only appears in one
    place on the screen at a time.
    :param image_tuple: a tuple for the image trying to be found containing (image, confidence)
    :param screenshot: the screenshot that the image might be in
    :return: a list with the rectangle for the image in [x, y, w, h] or [] if the image is not found
    """
    image, confidence = image_tuple
    threshold = 1 - confidence
    result = cv.matchTemplate(screenshot, image, cv.TM_SQDIFF_NORMED)
    location = np.where(result <= threshold)
    location = list(zip(*location[::-1]))
    rectangle = []
    if location:
        # Gets the first time the image is found
        location = location[0]
        rectangle = [location[0], location[1], image.shape[1], image.shape[0]]
    return rectangle


def find_image_rectangles(image_tuple: tuple, screenshot: Image) -> list:
    """
    Attempts to find the rectangleS of an image in a screenshot, this is good for when the image only appears in one
    place on the screen at a time.
    :param image_tuple: a tuple for the image trying to be found containing (image, confidence)
    :param screenshot: the screenshot that the image might be in
    :return: a list OF rectangleS for the image in [x, y, w, h] or [] if the image is not found
    """
    image, confidence = image_tuple
    threshold = 1 - confidence
    result = cv.matchTemplate(screenshot, image, cv.TM_SQDIFF_NORMED)
    locations = np.where(result <= threshold)
    locations = list(zip(*locations[::-1]))

    image_width = image.shape[1]
    image_height = image.shape[0]

    # Makes a list of rectangle lists that go [x, y, w, h]
    rectangle_list = []
    for location in locations:
        rectangle_list.append([
            int(location[0]),
            int(location[1]),
            image_width,
            image_height
        ])

    # Gets rid of rectangles too close together
    rectangles = list(cv.groupRectangles(rectangle_list, 1, .5)[0])
    return rectangles


def get_center_of_rectangle(rectangle: list) -> tuple:
    """
    Finds the center of a rectangle
    :param rectangle: the rectangle list [x, y, w, h]
    :return: a tuple containing the center in (x, y)
    """
    x = int(rectangle[0] + rectangle[2] / 2)
    y = int(rectangle[1] + rectangle[3] / 2)
    return x, y


def detect_if_color_present(color: list, cropped_screenshot: Image) -> bool:
    """
    Returns True if the specified color is in the screenshot
    :param color: the [r, g, b] list representing the color
    :param cropped_screenshot: the screenshot of the location where the color might be
    :return: a boolean for if the color is in the image
    """
    for y in range(len(cropped_screenshot)):
        for x in range(len(cropped_screenshot[y])):
            pixel_color = cropped_screenshot[y][x]
            if (abs(color[0] - pixel_color[0]) < 10 and
                abs(color[1] - pixel_color[1]) < 10 and
                abs(color[2] - pixel_color[2]) < 10):
                return True
    return False


def get_pixels_with_color(color: list, cropped_screenshot: Image, x_offset: int = 0, y_offset: int = 0) -> list:
    """
    Gets pixels with a certain color
    :param color: the [r, g, b] list representing the color
    :param cropped_screenshot: the screenshot of the location where the color might be
    :param x_offset: How many pixels off the cropped_screenshot is from the window's x coordinate
    :param y_offset: How many pixels off the cropped_screenshot is from the window's y coordinate
    :return: a list of (x, y) tuples containing the pixel coordinates for the color
    """
    pixel_coordinate_list = []
    for y in range(len(cropped_screenshot)):
        for x in range(len(cropped_screenshot[y])):
            pixel_color = cropped_screenshot[y][x]
            if (abs(color[0] - pixel_color[0]) < 2 and
                abs(color[1] - pixel_color[1]) < 2 and
                abs(color[2] - pixel_color[2]) < 2):
                pixel_coordinate_list.append((x + x_offset, y + y_offset))
                cropped_screenshot[y][x] = [0, 0, 255]
    return pixel_coordinate_list


def read_text(cropped_screenshot: Image) -> str:
    """
    Attempts to read the text in the cropped screenshot
    :param cropped_screenshot: the screenshot of the location where the text might be
    :return: the string of the text, "" if no text is found
    """
    pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
    processed_image = process_image_for_reading(cropped_screenshot)
    text = pytesseract.image_to_string(processed_image, lang="eng", config="-c tessedit_char_whitelist=0123456789 --psm 6")
    return text


def process_image_for_reading(cropped_screenshot: Image) -> Image:
    """
    Processes an image so that the text on it can be read easily
    :param cropped_screenshot: the image with text on it that needs to be processed
    :return: the processed image
    """
    hsv = cv.cvtColor(cropped_screenshot, cv.COLOR_BGR2HSV)
    # define range of text color in HSV
    lower_value = np.array([0, 0, 100])
    upper_value = np.array([179, 105, 255])
    # filters the HSV image to get only the text color, returns white text on a black background
    mask = cv.inRange(hsv, lower_value, upper_value)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)  # Gets rid of small dots
    # Inverts the image to black text on white background
    invert = 255 - opening
    # Adds gaps in between characters so that they can be more easily recognized
    processed_image = add_space_between_characters(invert, 5)

    opening = cv.morphologyEx(processed_image, cv.MORPH_CLOSE, kernel, iterations=1)  # Gets rid of small lines caused by adding gaps

    return opening


def add_space_between_characters(cropped_screenshot: Image, gap: int) -> Image:
    """
    Adds a gap in between characters so that they can be read more easily
    :param cropped_screenshot: The image with the characters, the characters are black, the background is white
    :param gap: The amount of pixels added in between the characters
    :return: The processed image with added gaps
    """
    columns_to_be_added = [0]  # List storing the indexes of each gap to be added
    # Iterates through the image by column then row
    for x in range(2, len(cropped_screenshot[0]) - 2):  # Each column
        column_black_pixels = 0
        last_column_black_pixels = 0
        next_column_black_pixels = 0
        for y in range(len(cropped_screenshot)):  # Each row
            color = cropped_screenshot[y][x]
            last_color = cropped_screenshot[y][x - 2]
            next_color = cropped_screenshot[y][x + 2]
            # Checks if it is black
            if color < 50:
                column_black_pixels += 1
                # Makes the pixel completely black
                cropped_screenshot[y, x] = 0
            else:
                # Makes the pixel completely white
                cropped_screenshot[y, x] = 255
            if last_color < 50:
                last_column_black_pixels += 1
            if next_color < 50:
                next_column_black_pixels += 1
        # Gets the percentage of black pixels in the column
        percentage_of_black_pixels = column_black_pixels / cropped_screenshot.shape[0]
        percentage_of_last_black_pixels = last_column_black_pixels / cropped_screenshot.shape[0]
        percentage_of_next_black_pixels = next_column_black_pixels / cropped_screenshot.shape[0]
        # Checks if a gap should be added
        if percentage_of_last_black_pixels > .3 and percentage_of_black_pixels < .22 and percentage_of_next_black_pixels > .3:
            if (x - columns_to_be_added[-1]) > 3:
                columns_to_be_added.append(x)
            else:
                columns_to_be_added[-1] = x

    # Adds the gaps
    for column in columns_to_be_added[::-1]:
        for i in range(gap):
            cropped_screenshot = np.insert(cropped_screenshot, column, [255] * len(cropped_screenshot), axis=1)

    return cropped_screenshot
