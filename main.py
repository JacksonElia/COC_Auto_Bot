from PyQt6.QtWidgets import QApplication

from main_window import *
import sys


def main():
    # Launches the PyQt6 Window
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    while True:
        window.update_message_text(window.window_message)
        window.update_mode_tries_text(window.mode, window.tries)
        QApplication.processEvents()
    app.exec()


if __name__ == "__main__":
    main()
