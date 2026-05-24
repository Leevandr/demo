from PyQt6.QtWidgets import QDialog

from db import dao
from gen.order_dialog import Ui_OrderDialog


class OrderDialog(QDialog):
    def __init__(self, item=None):
        super().__init__()
        self.ui = Ui_OrderDialog()
        self.ui.setupUi(self)
        self.item = item
        self.fill()

        if item:
            self.fill_this()

        self.ui.pushButton.clicked.connect(self.save)

    def fill(self):
        users = dao.get_all_users()
        statuses = dao.get_all_statuses()
        products = dao.get_all_items()

        for user in users:
            self.ui.userComboBox.addItem(user["username"], user["id"])
        for status in statuses:
            self.ui.statusComboBox.addItem(status["title"], status["id"])
        for product in products:
            self.ui.productComboBox.addItem(product["title"], product["id"])

    def fill_this(self):
        self.ui.userComboBox.setCurrentText(dao.get_user_by_id(self.item["user_id"])["username"])
        self.ui.statusComboBox.setCurrentText(dao.get_status_by_id(self.item["status_id"])["title"])
        self.ui.productComboBox.setCurrentText(dao.get_product_by_id(self.item["product_id"])["title"])
        self.ui.countSpinBox.setValue(self.item["count"])

    def save(self):

        user_id = self.ui.userComboBox.currentData()
        status_id = self.ui.statusComboBox.currentData()
        count = str(self.ui.countSpinBox.text())
        product_id = self.ui.productComboBox.currentData()

        dao.add_order(user_id, status_id, count, product_id)
        self.accept()
