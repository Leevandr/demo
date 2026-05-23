from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget

from auth import AuthWindow
from gen.auth import Ui_AuthForm

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = AuthWindow()
    ui.show()
    sys.exit(app.exec())
