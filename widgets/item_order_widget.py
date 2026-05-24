from PyQt6.QtWidgets import QWidget

from db import dao
from gen.OrderItemWidget import Ui_OrderItemWidget


class OrderItemWidget(QWidget):
    def __init__(self, item):
        super().__init__()
        self.ui = Ui_OrderItemWidget()
        self.ui.setupUi(self)
        self.item = item
        self.fill()

    def fill(self):
        self.ui.label_product_name.setText(dao.get_product_by_id(self.item["product_id"])["title"])
        self.ui.label_count.setText(str(self.item["count"]))
        self.ui.label_status.setText(dao.get_status_by_id(self.item["status_id"])["title"])
        self.ui.label_username.setText(dao.get_user_by_id(self.item["user_id"])["username"])

    def mousePressEvent(self, a0):
        main = self.window()
        main.select_widget(self)
