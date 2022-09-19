from bot_functions import *
from interaction_functions import *
from PyQt6 import QtWidgets, QtGui
from threading import *
from GUI.ui_main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    bot_active = False
    auto_bot = None

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("COC Auto Bot")
        self.setWindowIcon(QtGui.QIcon("GUI/COC_Auto_Bot_Icon.png"))
        self.pushButton.clicked.connect(self.start_button_clicked)
        self.spinBox.valueChanged.connect(self.spinbox_value_changed)
        self.spinBox.setValue(1)
        self.setFocus()

    def start_button_clicked(self):
        self.setFocus()
        self.bot_active = not self.bot_active
        # Starts or stops the bot, and updates the UI to match
        if self.bot_active:
            # Makes sure bluestacks is open
            if get_hwnd("bluestacks") is not None:
                # Gets the number of accounts from the spinbox
                self.auto_bot = AutoBot(self.spinBox.value(), self)
                self.auto_bot.bot_active = True
                t1 = Thread(target=self.auto_bot.run_bot)
                t1.start()
                self.pushButton.setText("Stop")
                self.update_message_text("Bot is running.")
            else:
                self.update_message_text("Please launch COC through Bluestacks.", is_error=True)
        else:
            if self.auto_bot is not None:
                self.auto_bot.bot_active = False
            self.pushButton.setText("Start")

    def spinbox_value_changed(self):
        # There can't be less than 1 account, or more than 50 accounts
        if self.spinBox.value() < 1:
            self.spinBox.setValue(1)
        elif self.spinBox.value() > 50:
            self.spinBox.setValue(50)

    def update_message_text(self, text: str, is_error=False):
        self.label_5.setText(text)
        if is_error:
            self.label_5.setStyleSheet("color: red;")
        else:
            self.label_5.setStyleSheet("color: black;")

    def update_mode_tries_text(self, mode: int, tries: int):
        self.label_4.setText(f"Mode: {mode}")
        self.label_6.setText(f"Tries: {tries}")
