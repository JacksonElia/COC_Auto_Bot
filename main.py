from main_window import *
import sys


def main():
    # Launches the PyQt6 Window
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
