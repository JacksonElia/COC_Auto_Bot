from PyQt6 import QtWidgets
from threading import *
from GUI.ui_main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    bot_active = False

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start_button_pressed)

    def start_button_pressed(self):
        self.bot_active = not self.bot_active
        if self.bot_active:
            self.pushButton.setText("Stop")
        else:
            self.pushButton.setText("Start")


