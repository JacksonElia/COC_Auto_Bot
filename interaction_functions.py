from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np
import time
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
    win32api.SetCursorPos((x + window_rectangle[0], y + window_rectangle[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def click_and_hold(x: int, y: int, hold_time: float, window_rectangle: list):
    """
    Clicks at the specified pixel coordinates relative to the window.
    :param x: x pixel
    :param y: y pixel
    :param hold_time: how long it holds the click for
    :param window_rectangle: the list with the rectangle for the window
    :return:
    """
    win32api.SetCursorPos((x + window_rectangle[0], y + window_rectangle[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(hold_time)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def zoom_out():
    """
    Zooms out the village
    :return:
    """
    win32api.keybd_event(40, 0, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(40, 0, win32con.KEYEVENTF_KEYUP, 0)


def x_out():
    """
    Zooms out the village
    :return:
    """
    win32api.keybd_event(51, 0, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(51, 0, win32con.KEYEVENTF_KEYUP, 0)


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
