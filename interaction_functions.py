from PIL import Image, ImageGrab
import time
import win32api
import win32con
import win32gui


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def get_screenshot():
    toplist, winlist = [], []

    def enum_cb(hwnd, result):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, toplist)
    hwnd_list = [(hwnd, title) for hwnd, title in winlist if "downloads" in title.lower()]
    hwnd = hwnd_list[0][0]
    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    return ImageGrab.grab(bbox)
