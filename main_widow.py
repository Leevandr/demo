from PyQt6.QtWidgets import QWidget, QLayout

from db import dao
from gen.main_window import Ui_MainForm
from item_widget import ItemWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.add_widgets()


    def add_widgets(self):
        self.clear_layout(self.ui.verticalLayout_4)
        items = dao.get_all_items()
        print(items)
        for item in items:
            self.ui.verticalLayout_4.addWidget(ItemWidget(item))

    def clear_layout(self, layout: QLayout):
        while layout.count():
            w = layout.takeAt(0).widget()
            if w:
                w.deleteLater()