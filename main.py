from PyQt6.QtWidgets import QApplication

from widgets.auth import AuthWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = AuthWindow()
    ui.show()
    sys.exit(app.exec())
