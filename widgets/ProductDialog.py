from PyQt6.QtWidgets import QDialog
from unicodedata import category, decimal

from db import dao
from gen.add_product_dialog import Ui_Dialog_add_product


class ProductDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_add_product()
        self.ui.setupUi(self)

        self.fill_combo_boxes()
        self.ui.pushButton.clicked.connect(self.add_product)

    def fill_combo_boxes(self):

        categories = dao.get_all_categories()
        for categoria in categories:
            self.ui.categoryComboBox.addItem(categoria["title"])

        brands = dao.get_all_brands()
        for brand in brands:
            self.ui.brandComboBox.addItem(brand["title"])

    def add_product(self):
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

        dao.add_product(title, category_id, brand_id, description, price, discount, image)
        print(
            "продукт успешно добавлен"
        )
        self.accept()
