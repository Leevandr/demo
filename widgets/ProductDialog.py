from PyQt6.QtWidgets import QDialog, QMessageBox
from unicodedata import category, decimal

from db import dao
from gen.add_product_dialog import Ui_Dialog_add_product


class ProductDialog(QDialog):
    def __init__(self, item=None):
        super().__init__()
        self.ui = Ui_Dialog_add_product()
        self.ui.setupUi(self)
        self.item = item
        if self.item:
            self.fill_combo_boxes(self.item)
        else:
            self.fill_combo_boxes()

        self.ui.pushButton.clicked.connect(self.save)

    def fill_combo_boxes(self, item=None):

        categories = dao.get_all_categories()
        for categoria in categories:
            self.ui.categoryComboBox.addItem(categoria["title"])

        brands = dao.get_all_brands()
        for brand in brands:
            self.ui.brandComboBox.addItem(brand["title"])
        if item:
            self.ui.categoryComboBox.setCurrentText(item["category"])
            self.ui.brandComboBox.setCurrentText(item["brand"])
            self.ui.titleLineEdit.setText(item["title"])
            self.ui.imageLineEdit.setText(item["image"])
            self.ui.descriptionLineEdit.setText(item["description"])
            self.ui.discountDoubleSpinBox.setValue(float(item["discount"]))
            self.ui.priceDoubleSpinBox.setValue(float(item["price"]))
            print(item)

    def save(self):
        categoria = self.ui.categoryComboBox.currentText()
        brand = self.ui.brandComboBox.currentText()

        category_id = dao.get_category_id(categoria)["id"]
        brand_id = dao.get_brand_id(brand)["id"]

        title = self.ui.titleLineEdit.text()
        description = self.ui.descriptionLineEdit.text()
        price = str(self.ui.priceDoubleSpinBox.text())
        discount = str(self.ui.discountDoubleSpinBox.text())
        image = self.ui.imageLineEdit.text()

        print(title, category_id, brand_id, description, price, discount, image)
        if self.item:
            dao.edit_product(self.item["id"], title, category_id, brand_id, description, price, discount, image)
            QMessageBox.information(self, "Успех", "Товар успешно отредактирован")

        else:
            dao.add_product(title, category_id, brand_id, description, price, discount, image)
            QMessageBox.information(self, "Успех", "Товар успешно добавлен")

        self.accept()
