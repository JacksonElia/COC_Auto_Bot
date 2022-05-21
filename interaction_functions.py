from PIL import Image, ImageGrab
import time
import win32api
import win32con
import win32gui


def click(x, y):
    """
    Clicks at the specified pixel coordinates.
    :param x: x pixel
    :param y: y pixel
    :return:
    """
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def zoom_out():
    """
    Zooms out the village
    :return:
    """
    win32api.keybd_event(40, 0, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(40, 0, win32con.KEYEVENTF_KEYUP, 0)


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
