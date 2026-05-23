from PyQt6.QtWidgets import QWidget, QMessageBox

from db import dao
from gen.auth import Ui_AuthForm
from widgets.main_widow import MainWindow


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AuthForm()
        self.ui.setupUi(self)
        self.main_window = None
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.guest)

    def login(self):
        login = self.ui.lineEdit_login.text().strip()
        password = self.ui.lineEdit_password.text().strip()
        print(login, password)

        if not password or not login:
            QMessageBox.warning(self, "лох", "заполни оба поля")
            return

        user = dao.login(login, password)

        if not user:
            QMessageBox.warning(self, "мне неприятно", "нет такого")
            return


        if user["role_id"] == 1:
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()

        if user["role_id"] == 2:
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()

        if user["role_id"] == 3:
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()

    def guest(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
